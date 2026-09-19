/*
 * Injected-tools review host for the existing review_lifecycle.py host-event API.
 * This file deliberately contains no filesystem, network, timer, or scheduler API.
 */
(function installReviewHost(root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.reviewHost = api.reviewHost;
  root.reviewHostDetailed = api.reviewHostDetailed;
  root.compactReviewHostState = api.compactReviewHostState;
})(globalThis, function reviewHostFactory() {
  'use strict';

  function requireConfig(cfg) {
    if (!cfg || typeof cfg !== 'object' || !Array.isArray(cfg.keys) || cfg.keys.length === 0)
      throw new Error('cfg.keys must be a nonempty ordered array');
    for (const name of ['children', 'outdir'])
      if (typeof cfg[name] !== 'string' || !cfg[name]) throw new Error(`cfg.${name} is required`);
    for (const name of ['profileIds', 'nativeLogs'])
      if (!cfg[name] || typeof cfg[name] !== 'object' || Array.isArray(cfg[name]))
        throw new Error(`cfg.${name} must be an object`);
    if (new Set(cfg.keys).size !== cfg.keys.length) throw new Error('cfg.keys contains duplicates');
  }

  function attentionFor(row) {
    const next = [];
    if (row.status === 'dispatching') next.push('reconcile ambiguous create; do not retry create');
    if (row.agent_id && !row.live_bound) next.push('bind the first complete live status');
    if (row.validation_state === 'pending') next.push('retry strict harvest from preserved raw');
    if (['completed', 'rejected'].includes(row.validation_state) && !row.archive_confirmed)
      next.push('use recover-archive with this key and agent_id');
    if (!row.archive_confirmed && row.archive_attempts_started >= 2)
      next.push('archive budget exhausted: confirm external state, then follow WAIT_USER recovery');
    if (row.create_blocked) next.push('new create is blocked; inspect task STATE and unsettled archive');
    return next.length ? {key: row.key, agent_id: row.agent_id || null, next} : null;
  }

  function compactReviewHostState(state, action, cfg, errors = []) {
    const stateKnown = Boolean(state && Array.isArray(state.rows));
    const rows = stateKnown ? state.rows : [];
    const status = {};
    for (const row of rows) status[row.status] = (status[row.status] || 0) + 1;
    const summary = {
      schema: 'review-host-summary/1',
      action: action && action.type || null,
      evidence: {journal: cfg.children, outdir: cfg.outdir},
      state: stateKnown ? 'known' : 'unknown',
      counts: stateKnown ? {
        total: rows.length,
        status,
        active: rows.filter(row => row.agent_id && !row.archive_confirmed).length,
        archived: rows.filter(row => row.archive_confirmed).length,
        blocked: rows.filter(row => row.create_blocked).length
      } : {
        state: 'unknown', total: null, status: null, active: null, archived: null, blocked: null
      },
      notifications: stateKnown ? rows.filter(row => row.agent_id && !row.archive_confirmed)
        .map(row => ({key: row.key, agent_id: row.agent_id})) : {state: 'unknown'}
    };
    const rejected = rows.filter(row => row.validation_state === 'rejected').map(row => ({
      key: row.key,
      agent_id: row.agent_id || null,
      validation_state: 'rejected',
      output_valid: false,
      next: 'invalid output: inspect preserved rejection evidence and use a fresh retry dispatch; do not accept this output'
    }));
    if (rejected.length) summary.rejected = rejected;
    const attention = rows.map(attentionFor).filter(Boolean);
    if (attention.length) summary.attention = attention;
    if (errors.length) summary.errors = errors.map(item => (
      {operation: item.operation || null, message: String(item.message)}));
    return summary;
  }

  async function executeReviewHost(tools, cfg, action) {
    requireConfig(cfg);
    if (!tools || typeof tools.exec_command !== 'function')
      throw new Error('injected tools.exec_command is required');
    const quote = value => "'" + String(value).replace(/'/g, "'\\''") + "'";
    const helper = cfg.helper || 'tools/orchestration/review_lifecycle.py';
    let state;

    async function event(key, op, extra = {}) {
      try {
        const input = JSON.stringify({op, ...extra});
        const args = ['python3', '-B', helper, 'host-event', cfg.children, key, '--outdir', cfg.outdir];
        if (cfg.nativeLogs[key]) args.push('--native-log', cfg.nativeLogs[key]);
        const reply = await tools.exec_command({
          cmd: "printf '%s' " + quote(input) + ' | ' + args.map(quote).join(' '),
          yield_time_ms: 1000,
          max_output_tokens: 4000
        });
        if (reply.session_id)
          throw new Error(`Local command is still running with session_id ${reply.session_id}; resume the original command session`);
        const combined = reply.output || '';
        if (reply.exit_code !== 0) throw new Error(combined || 'host-event failed');
        return JSON.parse(combined);
      } catch (error) {
        if (!error.reviewHostOperation) error.reviewHostOperation = op;
        throw error;
      }
    }

    async function call(key, op, fn, extra = {}) {
      const started_at = new Date().toISOString();
      let response;
      try {
        response = await fn();
      } catch (error) {
        try {
          await event(key, 'call-failed', {operation: op, started_at, ended_at: new Date().toISOString()});
        } catch (recordError) {
          error.reviewHostRecordError = String(recordError && recordError.message || recordError);
        }
        error.reviewHostOperation = op;
        throw error;
      }
      return event(key, op, {...extra, response, started_at, ended_at: new Date().toISOString()});
    }

    try {
      state = await event(cfg.keys[0], 'recover');
      const row = key => {
        const hits = state.rows.filter(item => item.key === key);
        if (hits.length !== 1) throw new Error('Unknown dispatch');
        return hits[0];
      };

      async function fill() {
        for (const key of cfg.keys) {
          if (state.rows.some(item => item.status === 'dispatching'))
            throw new Error('Ambiguous create: reconcile before any create');
          for (const item of state.rows.filter(item => item.status === 'created'))
            state = await call(item.key, 'bind', () => tools.mcp__paseo__get_agent_status({agentId: item.agent_id}));
          if (state.rows.some(item => item.create_blocked)) return;
          const occupied = state.rows.filter(item => item.agent_id ? !item.archive_confirmed :
            !['prepared', 'confirmed_absent'].includes(item.status)).length;
          if (occupied >= 3) return;
          if (!['prepared', 'confirmed_absent'].includes(row(key).status)) continue;
          state = await call(key, 'profiles', () => tools.mcp__paseo__list_profiles({}),
                             {profile_id: cfg.profileIds[key]});
          state = await call(key, 'create', () => tools.mcp__paseo__create_agent(state.parameters));
          const agentId = row(key).agent_id;
          state = await call(key, 'bind', () => tools.mcp__paseo__get_agent_status({agentId}));
        }
      }

      if (action.type === 'fill') {
        await fill();
      } else if (action.type === 'finish' || action.type === 'recover-archive') {
        const key = action.key;
        const current = row(key);
        if (current.agent_id !== action.agentId) throw new Error('Notification agent/dispatch mismatch');
        if (current.archive_confirmed) return state;
        if (!current.live_bound) throw new Error('Recover first live binding before processing notification');
        if (action.type === 'recover-archive' && !['completed', 'rejected'].includes(current.validation_state))
          throw new Error('Incomplete harvest requires original notification evidence');
        if (!['completed', 'rejected'].includes(current.validation_state)) {
          state = await call(key, 'harvest', () => tools.mcp__paseo__get_agent_status({agentId: current.agent_id}),
                             {notified: true, notification_received_at: action.receivedAt || null});
        }
        state = await call(key, 'archive-intent', () => tools.mcp__paseo__get_agent_status({agentId: current.agent_id}));
        if (state.archive) {
          try {
            state = await call(key, 'archive-response', () => tools.mcp__paseo__archive_agent({agentId: current.agent_id}));
          } finally {
            state = await call(key, 'archive-confirm', () => tools.mcp__paseo__get_agent_status({agentId: current.agent_id}));
          }
        }
        await fill();
      } else {
        throw new Error('Unknown host action');
      }
      return state;
    } catch (error) {
      const failure = {operation: error.reviewHostOperation || null, message: error.message || error};
      if (error.reviewHostRecordError) failure.message += '; call-failed record error: ' + error.reviewHostRecordError;
      error.reviewHostSummary = compactReviewHostState(state, action, cfg, [failure]);
      throw error;
    }
  }

  async function reviewHostDetailed(tools, cfg, action) {
    const state = await executeReviewHost(tools, cfg, action);
    return {state, summary: compactReviewHostState(state, action, cfg)};
  }

  async function reviewHost(tools, cfg, action) {
    return (await reviewHostDetailed(tools, cfg, action)).summary;
  }

  return {reviewHost, reviewHostDetailed, compactReviewHostState};
});

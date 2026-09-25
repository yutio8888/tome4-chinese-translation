# Resume of contextual-adjudication-chain after contextual-import succeeded and
# generate-adjudication failed on a wrong --source-root: same strict generate().
import sys
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/orchestration')
import make_adjudication as adjudication
C = Path('.artifacts/i18n/continuation-20260923')
frozen = adjudication.freeze_inputs(C / 'review279-host-decisions.json')
adjudication.generate(Path('.').resolve(), C / 'review279-host-decisions.json',
                      Path('.artifacts/i18n/adjudication-chain/review279-20260925-attempt01.json'),
                      source_root=C / 'review279-source-root', frozen=frozen)

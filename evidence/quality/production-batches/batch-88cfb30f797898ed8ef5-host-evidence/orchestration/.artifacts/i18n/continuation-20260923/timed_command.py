import sys,json,subprocess,time,datetime
from pathlib import Path
prefix=Path(sys.argv[1]);argv=sys.argv[2:];assert argv
log=Path(str(prefix)+'.log');timing=Path(str(prefix)+'-timing.json');assert not log.exists() and not timing.exists()
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with log.open('wb') as out:result=subprocess.run(argv,stdout=out,stderr=subprocess.STDOUT)
receipt=dict(argv=argv,started_at=started,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=time.monotonic()-t,exit_code=result.returncode,log_path=str(log))
timing.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps(receipt,ensure_ascii=False));print(log.read_text()[-2000:]);raise SystemExit(result.returncode)

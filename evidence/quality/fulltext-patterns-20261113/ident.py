import subprocess,re,json,sys,glob,os
names=sys.argv[1:]
core=subprocess.run(['git','-C','/workspace/t-engine4','grep','-n','-E','name = "('+'|'.join(re.escape(n) for n in names)+')"','624a67329fe2','--','game/modules/tome/data/talents','game/engines/default/data'],capture_output=True,text=True).stdout
dlc=subprocess.run(['grep','-rn','-E','name = "('+'|'.join(re.escape(n) for n in names)+')"','/workspace/tome4-dlcs','--include=*.lua'],capture_output=True,text=True).stdout
for l in (core+dlc).splitlines():
    if '/talents/' in l and 'locales' not in l:
        l=l.replace('624a67329fe2:game/modules/tome/','core:').replace('/workspace/tome4-dlcs/','dlc:')
        print(re.sub(r'\s+',' ',l)[:170])

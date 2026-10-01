import re
PH=re.compile(r'%[-+ #0]*\d*(?:\.\d+)?[diuxXeEfgG](?:%%)?')  # numeric conversions only; %s carries names/markup/fragments
SEP=set(' \t\n()[],')
MK=re.compile(r'#[A-Za-z0-9_]+#|#\{[a-z]+\}#')
CJK=re.compile(r'[一-鿿]')
CLOSE=set('，。、；：）！？…」』”》')
OPEN=set('（「『“《')
SIGN=set('+-±')
def plan(t0):
    m_=MK.sub(lambda m:' '*len(m.group()),t0)
    ins=set()
    for m in PH.finditer(m_):
        i=m.start();j=m.end()
        a=i
        while a>0 and m_[a-1] not in SEP:a-=1
        b=j
        while b<len(m_) and m_[b] not in SEP:b+=1
        if CJK.search(m_[a:i]):
            p=i
            while p>a and m_[p-1] in SIGN:p-=1
            while p>a and m_[p-1] in OPEN:p-=1
            if p>a: ins.add(p)
        if CJK.search(m_[j:b]):
            q=j
            while q<b and m_[q] in CLOSE:q+=1
            if q<b: ins.add(q)
    return ins
def apply(t):
    ins=plan(t);return ''.join(((' ' if k in ins else '')+ch) for k,ch in enumerate(t)),len(ins)

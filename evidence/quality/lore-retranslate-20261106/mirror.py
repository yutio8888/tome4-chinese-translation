def mirror(text):
    out=[]
    for l in text.split('\n'):
        r=l[::-1]
        r=r.replace(']b/[','\x01').replace(']b[','\x02').replace('\x01','[b]').replace('\x02','[/b]')
        r=r.translate(str.maketrans('()（）“”',')(）（”“'))
        out.append(r)
    return '\n'.join(out)

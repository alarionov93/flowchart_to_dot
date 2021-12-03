import glob

STATE=0
for f in glob.glob('*.py'):
    for l in open(f, 'r').readlines():
        if STATE == 0: #init
            if 'def ' in l:
                w = open('descr/%s.py' % l[4:6].strip(), 'a')
                w.write(l)
                STATE = 1
        elif STATE == 1:
            try:
                if 'def ' in l:
                    w.close()
                    w = open('descr/%s.py' % l[4:6].strip(), 'a')
                    w.write(l)
                else:
                    w.write(l)
            except NameError:
                pass

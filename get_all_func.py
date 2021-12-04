import glob
import sys

STATE = 0
path = sys.argv[1]
for f in glob.glob('%s*.py' % path):
    if f != last_f:
        STATE = 0
    for l in open(f, 'r').readlines():
        func_name = re.findall(r'^def\s(\w+)', l)
        if STATE == 0: #init
            if func_name:
                w = open('%sdescr/%s.py' % (path, func_name), 'a')
                w.write(l)
                STATE = 1
        elif STATE == 1:
            try:
                if func_name:
                    w.close()
                    w = open('%sdescr/%s.py' % (path, func_name), 'a')
                    w.write(l)
                else:
                    w.write(l)
            except NameError:
                pass
    last_f = f

 
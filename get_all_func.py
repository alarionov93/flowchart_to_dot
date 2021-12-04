import glob
import sys
import re

STATE = 0
path = sys.argv[1]
last_f = None
last_func_name = None


rm_words = [
    'json.',
    'self.',
    'os.path.',
    'hashlib.',
    '.hexdigest()',
    'shutil.',
    'print',
]

for f in glob.glob('%s*.py' % path):
    if f != last_f:
        STATE = 0
    for l in open(f, 'r').readlines():
        func_name = re.findall(r'def\s(\w+)', l)
        # print(f, func_name)
        if STATE == 0: #init
            if func_name:
                w = open('%sdescr/%s_%s' % (path, func_name[0], f.split('/')[-1]), 'a')
                w.write(l)
                STATE = 1
        elif STATE == 1:
            try:
                if func_name:
                    w.close()
                    w = open('%sdescr/%s_%s' % (path, func_name[0], f.split('/')[-1]), 'a')
                    w.write(l)
                else:
                    if '@' in l or 'print' in l or '\'\'\'' in l or '#' in l:
                        continue
                    else:
                        for rw in rm_words:
                            l = l.replace(rw, '')
                        w.write(l)
            except NameError:
                pass
    last_f = f
    if func_name:
        last_func_name = func_name

 
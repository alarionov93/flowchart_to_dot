import glob
import sys
import re

# tpls = [
#     '## Описание функции "A"',
#     'На вход функции "A" подаются данные "B"',
#     'Выполняется действие "A", потом "B".',
#     'При условии "A" выполняются действия "B" и "C".',
#     'Иначе выполняются дествия "A", "B" и "C".',
#     'В цикле "A" выполняются действия "B" и "C".',
#     'Функция "A" возвращает данные "B".',
#     'Далее выполняется действие "A".',
# ]


OPERATIONS = {
    'start': ['начало', '## Описание функции "F".'],
    'subroutine': ['подпрограмма', '"N". Выполняется подпрограмма "P", '],
    'operation': ['действие', '"N". Выполняется действие "A", '],
    'condition': ['условие', '"N". Проверяется условие "C", '],
    'inputoutput': ['ввод-вывод', 'Функция "F" на вход принимает данные "I".\n Состоит из операций:', 'Функция "F" возвращяет данные "O".'],
    'end': ['конец', 'end'],
}

work_dir = sys.argv[1]


def insert_desc(template: str, f_name: str, data: str, count: int) -> str:
    if not template:
        print('[ERROR] Template is None! \nSome additional info: \n%s : %s : %s' % (f_name, data, count))
        return
    paths = re.findall(r'\"[ACFINPO]\"', template)
    try:
        for path in paths:
            if '"F"' in path:
                template = template.replace(path, f_name)
            if '"I"' in path:
                template = template.replace(path, data).replace(' ввод ', '')
            if '"O"' in path:
                template = template.replace(path, data).replace(' вывод ', '')
            if '"N"' in path:
                template = template.replace(path, str(count))
            if path in ['"P"','"A"','"C"']:
                template = template.replace(path, data)
    except IndexError:
        print('[ERROR] Not found any rsymbols from re \"[ACFINPO]\"')
    return template


def generate_descr_line(file: '_io.TextIOWrapper', action: str, label: str, count: int) -> tuple:
    tpl = None
    try:
        tpl = OPERATIONS[action][1]
        if 'вывод' in label:
            tpl = OPERATIONS[action][2]
    except KeyError:
        print('[ERROR] This action (%s) not found in OPERATIONS keys!' % action)
    # for line in text.split('\n'):
        # gs = re.findall(rx, line)
    func_name = file.name.split('/')[-1].split('.')[0] # из start label
    # if 'ввод' in action:

    desc_line = insert_desc(tpl, func_name, label, count)
    file.write(desc_line)
    
    # print('%s : %s : %s : %s' % (func_name, action, tpl, label))

    return (action, tpl, func_name, label)


if __name__ == '__main__':
    for f in glob.glob('%s*.dot' % work_dir):
        for l in open(f, 'r').readlines():
            print(l)


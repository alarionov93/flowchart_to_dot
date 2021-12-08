import glob
import sys
import re

from random import choice
from sys import stderr
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
  "start": [
    "начало",
    [
      "## Описание функции \"F\".\n"
    ]
  ],
  "subroutine": [
    "подпрограмма",
    [
      "\"N\") подпрограммы \"P\"; \n",
      "\"N\") предопределенной операции \"P\"; \n",
      "\"N\") передача управления подпрограмме \"P\"; \n",
      "\"N\") вызова подпрограммы \"P\"; \n",
    ]
  ],
  "operation": [
    "действие",
    [
      "\"N\") действия \"A\"; \n",
      "\"N\") выполнения \"A\"; \n",
      "\"N\") вычисления \"A\"; \n",
      "\"N\") выполнения операции \"A\"; \n",
    ]
  ],
  "condition": [
    "условие",
    [
      "\"N\") проверки условия \"C\"; \n",
      "\"N\") условия \"C\"; \n",
      "\"N\") проверки \"C\"; \n",
    ]
  ],
  "condition_for": [
    "цикл",
    [
      "\"N\") цикла \"C\", в которм выполняются следующщие действия; \n",
      "\"N\") цикла \"C\"; \n",
      "\"N\") циклического выполнения действий \"C\"; \n",
    ]
  ],
  "inputoutput": [
    "ввод-вывод",
    [
      "Функция \"F\" на вход принимает следующие данные: \"I\". Она состоит из ряда операций:\n",
      "Функция \"F\" на вход принимает такие данные как: \"I\". Она состоит из операций:\n",
      "Функция \"F\" на вход принимает такие данные как: \"I\". Она состоит из следующих операций:\n"
    ],
    [
      "Функция \"F\" возвращает данные: \"O\".",
      "Выходные данные функции \"F\": \"O\".",
      "Функция \"F\" возвращает: \"O\".",
      "Выход функции \"F\": \"O\".",
    ]
  ],
  "end": [
    "конец",
    [
      "end"
    ]
  ]
}


def insert_desc(template: str, f_name: str, data: str, count: int) -> str:
    if not template:
        print('[ERROR] Template is None! \nSome additional info: \n%s : %s : %s' % (f_name, data, count), file=stderr)
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
        print('[ERROR] Not found any rsymbols from re \"[ACFINPO]\"', file=stderr)
    return template


def generate_descr_line(file: '_io.TextIOWrapper', action: str, label: str, count: int) -> tuple:
    tpl = None
    try:
        # print(label, file=stderr)
        tpl = choice(OPERATIONS[action][1])
        if 'вывод' in label:
            tpl = choice(OPERATIONS[action][2])
        elif 'for ' in label:
            tpl = choice(OPERATIONS['condition_for'][1])
    except KeyError:
        print('[ERROR] This action (%s) not found in OPERATIONS keys!' % action, file=stderr)
    except IndexError:
        print('[ERROR] Index 1 or 2 not found in OPERATIONS[\'%s\']'% action, file=stderr)
    # for line in text.split('\n'):
        # gs = re.findall(rx, line)
    func_name = file.name.split('/')[-1].split('.')[0] # из start label
    # if 'ввод' in action:

    desc_line = insert_desc(tpl, func_name, label, count)
    file.write(desc_line)

    # print('%s : %s : %s : %s' % (func_name, action, tpl, label), file=stderr)

    return (action, tpl, func_name, label)



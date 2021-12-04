import re
import sys
from glob import glob


'''
'start': 'ellipse',
'subroutine': 'box',
'operation': 'box',
'condition': 'diamond',
'inputoutput': 'parallelogram',
'end': 'ellipse',

'''

punct = set(' ,.[]()<>+-*/=')

def wrap(instr, w=20):
	outstr = ""
	l = 0
	last = len(instr)
	for x in instr:
		if l < w:
			outstr += x
		elif l >= w and x not in punct:
			outstr += x
		elif x in punct and last > w / 5:
			outstr += x+'\n'
			l = 0
		else:
			outstr += x
		l += 1
		last -= 1
	return outstr

def translate(node):
	return node.\
		replace('input', 'ввод ').\
		replace('output', 'вывод ').\
		replace('start', 'начало\n').\
		replace('end function return', 'конец')

SHAPES = {
	'start': 'ellipse',
	'subroutine': 'box',
	'operation': 'box',
	'condition': 'diamond',
	'inputoutput': 'parallelogram',
	'end': 'ellipse',
}

try:
	work_dir = sys.argv[1]
	for data_file in glob('%s*.d' % work_dir):
		# print(data_file)
		res_f = open('%s.dot' % (data_file), 'w')
		res_f.write('digraph G {\n')
		with open(data_file, 'r') as f:
			for l in f.readlines():
				if '=>' in l:
					node = l.split('=>')[0]
					action = l.split('=>')[1].split(':')[0]
					try:
						shape = SHAPES[action]
					except KeyError:
						shape = 'box'
					if 'input' in action:
						in_str = l.split(':')[2].strip().replace('"','\\"')
					else:
						in_str = ''
					label = '%s %s' % (translate(l.split(':')[1].strip().replace('"','\\"')), in_str)
					res_str = '%s [shape="%s" label="%s"]\n' % (node, shape, wrap(label, 20))
					res_f.write(res_str)
				elif '->' in l:
					line = re.findall(r'(\w+)(\((\w+)\))?->(\w+)', l)
					label = ''
					if line[0][2]:
						label = '[label="%s"]' % line[0][2].replace('"','\\"')
					res_str = '%s->%s %s\n' % (line[0][0], line[0][3], wrap(label, 20))
					res_f.write(res_str)
		res_f.write('}\n')
		res_f.close()
except IndexError:
	print('Pass working directory parameter!')


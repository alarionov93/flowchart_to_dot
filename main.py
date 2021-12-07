import re
import sys
from glob import glob
from descr_gen import generate_descr_line


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
		replace('input:', 'ввод ').\
		replace('output:', 'вывод ').\
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
		descr_f = open('%s.txt' % (data_file), 'w')
		res_f = open('%s.dot' % (data_file), 'w')
		res_f.write('digraph G {\nsplines=ortho\nnodesep=1\n')
		with open(data_file, 'r') as f:
			count = 0
			for l in f.readlines():
				if '=>' in l:
					node = l.split('=>')[0]
					action = l.split('=>')[1].split(':')[0]
					try:
						shape = SHAPES[action]
					except KeyError:
						shape = 'box'
					if 'input' in action or 'output' in action:
						in_str = ': %s' % l.split(':')[2].strip().replace('"','\\"')
						# print(in_str)
					else:
						in_str = ''
					# print(l.split(':')[1].strip().replace('"','\\"'))
					# print(l.split(':')[1])
					label = '%s%s' % (l.split(':')[1].strip().replace('"','\\"'), in_str)
					print(label)
					label = translate(label)
					if 'for' in label:
						shape = 'hexagon'
					res_str = '%s [shape="%s" label="%s"]\n' % (node, shape, wrap(label, 20))
					res_f.write(res_str)
					generate_descr_line(descr_f, action, label, count)
					if action in ['subroutine','operation','condition']:
						count+=1
				elif '->' in l:
					line = re.findall(r'(\w+)(\((\w+)\))?->(\w+)', l)
					label = ''
					if line[0][2]:
						label = '[xlabel="%s"]' % line[0][2].replace('"','\\"')
					res_str = '%s->%s %s\n' % (line[0][0], line[0][3], wrap(label, 20))
					res_f.write(res_str)
		res_f.write('}\n')
		res_f.close()
		descr_f.close()
except IndexError:
	print('Pass working directory parameter!')


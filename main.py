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
		print(data_file)
		res_f = open('%s.dot' % (data_file), 'w')
		with open(data_file, 'r') as f:
			for l in f.readlines():
				if '=>' in l:
					node = l.split('=>')[0]
					action = l.split('=>')[1].split(':')[0]
					try:
						shape = SHAPES[action]
					except KeyError:
						shape = 'box'
					label = l.split(':')[1].strip()
					res_str = '%s [shape="%s" label="%s"]\n' % (node, shape, label)
					res_f.write(res_str)
				elif '->' in l:
					line = re.findall(r'(\w+)(\((\w+)\))?->(\w+)', l)
					label = ''
					if line[0][2]:
						label = '[label=%s]' % line[0][2]
					res_str = '%s->%s %s\n' % (line[0][0], line[0][3], label)
					res_f.write(res_str)
		res_f.close()
except IndexError:
	print('Pass working directory parameter!')


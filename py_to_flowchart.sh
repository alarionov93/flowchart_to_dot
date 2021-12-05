#!/bin/bash

# TODO: static path - add $ params!
for f in /home/student/flowchart_to_dot_train_data/descr/*.py; 
do
	python3 -m pyflowchart "$f" > $(echo "$f" | cut -d '.' -f 1).d
done;
python3 main.py /home/student/flowchart_to_dot_train_data/descr/

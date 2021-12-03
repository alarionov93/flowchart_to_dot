for f in *.py
do
	python3 -m pyflowchart "$f" > $(echo "$f" | cut -d '.' -f 1).d
done;

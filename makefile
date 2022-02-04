MAIN=skeleton.py

local:
	python3 $(MAIN) --local

online:
	python3 $(MAIN) --online

stats:
	python3 $(MAIN) --stats
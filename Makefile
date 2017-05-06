.PHONY = all, clean

all: environment.yml

environment.yml: 
	conda env export > $@



################## MAKEFILE #####################

TARGET	=	speechReco.py

all: run

env:
	conda activate speechReco

clean:
	rm -r input/*

logclean: 
	rm audioTranslate/*

fclean: 
	rm -rf input/*
	rm -rf audioTranslate/*
	rm -r video/*

.PHONY: clean fclean logclean run env
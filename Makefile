install:
	poetry lock && poetry install

run:
	poetry run streamlit run 📖はじめに.py

all: run
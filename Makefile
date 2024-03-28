.ONE_SHELL:

#* Create/update a requirements.txt file
freeze:
	poetry export -f requirements.txt --output requirements.txt  

# ! ----------------- POETRY COMMANDS (Recommended) ----------------- ! #
init-poetry:
	poetry env use 3.12
	poetry install
	poetry update
	${MAKE} freeze

run: init-poetry
	clear
	poetry run python test.py
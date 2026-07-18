

.PHONY: quality mypy pylint ruff format

quality: ruff mypy pylint

mypy:
	PYTHONPATH=./ uv run mypy ./duplicata_finder

pylint:
	PYTHONPATH=./ uv run pylint duplicata_finder

ruff:
	PYTHONPATH=./ uv run ruff check

format:
	PYTHONPATH=./ uv run ruff format

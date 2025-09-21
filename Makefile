run_ruff:
	uv run ruff check --fix ; uv run ruff format

run_tests:
	uv run pytest -vv --cov=src --cov-report term-missing --cov-fail-under=50

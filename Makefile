run_ruff:
	uv run ruff check --fix ; uv run ruff format

run_tests:
	uv run pytest -vv --cov=src --cov-report term-missing --cov-fail-under=50

run_raw_layer:
	uv run ./src/football_pipeline/stages/pipe_001_raw.py --config-path ./configs/001_raw_layer.yaml

create_branch:
	@DEV_BRANCH=dev; \
	echo "Using develop branch \`$$DEV_BRANCH\`."; \
	BRANCH_TYPES=("feat" "fix"); \
	while true; do \
		echo "Enter branch type [$${BRANCH_TYPES[*]}]:"; \
		read BRANCH_TYPE; \
		if [[ " $${BRANCH_TYPES[@]} " =~ " $${BRANCH_TYPE} " ]]; then \
			break; \
		else \
			echo "Invalid branch type. Please choose from: $${BRANCH_TYPES[*]}"; \
		fi; \
	done; \
	echo "selected branch type: $${BRANCH_TYPE}"; \
	echo "Enter a short description:"; \
	read INP_BRANCH_DESC; \
	BRANCH_DESC=$$(echo "$${INP_BRANCH_DESC}" | sed 's/ /_/g'); \
	FINAL_BRANCH_NAME="$${BRANCH_TYPE}/$${BRANCH_DESC}"; \
	echo "Branch name will be: \`$${FINAL_BRANCH_NAME}\`. Are you sure you want to create this branch? [Y/N]:"; \
	read CONFIRMATION; \
	if [[ "$${CONFIRMATION}" != "Y" ]]; then \
		echo "\nOperation cancelled by user.\n"; \
		exit 1; \
	fi; \
	git checkout $${DEV_BRANCH}; \
	git pull; \
	git checkout -b $${FINAL_BRANCH_NAME}; \
	git push --set-upstream origin $${FINAL_BRANCH_NAME}; \
	echo "created branch name $${FINAL_BRANCH_NAME} and pushed to origin"; \
	uv sync --all-packages; \
	uv run pre-commit install; \
	uv run pre-commit run --all-files; \

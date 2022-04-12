
.PHONY: dev-env
save_deps:
	pip freeze > requirements.txt

.PHONY: dev-env
get_deps:
	pip install -r requirements.txt



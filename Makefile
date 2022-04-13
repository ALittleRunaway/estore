include .env
export

# Don't forget to change it!
MIGRATION_NAME := test

.PHONY: save_deps
save_deps:
	pip freeze > requirements.txt

.PHONY: get_deps
get_deps:
	pip install -r requirements.txt

.PHONY: compile
compile:
	pyinstaller --onefile --noconfirm --windowed -i estore/gui/static/icon.ico -n estore estore/__main__.py
# TODO: add modules and so on

.PHONY: migrate_up
migrate_up:
	migrate -source file://./estore/db/migration -database mysql://${DB_USERNAME}:${DB_PASSWORD}@/estore up

.PHONY: migrate_down
migrate_down:
	migrate -source file://./estore/db/migration -database mysql://${DB_USERNAME}:${DB_PASSWORD}@/estore down

.PHONY: migrate_version
migrate_version:
	migrate -source file://./estore/db/migration -database mysql://${DB_USERNAME}:${DB_PASSWORD}@/estore version

.PHONY: migrate_force_version
migrate_force_version:
	migrate -source file://./estore/db/migration -database mysql://${DB_USERNAME}:${DB_PASSWORD}@/estore force -1

.PHONY: migrate_new
migrate_new:
	migrate create -dir estore/db/migration -ext sql ${MIGRATION_NAME}


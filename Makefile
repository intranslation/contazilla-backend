.PHONY: migrate upgrade downgrade revision current history

# Run all pending migrations (upgrade to latest)
migrate:
	alembic upgrade head

upgrade: migrate

# Rollback one migration
downgrade:
	alembic downgrade -1

# Create a new migration (use: make revision msg="description of changes")
revision:
	alembic revision --autogenerate -m "$(msg)"

# Show current migration revision
current:
	alembic current

# Show migration history
history:
	alembic history -v

organize-imports:
	isort .

check-types:
	ty check
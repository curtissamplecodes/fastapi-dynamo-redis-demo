up: start-infra apply-terraform

down:
	cd infra && terraform destroy --auto-approve
	docker compose down

run: up
	docker compose --profile app up -d --build

stop: 
	docker compose stop app

run-local: up
	uvicorn app.main:app --reload

test: up
	@bash -c 'trap "make down" EXIT; pytest; sleep 5'

# helpers
start-infra: 
	docker compose up -d

apply-terraform:
	cd infra && terraform init && terraform apply --auto-approve
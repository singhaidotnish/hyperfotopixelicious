.PHONY: dev dev-fe dev-be be-venv be-install

# Create venv if missing
be-venv:
	@test -d .venv || python3 -m venv .venv

be-install: be-venv
	. .venv/bin/activate; pip install -r apps/backend/requirements.txt

dev-be:
	. .venv/bin/activate; cd apps/backend && uvicorn main:app --reload --port 8000

dev-fe:
	cd apps/frontend && pnpm dev

# Run both (two terminals recommended), or rely on package.json script
dev:
	make -j2 dev-be dev-fe
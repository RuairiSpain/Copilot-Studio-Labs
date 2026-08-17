.PHONY: verify golden plan apply teardown notebooks-validate

# Runs the shared golden set against the currently published agent(s).
# Application/SP auth path — same as CI.
verify:
	python -m csx.run_gate --tags core --min-pass-rate 0.8

# Full golden set, all tags — the broad regression sweep, not the CI-fast subset.
golden:
	python -m csx.run_gate --min-pass-rate 0.8

# Platform layer plan (see infra/terraform/platform)
plan:
	cd infra/terraform/platform && terraform init -upgrade && terraform plan

apply:
	cd infra/terraform/platform && terraform apply

teardown:
	cd infra/terraform/platform && terraform destroy

# Sanity check every notebook is valid nbformat JSON — cheap, run before any commit
notebooks-validate:
	python -c "import nbformat, glob; [nbformat.validate(nbformat.read(f, as_version=4)) for f in glob.glob('notebooks/*.ipynb')]; print('all notebooks valid')"

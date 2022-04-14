Remove-Item -Recurse .git
Remove-Item -Recurse .mypy_cache
Remove-Item -Recurse .github
Remove-Item -Recurse venv
git init
python -m venv venv
mkdir docs
cd docs
sphinx-quickstart
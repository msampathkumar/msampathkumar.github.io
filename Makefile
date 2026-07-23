.all: run
	@echo "make all"

clean:
	rm -f *.o

run:
	@echo "Running the mkdocs"
	mkdocs serve -a localhost:8099 -c

# Scaffold a new blog post: make new-post TITLE="My Title"
new-post:
	@test -n "$(TITLE)" || (echo 'Usage: make new-post TITLE="My Title"' && exit 1)
	python scripts/new_post.py "$(TITLE)"

# Regenerate llms-full.txt (full inlined content) from the curated llms.txt
llms:
	python scripts/gen_llms_full.py

# Import dev.to/Medium posts into _internal/devto_import/ for review
import-devto:
	python scripts/import_devto.py --username sampathm

deploy: llms
	@echo "Deploying to GitHub Pages"
	mkdocs gh-deploy --clean --force


check-ga:
	@echo "Checking Google Analytics ("${GOOGLE_ANALYTICS_KEY_GITHUB_IO_BLOG}") "
	rm -rf site/
	mkdocs build
	grep __md_analytics site/*


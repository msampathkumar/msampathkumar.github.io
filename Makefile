.all: run
	@echo "make all"

clean:
	rm -f *.o

run:
	@echo "Running the mdformat"
	mdformat .
	@echo "Running the black"
	black .
	@echo "Running the mkdocs"
	mkdocs serve

deploy:
	@echo "Deploying to GitHub Pages"
	mkdocs gh-deploy


check-ga:
	@echo "Checking Google Analytics ("${GOOGLE_ANALYTICS_KEY_GITHUB_IO_BLOG}") "
	rm -rf site/
	mkdocs build
	grep __md_analytics site/*


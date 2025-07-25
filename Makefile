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
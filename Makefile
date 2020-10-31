BUILD_DIR=_build/html

html: bibliography
	jupyter-book build .
	python _scripts/make_redirects.py

github: html
	ghp-import -n _build/html -p -f

clean:
	rm -rf _build

BIBLIOGRAPHIES= bib/data-science-bib/data_science.bib \
				bib/course_refs.bib

bibliography: $(BIBLIOGRAPHIES)
	cat $(BIBLIOGRAPHIES) > _references.bib

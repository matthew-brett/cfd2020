html:
	jupyter-book build .

github: html
	ghp-import -n _build/html -p -f

clean:
	rm -rf _build

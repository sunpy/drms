all: paper.pdf

paper.pdf: paper.md paper.bib latex.template
	pandoc \
	-o paper.pdf \
	-f markdown paper.md \
	-V graphics="true" \
	-V logo_path="joss-logo.png" \
	-V geometry:margin=1in \
	--pdf-engine=xelatex \
	--filter pandoc-citeproc --bibliography paper.bib \
	--from markdown+autolink_bare_uris \
	--template latex.template

clean:
	rm -f paper.pdf

.PHONY: clean all

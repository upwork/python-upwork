# First delete ``reference-docs`` and ``_gh-pages`` folders

sphinx-apidoc --force -o reference-docs upwork
sphinx-build -a -b html . _gh-pages

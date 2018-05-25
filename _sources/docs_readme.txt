========================
Generating documentation
========================

For documentation we use ``sphinx``, it autogenerates the documentation into html.

To generate new docs do the following:

1) Generate reference documetation for ``upwork`` module::

    sphinx-apidoc --force -o reference-docs upwork

2) Edit the ``reference-docs/upwork.rst``:

    * Move ``Module contents`` section to the top
    * Delete ``upwork.tests module`` section

3) Edit the ``reference-docs/upwork.routers.rst``:

   * Move ``Module contents`` section to the top

4) Generate documentation in html format::

    sphinx-build -b html . _gh-pages

5) Check the documentation html that everything is okay.

6) Upload contents of ``_gh-pages`` folder to the Github Pages (see ``gh-pages`` branch)::

     sh update_docs.sh

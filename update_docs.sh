# Before don't forget to check generated html docs before update

rm -r /tmp/_gh-pages
cp -r _gh-pages /tmp/.
mv /tmp/_gh-pages/_static /tmp/_gh-pages/static
mv /tmp/_gh-pages/_sources /tmp/_gh-pages/sources
perl -pi -e "s/_static/static/g;" /tmp/_gh-pages/*.html
perl -pi -e "s/_sources/sources/g;" /tmp/_gh-pages/*.html
perl -pi -e "s/_static/static/g;" /tmp/_gh-pages/reference-docs/*.html
perl -pi -e "s/_sources/sources/g;" /tmp/_gh-pages/reference-docs/*.html
git checkout gh-pages -f
cp -rf /tmp/_gh-pages/* .

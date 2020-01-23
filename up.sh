#!/bin/bash -eux
echo -n "plz version: "
read -r v
echo "new version: ${v}"
echo -n "update files ok?:"
read
for i in README.md setup.py wbsv/__init__.py wbsv/Archive.py;do
  sed -r "s/[0-9]\.[0-9]\.[0-9]/${v}/" "${i}" |sponge "${i}"
done
echo -n "rm build dist wbsv.egg-info ok?:"
read
rm -rf build dist wbsv.egg-info
python3 setup.py sdist bdist_wheel
echo -n "commit ok?:"
read
git add .
git commit -m "launch ${v}"
# twine upload --repository pypi dist/*
# git push

#!/usr/bin/zsh -eux
echo -n "plz version: "
read -r v
echo "new version: ${v}"
echo -n "update files ok?:"
read
for i in README.md setup.py wbsv/__init__.py wbsv/Archive.py;do
  sed -r "s/[0-9]\.[0-9]\.[0-9]/${v}/g" "${i}" |sponge "${i}"
done
echo -n "rm build dist wbsv.egg-info ok?:"
read
sudo rm -rf build dist wbsv.egg-info
python3 setup.py sdist bdist_wheel
echo -n "commit ok?:"
read
git add .
git commit -m "launch ${v}"
echo -n "deploy pypi ok?:"
read
/home/eggplants/usr/pip/bin/twine upload --repository pypi dist/*
echo -n "push github ok?:"
read
git push

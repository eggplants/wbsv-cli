#!/usr/bin/zsh
echo -n "plz version: "
read -r v

echo "new version: ${v}"
echo -n "update files ok?:"
read -r f
if [[ "${f}" -eq "y" ]];then
  for i in README.md setup.py wbsv/__init__.py wbsv/Archive.py;do
    sed -r "s/[0-9]\.[0-9]\.[0-9]/${v}/g" "${i}" |sponge "${i}"
  done
fi

echo -n "rm build dist wbsv.egg-info ok?:"
read -r f
if [[ "${f}" -eq "y" ]];then
  sudo rm -rf build dist wbsv.egg-info
  python3 setup.py sdist bdist_wheel
fi

echo -n "commit ok?:"
read -r f
if [[ "${f}" -eq "y" ]];then
  git add .
  git commit -m "launch ${v}"
fi

echo -n "deploy pypi ok?:"
read -r f
if [[ "${f}" -eq "y" ]];then
  twine upload --repository pypi dist/*
fi

echo -n "push github ok?:"
read -r f
if [[ "${f}" -eq "y" ]];then
  git push
fi

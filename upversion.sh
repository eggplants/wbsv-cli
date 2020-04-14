#!/bin/bash

echo "?=>(y|RETURN KEY)"
echo -n "plz version: "
read -r v

echo "new version: ${v}"
echo -n "update files ok?:"
read -r f
if [[ "${f}" -eq 'y' ]]; then
	for i in README.md setup.py wbsv/*py; do
		sed -i -r "s_[0-9]+\.[0-9]+\.[0-9]+_${v}_g" "${i}"
	done
fi

echo -n "rm build dist wbsv.egg-info ok?:"
read -r f
if [[ "${f}" -eq 'y' ]]; then
	sudo rm -rf build dist wbsv.egg-info
	python3 setup.py sdist bdist_wheel
fi

echo -n "git add ok?:"
read -r f
if [[ "${f}" -eq 'y' ]]; then
	git add .
fi

echo -n "git commit ok?:"
read -r f
if [[ "${f}" -eq 'y' ]]; then
	echo -n "plz message(${v}): "
	read -r m
	git commit -m "${m}"
fi

echo -n "deploy pypi ok?(${v}):"
read -r f
if [[ "${f}" -eq 'y' ]]; then
	python3 -m twine upload --repository pypi dist/*
fi

echo -n "push github ok?:"
read -r f
if [[ "${f}" -eq 'y' ]]; then
	git push
fi

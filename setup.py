from setuptools import find_packages, setup

from wbsv import __version__

setup(
    name="wbsv",
    version=__version__,
    description="Throw all URIs in a page on to Wayback Machine from CLI.",
    description_content_type="",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/eggplants/wbsv-cli",
    author="eggplants",
    packages=find_packages(),
    python_requires='>=3.5',
    include_package_data=True,
    license='MIT',
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        "console_scripts": [
            "wbsv=wbsv.main:main"
        ]
    }
)

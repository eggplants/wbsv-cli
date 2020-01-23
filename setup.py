from setuptools import setup, find_packages
setup(
    name="wbsv",
    version="0.0.1",
    description="Throw all URIs in a page on to Wayback Machine savepagenow from CLI.",
    long_description="https://github.com/eggplants/wbsv-cli/blob/master/README.md",
    long_description_content_type='text/markdown',
    url="https://github.com/eggplants/wbsv-cli",
    author="eggplants",
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=["beautifulsoup4", "savepagenow"],
    entry_points={
        "console_scripts": [
            "wbsv=wbsv.Archive:main"
        ]
    }
)

from setuptools import setup, find_packages
setup(
    name="wbsv",
    version="0.1.5",
    description="Throw all URIs in a page on to Wayback Machine savepagenow from CLI.",
    description_content_type="",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/eggplants/wbsv-cli",
    author="eggplants",
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=["beautifulsoup4", "savepagenow"],
    entry_points={
        "console_scripts": [
            "wbsv=wbsv.main:main"
        ]
    }
)

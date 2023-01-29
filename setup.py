from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

name = "sym_mesh"
author = "Martin L'Anton"
author_email = "lantonmartin@gmail.com"
url = "https://github.com/martinlanton/sym_mesh"

description = "Template python package for Maya projects"

python_requires = ">=3.6, <4"

setup(
    name=name,
    version="0.11.0",
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    url=url,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=python_requires,
)

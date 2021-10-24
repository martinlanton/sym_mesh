from setuptools import setup, find_packages

name = 'template_project'
author = "Martin L'Anton"
author_email = "lantonmartin@gmail.com"
url = "https://github.com/martinlanton/tox_template_project"

setup(
    name=name,
    version='0.1.0',
    author=author,
    author_email=author_email,
    url=url,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
)

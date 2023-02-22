import frameworks
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(name="pastelaria-1",
    version=frameworks.__version__,
    author='Thais Ribeiro',
    author_email='thaisribeirodn@gmail.com',
    description='CLI for generating API boilerplates',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thaisribeiro/pastelaria",
    packages=find_packages(),
    py_modules = ['pastelaria', 'frameworks'],
    install_requires=[requirements],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        pastelaria=pastelaria:cli
    ''',
    python_requires=">=3.10",
)
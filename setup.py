import glob
import frameworks
from setuptools import setup, find_packages

def get_scripts_bin():
    return glob.glob("cli/*")

def get_package_description():
    with open("README.md", "r") as stream:
        readme = stream.read()
    with open("HISTORY.md", "r") as stream:
        history = stream.read()
    return f"{readme}\n\n{history}"

def get_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    return requirements

setup(
    name="pastelaria",
    version=frameworks.__version__,
    author = 'Thais Ribeiro',
    author_email = 'thaisribeirodn@gmail.com',
    description = 'CLI for generating API boilerplates',
    long_description=get_package_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/thaisribeiro/pastelaria",
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=get_scripts_bin(),
    python_requires=">=3.10",
)
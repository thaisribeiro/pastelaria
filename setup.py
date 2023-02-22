from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'ranpass',
    version = '0.0.4',
    author = 'Anish Krishnaswamy',
    author_email = 'kanish671@gmail.com',
    license = 'MIT',
    description = 'random password generator',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/kanish671/ranpass',
    py_modules = ['pastelaria', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        ranpass=ranpass:cli
    '''
)
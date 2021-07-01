from setuptools import setup

setup(
    name="BibtexFixer",
    version="0.1.0",
    description="A CLI for removing duplicate entries in Bibtex file",
    url="https://github.com/masrul/BibtexFixer",
    author="Masrul Huda",
    author_email="mmh568@msstate.edu",
    packages=["BibtexFixer"],
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: General",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["BibtexFixer=BibtexFixer.BibtexFixer:main"],},
)

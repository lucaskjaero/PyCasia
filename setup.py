from distutils.core import setup
from setuptools import find_packages

setup(
    name = "Pycasia",
    packages = find_packages(exclude=['contrib', 'docs', 'tests*']),
    version = "v0.2",
    description = "Pycasia is an open source library to work with the CASIA Chinese Handwriting library.",
    author = "Lucas Kjaero",
    author_email = "Lucas@LucasKjaero.com",
    url = "https://github.com/lucaskjaero/pycasia",
    keywords = ["handwriting", "Chinese", "CASIA"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
    ],
    long_description=open('README.txt').read(),
    install_requires=['numpy', 'Pillow', 'tqdm'],
)

from distutils.core import setup
setup(
    name = "pycasia",
    packages = []
    version = "v0.1",
    description = "Open source library to work with the CASIA Chinese Handwriting library.",
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
)

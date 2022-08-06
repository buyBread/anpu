from setuptools import setup

with open("README.md", "r") as fp:
    readme = fp.read()

setup(
    name="anpu",
    version="1.0",
    description="A small library to search Spotify music.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="buyBread",
    url="https://github.com/buyBread/anpu",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3"],
    keywords=[
        "spotify",
        "spotify api"],
    install_requires=["requests"])

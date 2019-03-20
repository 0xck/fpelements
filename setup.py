from setuptools import setup, find_packages

PACKAGE = "fpe"


setup(
    name=PACKAGE,
    version=__import__(PACKAGE).__version__,
    packages=find_packages(
        exclude=["tests.*", "tests", "*.md", "requirements"]),
    description="Functional programming tools",
    long_description=open("README.txt").read(),
    test_suite="tests",
    author="Constantine Kormashev",
    author_email="constantine.kormashev@gmail.com",
    license="Mozilla Public License 2.0",
    url="https://github.com/0xck/fpelements",
    zip_safe=False
)

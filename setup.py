from setuptools import setup, find_packages

# import unittest
# import doctest
requirements = ["numpy"]

setup(
    name="testzd",
    version="0.0.1",
    install_requires=requirements,
    packages=find_packages("src"),
    package_dir={"": "src"},
    description="Code to test if a strategy is Zero determinant",
)

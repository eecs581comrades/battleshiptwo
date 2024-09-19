
from setuptools import setup, find_packages

setup(
    name="Battleship",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
    ],
    scripts=[
        'scripts/explode.py',
        'scripts/shatter_explode.py',
    ],
)

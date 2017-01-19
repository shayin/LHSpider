# _*_ coding: utf-8 _*_

"""
install script: python setup.py install
"""

from setuptools import setup, find_packages

setup(
    name="lhspider",
    version="0.1",
    author="huangxuanxin",
    keywords=["spider", "crawler"],
    packages=find_packages(exclude=("app", "bin")),
    package_data={
        "": ["*.conf"],  # include all *.conf files
    },
    install_requires=[

    ]
)

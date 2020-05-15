#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: qintianchen
# Mail: 1365265750@qq.com
# Created Time: 2020-5-15 11:44:00
#############################################


from setuptools import setup, find_packages

setup(
    name="GAutomatorAndroid",
    version="0.1.0",
    keywords=("pip", "pathtool", "timetool", "magetool", "mage"),
    description="A tool for android automation",
    long_description="time and path tool",
    license="MIT Licence",

    url="https://github.com/qintianchen/GAutomator/tree/master/GAutomatorAndroid",
    author="qintianchen",
    author_email="1365265750@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "numpy>=1.18.3",
        "opencv-python>=4.2.0.34",
        "xlrd>=1.2.0",
        "xlwt>=1.3.0",
    ]
)
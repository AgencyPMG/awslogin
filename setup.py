#! /usr/bin/env python

import setuptools

setuptools.setup(
    name="awslogin",
    version="0.1",
    url="https://github.com/AgencyPMG/awslogin",
    author="Christopher Davis",
    author_email="chris@pmg.com",
    description="A command line tool to log into AWS accounts via a switched role",
    py_modules=["awslogin"],
    classifiers=[
        "License :: MIT",
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'boto3>=1.4,<2.0',
    ],
    entry_points={
        "console_scripts": [
            "awslogin = awslogin:main",
        ]
    }
)

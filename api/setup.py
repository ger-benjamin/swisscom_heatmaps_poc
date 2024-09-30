# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
INSTALL_REQUIRES = open(os.path.join(HERE, "requirements.txt")).read().splitlines()

setup(
    name="swisscom_heatmap_geoproxy",
    version="1.0.0",
    description="Proxy for the swisscom heatmap to returns geo-compatible info",
    author="camptocamp",
    author_email="info@camptocamp.com",
    url="https://camptocamp.com/geospatial-solutions",
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "paste.app_factory": [
            "main = swisscom_heatmap_geoproxy:main",
        ],
    },
)

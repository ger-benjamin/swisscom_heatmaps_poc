# -*- coding: utf-8 -*-

from c2cwsgiutils.health_check import HealthCheck
from pyramid.config import Configurator

import logging

LOG = logging.getLogger(__name__)


def main(global_config, **settings):
    LOG.warning("setup main")
    config = Configurator(settings=settings)
    config.include("c2cwsgiutils.pyramid")
    config.scan("swisscom_heatmap_geoproxy.views")

    # Initialize the health checks
    health_check = HealthCheck(config)
    LOG.warning("main is set up")

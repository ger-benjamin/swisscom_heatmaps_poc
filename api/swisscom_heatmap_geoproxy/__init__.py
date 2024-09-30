# -*- coding: utf-8 -*-

from c2cwsgiutils.health_check import HealthCheck
from pyramid.config import Configurator
from papyrus.renderers import GeoJSON

import logging

LOG = logging.getLogger(__name__)


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("c2cwsgiutils.pyramid")
    config.scan("swisscom_heatmap_geoproxy.views")
    config.add_renderer("geojson", GeoJSON())

    # Initialize the health checks
    health_check = HealthCheck(config)
    LOG.info("swisscom_heatmap_geoapi is now up")
    return config.make_wsgi_app()

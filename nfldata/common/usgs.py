"""Defines common utilities needed to scrape the USGS website."""
from urllib.parse import urljoin
from scrapy_splash import SplashRequest

USGS_GEONAMES_DOMAIN = 'geonames.usgs.gov'
SPLASH_REQUEST_ARGS = {'wait': 1, 'timeout': 300}


def usgs_geonames_request(uri, query='', meta=None, callback=None):
    """Creates a SplashRequest specifically for the USGS GeoNames service."""

    url = urljoin(f'http://{USGS_GEONAMES_DOMAIN}', uri) + f'?{query}'
    return SplashRequest(url,
                         callback=callback,
                         args=SPLASH_REQUEST_ARGS,
                         meta=meta)

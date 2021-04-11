"""Defines common utilities needed to scrape Pro Football Reference."""
from urllib.parse import urljoin
from scrapy_splash import SplashRequest

PRO_FOOTBALL_REFERENCE_DOMAIN = 'pro-football-reference.com'
SPLASH_REQUEST_ARGS = {'wait': 1, 'timeout': 300}


def pfr_request(uri, meta=None, callback=None):
    """Creates a SplashRequest specifically for Pro Football Reference."""

    url = urljoin('http://' + PRO_FOOTBALL_REFERENCE_DOMAIN, uri)
    return SplashRequest(url,
                         callback=callback,
                         args=SPLASH_REQUEST_ARGS,
                         meta=meta)

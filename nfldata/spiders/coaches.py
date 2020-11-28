"""Defines spiders related to NFL coaches."""
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.coaches import Coach


class CoachesSpider(scrapy.Spider):
    """The spider that crawls and stores information about NFL coaches."""

    name = 'coaches'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""

        Coach.sql_create(database)

    def start_requests(self):
        return [pfr_request('coaches')]

    def parse(self, response):  # pylint: disable=arguments-differ
        for row in response.css('table#coaches tbody tr:not(.thead)'):
            coach = row.css('td[data-stat="coach"] a::attr(href)').get()
            name = row.css('td[data-stat="coach"] a::text').get()
            yield Coach(coach=coach, name=name)

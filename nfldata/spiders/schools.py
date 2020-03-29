"""Defines spiders related to schools that NFL players have attended."""
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.schools import School


class SchoolsSpider(scrapy.Spider):
    """The spider that crawls and stores information about schools that players
    have attended."""

    name = 'schools'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""

        School.sql_create(database)

    def start_requests(self):
        return [pfr_request('schools')]

    def parse(self, response):
        for row in response.css(
                'table#college_stats_table tbody tr:not(.thead)'):
            school = row.css('td[data-stat="college_name"] a::attr(href)').get()
            if school:
                name = row.css('td[data-stat="college_name"] a::text').get()
                yield School(school=school, name=name)

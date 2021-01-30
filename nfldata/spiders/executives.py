"""Defines spiders related to NFL executives."""
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.executives import Executive, FrontOfficeMember


# TODO parse player transactions for free agents and undrafted free agents.
class ExecutivesSpider(scrapy.Spider):
    """The spider that crawls and stores information about NFL coaches."""

    name = 'executives'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Creates the table needed for this spider."""
        Executive.sql_create(database)

    def start_requests(self):
        return [pfr_request('executives')]

    def parse(self, response):  # pylint: disable=arguments-differ
        for row in response.css('table#executives tbody tr:not(.thead)'):
            executive = row.css('th[data-stat=exec] a::attr(href)').get()
            name = row.css('th[data-stat=exec] a::text').get()
            yield Executive(executive=executive, name=name)


class FrontOfficeMembersSpider(scrapy.Spider):
    """The spider that crawls and stores the executives of each team across NFL
    history."""

    name = 'front_office_members'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""
        FrontOfficeMember.sql_create(database)

    def start_requests(self):
        return [pfr_request('executives')]

    def parse(self, response):  # pylint: disable=arguments-differ
        for row in response.css('table#executives tbody tr:not(.thead)'):
            link = row.css('th[data-stat=exec] a::attr(href)').get()
            yield pfr_request(link,
                              meta={'executive': link},
                              callback=parse_executive)


def parse_executive(response):
    """Parse the executive's jobs from their page."""

    for row in response.css('table#exec_results tbody tr:not(.thead)'):
        executive = response.meta['executive']
        team = row.css('td[data-stat=team] a::attr(href)').get()
        title = row.css('td[data-stat=job_title]::text').get()
        yield FrontOfficeMember(executive=executive, team=team, title=title)

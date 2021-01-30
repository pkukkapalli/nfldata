"""Defines spiders related to NFL coaches."""
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.coaches import Coach, CoachingStaffMember


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


class CoachingStaffMembersSpider(scrapy.Spider):
    """The spider that crawls and stores the coaches of each team across NFL
    history.

    Note that right now, only head coaches are scraped."""

    name = 'coaching_staffs'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""

        CoachingStaffMember.sql_create(database)

    def start_requests(self):
        return [pfr_request('teams')]

    def parse(self, response):  # pylint: disable=arguments-differ
        for link in response.css(
                'th[data-stat=team_name] a::attr(href)').getall():
            yield pfr_request(link, callback=parse_franchise)


def parse_franchise(response):
    """Follow the links to all of the teams for this franchise."""

    for link in response.css('th[data-stat=year_id] a::attr(href)').getall():
        yield pfr_request(link, meta={'team': link}, callback=parse_coach)


def parse_coach(response):
    """Parse the coach from a team's page."""

    coach = response.xpath("//p[contains(., 'Coach:')]/a/@href").get()
    team = response.meta['team']
    yield CoachingStaffMember(coach=coach, team=team)

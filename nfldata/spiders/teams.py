"""Defines the spiders related to NFL teams"""
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.teams import Franchise, Team


class FranchisesSpider(scrapy.Spider):
    """The spider that crawls and stores the franchises throughout history."""

    name = 'franchises'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""
        Franchise.sql_create(database)

    def start_requests(self):
        return [pfr_request('teams')]

    def parse(self, response):
        for row in response.css('th[data-stat="team_name"] a'):
            franchise = row.css('::attr(href)').get()
            if franchise.endswith('/'):
                franchise = franchise[:-1]
            name = row.css('::text').get()
            yield Franchise(franchise=franchise, name=name)


class TeamsSpider(scrapy.Spider):
    """The spider that crawls and stores the teams that have played throughout
    NFL history."""

    name = 'teams'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""
        Team.sql_create(database)

    def start_requests(self):
        return [pfr_request('teams')]

    def parse(self, response):  # pylint: disable=arguments-differ
        for row in response.css('th[data-stat="team_name"] a'):
            franchise = row.css('::attr(href)').get()
            if franchise.endswith('/'):
                franchise = franchise[:-1]
            yield pfr_request(franchise,
                              meta={'franchise': franchise},
                              callback=parse_franchise)


def parse_franchise(response):
    """Parses all of the teams in a single franchise into Team items."""

    for row in response.css('table#team_index tr[data-row]:not(.thead)'):
        team = row.css('td[data-stat="team"] a::attr(href)').get()
        year = int(row.css('th[data-stat="year_id"] a::text').get())
        name = row.css('td[data-stat="team"] a::text').get()
        franchise = response.meta['franchise']
        regular_season_wins = int(row.css('td[data-stat="wins"]::text').get())
        regular_season_losses = int(
            row.css('td[data-stat="losses"]::text').get())

        # Some tables do not have a ties column if there were no ties that year.
        regular_season_ties = row.css('td[data-stat="ties"]::text').get()
        if regular_season_ties:
            regular_season_ties = int(regular_season_ties)
        else:
            regular_season_ties = 0

        yield Team(team=team,
                   year=year,
                   name=name,
                   franchise=franchise,
                   regular_season_wins=regular_season_wins,
                   regular_season_losses=regular_season_losses,
                   regular_season_ties=regular_season_ties)

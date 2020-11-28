"""Defines the spiders related to NFL teams"""
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.teams import Team


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
        return [pfr_request('years')]

    def parse(self, response):  # pylint: disable=arguments-differ
        for row in response.css('th[data-stat="year_id"] a'):
            link = row.css('::attr(href)').get()
            year = int(row.css('::text').get())
            yield pfr_request(link, meta={'year': year}, callback=parse_year)


def parse_year(response):
    """Parses all of the teams in a single year into Team items."""

    rows = [
        *response.css('table#NFL tr[data-row]:not(.thead)'),
        *response.css('table#APFA tr[data-row]:not(.thead)'),
        *response.css('table#NFC tr[data-row]:not(.thead)'),
        *response.css('table#AFC tr[data-row]:not(.thead)'),
    ]
    for row in rows:
        team = row.css('th[data-stat="team"] a::attr(href)').get()
        year = response.meta['year']
        name = row.css('th[data-stat="team"] a::text').get()
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
                   regular_season_wins=regular_season_wins,
                   regular_season_losses=regular_season_losses,
                   regular_season_ties=regular_season_ties)

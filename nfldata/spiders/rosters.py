"""Defines spiders related to NFL rosters."""
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.rosters import RosterMember


class RosterMembersSpider(scrapy.Spider):
    """The spider that crawls and stores the rosters of all teams across NFL
    history."""

    name = 'roster_members'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""

        RosterMember.sql_create(database)

    def start_requests(self):
        return [pfr_request('teams')]

    def parse(self, response):
        for link in response.css(
                'th[data-stat=team_name] a::attr(href)').getall():
            yield pfr_request(link, callback=parse_franchise)


def parse_franchise(response):
    """Follow the links to all of the teams for this franchise."""

    for link in response.css('th[data-stat=year_id] a::attr(href)').getall():
        yield pfr_request(link, meta={'team': link}, callback=parse_team)


def parse_team(response):
    """Follow link for this team's roster."""

    link = response.css('a:contains("Starters & Roster")::attr(href)').get()
    yield pfr_request(link,
                      meta={'team': response.meta['team']},
                      callback=parse_roster)


def parse_roster(response):
    """Parse all of the player rows in this roster."""

    for row in response.css('table#games_played_team tbody tr:not(.thead)'):
        player = row.css('[data-stat="player"] a::attr(href)').get()
        team = response.meta['team']
        approximate_value = row.css('[data-stat="av"]::text').get()
        approximate_value = int(approximate_value) if approximate_value else 0
        yield RosterMember(player=player,
                           team=team,
                           approximate_value=approximate_value)

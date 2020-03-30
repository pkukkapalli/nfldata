"""Defines spiders related to NFL players."""
import re
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.players import (Player, PlayerType, PlayerPosition,
                                   PFR_POSITION_CODES_TRANSLATIONS)


class PlayersSpider(scrapy.Spider):
    """The spider that crawls and stores all of the players that have played
    throughout NFL history."""

    name = 'players'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""

        Player.sql_create(database)
        PlayerPosition.sql_create(database)

    def start_requests(self):
        return [pfr_request('players')]

    def parse(self, response):
        for link in response.css('#div_alphabet a::attr(href)').getall():
            yield pfr_request(link, callback=parse_players)


def parse_players(response):
    """Parses a page of players into many Player items."""

    for link in response.css('#div_players a::attr(href)').getall():
        yield pfr_request(link, meta={'player': link}, callback=parse_player)


def parse_player(response):
    """Parse player details from a single player's profile."""

    player = response.meta['player']
    name = response.css('[itemprop=name]::text').get()
    first_team_all_pros = parse_first_team_all_pros(response)
    pro_bowls = parse_pro_bowls(response)
    career_approx_value = parse_career_approx_value(response)

    yield Player(player=player,
                 name=name,
                 first_team_all_pros=first_team_all_pros,
                 pro_bowls=pro_bowls,
                 career_approx_value=career_approx_value)

    for position in parse_positions(response):
        yield PlayerPosition(player=player, position=position)


def parse_first_team_all_pros(response):
    """Parse the number of first team all-pros that a player has from his
    profile page."""

    first_team_all_pros = response.css(
        '#leaderboard_all_pro button::text').get()

    if not first_team_all_pros:
        return 0

    return int(first_team_all_pros.split(' ')[0])


def parse_pro_bowls(response):
    """Parse the number of pro bowls that a player has from his profile page."""

    pro_bowls = response.css('#leaderboard_pro_bowls button::text').get()

    if not pro_bowls:
        return 0

    return int(pro_bowls.split(' ')[0])


def parse_career_approx_value(response):
    """Parse the amount of approximate value a player has accumulated over their
    career from their profile page."""

    career_approx_value = response.css(
        '[itemscope] p:contains("Weighted Career AV")::text').get()

    if not career_approx_value:
        return 0

    return int(career_approx_value.strip().split(' ')[0])


def parse_positions(response):
    """Parse out the positions that his player has played over their career."""

    positions = response.css(
        'table.stats_table td[data-stat=pos]::text').getall()
    positions = [re.split('[,/\-]', p) for p in positions if p]
    # Flatten list
    positions = [p for sublist in positions for p in sublist]
    positions = [parse_position(p.upper().strip()) for p in positions if p]
    # Flatten list and make unique.
    return list(set([p for sublist in positions for p in sublist]))


def parse_position(position):
    """Parse an individual position code into an instance of PlayerType."""

    if position in PFR_POSITION_CODES_TRANSLATIONS:
        return PFR_POSITION_CODES_TRANSLATIONS[position]

    return [PlayerType[position]]

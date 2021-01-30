""" Defines spiders related to the NFL draft."""
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.draft import DraftPick, DraftType


class DraftPicksSpider(scrapy.Spider):
    """The spider that crawls and stores the draft selections of all teams
    across NFL history."""

    name = 'draft_picks'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""

        DraftPick.sql_create(database)

    def start_requests(self):
        return [create_request(year) for year in range(1936, 2020)]

    def parse(self, response):  # pylint: disable=arguments-differ
        for row in response.css('table#drafts tbody tr:not(.thead)'):
            yield parse_item(response.meta['year'], DraftType.NORMAL, row)

        for row in response.css('table#drafts_supp tbody tr:not(.thead)'):
            yield parse_item(response.meta['year'], DraftType.SUPPLEMENTAL, row)


def create_request(year):
    """Returns a splash request for the draft picks from the given year."""

    return pfr_request('years/{}/draft.htm'.format(year), meta={'year': year})


def parse_int(row, css, invalid_value):
    """Parses an int from the given row using the css selector. Returns
    invalid_value if there is no value."""

    result = row.css(css).get()
    if result:
        return int(result)
    return invalid_value


def parse_item(year, draft_type, row):
    """Parses the given row out into a DraftPick item."""

    draft_round = parse_int(row, 'th[data-stat="draft_round"]::text', -1)
    draft_pick = parse_int(row, 'td[data-stat="draft_pick"]::text', -1)
    franchise = '/'.join(
        row.css('td[data-stat="team"] a::attr(href)').get().split('/')[:-1])

    player = row.css('td[data-stat="player"] a::attr(href)').get()
    if not player:
        player = row.css('td[data-stat="player"]::text').get()

    position = row.css('td[data-stat="pos"]::text').get()
    age = parse_int(row, 'td[data-stat="age"]::text', -1)
    first_team_all_pros = parse_int(
        row, 'td[data-stat="all_pros_first_team"]::text', 0)
    pro_bowls = parse_int(row, 'td[data-stat="pro_bowls"]::text', 0)
    career_approx_value = parse_int(row, 'td[data-stat="career_av"]::text', 0)
    draft_approx_value = parse_int(row, 'td[data-stat="draft_av"]::text', 0)

    college = row.css('td[data-stat="college_id"] a::attr(href)').get()
    if not college:
        college = row.css('td[data-stat="college_id"]::text').get()

    return DraftPick(year=year,
                     draft_type=draft_type,
                     draft_round=draft_round,
                     draft_pick=draft_pick,
                     franchise=franchise,
                     player=player,
                     position=position,
                     age=age,
                     first_team_all_pros=first_team_all_pros,
                     pro_bowls=pro_bowls,
                     career_approx_value=career_approx_value,
                     draft_approx_value=draft_approx_value,
                     college=college)

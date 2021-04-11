import logging
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.common.usgs import usgs_geonames_request, USGS_GEONAMES_DOMAIN
from nfldata.common.address import parse_address
from nfldata.items.stadiums import Stadium, StadiumMember


class StadiumsSpider(scrapy.Spider):
    """The spider that crawls and stores the stadiums that teams play at."""

    name = 'stadiums'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""
        Stadium.sql_create(database)
        StadiumMember.sql_create(database)

    def start_requests(self):
        return [pfr_request('teams')]

    def parse(self, response):  # pylint: disable=arguments-differ
        for row in response.css('th[data-stat="team_name"] a'):
            franchise = row.css('::attr(href)').get()
            if franchise.endswith('/'):
                franchise = franchise[:-1]
            yield pfr_request(franchise,
                              meta={'franchise': franchise},
                              callback=parse_teams_for_franchise)


def parse_teams_for_franchise(response):
    """Parses all of the teams in a single franchises."""

    for row in response.css('table#team_index tr[data-row]:not(.thead)'):
        team = row.css('td[data-stat="team"] a::attr(href)').get()
        yield pfr_request(team, meta={'team': team}, callback=parse_stadium)


def parse_stadium(response):
    team = response.meta['team']
    stadium = response.xpath("//p[contains(., 'Stadium:')]/a/@href").get()
    if stadium:
        yield pfr_request(stadium,
                          meta={
                              'team': team,
                              'stadium': stadium
                          },
                          callback=parse_stadium_address)
    else:
        logging.warning(f'No stadium found for {team}')


def parse_stadium_address(response):
    name = response.css('#meta h1[itemprop="name"]::text').get().rstrip(
        ' History')

    address = response.css('#meta p::text').get()
    if not address.strip():
        return

    address = parse_address(address)
    stadium = response.meta['stadium']
    yield Stadium(stadium=stadium,
                  name=name,
                  city=address.city,
                  state=address.state)
    yield StadiumMember(stadium=stadium, team=response.meta['team'])


class CityElevationsSpider(scrapy.Spider):
    """The spider that crawls and stores the elevations of various cities."""

    name = 'city_elevations'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN, USGS_GEONAMES_DOMAIN]

    def start_requests(self):
        return [usgs_geonames_request('/apex/f', query='p=gnispq')]

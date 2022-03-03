"""Defines spiders related to NFL coaches."""
import re
import numpy as np
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.coaches import Coach, CoachingPosition, CoachingStaffMember, coaching_position_from_string

COACHES_POSITION_REGEX = re.compile(r'\((.+)\)')


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
        yield pfr_request(link, meta={'team': link}, callback=parse_coaches)


def parse_coaches(response):
    """Parse the coaches from a team's page."""

    coach = response.xpath("//p[contains(., 'Coach:')]/a/@href").get()
    team = response.meta['team']
    yield CoachingStaffMember(coach=coach,
                              team=team,
                              position=CoachingPosition.HEAD_COACH)

    offensive_coordinator = response.xpath(
        "//p[contains(., 'Offensive Coordinator:')]/a/@href").get()
    if offensive_coordinator:
        yield CoachingStaffMember(
            coach=offensive_coordinator,
            team=team,
            position=CoachingPosition.OFFENSIVE_COORDINATOR)

    defensive_coordinator = response.xpath(
        "//p[contains(., 'Defensive Coordinator:')]/a/@href").get()
    if defensive_coordinator:
        yield CoachingStaffMember(
            coach=defensive_coordinator,
            team=team,
            position=CoachingPosition.DEFENSIVE_COORDNATOR)

    assistant_coaches = response.xpath(
        "//p[contains(., 'Other Notable Asst')]/a/@href").getall()
    if assistant_coaches is not None and len(assistant_coaches) > 0:
        positions = response.xpath(
            "//p[contains(., 'Other Notable Asst')]/text()").getall()
        positions = np.hstack(
            [COACHES_POSITION_REGEX.findall(p) for p in positions])
        if len(assistant_coaches) != len(positions):
            raise ValueError(
                f'different number of assistant coaches ({assistant_coaches}) and positions ({positions}) found'
            )
        for coach, position in zip(assistant_coaches, positions):
            position = position.replace(' ', '_').upper()
            position = coaching_position_from_string(position)
            yield CoachingStaffMember(coach=coach, team=team, position=position)

"""Defines spiders related to player injuries."""
import re
import scrapy
from nfldata.common.pfr import pfr_request, PRO_FOOTBALL_REFERENCE_DOMAIN
from nfldata.items.injuries import (Injury, InjuryReason, InjuryStatus,
                                    InjuryOutcome, InjuryType,
                                    PFR_INJURY_REASON_SUBSTITUTIONS)


class InjuriesSpider(scrapy.Spider):
    """The spider that crawls and stores all of the injuries that players have
    had in NFL history."""

    name = 'injuries'
    allowed_domains = [PRO_FOOTBALL_REFERENCE_DOMAIN]

    @classmethod
    def create_table(cls, database):
        """Create the table needed for this spider."""

        Injury.sql_create(database)
        InjuryReason.sql_create(database)

    def start_requests(self):
        return [pfr_request('teams')]

    def parse(self, response):
        for link in response.css(
                'th[data-stat=team_name] a::attr(href)').getall():
            yield pfr_request(link, callback=parse_franchise)


def parse_franchise(response):
    """Follow the links to all of the teams for this franchise."""

    for link in parse_team_links(response):
        yield pfr_request(link, meta={'team': link}, callback=parse_team)


def parse_team_links(response):
    """Parse the links to individual teams from a franchise page to get injury
    reports."""

    years = response.css('th[data-stat=year_id] a::text').getall()
    links = response.css('th[data-stat=year_id] a::attr(href)').getall()
    # Injury reports are only available from 2009 onwards.
    return [link for year, link in zip(years, links) if int(year) >= 2009]


def parse_team(response):
    """Follow link for this team's roster."""

    link = response.css('a:contains("Injury Report")::attr(href)').get()
    yield pfr_request(link,
                      meta={'team': response.meta['team']},
                      callback=parse_injuries)


def parse_injuries(response):
    """Parse and yield Injury items for each injury report."""

    for row in response.css('table#team_injuries tbody tr:not(.thead)'):
        player = row.css('[data-stat=player] a::attr(href)').get()
        team = response.meta['team']
        for column in [c for c in row.css('td') if c.css('::text').get()]:
            week = parse_week(column)
            status = parse_status(column)
            yield Injury(player=player,
                         team=team,
                         week=week,
                         status=status,
                         outcome=parse_outcome(column))

            for reason in parse_reasons(status, column):
                yield InjuryReason(player=player,
                                   team=team,
                                   week=week,
                                   reason=reason)


def parse_week(column):
    """Parse the week number of the given injury report column."""

    week = column.css('::attr(data-stat)').get()
    return int(week.lstrip('week_'))


def parse_reasons(status, column):
    """Parse the injury type of the given injury report column."""

    if status == InjuryStatus.SUSPENDED:
        return [InjuryType.SUSPENSION]

    reasons = column.css('::attr(data-tip)').get()
    _, reasons = reasons.split(':')
    reasons = re.split(', |/|,', reasons.strip().upper())
    reasons = [parse_reason(r) for r in reasons]
    # Flatten list before returning
    return [r for sublist in reasons for r in sublist]


def parse_reason(reason):
    """Parse the given reason into one or more instances of InjuryReason."""

    reason = ascii(reason).replace(' ', '_').replace('-', '_').replace(
        '\'', '').replace('\"', '')

    # Correct typo
    if reason in PFR_INJURY_REASON_SUBSTITUTIONS:
        return PFR_INJURY_REASON_SUBSTITUTIONS[reason]

    return [InjuryType[reason]]


def parse_status(column):
    """Parse the status of the given injury report column."""

    status = column.css('::attr(data-tip)').get()
    raw_status, _ = status.split(':')
    status = raw_status.strip().upper().replace(' ', '_')

    # Will throw an exception if the status is missing from InjuryStatus.
    return InjuryStatus[status]


def parse_outcome(column):
    """Parse whether the player played or not from the given injury report
    column."""

    classes = column.css('::attr(class)').get().split(' ')

    if 'dnp' in classes:
        return InjuryOutcome.DID_NOT_PLAY

    return InjuryOutcome.PLAYED

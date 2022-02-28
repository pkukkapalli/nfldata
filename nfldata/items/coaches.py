"""Defines items related to NFL coaches."""
from enum import Enum, auto
from turtle import pos
import scrapy


class Coach(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines information related to a specific NFL coach."""

    # A relative link on Pro Football Reference to the coach.
    coach = scrapy.Field()

    # The display name of the coach.
    name = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """Creates the coaches table if one does not exist in the given
        database. Note that this does not update the fields if the table already
        exists, but the fields are outdated."""

        database.execute('''
            CREATE TABLE IF NOT EXISTS coaches (
                coach TEXT PRIMARY KEY,
                name TEXT
            )
        ''')

    def sql_insert(self, database):
        """Inserts this coach into the coaches table in the given database."""

        database.execute(
            '''
            INSERT OR REPLACE INTO coaches (
                coach,
                name
            ) VALUES (
                ?,
                ?
            )
        ''', (self['coach'], self['name']))


class CoachingStaffMember(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines a single coach's membership on a coaching staff."""

    # A relative link on Pro Football Reference to the coach.
    coach = scrapy.Field()

    # A relative link on Pro Football Reference to the coach's team.
    team = scrapy.Field()

    # The position of the coach on this team.
    position = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """
        Creates the coaching_staff_members table if one does not exist in the
        given databse. Note that this does not update the fields if the table
        already exists, but the fields are outdated.
        """
        database.execute('''
            CREATE TABLE IF NOT EXISTS coaching_staff_members (
                coach TEXT,
                team TEXT,
                position TEXT,
                PRIMARY KEY (coach, team),
                FOREIGN KEY (coach) REFERENCES coaches(coach),
                FOREIGN KEY (team) REFERENCES teams(team)
            )
        ''')

    def sql_insert(self, database):
        """
        Insert this coach into the coaching_staff_members table in the given
        database.
        """
        database.execute(
            '''
            INSERT OR REPLACE INTO coaching_staff_members (
                coach,
                team,
                position
            ) VALUES (
                ?,
                ?,
                ?
            )
            ''', (self['coach'], self['team'], self['position'].name))


class CoachingPosition(Enum):
    # Major coaching positions
    HEAD_COACH = auto()
    ASSISTANT_HEAD_COACH = auto()
    OFFENSIVE_COORDINATOR = auto()
    DEFENSIVE_COORDNATOR = auto()
    # Offensive position coaches
    QUARTERBACKS = auto()
    ASSISTANT_QUARTERBACKS = auto()
    RUNNING_BACKS = auto()
    ASSISTANT_RUNNING_BACKS = auto()
    WIDE_RECEIVERS = auto()
    ASSISTANT_WIDE_RECEIVERS = auto()
    TIGHT_ENDS = auto()
    ASSISTANT_TIGHT_ENDS = auto()
    OFFENSIVE_LINE = auto()
    ASSISTANT_OFFENSIVE_LINE = auto()
    ENDS = auto()
    BACKFIELD_COACH = auto()
    OFFENSIVE_ASSISTANT = auto()
    # Defensive position coaches
    DEFENSIVE_LINE = auto()
    ASSISTANT_DEFENSIVE_LINE = auto()
    LINEBACKERS = auto()
    ASSISTANT_LINEBACKERS = auto()
    DEFENSIVE_BACKS = auto()
    ASSISTANT_DEFENSIVE_BACKS = auto()
    DEFENSIVE_ASSISTANT = auto()
    # Special teams
    SPECIAL_TEAMS_COORDINATOR = auto()
    KICKING = auto()
    # Other/legacy coaches
    SCOUT = auto()
    STRENGTH_AND_CONDITIONING = auto()
    # Catch-all for uncategorized assistant coaching positions.
    OTHER_ASSISTANT = auto()


# Common typos and substitutions necessary to parse coaching positions from Pro
# Football Reference.
PFR_COACHING_POSITION_SUBSTITUTIONS = {
    'ASSISTANT_COACH': CoachingPosition.OTHER_ASSISTANT,
    'ASSISTANT_O-LINE_COACH': CoachingPosition.ASSISTANT_OFFENSIVE_LINE,
    'ASSISTANT_QB_COACH': CoachingPosition.ASSISTANT_QUARTERBACKS,
    'ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'COACHING_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'CORNERBACKS': CoachingPosition.DEFENSIVE_BACKS,
    'DEFENSIVE_BACKFIELD': CoachingPosition.DEFENSIVE_BACKS,
    'DEFENSIVE_COACH': CoachingPosition.DEFENSIVE_ASSISTANT,
    'DEFENSIVE_QUALITY_CONTROL': CoachingPosition.DEFENSIVE_ASSISTANT,
    'DEFENSIVE': CoachingPosition.DEFENSIVE_ASSISTANT,
    'FOOTBALL_SYSTEMS_ANALYST': CoachingPosition.OTHER_ASSISTANT,
    'INSIDE_LINEBACKERS': CoachingPosition.LINEBACKERS,
    'LINE_COACH': CoachingPosition.OFFENSIVE_LINE,
    'OFFENSIVE_ASISTANT': CoachingPosition.OFFENSIVE_ASSISTANT,
    'OFFENSIVE_BACKFIELD': CoachingPosition.BACKFIELD_COACH,
    'OFFENSIVE_BACKS': CoachingPosition.BACKFIELD_COACH,
    'OFFENSIVE_COACH': CoachingPosition.OFFENSIVE_ASSISTANT,
    'OFFENSIVE_CONSULTANT': CoachingPosition.OTHER_ASSISTANT,
    'OFFENSIVE_QUALITY_CONTROL': CoachingPosition.OFFENSIVE_ASSISTANT,
    'OL': CoachingPosition.OFFENSIVE_LINE,
    'PERSONNEL_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'PLAYER_PERSONNEL_INTERN': CoachingPosition.OTHER_ASSISTANT,
    'QUALITY_CONTROL': CoachingPosition.OTHER_ASSISTANT,
    'RECEIVERS': CoachingPosition.WIDE_RECEIVERS,
    'SAFETIES': CoachingPosition.DEFENSIVE_BACKS,
    'SECONDARY': CoachingPosition.DEFENSIVE_BACKS,
    'SENIOR_DEFENSIVE_ASSISTANT': CoachingPosition.DEFENSIVE_ASSISTANT,
    'SPECIAL_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'VOLUNTEER_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'CONSULTANT': CoachingPosition.OTHER_ASSISTANT,
    'DEF._QUALITY_CONTROL': CoachingPosition.DEFENSIVE_ASSISTANT,
    'ASSISTANT_TO_THE_HEAD_COACH': CoachingPosition.OTHER_ASSISTANT,
    'SENIOR_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'COACHING_INTERN': CoachingPosition.OTHER_ASSISTANT,
    'ADMINISTRATIVE_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    "COACHES'_ASSISTANT": CoachingPosition.OTHER_ASSISTANT,
    'COACHING_ADMINISTRATIVE_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'OFFENSIVE_COACHING_INTERN': CoachingPosition.OFFENSIVE_ASSISTANT,
    'SR._OFFENSIVE_CONSULTANT': CoachingPosition.OFFENSIVE_ASSISTANT,
    'SPECIAL_ADVISOR': CoachingPosition.OTHER_ASSISTANT,
    'ST': CoachingPosition.SPECIAL_TEAMS_COORDINATOR,
    'ASSISTANT_SECONDARY': CoachingPosition.ASSISTANT_DEFENSIVE_BACKS,
    'ASSOCIATE_HEAD_COACH': CoachingPosition.ASSISTANT_HEAD_COACH,
    'INTERN': CoachingPosition.OTHER_ASSISTANT,
    'TACKLES': CoachingPosition.OFFENSIVE_LINE,
    'SECONDARY_COACH': CoachingPosition.DEFENSIVE_BACKS,
    'INTERIM_DL_COACH': CoachingPosition.DEFENSIVE_LINE,
    'QUALITY_CONTROL_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'PLAYER_PERSONNEL_STAFF': CoachingPosition.SCOUT,
    'DL': CoachingPosition.DEFENSIVE_LINE,
    'LB': CoachingPosition.LINEBACKERS,
    'DB': CoachingPosition.DEFENSIVE_BACKS,
    'ASSISTANT_ST_COACH': CoachingPosition.OTHER_ASSISTANT,
    'DEFENSIVE_INTERN': CoachingPosition.DEFENSIVE_ASSISTANT,
    'QUALITY_CONTROL_COORDINATOR': CoachingPosition.OTHER_ASSISTANT,
    'SPREAD_GAME_ANALYST': CoachingPosition.OTHER_ASSISTANT,
    'RUNNING_GAME_COORDINATOR': CoachingPosition.OFFENSIVE_ASSISTANT,
    'DC': CoachingPosition.DEFENSIVE_COORDNATOR,
    'DEF._RUNNING_GAME_COORDINATOR': CoachingPosition.DEFENSIVE_ASSISTANT,
    'OFF._LINE_ASSISTANT': CoachingPosition.ASSISTANT_OFFENSIVE_LINE,
    'COACHES_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'SECONDARY_(NICKEL_PACKAGE)': CoachingPosition.ASSISTANT_DEFENSIVE_BACKS,
    'SENIOR_ADVISOR': CoachingPosition.OTHER_ASSISTANT,
    'SPECIAL_TEAM_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'ASSISTANT_TO_HEAD_COACH': CoachingPosition.OTHER_ASSISTANT,
    'INTERIM_HEAD_COACH': CoachingPosition.HEAD_COACH,
    'PGC': CoachingPosition.OFFENSIVE_ASSISTANT,
    'DEFENSIVE_TACKLES': CoachingPosition.ASSISTANT_DEFENSIVE_LINE,
    'SR._COACHING_ASSISTANT': CoachingPosition.OTHER_ASSISTANT,
    'DEF._PASSING_GAME_SPECIALIST': CoachingPosition.DEFENSIVE_ASSISTANT,
    'QUATERBACKS': CoachingPosition.QUARTERBACKS,
    'DEFENSIVE_ENDS': CoachingPosition.ASSISTANT_DEFENSIVE_LINE,
    'OFFENSE': CoachingPosition.OFFENSIVE_ASSISTANT,
    'SPECIAL_ASSISTANT_TO_HEAD_COACH': CoachingPosition.OTHER_ASSISTANT,
    'INTERIM_OC': CoachingPosition.OFFENSIVE_ASSISTANT,
    'SAFETIES_COACH': CoachingPosition.ASSISTANT_DEFENSIVE_BACKS,
    'OFFENSIVE_INTERN': CoachingPosition.OFFENSIVE_ASSISTANT,
    'ASSOCIATE_HEAD_COACH-OFFENSE': CoachingPosition.OFFENSIVE_ASSISTANT,
    'DEFENSIVE_ASISTANT': CoachingPosition.DEFENSIVE_ASSISTANT,
}


def coaching_position_from_string(position):
    position = position.replace('ASST.', 'ASSISTANT')
    position = position.replace('ASST', 'ASSISTANT')
    positions = position.split('/')

    for position in positions:
        try:
            return CoachingPosition[position]
        except:
            pass

        if position in PFR_COACHING_POSITION_SUBSTITUTIONS:
            return PFR_COACHING_POSITION_SUBSTITUTIONS[position]
        if 'ASSISTANT_HEAD_COACH' in position or 'ASSISTANT_HC' in position:
            return CoachingPosition.ASSISTANT_HEAD_COACH
        if 'OFFENSIVE_COORDINATOR' in position:
            return CoachingPosition.OFFENSIVE_COORDINATOR
        if 'DEFENSIVE_COORDINATOR' in position:
            return CoachingPosition.DEFENSIVE_COORDNATOR

        if position.startswith('QUARTERBACKS') or position.startswith(
                'QB') or position.endswith('QBS'):
            return CoachingPosition.QUARTERBACKS
        if position.startswith('ASSISTANT_QUARTERBACKS') or position.startswith(
                'ASSISTANT_QB'):
            return CoachingPosition.ASSISTANT_QUARTERBACKS

        if position.startswith('RUNNING_BACKS'):
            return CoachingPosition.RUNNING_BACKS
        if position.startswith('ASSISTANT_RUNNING_BACKS'
                              ) or position.startswith('ASSISTANT_RB'):
            return CoachingPosition.ASSISTANT_RUNNING_BACKS

        if position.startswith('WIDE_RECEIVERS') or position.startswith('WR'):
            return CoachingPosition.WIDE_RECEIVERS
        if position.startswith('ASSISTANT_WIDE_RECEIVERS'
                              ) or position.startswith('ASSISTANT_WR'):
            return CoachingPosition.ASSISTANT_WIDE_RECEIVERS

        if position.startswith('TIGHT_ENDS') or position.startswith('TE'):
            return CoachingPosition.TIGHT_ENDS
        if position.startswith('ASSISTANT_TIGHT_ENDS') or position.startswith(
                'ASSISTANT_TE'):
            return CoachingPosition.ASSISTANT_TIGHT_ENDS

        if position.startswith('OFFENSIVE_LINE') or position.startswith('OL'):
            return CoachingPosition.OFFENSIVE_LINE
        if position.startswith(
                'ASSISTANT_OFFENSIVE_LINE'
        ) or 'OL_COACH' in position or position.startswith('ASSISTANT_OL'):
            return CoachingPosition.ASSISTANT_OFFENSIVE_LINE

        if position.startswith('ENDS'):
            return CoachingPosition.ENDS
        if position.startswith('BACKFIELD_COACH'):
            return CoachingPosition.BACKFIELD_COACH
        if position.startswith(
                'PASSING_COORDINATOR'
        ) or 'OFFENSIVE_ASSISTANT' in position or position.startswith(
                'OFFENSIVE_ASST'
        ) or position.startswith('ASSISTANT_OFFENSE') or position.startswith(
                'PASSING_GAME') or position.startswith('RUN_GAME') or (
                    'OFF' in position and 'QUALITY_CONTROL' in position):
            return CoachingPosition.OFFENSIVE_ASSISTANT

        if position.startswith('DEFENSIVE_LINE'):
            return CoachingPosition.DEFENSIVE_LINE
        if position.startswith('ASSISTANT_DEFENSIVE_LINE'
                              ) or position.startswith('ASSISTANT_DL'):
            return CoachingPosition.ASSISTANT_DEFENSIVE_LINE

        if position.startswith('LINEBACKERS'):
            return CoachingPosition.LINEBACKERS
        if position.startswith(
                'ASSISTANT_LINEBACKERS'
        ) or 'ASSISTANT_LB' in position or 'OUTSIDE_LINEBACKERS' in position or 'INSIDE_LINEBACKERS' in position:
            return CoachingPosition.ASSISTANT_LINEBACKERS

        if position.startswith('DEFENSIVE_BACKS') or position.startswith('DB'):
            return CoachingPosition.DEFENSIVE_BACKS
        if position.startswith('ASSISTANT_DEFENSIVE_BACKS'
                              ) or position.startswith('ASSISTANT_DB'):
            return CoachingPosition.ASSISTANT_DEFENSIVE_BACKS

        if 'DEFENSIVE_ASSISTANT' in position or position.startswith(
                'DEFENSIVE_QUALITY_CONTROL'
        ) or position.startswith('DEFENSIVE_QUALITY') or (
                'DEF' in position and 'QUALITY_CONTROL'
                in position) or position.startswith('SENIOR_DEF._ASSISTANT'):
            return CoachingPosition.DEFENSIVE_ASSISTANT

        if 'SPECIAL_TEAMS' in position:
            return CoachingPosition.SPECIAL_TEAMS_COORDINATOR
        if position.startswith('KICKING'):
            return CoachingPosition.KICKING

        if 'SCOUT' in position:
            return CoachingPosition.SCOUT
        if ('STRENGTH' in position and
                'CONDITIONING' in position) or 'S&C' in position:
            return CoachingPosition.STRENGTH_AND_CONDITIONING

    raise ValueError(f'Could not find position for {positions}')

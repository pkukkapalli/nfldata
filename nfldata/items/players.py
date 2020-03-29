"""Defines items related to NFL players."""
from enum import Enum, auto
import scrapy


# TODO: Rename all items to be suffixed with Item to avoid name collisions with
# enums.
class PlayerType(Enum):
    """Enumerates the positions that an NFL player could have."""

    C = auto()
    CB = auto()
    DE = auto()
    DT = auto()
    ILB = auto()
    K = auto()
    LS = auto()
    OG = auto()
    OLB = auto()
    OT = auto()
    P = auto()
    QB = auto()
    RB = auto()
    S = auto()
    TE = auto()
    WR = auto()


class Player(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines a single player who has played in the NFL."""

    # A relative link on Pro Football Reference to the player.
    player = scrapy.Field()

    # The display name of the player.
    name = scrapy.Field()

    first_team_all_pros = scrapy.Field()

    pro_bowls = scrapy.Field()

    career_approx_value = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """
        Creates the players table if one does not exist in the given database.
        Note that this does not update the fields if the table already exists,
        but the fields are outdated.
        """
        database.execute('''
            CREATE TABLE IF NOT EXISTS players (
                player TEXT PRIMARY KEY,
                name TEXT,
                first_team_all_pros INTEGER,
                pro_bowls INTEGER,
                career_approx_value INTEGER
            )
        ''')

    def sql_insert(self, database):
        """
        Insert this player into the players table in the given database.
        """
        database.execute(
            '''
            INSERT OR REPLACE INTO players (
                player,
                name,
                first_team_all_pros,
                pro_bowls,
                career_approx_value
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?
            )
        ''', (self['player'], self['name'], self['first_team_all_pros'],
              self['pro_bowls'], self['career_approx_value']))


# TODO: Replace all relative links on pro football reference with absolute
# links.
class PlayerPosition(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines a position played by a player. It is possible for a player to
    play multiple positions, so a single player may yield multiple items."""

    # A relative link on Pro Football Reference to the player.
    player = scrapy.Field()

    # A position that is played by the player.
    position = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """
        Creates the player_positions table if one does not exist in the given
        database.
        """
        database.execute('''
            CREATE TABLE IF NOT EXISTS player_positions (
                player TEXT,
                position TEXT,
                PRIMARY KEY (player, position),
                FOREIGN KEY (player) REFERENCES players(player)
            )
        ''')

    def sql_insert(self, database):
        """
        Insert this item into the player_positions table.
        """
        database.execute(
            '''
            INSERT OR REPLACE INTO player_positions (
                player,
                position
            ) VALUES (
                ?,
                ?
            )
        ''', (self['player'], self['position'].name))


PFR_POSITION_CODES_TRANSLATIONS = {}

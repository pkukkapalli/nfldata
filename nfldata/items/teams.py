"""Defines items related to NFL teams."""
import scrapy


class Franchise(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines information related to an NFL franchise."""

    # A relative link on Pro Football Reference to this franchise.
    franchise = scrapy.Field()

    # The display name for this franchise.
    name = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """Creates the franchises table if one does not exist in the given
        database. Note that this does not update the fields if the table already
        exists, but the fields are outdated."""

        database.execute('''
            CREATE TABLE IF NOT EXISTS franchises (
                franchise TEXT PRIMARY KEY,
                name TEXT
            )
        ''')

    @staticmethod
    def from_sql_cursor(cursor):
        """Given a cursor that already contains selected rows, with both the franchise and name fields, return a set of Franchise items."""

    def sql_insert(self, database):
        """Inserts this franchise into the franchises table in the given
        database."""

        database.execute(
            '''
            INSERT OR REPLACE INTO franchises (
                franchise,
                name
            ) VALUES (
                ?,
                ?
            )
            ''', (self['franchise'], self['name']))


class Team(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines information related to a specific NFL team in a specific year."""

    # A relative link on Pro Football Reference to this team.
    team = scrapy.Field()

    # The year in which this team played.
    year = scrapy.Field()

    # The display name for this team.
    name = scrapy.Field()

    # A relative link on Pro Football Reference to the franchise this team belongs to.
    franchise = scrapy.Field()

    regular_season_wins = scrapy.Field()
    regular_season_losses = scrapy.Field()
    regular_season_ties = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """Creates the teams table if one does not exist in the given
        database. Note that this does not update the fields if the table already
        exists, but the fields are outdated."""

        database.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                team TEXT PRIMARY KEY,
                year INTEGER,
                name TEXT,
                franchise TEXT,
                regular_season_wins INTEGER,
                regular_season_losses INTEGER,
                regular_season_ties INTEGER,
                FOREIGN KEY (franchise) REFERENCES franchises(franchise)
            )
        ''')

    def sql_insert(self, database):
        """Inserts this team into the teams table in the given database."""

        database.execute(
            '''
            INSERT OR REPLACE INTO teams (
                team,
                year,
                name,
                franchise,
                regular_season_wins,
                regular_season_losses,
                regular_season_ties
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        ''', (self['team'], self['year'], self['name'], self['franchise'],
              self['regular_season_wins'], self['regular_season_losses'],
              self['regular_season_ties']))

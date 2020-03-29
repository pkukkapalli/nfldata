"""Defines items related to NFL teams."""
import scrapy


class Team(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines information related to a specific NFL team in a specific year."""

    # A relative link on Pro Football Reference to this team.
    team = scrapy.Field()

    # The year in which this team played.
    year = scrapy.Field()

    # The display name for this team.
    name = scrapy.Field()

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
                regular_season_wins INTEGER,
                regular_season_losses INTEGER,
                regular_season_ties INTEGER
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
                regular_season_wins,
                regular_season_losses,
                regular_season_ties
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        ''', (self['team'], self['year'], self['name'],
              self['regular_season_wins'], self['regular_season_losses'],
              self['regular_season_ties']))

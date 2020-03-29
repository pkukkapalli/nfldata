"""Defines items related to NFL rosters."""
import scrapy


class RosterMember(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines a single player's membership on a particular team's roster."""

    player = scrapy.Field()
    team = scrapy.Field()
    approximate_value = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """
        Creates the roster_members table if one does not exist in the given database.
        Note that this does not update the fields if the table already exists,
        but the fields are outdated.
        """
        database.execute('''
            CREATE TABLE IF NOT EXISTS roster_members (
                player TEXT,
                team TEXT,
                approximate_value INTEGER,
                PRIMARY KEY (player, team),
                FOREIGN KEY (player) REFERENCES players(player),
                FOREIGN KEY (team) REFERENCES teams(team)
            )
        ''')

    def sql_insert(self, database):
        """
        Insert this roster member into the roster_members table in the given
        database.
        """
        database.execute(
            '''
            INSERT OR REPLACE INTO roster_members (
                player,
                team,
                approximate_value
            ) VALUES (
                ?,
                ?,
                ?
            )
        ''', (self['player'], self['team'], self['approximate_value']))

"""Defines items related to NFL rosters."""
import scrapy


class RosterMember(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines a single player's membership on a particular team's roster."""

    # A relative link on Pro Football Reference to the player.
    player = scrapy.Field()

    # A relative link on Pro Football Reference to the player's team.
    team = scrapy.Field()

    # The approximate value the player accumulated on this team.
    approximate_value = scrapy.Field()

    # Whether or not this player was selected to the Pro Bowl in this year.
    pro_bowl = scrapy.Field()

    # Whether or not this player was selected as a First Team All-Pro this year.
    first_team_all_pro = scrapy.Field()

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
                pro_bowl INTEGER,
                first_team_all_pro INTEGER,
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
                approximate_value,
                pro_bowl,
                first_team_all_pro
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?
            )
        ''', (self['player'], self['team'], self['approximate_value'],
              int(self['pro_bowl']), int(self['first_team_all_pro'])))

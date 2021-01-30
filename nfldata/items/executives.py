"""Defines items related to NFL executives."""

import scrapy


class Executive(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines information related to a specific NFL executive."""

    # A relative link on Pro Football Reference to the executive.
    executive = scrapy.Field()

    # The display name of the coach.
    name = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """Creates the executives table if one does not exist in the given
        database. Note that this does not update the fields if the table
        already exists, but the fields are outdated."""

        database.execute('''
            CREATE TABLE IF NOT EXISTS executives (
                executive TEXT PRIMARY KEY,
                name TEXT
            ) 
        ''')

    def sql_insert(self, database):
        """Inserts this executive into the executives table in the given
        database."""

        database.execute(
            '''
            INSERT OR REPLACE INTO executives (
                executive,
                name
            ) VALUES (
                ?,
                ?
            )
            ''', (self['executive'], self['name']))


class FrontOfficeMember(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines a single executive's membership on a front office."""

    # A relative link on Pro Football Reference to the executive.
    executive = scrapy.Field()

    # A relative link on Pro Football Reference to the executive's team.
    team = scrapy.Field()

    # The title that the executive held on the team.
    title = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """Creates the front_office_members table if one does not exist in the
        given database. Note that this does not update the fields if the table
        already exists, but the fields are outdated."""
        database.execute('''
            CREATE TABLE IF NOT EXISTS front_office_members (
                executive TEXT,
                team TEXT,
                title TEXT,
                PRIMARY KEY (executive, team),
                FOREIGN KEY (executive) REFERENCES executives(executive),
                FOREIGN KEY (team) REFERENCES teams(team)
            )
        ''')

    def sql_insert(self, database):
        """
        Insert this executive into the front_office_members table in the given
        database.
        """
        database.execute(
            '''
            INSERT OR REPLACE INTO front_office_members (
                executive,
                team,
                title
            ) VALUES (
                ?,
                ?,
                ?
            )
            ''', (self['executive'], self['team'], self['title']))

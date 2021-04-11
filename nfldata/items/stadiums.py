import scrapy


class Stadium(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines information related to a stadium that an NFL team plays at."""

    # A relative link on Pro Football Reference to this stadium.
    stadium = scrapy.Field()

    # The name of the stadium.
    name = scrapy.Field()

    # The city where this stadium is located.
    city = scrapy.Field()

    # The state where this stadium is located.
    state = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """Creates the stadiums table if one does not exist in the given
        database. Note that this does not update the fields if the table already
        exists, but the fields are outdated."""

        database.execute('''
            CREATE TABLE IF NOT EXISTS stadiums (
                stadium TEXT PRIMARY KEY,
                name TEXT,
                city TEXT,
                state TEXT
            )
        ''')

    def sql_insert(self, database):
        """Inserts this stadium into the stadiums table in the given database."""

        database.execute(
            '''
            INSERT OR REPLACE INTO stadiums (
                stadium,
                name,
                city,
                state
            ) VALUES (
                ?,
                ?,
                ?,
                ?
            )
            ''', (self['stadium'], self['name'], self['city'], self['state']))


class StadiumMember(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines a single team's membership at a particular stadium."""

    # A relative link on Pro Football Reference to the stadium.
    stadium = scrapy.Field()

    # A relative link on Pro Football Reference to the team playing at the stadium.
    team = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """Creates the stadium_members table if one does not exist in the given
        database. Note that this does not update the fields if the table
        already exists, but the fields are outdated."""

        database.execute('''
            CREATE TABLE IF NOT EXISTS stadium_members (
                stadium TEXT,
                team TEXT,
                PRIMARY KEY (stadium, team),
                FOREIGN KEY (stadium) REFERENCES stadiums(stadium)
                FOREIGN KEY (team) REFERENCES teams(team)
            )
        ''')

    def sql_insert(self, database):
        """Inserts this item into the stadium_members table in the given
        database."""

        database.execute(
            '''
            INSERT OR REPLACE INTO stadium_members (
                stadium,
                team
            ) VALUES (
                ?,
                ?
            )
        ''', (self['stadium'], self['team']))


class CityElevation(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines the elevation of a city that a team plays in."""

    # The city name.
    city = scrapy.Field()

    # The state where the city is located.
    state = scrapy.Field()

    # The elevation of the city in feet.
    elevation = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """Creates the city_elevations table if one does not exist in the given
        database. Note that this does not update the fields if the table
        already exists, but the fields are outdated."""

        database.execute('''
            CREATE TABLE IF NOT EXISTS city_elevations (
                city TEXT,
                state TEXT,
                elevation INTEGER,
                PRIMARY KEY (city, state)
            )
        ''')

    def sql_insert(self, database):
        """Inserts this item into the city_elevations table in the given
        database."""

        database.execute(
            '''
            INSERT OR REPLACE INTO city_elevations (
                city,
                state,
                elevation
            ) VALUES (
                ?,
                ?,
                ?
            )
        ''', (self['city'], self['state'], self['elevation']))

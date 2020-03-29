"""Defines items related to NFL coaches."""
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

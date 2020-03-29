"""Defines items related to schools that NFL players have attended."""
import scrapy


class School(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines a school that has produced at least one NFL player."""

    # A relative link on Pro Football Reference to the college.
    school = scrapy.Field()

    # The display name of the college.
    name = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """
        Creates the schools table if one does not exist in the given database.
        Note that this does not update the fields if the table already exists,
        but the fields are outdated.
        """

        database.execute('''
            create table if not exists schools (
                school text,
                name text,
                primary key (school)
            )
        ''')

    def sql_insert(self, database):
        """
        Insert this school into the schools table in the given database.
        """

        database.execute(
            '''
            insert or replace into schools (
                school,
                name
            ) values (
                ?,
                ?
            )
        ''', (self['school'], self['name']))

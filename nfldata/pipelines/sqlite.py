"""Defines pipelines to write items to a SQLite database."""
import sqlite3


class SqlitePipeline:
    """Writes the items in supported_items to a SQLite database."""

    def __init__(self):
        self.database = None

    def open_spider(self, spider):
        """Sets up the SQLite table to consume the items created by the
        spider."""

        self.database = sqlite3.connect('nfldata.sqlite')
        if 'create_table' in dir(spider):
            spider.create_table(self.database)

    def close_spider(self, spider):  # pylint: disable=unused-argument
        """Commits all of the changes made to the database."""

        self.database.commit()
        self.database.close()

    def process_item(self, item, spider):  # pylint: disable=unused-argument
        """Writes the given item to SQLite."""

        item.sql_insert(self.database)
        return item

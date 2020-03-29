"""Defines utilities for working with SQLite tables while performing
analyses."""


def print_schema(database, table_name):
    """Prints the schema of the table named table_name in the given database
    connection."""

    [schema] = database.execute(
        '''
        SELECT sql FROM sqlite_master
        WHERE type='table' AND name = ?
    ''', [table_name]).fetchone()
    print(schema)

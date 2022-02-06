import sqlite3

from nfldata.items.coaches import Coach


class CoachesDao:

    def __init__(self):
        self.database = sqlite3.connect('nfldata.sqlite')

    def lookup_coaches(self, query=None, limit=None):
        if query is not None and limit is not None:
            cursor = self.database.execute(
                '''
                SELECT coach, name FROM coaches
                WHERE lower(name) LIKE ?
                ORDER BY name ASC
                LIMIT ?
            ''', (f'%{query.lower()}%', limit))
        elif query is not None:
            cursor = self.database.execute(
                '''
                SELECT coach, name FROM coaches
                WHERE lower(name) LIKE ?
                ORDER BY name ASC
            ''', (f'%{query.lower()}%',))
        elif limit is not None:
            cursor = self.database.execute(
                '''
                SELECT coach, name FROM coaches
                ORDER BY name ASC
                LIMIT ?
            ''', (limit,))
        else:
            cursor = self.database.execute('''
                SELECT coach, name FROM coaches
                ORDER BY name ASC
            ''')
        coaches = cursor.fetchall()
        return [Coach(coach=coach, name=name) for coach, name in coaches]

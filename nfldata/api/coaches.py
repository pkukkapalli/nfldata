import sqlite3

from nfldata.items.coaches import Coach, CoachingPosition, CoachingStaffMember


class CoachesDao:

    def __init__(self):
        self.database = sqlite3.connect('nfldata.sqlite')

    def lookup_coaches(self, query=None, limit=None):
        '''
        Look up coaches using the given search query.
        
        It's a simple substring search, and you can use the limit parameter to limit how many results are returned.
        '''

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

    def lookup_coaching_tree(self, coach):
        pass

    def _lookup_direct_assistant_head_coaches(self, coach):
        cursor = self.database.execute(
            '''
            SELECT coach, team, position FROM coaching_staff_members
            WHERE position != 'HEAD_COACH'
            AND team in (
                SELECT team FROM coaching_staff_members
                WHERE coach = ? AND position = 'HEAD_COACH'
            )
        ''', (coach,))
        return [
            CoachingStaffMember(coach=coach,
                                team=team,
                                position=CoachingPosition[position])
            for coach, team, position in cursor.fetchall()
        ]

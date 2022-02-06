import sqlite3
import pandas as pd


def import_elevations_csv():
    database = sqlite3.connect('nfldata.sqlite')

    database.execute('DROP TABLE IF EXISTS city_elevations')
    database.execute('''
      CREATE TABLE city_elevations (
          city TEXT,
          state TEXT,
          elevation INTEGER,
          PRIMARY KEY (city, state)
      )
    ''')

    elevations = pd.read_csv('elevations.csv')
    for _, row in elevations.iterrows():
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
        ''', (row['city'], row['state'], row['elevation']))

    database.commit()
    database.close()


if __name__ == '__main__':
    import_elevations_csv()

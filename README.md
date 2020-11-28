# NFL Data

This is a project I put together to gather and analyze NFL data. Feel free to
use it for your own projects. I have not published any of the data itself,
because that would be violating the Terms of Service of the websites that host
this data.

## Prequisites

To run the code in this project, you need to have [Poetry][poetry], and
[Docker][docker] installed on your computer. 

Then, to install of the project dependencies, run:

```sh
poetry install
```

Then, activate the project's virtual environment by running:

```sh
poetry shell
```

## How to scrape data

I use the [Scrapy][scrapy] library to crawl web pages, and extract the data.
However, the websites may render the data using Javascript. Scrapy by default
does not run any scripts. To fix this, I also use [Splash][splash] plugin, which
proxies all of the requests through a Javascript rendering service.

You need the Splash service running before you start your spider. You can do
that by running:

```sh
./scripts/splash-server.sh
``` 

Then, run one of the spiders using:

```sh
scrapy crawl <spider>
```

Each of these spiders writes the data to a SQLite database saved as
`nfldata.sqlite`. The database is not included as part of this repo, because my
intention is not to mirror the data already available on Pro Football Reference.
Rather, it is to provide a way to get that data in a way that is easy to
analyze.

## How to analyze data

As mentioned above, all of the data is stored in an `nfldata.sqlite` file after
you run each spider. The schemas of the tables match one to one with the
`scrapy.Item` classes in `nfldata.items`. So, you can analyze them using the
[`sqlite3`][sqlite] library in Python or using the `sqlite3` command line tool.

There are also [Jupyter][jupyter] notebooks, under the `notebooks` directory
that I made containing some of my own work. Feel free to copy or use these to
get an idea of how to perform your own analyses.

## Improvements

- [] Remove `DraftPick.position`, `DraftPick.first_team_all_pros`, `DraftPick.pro_bowls`, and `DraftPick.career_approx_value` and join with the corresponding fields in `Player` instead.
- [] Rename all items to be suffixed with "Item" to avoid naming collisions with enums.
- [] Change all relative links to Pro Football Reference to absolute links.
- [] Add a year field to `PlayerPosition` as players may change positions throughout their career.

[poetry]:https://python-poetry.org/
[docker]:https://docs.docker.com/
[scrapy]:https://scrapy.org/
[splash]:https://github.com/scrapy-plugins/scrapy-splash
[sqlite]:https://docs.python.org/3/library/sqlite3.html
[jupyter]:https://jupyter.org/

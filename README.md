# NFL Data

This is a project I put together to gather and analyze NFL data. Feel free to
use it for your own projects. I have not published any of the data itself,
because that would be violating the Terms of Service of the websites that host
this data.

## Prequisites

To run the code in this project, you need to have [Python 3][python], and
[Docker][docker] installed on your computer. 

Then, to create a virtual environment, run:

```sh
scripts/create-env
```

Then, activate the project's virtual environment by running:

```sh
scripts/activate-env
```

## How to scrape data

I use the [Scrapy][scrapy] library to crawl web pages, and extract the data.
However, the websites may render the data using Javascript. Scrapy by default
does not run any scripts. To fix this, I also use [Splash][splash] plugin, which
proxies all of the requests through a Javascript rendering service.

You need the Splash service running before you start your spider. You can do
that by running:

```sh
scripts/splash-server
``` 

Then, run the spiders and build up the SQLite database use:

```sh
scripts/build-database
```

Each of the spiders writes the data to a SQLite database saved as
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
- [] Consolidate spiders, so that there are fewer passes over the same web pages.
- [] Parse player transactions for free agents and undrafted free agents.

## Dockerize everything

To containerize this entire process, and be able to use Kubernetes on this
project, we need to do the following things.

1. Make a proper web app. We need a proper web app in order to actually show off
   the usefulness of having different services and k8s.
2. Create a Dockerfile for each scraper.
3. Create an analysis API server.
4. Dockerfile for the analysis server.
5. Create a script to start all the Docker containers together, and have them communicate via localhost.
6. Transition to k8s.

For actually building the web app, let's start with the following analyses:

1. Injuries
  - Breakdowns offered by year, team, coach, position
  - Present in both graph and table format
2. Draft record for general managers
  - Breakdowns by general manager, team, year, draft round
  - Present in both graph and table formats

[python]:https://wiki.python.org/moin/BeginnersGuide/Download
[docker]:https://docs.docker.com/
[scrapy]:https://scrapy.org/
[splash]:https://github.com/scrapy-plugins/scrapy-splash
[sqlite]:https://docs.python.org/3/library/sqlite3.html
[jupyter]:https://jupyter.org/

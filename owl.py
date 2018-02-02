#!/Users/coljac/anaconda/envs/owl/bin/python

import sys
import os
import time
import coltools as ct
import urllib2
from bs4 import BeautifulSoup
from collections import defaultdict, OrderedDict
import webbrowser

URL = 'https://www.reddit.com/r/overwatched/comments/7pjn08/overwatch_league_season_1_stage_1/'
# URL = 'file://' + os.environ['HOME'] + '/dev/dev/owl/ow.html'

def main(argv):

    maps = OrderedDict()

    page = urllib2.urlopen(URL)
    soup = BeautifulSoup(page, 'lxml') # 'html.parser')

    last_day = soup.find("h4")
    next_els = last_day.next_elements
    for el in next_els:
        if el.name == "table":
            tab = el

    if tab is None:
        print("Can't find match table.")
        return

    body = tab.find("tbody")
    rows = body.children
    for row in rows:
        if row.name != "tr":
            continue
        parse_row(row, maps)

    urls = []
    for i, k in enumerate(maps.keys()):
        print("%d: %s"  % (i + 1, k))
    try:
        match_index = int(raw_input('Match: '))
        print
        for i, j in enumerate(maps[maps.keys()[match_index - 1]]):
            print("%d: %s" % (i + 1, j[0]))
            urls.append(j[1])
    except (ValueError, IndexError):
        sys.exit(0)

    try:
        map_index = int(raw_input('Map: '))
        url = urls[map_index - 1]
        webbrowser.open(url, new=2)
    except (ValueError, IndexError):
        sys.exit(0)


def parse_row(row, maps):
    cell_data = []
    cells = row.children
    for cell in cells:
        if cell.name == "td":
            cell_data.append(cell)
    try:
        map_, team_a, team_b, vod = cell_data[1].string, cell_data[2].strong.string, cell_data[4].strong.string, cell_data[5].a['href']
    except:
        return
    key = team_a + " @ " + team_b
    games = maps.get(key, list())
    games.append((map_, vod)) 
    maps[key] = games

if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/env python2

import os
from sys import maxint as MAXINT
import re
import datetime
import requests
import pandas as pd
import xml.etree.ElementTree as etree
# import numpy as np
# import matplotlib.pyplot as plt


avatars = [
    "Fedora", "Blue", "Red", "Green", "Yellow", "Lime", "Purple", "Cyan",
    "Helsing", "Warrior", "MeatBoy", "Yang", "Eskimo", "RoundB", "Ninja",
    "RoundG", "Cyclops", "Viking", "Robot", "Monk"
]
_index_url = 'http://steamcommunity.com/stats/239350/leaderboards/?xml=1'
_tree = None
_leaderboards = None
_all_time_url = 'http://steamcommunity.com/stats/239350/leaderboards/166704/?xml=1'
_all_time = None
_release = datetime.date(2013,8,8)

def read_details(details):
    avatar = int(details[0:2], 16)
    stage = int(details[8:10], 16)

    return avatar, stage


def pretty_stage(stage):
    if stage % 4 == 0:
        world = stage/4
        level = 4
    else:
        world = stage/4+1
        level = stage % 4
    return "%i-%i" % (world, level)


def coerce_date(date):
    if type(date) is datetime.date:
        return date
    elif type(date) is tuple:
        return datetime.date(date)
    elif type(date) is str:
        #MM/DD/YYYY format from XML titles in Steam Community API
        date = date.replace('/', '')
        month = int(date[0:2])
        day = int(date[2:4])
        year = int(date[4:8])
        return datetime.date(year, month, day)

def leaderboards(infile=None, persist=True, force=False):
    global _tree
    global _leaderboards
    global _index_url
    if _tree is None or force:
        if infile and not force:
            _tree = etree.parse(infile)
        else:
            infile = os.path.join('data', 'leaderboards.xml')
            try:
                r = requests.get(_index_url)
                _tree = etree.fromstring(r.content)
            except requests.exceptions.ConnectionError as e:
                print(e.message)
                print("Trying to read from local cache...")
                try:
                    _tree = etree.parse(infile)
                    persist = False
                except StandardError as er:
                    raise er
        if persist:
            with open(infile, 'w') as outfile:
                outfile.write(etree.tostring(_tree))
    _leaderboards = (Leaderboard(lb, force=force) for lb in _tree.iter('leaderboard'))
    return _leaderboards

#Look at this, look at leaderboards() above. Obviously can be abstracted!
def all_time(infile=None, persist=True, force=True):
    global _all_time
    if _all_time is None or force:
        if infile:
            tree = etree.parse(infile)
        else:
            infile = os.path.join('data', 'alltime.xml')
            r = requests.get(_all_time_url)
            tree = etree.fromstring(r.content)
        if persist:
            with open(infile, 'w') as outfile:
                outfile.write(etree.tostring(tree))

    return Leaderboard(tree, force=force)

def dailies(infile=None, persist=True, force=False, sort=True,
            since=None, until=None):
    '''
    Returns list of Daily Challenge Leaderboard objects,
    optionally limited/sorted by date.
    '''
    since = since or _release
    until = until or datetime.date.today()
    dailies = (lb for lb in leaderboards(infile, persist, force)
               if lb._date and lb._date >= since and lb._date <= until)
    if sort:
        return sorted(dailies)
    else:
        return list(dailies)


class Leaderboard(object):
    def __init__(self, lb=None, lbid=None, name=None, force=False,
                 date=None, infile=None, entries=0):
        if lb is not None:
            (self.url, self.lbid, self.name, _ign,
             self.entries, _ign, _ign) = (f.text for f in lb)
            self.entries = int(self.entries)
        else:
            self.lbid = str(lbid)
            self.name = str(name)
            self.entries = int(entries)
            self.url = ('http://steamcommunity.com/stats/23950/leaderboards/%s/?xml=1' % lbid)

        if infile is None:
            self._file = os.path.join('data', self.lbid + '.xml')
            self._persisted = False
        else:
            self._file = infile
            self._persisted = True
        self._tree = None
        self._rows = None
        self._data = None
        self._force = force

        if self.entries > 5000:
            self.next_url = self.url + "&start=5002"
        else:
            self.next_url = None

        if self.name.endswith('DAILY'):
            m, d, y = [int(n) for n in self.name.split(' ')[0].split('/')]
            self._date = datetime.date(y, m, d)
        else:
            self._date = None

    def __iter__(self):
        return self.rows

    def __lt__(self, other):
        return self._date < other._date

    def __enter__(self):
        #print "Working with %s - %s" % (self.lbid, self.date)
        return self

    def __exit__(self, e, err, trace):
        self._tree = None
        self._rows = None
        self._data = None

    @property
    def date(self):
        if self._date is None:
            return self._date
        return self._date.strftime('%m/%d/%Y')

    @property
    def rows(self):
        if self._rows is None:
            self._rows = (LbRow(e, date=self.date)
                          for e in self.tree.iter('entry'))
        return self._rows

    @property
    #TODO: Get 5001+ (self.next_url)
    def tree(self):
        if self._tree is None:
            if os.path.exists(self._file) and not self._force:
                self._tree = etree.parse(self._file)
            else:
                r = requests.get(self.url)
                self._tree = etree.fromstring(r.content)
        return self._tree

    @property
    def data(self):
        if self._data is None:
            self._data = pd.DataFrame({
                'Date': pd.Series(r.date for r in self.rows),
                'Rank': pd.Series(r.rank for r in self.rows),
                'Score': pd.Series(r.score for r in self.rows),
                'Avatar': pd.Series(r.avatar for r in self.rows),
                'Stage': pd.Series(r.stage for r in self.rows),
                'Steam_id': pd.Series(r.steamid for r in self.rows)
            })
        return self._data

    def persist(self, outpath=None, force=False):
        outpath = outpath or self._file
        if force or not os.path.exists(outpath):
            tree = self.tree
            with open(outpath, 'w') as outfile:
                outfile.write(etree.tostring(tree))
            self._persisted = True
        return self._persisted


class LbRow(object):
    def __init__(self, entry=None, date=None, **kwargs):
        for kw in kwargs:
            self[kw] = kwargs[kw]

        if entry is not None:
            (self.steamid, self.score, self.rank,
             self._, self.details) = (f.text for f in entry)
            self._avatar, self._stage = read_details(self.details)

        self._date = coerce_date(date)
        self.score = int(self.score)
        self.rank = int(self.rank)

    def __repr__(self):
        return "%s\t%s\t%s\t%s\t%s" % (self.rank, self.score, self.avatar,
                                       self.stage, self.steamid)
    def pretty_stage(self):
        stage = self._stage
        if stage % 4 == 0:
            world = stage/4
            level = 4
        else:
            world = stage/4+1
            level = stage % 4
        return "%i-%i" % (world, level)

    @property
    def stage(self):
        return pretty_stage(self._stage)

    @property
    def avatar(self):
        return avatars[self._avatar]

    @property
    def date(self):
        # return self._date.strftime('%Y-%m-%d') #do this instead?
        return self._date.strftime('%m/%d/%Y')

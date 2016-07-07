# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import requests
import sys
from bs4 import BeautifulSoup
from config import config


def _get_static_post_attr(page_content):
    """
    拿到<input type='hidden'>的post参数，并return
    """
    _dict = {}
    soup = BeautifulSoup(page_content, "html.parser")
    for each in soup.find_all('input'):
        if 'value' in each.attrs and 'name' in each.attrs:
            _dict[each['name']] = each['value']
    return _dict


if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit('Usage: python pocscan-cli.py [target-file]')

    targets = open(sys.argv[1]).readlines()
    targets = ''.join(targets).replace('\n', ',')
    print targets

    s = requests.session()

    """
    csrfmiddlewaretoken=BrHUOTCdf06oV6RJH7E7lWABvtnujQBa&username=root&password=Xyntax%40pocscan

    """
    gc = s.get(config.SERVER_URL).content
    d = _get_static_post_attr(gc)
    d['username'] = config.USR
    d['password'] = config.PWD
    print d

    pc = s.post(url=config.SERVER_URL + '/login/', data=d).content
    if '添加扫描' in pc:
        print '[*]Login success!'
    else:
        sys.exit('[!]Login failed!')

    """
    domains=http%3A%2F%2Flife.sinosig.com%2Chttp%3A%2F%2Fwww.sinosig.com&poc_name=&mode=0&csrfmiddlewaretoken
    =OjENiaw9GVlMapyRgYvTpzyTlKeiIZqY
    """
    d = _get_static_post_attr(gc)
    d['domains'] = targets.encode('utf8')
    d['poc_name'] = ''
    d['mode'] = '0'
    print d

    pc2 = s.post(url=config.SERVER_URL + '/scan/', data=d).content
    print pc2

    if '200' in pc2:
        print '[*]success!'
    elif '"status": 1' in pc2:
        print '[-]Already scanned before.'
    else:
        print '[!]U need to update this script!'

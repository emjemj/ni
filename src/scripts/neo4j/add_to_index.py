# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 15:39:31 2011

@author: lundberg
"""

# Add nodes which has the supplied property/key to the index with the name
# supplied.

import sys
import os
import argparse

## Need to change this path depending on where the Django project is
## located.
path = '/var/opt/norduni/src/niweb/'
#path = '/home/lundberg/norduni/src/niweb/'
##
##
sys.path.append(os.path.abspath(path))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import norduniclient as nc

# User friendly usage output
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--index', nargs='?', help='Index name.')
parser.add_argument('-p', '--property', nargs='?', help='Node property/key \
whose value you want to add for all nodes.')
parser.add_argument('-l', '--list', action='store_true',
    help='List available indexes.')
args = parser.parse_args()

if args.list:
    print 'Available indexes:'
    for name in nc.neo4jdb.index().nodeIndexNames():
        print name
    sys.exit(0)

if args.index and args.property:
    for node in nc.get_all_nodes(nc.neo4jdb):
        index = nc.get_node_index(nc.neo4jdb, args.index)
        added = nc.add_index_item(nc.neo4jdb, index, node, args.property)
        if added:
            print 'Node(%d), \'%s\' = \'%s\', added to index %s' % (node.id,
                                                                    args.property,
                                                                    node[args.property],
                                                                    args.index)
else:
    parser.print_help()


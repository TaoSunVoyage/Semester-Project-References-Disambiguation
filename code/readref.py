"""
Functions of reading and storing references into different structure.

Author: Tao Sun
"""

import mongoengine
from mongoengine import *
from mongoengine.queryset.visitor import Q
from dbmodels import *

import configparser

# Read the confidentials.
credentials = configparser.ConfigParser()
credentials.read('credentials.ini')

# Connect to the database.
connect(
    db = credentials.get('lb', 'db'),
    username = credentials.get('lb', 'username'),
    password = credentials.get('lb', 'password'),
    host = credentials.get('lb', 'host'), 
    port = int(credentials.get('lb', 'port')), 
);

def read_ref(ref):
    '''
    Read a ref from database and store useful information in dictionary locally.
    Useful information: 
    doc_id, ref_id, surface, order, title, author, year, page, abbre, abbre_pos.
    '''
    contents = ref.contents
    d = dict()
    doc = ref.get_containing_publication()
    d['doc_id'] = doc.id if doc else 0
    d['ref_id'] = ref.id
    d['surface'] = ref.reference_string
    d['order'] = ref.start_img_number * 1000 + ref.order_in_page
    # Choose what we want to use
    for i, c in contents.items():
        # title
        if c['tag'] == 'title':
            if 'title' in d:
                d['title'].append(c['surface'])
            else:
                d['title'] = [c['surface']]
        # author
        elif c['tag'] == 'author':
            if 'author' in d:
                d['author'].append(c['surface'])
            else:
                d['author'] = [c['surface']]
        # year
        elif c['tag'] == 'year':
            if 'year' in d:
                d['year'].append(c['surface'])
            else:
                d['year'] = [c['surface']]
        # page number
        elif c['tag'] == 'pagination':
            if 'page' in d:
                d['page'].append(c['surface'])
            else:
                d['page'] = [c['surface']]
        # abbreviation
        elif c['tag'] == 'abbreviation':
            if 'abbre' in d:
                d['abbre'].append(c['surface'])
                d['abbre_pos'].append(int(i))
            else:
                d['abbre'] = [c['surface']]
                d['abbre_pos'] = [int(i)]
    return d


def read_refs_publication(refs):
    '''
    Read all refs of one publication from database and store useful information in dictionary locally.
    Structure: 
    pub_id: {
            order:{
                rid,
                surface,
                title,
                author,
                year,
                abbre,
                abbre_pos
            }
            order:...
    }
    '''
    d = dict()
    for rid in refs:
        ref = Reference.objects(_id=rid).first()
        order = ref.start_img_number * 1000 + ref.order_in_page  # Define the order as page + order_in_page
        d[order] = dict()
        d[order]['rid'] = rid
        d[order]['surface'] = ref.reference_string
        contents = ref.contents
        # Choose what we want to use
        for i, c in contents.items():
            if c['tag'] == 'title':
                if 'title' in d[order]:
                    d[order]['title'].append(c['surface'])
                else:
                    d[order]['title'] = [c['surface']]
            elif c['tag'] == 'author':
                if 'author' in d[order]:
                    d[order]['author'].append(c['surface'])
                else:
                    d[order]['author'] = [c['surface']]
            elif c['tag'] == 'year':
                if 'year' in d[order]:
                    d[order]['year'].append(c['surface'])
                else:
                    d[order]['year'] = [c['surface']]
            elif c['tag'] == 'pagination':
                if 'page' in d[order]:
                    d[order]['page'].append(c['surface'])
                else:
                    d[order]['page'] = [c['surface']]
            elif c['tag'] == 'abbreviation':
                if 'abbre' in d[order]:
                    d[order]['abbre'].append(c['surface'])
                    d[order]['abbre_pos'].append(int(i))
                else:
                    d[order]['abbre'] = [c['surface']]
                    d[order]['abbre_pos'] = [int(i)]
    return d
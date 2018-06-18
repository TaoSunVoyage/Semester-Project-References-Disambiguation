"""
In this file, we get all of the "full" references which at least have fields "author", "title" and "year".

Author: Tao Sun
"""

import mongoengine
from mongoengine import *
from mongoengine.queryset.visitor import Q
from dbmodels import *
from hashfunction import *
from readref import *

import pandas as pd
from bson.objectid import ObjectId
import configparser
from multiprocessing import Pool
import pickle

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


# function for the reference resolutions
def retain_reference(journal_reference, min_size=3, required_fields=["author", "title"]):
    """
    Determine whether the input reference should be retained, and thus resolved, or skipped.
    This allows to skip erroneously extracted references, partial ones, etc.
    :param journal_reference: the input reference (extracted from journals in LinkedBooks)
    :type journal_reference: dict
    :param min_size: the minimum number of fields `journal_reference` must have
    :type min_size: int
    :param required_fields: the fields that must be contained in `journal_reference`
    :type required_fields: list of str
    :return: bool -- True if the reference should be retained, False otherwise
    """
    fields = [field["tag"] for field in journal_reference["contents"].values()]
    if(len(fields)>=min_size):
        if(len(set(fields).intersection(set(required_fields))) >= len(required_fields)):
            return True
        else:
            return False
    else:
        return False


print("get refs1")
refs1 = [r.id for r in Reference.objects()[:1000000] if retain_reference(r, 3, required_fields=["author", "title", "year"])]

print("transform to dataframe")
df_refs1 = pd.DataFrame(refs1)

print("store pickle")
df_refs1.to_pickle('./pickle/refs1.pickle')

print(len(df_refs1))
del df_refs1

print("get refs2")
refs2 = [r.id for r in Reference.objects()[1000000:2000000] if retain_reference(r, 3, required_fields=["author", "title", "year"])]

print("transform to dataframe")
df_refs2 = pd.DataFrame(refs2)

print("store pickle")
df_refs2.to_pickle('./pickle/refs2.pickle')

print(len(df_refs2))
del df_refs2

print("get refs3")
refs3 = [r.id for r in Reference.objects()[2000000:3000000] if retain_reference(r, 3, required_fields=["author", "title", "year"])]

print("transform to dataframe")
df_refs3 = pd.DataFrame(refs3)

print("store pickle")
df_refs3.to_pickle('./pickle/refs3.pickle')

print(len(df_refs3))
del df_refs3

print("get refs4")
refs4 = [r.id for r in Reference.objects()[3000000:4000000] if retain_reference(r, 3, required_fields=["author", "title", "year"])]

print("transform to dataframe")
df_refs4 = pd.DataFrame(refs4)

print("store pickle")
df_refs4.to_pickle('./pickle/refs4.pickle')

print(len(df_refs4))
del df_refs4

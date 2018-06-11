import mongoengine
from mongoengine import *
from mongoengine.queryset.visitor import Q
from dbmodels import *
from hashfunction import *
from readref import *

import pandas as pd
import configparser
from bson.objectid import ObjectId
from multiprocessing import Pool


list_split = []
for i in range(1, 5):
    df_temp = pd.read_pickle(f"./pickle/hash_split{i}.pickle")
    list_split.append(df_temp)


def find_match(ref):
    # get hashes of the ref
    rid = ref['ref_id']
    doc_id = ref['doc_id']
    hashes = ref['hashes']

    # get all matches
    list_result = []
    for i in range(4):
        cid = list_split[i].query('hashtag in @hashes and doc_id != @doc_id')['ref_id'].values
        list_result.extend(list(set(cid)))

    list_result = list(set(list_result))

    d = {
        'rid': rid,
        'cid': list_result,
        'num': len(list_result)
    }

    return d


pool = Pool(4)

df = pd.DataFrame()
for i in [1, 2, 3, 4]:
    print("Now we are at {}.".format(i))
    refs = pd.read_pickle(f'./pickle/hash_ref{i}.pickle').to_dict(orient='records')
    temp = pool.map(find_match, refs)
    df_temp = pd.DataFrame(temp)
    df_temp.to_pickle(f"./pickle/hash_match{i}.pickle")

pool.close()
pool.join()

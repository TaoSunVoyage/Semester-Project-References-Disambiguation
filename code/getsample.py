import mongoengine
from mongoengine import *
from mongoengine.queryset.visitor import Q
from dbmodels import *
from hashfunction import *
from readref import *

import pandas as pd
import configparser
from multiprocessing import Pool

# Read the confidential.
credentials = configparser.ConfigParser()
credentials.read('credentials.ini')

# Connect to the database.
connect(
    db=credentials.get('lb', 'db'),
    username=credentials.get('lb', 'username'),
    password=credentials.get('lb', 'password'),
    host=credentials.get('lb', 'host'),
    port=int(credentials.get('lb', 'port')),
);

# refs = Reference.objects.filter(Q(contents__1__tag='author', contents__2__tag='title') |
#                                 Q(contents__2__tag='author', contents__1__tag='title') |
#                                 Q(contents__2__tag='author', contents__3__tag='title') |
#                                 Q(contents__3__tag='author', contents__2__tag='title'))
#
# refNum = refs.count()
#
# # test
# for r in refs.limit(3):
#     try:
#         print(read_ref(r))
#         print("\n")
#     except:
#         print(read_ref(r))
#         print("\n")


def read_hash(ref_id):
    """Read reference and generate hashes."""
    ref = Reference.objects(id=ref_id).first()
    citation = read_ref(ref)
    d = {
        'doc_id': citation['doc_id'],
        'ref_id': citation['ref_id'],
        'surface': citation['surface'],
        'hashes': hashCombined(citation)
    }
    return d


pool = Pool(8)

# test
refs = pd.read_pickle('./pickle/refs1.pickle')[0].values
temp = pool.map(read_hash, refs[:3])
df = pd.DataFrame(temp)
print(df.head())

df = pd.DataFrame()
for i in [1, 2, 3, 4]:
    print("Now we are at {}.".format(i))
    refs = pd.read_pickle(f'./pickle/refs{i}.pickle')[0].values
    temp = pool.map(read_hash, refs)
    df_temp = pd.DataFrame(temp)
    df_temp.to_pickle(f"./pickle/hash_ref{i}.pickle")

pool.close()
pool.join()

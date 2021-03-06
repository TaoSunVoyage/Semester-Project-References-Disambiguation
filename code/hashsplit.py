"""
In this file, we change the way we store hashes of each reference.
From  ref -> [hash1, hash2, ..]  to  ref -> hash1, ref -> hash2, ...

Author: Tao Sun
"""

import pandas as pd

def splitHash(df):
    s = df.apply(lambda x: pd.Series(x['hashes']), axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'hashtag'
    return df.drop('hashes', axis=1).join(s)


df = pd.DataFrame()
df_hash = pd.DataFrame()
for i in range(1, 5):
    print(f"Read pickle {i}.")
    df_temp = pd.read_pickle(f'./pickle/hash_ref{i}.pickle')

    print(f"Split pickle {i}.")

    list_temp = []
    print(len(df_temp))
    for j in range(0, len(df_temp), 5000):
        print(str(i) + " : " + str(j))
        temp = splitHash(df_temp.iloc[j:j + 5000])
        list_temp.append(temp)
    df_hash_temp = pd.concat(list_temp, axis=0)

    print(f"Store split pickle {i}.")
    df_hash_temp.to_pickle(f'./pickle/hash_split{i}.pickle')

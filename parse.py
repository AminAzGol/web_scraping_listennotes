import pandas
import json
from time import time
from ast import literal_eval
import math
df = pandas.read_csv('listennotes_podcasts_1560845121.csv')
# python_dict = literal_eval(df.loc[:, 'extra_urls'].values[0])
# df.loc[df['First Season'] > 1990, 'First Season'] = 1
# df['extra_urls'] = literal_eval((df['extra_urls']))
# lis = df['extra_urls']
# for i in lis:
#     p = literal_eval(i)
    # df.loc[i, 'extra_urls'] = 0
    # df.set_value(i,'extra_urls',0)
for i, row in df.iterrows():
    for m in ['extra_urls', 'genres', 'tags']:
        ext = row[m]
        if type(ext) is not str and math.isnan(ext):
            new_ext = ''
        elif ext is 'nan' or ext is 'NAN':
            new_ext = ''
        else:
            new_ext = literal_eval(ext)
        df.set_value(i, m, new_ext)


file_name = "parsed_"+str(int(time()))
print('parsed')
# df.to_csv(file_name+".csv",  header=True)
with open(file_name+'.json', 'w', encoding='utf-8') as file:
    df.to_json(file, force_ascii=False)
print('saved')

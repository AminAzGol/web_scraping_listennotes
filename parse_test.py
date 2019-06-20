import pandas
df = pandas.read_json('parsed_1560880516.json')
a = df['extra_urls'].values[0:10]
b = [type(i) for i in a]
print(a)
print(b)
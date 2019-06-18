
# keywords = [
#     'politics',
#     'Government',
#     'News',
#     'Business',
#     'Organizations',
#     'Investing',
#     'TV',
#     'Film',
#     'National',
#     'Society',
#     'Culture',
#     'History',
#     'Parenting',
#     'Health',
#     'Family',
#     'Comedy',
#     'Arts',
#     'Literature',
#     'Science',
#     'Medicine',
#     'Philosophy',
#     'Sexuality',
#     'Fashion',
#     'Beauty'
#     ]

keywords = []
with open('keyword_bank_3.txt') as f:
    print('read keywords file')
    if f.readable():
        txt = f.readline()
        while txt:
            txt = txt.replace('\n', '')
            names = txt.split(' ')
            for n in names:
                keywords.append(n)
            txt = f.readline()
        # print('removing keywords duplicate')
        # for k in keywords:
        #     if k is '':
        #         keywords.remove(k)
        #         continue
        #     for k2 in keywords:
        #         if k.lower() == k2.lower():
        #             keywords.remove(k2)

        # with open('keyword_bank_2.txt') as f2:
        #     line = f2.readline()
        #     while(line):
        #         for k in keywords:
        #             if line == k:
        #                 keywords.remove(k)
        #         line = f2.readline()
        #
        # print('saving new keywords')
        # with open('keyword_bank_3.txt', 'w+') as f2:
        #     for k in keywords:
        #         f2.write(k)
        #         f2.write('\n')

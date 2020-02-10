from News import API
from News.Search import Search
import requests

class Stories(Search):
    #TODO use API SDK for real time monitoring and simple data indexing
    # inherit Search initializer and set endpoints
    def __init__(self):
        Search.__init__(self, endpoint=API.endpoints['stories'])

    # quick search method for finance iptc code 0400000: economy...
    def quick_search(self, days=14):
        params = {
            'published_at.start': 'NOW-' + str(days) + 'DAYS/DAY',
            'published_at.end': 'NOW',
            'language': ['en'],
            'source.locations.country': ['GB'],
            'categories.taxonomy': 'iptc-subjectcode',
            'categories.id[]': ['04000000'],
            'source.rankings.alexa.rank.min': 1,
            'source.rankings.alexa.rank.max': 100
        }
        try:
            url = self.encode_params(params)
            print(url)
            r = self.response(url)['stories']
            if len(r) > 0:
                return r
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)


if __name__ == '__main__':
    # test finance quick function
    finance = Stories()
    r = finance.quick_search()
    for story in r:
        print(story['title'])
        print(story['summary']['sentences'])
        print(story['sentiment']['title']['polarity'])
        print()
    #
    # print(type(r))
    # for x in r[:1]:
    #     print(type(x))
    #     for k in x['summary']:
    #         print(type(k), k)
    #
    #
    # print([r for r in r[0]])
    # print([s.keys() for s in r])
    # story_outer = ['title', 'summary', 'sentiment']
    # story_inner = ['sentences']
    # for m in story_outer:
    #     for k in r:
    #         print(type(k[m]))
    #         print(m, k[m])
    #         if type(k[m]) is dict:
    #             print([k[m][r] for r in k[m].keys()])

    #story_outer = ['title', 'body', 'summary', 'sentiment']

    #
    # def recursive_items(dictionary):
    #     for key, value in dictionary.items():
    #         if key in story_outer:
    #             if type(value) is dict:
    #                 yield (key, value)
    #                 yield from recursive_items(value)
    #             else:
    #                 yield (key, value)
    #
    #
    #
    # for x in r[:10]:
    #     for k,v in recursive_items(x):
    #         print(k)
    #         print(v)
    #     print('\n')













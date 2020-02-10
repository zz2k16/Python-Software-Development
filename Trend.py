"""
Class containing Trends methods
"""
from News import API
from News.Search import Search
import requests

class Trends(Search):
    def __init__(self):
        Search.__init__(self, endpoint=API.endpoints['trends'])

    # define quick search sentiment trends
    # must set one of boolean values
    def quick_search_sentiments(self, title, days=7, sent_title=False, sent_body=False):
        params = {
            'field': None,
            'published_at.start': 'NOW-' + str(days) + 'DAYS/DAY',
            'published_at.end': 'NOW', 'language': ['en'],
            'sort_by': 'recency'
        }
        # check for field type
        if sent_title:
            params['field'] = 'sentiment.title.polarity'

        if sent_body:
            params['field'] = 'sentiment.body.polarity'

        # set text parameters and try search
        if title is not '':
            params['title'] = title
            params['body'] = title
            params['text'] = title
            try:
                url = self.encode_params(params)
                print(url)
                r = self.response(url)['trends']
                if len(r) > 0:
                    return r
                else:
                    return 'No Trends Found. Please Try Again'
            except requests.exceptions.RequestException as e:
                print(e)
                exit(1)

    # advanced sentiments trends methods for specific date ranges
    # extends quick_search_sentiments with specific dates
    def advanced_search_sentiments(self, title, start_date, end_date, sent_title=False, sent_body=False):
        params = {
            'field': None,
            'published_at.start': self.date_formatter(start_date),
            'published_at.end': self.date_formatter(end_date),
            'language': ['en'], 'sort_by': 'recency',
        }
        # check for field type
        if sent_title:
            params['field'] = 'sentiment.title.polarity'

        if sent_body:
            params['field'] = 'sentiment.body.polarity'

        # set text parameters and try search
        if title is not '':
            params['title'] = title
            params['body'] = title
            params['text'] = title
            try:
                url = self.encode_params(params)
                print(url)
                r = self.response(url)['trends']
                if len(r) > 0:
                    return r
                else:
                    return 'No Trends Found. Please Try Again'
            except requests.exceptions.RequestException as e:
                print(e)
                exit(1)

    # word cloud for quick search. Allows for keywords only and extended functionality for sentiments
    def word_clouds(self, title, days=7, sent_title=False, sent_body=False, sentiment=None):
        params = {
            'field': 'keywords',
            'published_at.start': 'NOW-' + str(days) + 'DAYS/DAY',
            'published_at.end': 'NOW', 'language': ['en'],
            'sort_by': 'recency'
        }

        # test for title or body sentiment
        # test for sentiment polarity
        if sent_title:
            if sentiment is not None:
                params['sentiment.title.polarity'] = sentiment

        if sent_body:
            if sentiment is not None:
                params['sentiment.body.polarity'] = sentiment

        # set text parameters and try search
        if title is not '':
            params['title'] = title
            params['body'] = title
            params['text'] = title
            try:
                url = self.encode_params(params)
                print(url)
                r = self.response(url)['trends']
                if len(r) > 0:
                    return r
                else:
                    return 'No Trends Found. Please Try Again'
            except requests.exceptions.RequestException as e:
                print(e)
                exit(1)

    # word cloud for advanced search
    def word_cloud_advanced(self, title, start_date, end_date, sent_title=False, sent_body=False, sentiment=None):
        params = {
            'field': 'keywords',
            'published_at.start': self.date_formatter(start_date),
            'published_at.end': self.date_formatter(end_date),
            'language': ['en'],
            'sort_by': 'recency'
        }

        # test for title or body sentiment
        # test for sentiment polarity
        if sent_title:
            if sentiment is not None:
                params['sentiment.title.polarity'] = sentiment

        if sent_body:
            if sentiment is not None:
                params['sentiment.body.polarity'] = sentiment

        # set text parameters and try search
        if title is not '':
            params['title'] = title
            params['body'] = title
            params['text'] = title
            try:
                url = self.encode_params(params)
                print(url)
                r = self.response(url)['trends']
                if len(r) > 0:
                    return r
                else:
                    return 'No Trends Found. Please Try Again'
            except requests.exceptions.RequestException as e:
                print(e)
                exit(1)


if __name__ == '__main__':

    # test trends methods
    trends = Trends()
    # words = trends.word_clouds('Tesla')
    startdate = '18/06/2018'
    enddate = '22/06/2018'
    #words = trends.word_cloud_advanced('Tesla', startdate, enddate)
    #print(words)

    # q_title = trends.quick_search_sentiments('Tesla', sent_title=True)
    # q_content = trends.quick_search_sentiments('Tesla', sent_body=True)
    # print(q_title)
    # print(q_content)
    #
    from News import Graph
    g = Graph.Visualise()
    #g.word_clouds(words, graph_title='Overall Most Frequent Keywords', width=1400, color='#FFCD76')

    # g.overall_sentiment(q_title, graph_title='Overall Title Sentiment')
    # g.overall_sentiment(q_content, graph_title='Overall Content Sentiment', color='violet')









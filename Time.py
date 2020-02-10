from News import API
from News.Search import Search
import requests


class Series(Search):
    # inherit Search initializer and set Time Series endpoint
    def __init__(self):
        Search.__init__(self, endpoint=API.endpoints['time_series'])

    # quick search with extension for title and body sentiments
    def quick_search(self, title, days=7, sent_title=False, sent_body=False, sentiment=None):
        params = {
            'period': '+1DAY',
            'published_at.start': 'NOW-' + str(days) + 'DAYS/DAY',
            'published_at.end': 'NOW', 'language': ['en'],
            'sort_by': 'recency'
        }
        if title is not '':
            params['title'] = title
            params['body'] = title
            params['text'] = title
            # default return values are stories published over time per day

        # test for title or body sentiment
        # test for sentiment polarity
        if sent_title:
            if sentiment is not None:
                params['sentiment.title.polarity'] = sentiment

        if sent_body:
            if sentiment is not None:
                params['sentiment.body.polarity'] = sentiment

        try:
            url = self.encode_params(params)
            print(url)
            r = self.response(url)['time_series']
            if len(r) > 0:
                print(len(r))
                return r
            else:
                return 'No Trends Found. Please Try Again'
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)

    # aggregate function for quick search to return title [positive negative and neutral] time series data
    def quick_search_sentiments_title(self, title):
        positive = self.quick_search(title, sent_title=True, sentiment='positive')
        negative = self.quick_search(title, sent_title=True, sentiment='negative')
        neutral = self.quick_search(title, sent_title=True, sentiment='neutral')
        return positive, negative, neutral

    # aggregate function for quick search to return content [positive negative and neutral] time series data
    def quick_search_sentiments_content(self, title):
        positive = self.quick_search(title, sent_body=True, sentiment='positive')
        negative = self.quick_search(title, sent_body=True, sentiment='negative')
        neutral = self.quick_search(title, sent_body=True, sentiment='neutral')
        return positive, negative, neutral

    # TODO advanced method for specific date ranges ? split title and body
    def advanced_search(self, title, start_date, end_date, entity=False, sent_title=False, sent_body=False, sentiment=None):
        params = {
            'period': '+1DAY',
            'published_at.start': self.date_formatter(start_date),
            'published_at.end': self.date_formatter(end_date),
            'language': ['en'], 'sort_by': 'recency',
            'title': title, 'body': title, 'text': title
        }
        # check for entity requirement
        if entity:
            params.pop('title')
            params.pop('body')
            params.pop('text')
            params['entities.title.text'] = [title],
            params['entities.body.text'] = [title]

        # test for sentiment
        # test for title sentiment
        if sent_title:
            if sentiment is not None:
                params['sentiment.title.polarity'] = sentiment

        if sent_body:
            if sentiment is not None:
                params['sentiment.body.polarity'] = sentiment

        try:
            url = self.encode_params(params)
            print(url)
            r = self.response(url)['time_series']
            if len(r) > 0:
                print(len(r))
                return r
            else:
                return 'No Trends Found. Please Try Again'
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)

    # aggregate function for advanced search to return title sentiments
    def advanced_search_sentiments_title(self, title, start_date, end_date):
        positive = self.advanced_search(title=title, start_date=start_date, end_date=end_date, sent_title=True, sentiment='positive')
        negative = self.advanced_search(title=title, start_date=start_date, end_date=end_date, sent_title=True, sentiment='negative')
        neutral = self.advanced_search(title=title, start_date=start_date, end_date=end_date, sent_title=True, sentiment='neutral')
        return positive, negative, neutral

    # aggregate function for advanced search to return content sentiments
    def advanced_search_sentiments_content(self, title, start_date, end_date):
        positive = self.advanced_search(title=title, start_date=start_date, end_date=end_date, sent_body=True, sentiment='positive')
        negative = self.advanced_search(title=title, start_date=start_date, end_date=end_date, sent_body=True, sentiment='negative')
        neutral = self.advanced_search(title=title, start_date=start_date, end_date=end_date, sent_body=True, sentiment='neutral')
        return positive, negative, neutral


if __name__ == '__main__':
    t = Series()
    tesla_p, tesla_neg, tesla_neu = t.quick_search_sentiments_title('Tesla')
    print(tesla_p)
    print(tesla_neg)
    print(tesla_neu)
    # import pandas as pd
    #
    # pos_polar = pd.DataFrame.from_dict(tesla_p)
    # print(pos_polar)
    # neg_polar = pd.DataFrame.from_dict(tesla_neg)
    # print(neg_polar)
    # pos_polar['diff'] = pos_polar['count'] - neg_polar['count']
    # print(pos_polar)

    from News import Graph
    g = Graph.Visualise()
    g.time_series_polarity(tesla_p, tesla_neg, graph_title='Polarity Change Over Time', legend='Polarity Delta', color='crimson')

    #
    # startdate = '20/06/2018'
    # enddate = '21/06/2018'
    #
    # tesla_a_p = t.advanced_search(title='Tesla', start_date=startdate, end_date=enddate, sent_title=True, sentiment='positive')
    # tesla_ap, tesla_aneg, tesla_aneu = t.advanced_search_sentiments_title('Tesla', startdate, enddate)
    # print(tesla_ap)
    # print(tesla_aneg)
    # print(tesla_aneu)









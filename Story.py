from News import API
from News.Search import Search
import requests


class Story(Search):
    # inherit Search initializer and set Stories endpoint
    def __init__(self):
        Search.__init__(self, endpoint=API.endpoints['stories'])

    # quick search method to extract most recent stories
    def quick_search(self, title, days=7, pages=10):

        params = {'published_at.start': 'NOW-' + str(days) + 'DAYS/DAY',
                  'published_at.end': 'NOW', 'language': ['en'],
                  'per_page': pages
                  }

        if title is not '':
            params['title'] = title
            params['body'] = title
            params['text'] = title
            try:
                url = self.encode_params(params)
                print(url)
                r = self.response(url)['stories']
                if len(r) > 0:
                    return r
                else:
                    return 'No Stories Found. Please Try Again'
            except requests.exceptions.RequestException as e:
                print(e)
                exit(1)

    # advanced search method for specific date ranges
    # limit user values by expecting title and dates, optional? number of stories
    # if entity is True, replace title with entity parameters
    def advanced_search(self, title, start_date, end_date, pages=50, entity=False):
        params = {
            'published_at.start': self.date_formatter(start_date),
            'published_at.end': self.date_formatter(end_date),
            'language': ['en'], 'per_page': pages, 'sort_by': 'recency',
            'title': title, 'body': title, 'text': title
        }
        # check for entity requirement
        if entity:
            params.pop('title')
            params.pop('body')
            params.pop('text')
            params['entities.title.text'] = [title],
            params['entities.body.text'] = [title]

        try:
            url = self.encode_params(params)
            print(url)
            r = self.response(url)['stories']
            if len(r) > 0:
                # if stories found, return response and number of stories
                print(len(r))
                return r
            else:
                return 'No Stories Found. Please refine your search'
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)


if __name__ == '__main__':
    s = Story()
    start_date = '20/06/2018'
    end_date = '21/06/2018'
    # aapl = s.quick_search('Tesla')
    aapl = s.advanced_search(title='Tesla', start_date=start_date, end_date=end_date, entity=False)
    for story in aapl:
        print(story)

from flask import Flask, render_template, request
from News import Graph, Story, Time, Trend

application = Flask(__name__)

# default route for amazon flask app
# @application.route('/')
# def hello_world():
#      return 'Hello World! Application Test by Mo'


@application.route('/')
def index():
    return render_template('index.html')

@application.route('/help')
def help():
    return render_template('help.html')


@application.route('/results', methods=['POST'])
def results():
    # search term
    search_term = request.form['quicksearchtext_']

    # Stories
    story = Story.Story()
    stories = story.quick_search(search_term)

    # Trends
    trends = Trend.Trends()
    overall_title = trends.quick_search_sentiments(search_term, sent_title=True)
    overall_content = trends.quick_search_sentiments(search_term, sent_body=Trend)
    word_cloud = trends.word_clouds(search_term)

    # Time Series
    time = Time.Series()
    # Sentiments Title Time Series
    pos_titles, neg_titles, neut_titles = time.quick_search_sentiments_title(search_term)
    print(pos_titles)  # test response
    # Positive Content Time Series
    pos_content, neg_content, neut_content = time.quick_search_sentiments_content(search_term)

    # - Graphs
    g = Graph.Visualise()

    # overall Trends - Title, Content
    ov_title_script, ov_title_div = g.overall_sentiment(overall_title, graph_title='Overall Title Sentiment')
    ov_content_script, ov_content_div = g.overall_sentiment(overall_content,
                                                            graph_title='Overall Content Sentiment',
                                                            color='salmon')
    # word cloud
    word_cloud_script, word_cloud_div = g.word_clouds(word_cloud,
                                                      graph_title='Most Common Keywords',
                                                      width=1100, color='moccasin')
    # Time Series
    # Title Positive Sentiments
    pos_title_script, pos_title_div = g.time_series_sentiment(pos_titles,
                                                              graph_title='Positive Titles',
                                                              legend='Positive Title Articles per Day',
                                                              color='#ACE878')
    # Content Positive Sentiments
    pos_content_script, pos_content_div = g.time_series_sentiment(pos_content,
                                                                  graph_title='Positive Content',
                                                                  legend='Positive Content Articles per Day',
                                                                  color='#69E348')
    # Title Negative Sentiments
    neg_title_script, neg_title_div = g.time_series_sentiment(neg_titles, graph_title='Negative Titles',
                                                              legend='Negative Title Articles per Day',
                                                              color='#F05346')
    # Content Negative Sentiments
    neg_content_script, neg_content_div = g.time_series_sentiment(neg_content, graph_title='Negative Content',
                                                              legend='Negative Content Articles per Day',
                                                              color='crimson')
    # Neutral Title Sentiments
    neut_title_script, neut_title_div = g.time_series_sentiment(neut_titles, graph_title='Neutral Titles',
                                                                legend='Neutral Title Articles per Day',
                                                                color='#FFB876')

    # Neutral Content Sentiments
    neut_content_script, neut_content_div = g.time_series_sentiment(neut_content, graph_title='Neutral Content',
                                                                    legend='Neutral Content Articles per Day',
                                                                    color='#FFA376')

    # polarity change in Title Sentiments, Positive - Negative
    title_polarity_script, title_polarity_div = g.time_series_polarity(pos_titles, neg_titles,
                                                                       graph_title='Polarity Change in Title Sentiment',
                                                                       legend='Polarity')

    # polarity change in Content Sentiments, Positive - Negative
    content_polarity_script, content_polarity_div = g.time_series_polarity(pos_content, neg_content,
                                                                           graph_title='Polarity Change in Content Sentiment',
                                                                           legend='Polarity')

    return render_template('results.html', search_term=search_term,
                           ov_title_script=ov_title_script, ov_title_div=ov_title_div,
                           ov_content_script=ov_content_script, ov_content_div=ov_content_div,
                           word_cloud_script=word_cloud_script, word_cloud_div=word_cloud_div,
                           time_pos_title_script=pos_title_script, time_pos_title_div=pos_title_div,
                           time_pos_content_script=pos_content_script, time_pos_content_div=pos_content_div,
                           time_neg_title_script=neg_title_script, time_neg_title_div=neg_title_div,
                           time_neg_content_script=neg_content_script, time_neg_content_div=neg_content_div,
                           time_neut_title_script=neut_title_script, time_neut_title_div=neut_title_div,
                           time_neut_content_script=neut_content_script, time_neut_content_div=neut_content_div,
                           time_polar_title_script=title_polarity_script, time_polar_title_div=title_polarity_div,
                           time_polar_content_script=content_polarity_script,
                           time_polar_content_div=content_polarity_div,
                           Stories = True, stories = stories
                           )


@application.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        story = Story.Story()
        # retrieve form variables
        # search term
        search_term = request.form['quicksearchtext_']
        # dates
        datefrom = request.form['start_date_']
        enddate = request.form['end_date_']

        # Stories
        stories = story.advanced_search(search_term, start_date=datefrom, end_date=enddate)

        # Trends
        trends = Trend.Trends()
        overall_title = trends.advanced_search_sentiments(search_term, datefrom, enddate, sent_title=True)
        overall_content = trends.advanced_search_sentiments(search_term, datefrom, enddate, sent_body=True)
        word_cloud = trends.word_cloud_advanced(search_term, datefrom, enddate)

        # Time Series
        time = Time.Series()
        # Sentiments Title Time Series
        pos_titles, neg_titles, neut_titles = time.advanced_search_sentiments_title(search_term, datefrom, enddate)
        print(pos_titles)  # test response
        # Positive Content Time Series
        pos_content, neg_content, neut_content = time.advanced_search_sentiments_content(search_term, datefrom, enddate)

        # - Graphs
        g = Graph.Visualise()

        # overall Trends - Title, Content
        ov_title_script, ov_title_div = g.overall_sentiment(overall_title, graph_title='Overall Title Sentiment')
        ov_content_script, ov_content_div = g.overall_sentiment(overall_content,
                                                                graph_title='Overall Content Sentiment',
                                                                color='salmon')
        # word cloud
        word_cloud_script, word_cloud_div = g.word_clouds(word_cloud,
                                                          graph_title='Most Common Keywords',
                                                          width=1100, color='moccasin')
        # Time Series
        # Title Positive Sentiments
        pos_title_script, pos_title_div = g.time_series_sentiment(pos_titles,
                                                                  graph_title='Positive Titles',
                                                                  legend='Positive Title Articles per Day',
                                                                  color='#ACE878')
        # Content Positive Sentiments
        pos_content_script, pos_content_div = g.time_series_sentiment(pos_content,
                                                                      graph_title='Positive Content',
                                                                      legend='Positive Content Articles per Day',
                                                                      color='#69E348')
        # Title Negative Sentiments
        neg_title_script, neg_title_div = g.time_series_sentiment(neg_titles, graph_title='Negative Titles',
                                                                  legend='Negative Title Articles per Day',
                                                                  color='#F05346')
        # Content Negative Sentiments
        neg_content_script, neg_content_div = g.time_series_sentiment(neg_content, graph_title='Negative Content',
                                                                      legend='Negative Content Articles per Day',
                                                                      color='crimson')
        # Neutral Title Sentiments
        neut_title_script, neut_title_div = g.time_series_sentiment(neut_titles, graph_title='Neutral Titles',
                                                                    legend='Neutral Title Articles per Day',
                                                                    color='#FFB876')

        # Neutral Content Sentiments
        neut_content_script, neut_content_div = g.time_series_sentiment(neut_content, graph_title='Neutral Content',
                                                                        legend='Neutral Content Articles per Day',
                                                                        color='#FFA376')

        # polarity change in Title Sentiments, Positive - Negative
        title_polarity_script, title_polarity_div = g.time_series_polarity(pos_titles, neg_titles,
                                                                           graph_title='Polarity Change in Title Sentiment',
                                                                           legend='Change in Positive / Negative Sentiment')

        # polarity change in Content Sentiments, Positive - Negative
        content_polarity_script, content_polarity_div = g.time_series_polarity(pos_content, neg_content,
                                                                               graph_title='Polarity Change in Content Sentiment',
                                                                               legend='Change in Positive / Negative Sentiment')

        # polarity change in Title Sentiments, Positive - Negative
        title_polarity_script, title_polarity_div = g.time_series_polarity(pos_titles, neg_titles, graph_title='Polarity Change in Title Sentiment', legend='Polarity')

        # polarity change in Content Sentiments, Positive - Negative
        content_polarity_script, content_polarity_div = g.time_series_polarity(pos_content, neg_content, graph_title='Polarity Change in Content Sentiment', legend='Polarity')


        return render_template('results.html', search_term=search_term,
                               ov_title_script=ov_title_script, ov_title_div=ov_title_div,
                               ov_content_script=ov_content_script, ov_content_div=ov_content_div,
                               word_cloud_script=word_cloud_script, word_cloud_div=word_cloud_div,
                               time_pos_title_script=pos_title_script, time_pos_title_div=pos_title_div,
                               time_pos_content_script=pos_content_script, time_pos_content_div=pos_content_div,
                               time_neg_title_script=neg_title_script, time_neg_title_div=neg_title_div,
                               time_neg_content_script=neg_content_script, time_neg_content_div=neg_content_div,
                               time_neut_title_script=neut_title_script, time_neut_title_div=neut_title_div,
                               time_neut_content_script=neut_content_script, time_neut_content_div=neut_content_div,
                               time_polar_title_script = title_polarity_script, time_polar_title_div = title_polarity_div,
                               time_polar_content_script = content_polarity_script, time_polar_content_div = content_polarity_div,
                               Stories=True, stories=stories
                               )

@application.route('/trends', methods=['Get', 'POST'])
def trends():
    if request.method == 'GET':
        return render_template('trends.html')
    else:
        # retrieve form variables
        # search term
        search_term = request.form['quicksearchtext_']
        # dates
        datefrom = request.form['start_date_']
        enddate = request.form['end_date_']
        print(datefrom)
        print(enddate)

        # Trends
        trends = Trend.Trends()
        overall_title = trends.advanced_search_sentiments(search_term, datefrom, enddate, sent_title=True)
        overall_content = trends.advanced_search_sentiments(search_term, datefrom, enddate, sent_body=True)
        word_cloud = trends.word_cloud_advanced(search_term, datefrom, enddate)

        # Time Series
        time = Time.Series()
        # Sentiments Title Time Series
        pos_titles, neg_titles, neut_titles = time.advanced_search_sentiments_title(search_term, datefrom, enddate)
        print(pos_titles)  # test response
        # Positive Content Time Series
        pos_content, neg_content, neut_content = time.advanced_search_sentiments_content(search_term, datefrom, enddate)

        # - Graphs
        g = Graph.Visualise()

        # overall Trends - Title, Content
        ov_title_script, ov_title_div = g.overall_sentiment(overall_title, graph_title='Overall Title Sentiment')
        ov_content_script, ov_content_div = g.overall_sentiment(overall_content,
                                                                graph_title='Overall Content Sentiment',
                                                                color='salmon')
        # word cloud
        word_cloud_script, word_cloud_div = g.word_clouds(word_cloud,
                                                          graph_title='Most Common Keywords',
                                                          width=1100, color='moccasin')
        # Time Series
        # Title Positive Sentiments
        pos_title_script, pos_title_div = g.time_series_sentiment(pos_titles,
                                                                  graph_title='Positive Titles',
                                                                  legend='Positive Title Articles per Day',
                                                                  color='#ACE878')
        # Content Positive Sentiments
        pos_content_script, pos_content_div = g.time_series_sentiment(pos_content,
                                                                      graph_title='Positive Content',
                                                                      legend='Positive Content Articles per Day',
                                                                      color='#69E348')
        # Title Negative Sentiments
        neg_title_script, neg_title_div = g.time_series_sentiment(neg_titles, graph_title='Negative Titles',
                                                                  legend='Negative Title Articles per Day',
                                                                  color='#F05346')
        # Content Negative Sentiments
        neg_content_script, neg_content_div = g.time_series_sentiment(neg_content, graph_title='Negative Content',
                                                                      legend='Negative Content Articles per Day',
                                                                      color='crimson')
        # Neutral Title Sentiments
        neut_title_script, neut_title_div = g.time_series_sentiment(neut_titles, graph_title='Neutral Titles',
                                                                    legend='Neutral Title Articles per Day',
                                                                    color='#FFB876')

        # Neutral Content Sentiments
        neut_content_script, neut_content_div = g.time_series_sentiment(neut_content, graph_title='Neutral Content',
                                                                        legend='Neutral Content Articles per Day',
                                                                        color='#FFA376')
        # polarity change in Title Sentiments, Positive - Negative
        title_polarity_script, title_polarity_div = g.time_series_polarity(pos_titles, neg_titles,
                                                                           graph_title='Polarity Change in Title Sentiment',
                                                                           legend='Polarity')

        # polarity change in Content Sentiments, Positive - Negative
        content_polarity_script, content_polarity_div = g.time_series_polarity(pos_content, neg_content,
                                                                               graph_title='Polarity Change in Content Sentiment',
                                                                               legend='Polarity')

        return render_template('results.html', search_term=search_term,
                               ov_title_script=ov_title_script, ov_title_div=ov_title_div,
                               ov_content_script=ov_content_script, ov_content_div=ov_content_div,
                               word_cloud_script=word_cloud_script, word_cloud_div=word_cloud_div,
                               time_pos_title_script=pos_title_script, time_pos_title_div=pos_title_div,
                               time_pos_content_script=pos_content_script, time_pos_content_div=pos_content_div,
                               time_neg_title_script=neg_title_script, time_neg_title_div=neg_title_div,
                               time_neg_content_script=neg_content_script, time_neg_content_div=neg_content_div,
                               time_neut_title_script=neut_title_script, time_neut_title_div=neut_title_div,
                               time_neut_content_script=neut_content_script, time_neut_content_div=neut_content_div,
                               time_polar_title_script=title_polarity_script, time_polar_title_div=title_polarity_div,
                               time_polar_content_script=content_polarity_script,
                               time_polar_content_div=content_polarity_div,
                               Stories=False
                               )

if __name__ == '__main__':
    application.run()

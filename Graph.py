"""
Class containing data visualisation methods for Trends and Time Series responses
"""
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components


class Visualise:
    # Time Series Visualisation
    def time_series_sentiment(self, data, graph_title, legend, color='lightsalmon', width=530, height=500):
        colour = color
        data = data  # data must be filtered by 'trend' key as passed as data param
        # transform json response to pandas data frame
        df = pd.DataFrame.from_dict(data, orient='columns')
        df['published'] = df['published_at'].str[:-10]  # strip out ISO Date format for graph readability
        print(df)
        # transform data into data source and define x, y attributes
        src = ColumnDataSource(df)
        dates = df['published'].values
        sentiment_count = df['count'].values

        # build graph
        p = figure(x_range=dates, y_range=(0, (max(sentiment_count)+1)),
                   plot_width=width, plot_height=height, title=graph_title, tools='hover, save, pan, wheel_zoom, reset',
                   toolbar_location='below'
                   )
        p.vbar(x='published', top='count', width=0.8, color=colour, legend=legend, source=src)
        p.select_one(HoverTool).tooltips = [('date', '@published'),('count', '@count')]
        p.legend.orientation = 'horizontal'
        p.legend.location = 'top_center'
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.xaxis.major_label_orientation = np.pi / 3

        # return graph to html
        script, div = components(p)
        #show(p)
        return script, div

    def time_series_polarity(self, pos_data, neg_data, graph_title, legend, color='crimson', width=530, height=500):
        colour = color
        posdata = pos_data  # set positive and negative time series objects
        negdata = neg_data
        pos_df = pd.DataFrame.from_dict(posdata)
        neg_df = pd.DataFrame.from_dict(negdata)
        # count difference and attach new column to positive df
        pos_df['diff'] = pos_df['count'] - neg_df['count']
        # transform json response to pandas data frame
        pos_df['published'] = pos_df['published_at'].str[:-10]  # strip out ISO Date format for graph readability
        print(pos_df)
        # transform data into data source and define x, y attributes
        src = ColumnDataSource(pos_df)
        dates = pos_df['published'].values
        sentiment_count = pos_df['diff'].values

        # build graph
        p = figure(x_range=dates, y_range=(min(sentiment_count), (max(sentiment_count))),
                   plot_width=width, plot_height=height, title=graph_title, tools='hover, save, pan, wheel_zoom, reset',
                   toolbar_location='below'
                   )
        p.line(x='published', y='diff', line_width=4,  color=colour, legend=legend, source=src)
        p.select_one(HoverTool).tooltips = [('date', '@published'),('count', '@diff')]
        p.legend.orientation = 'horizontal'
        p.legend.location = 'top_center'
        p.grid.grid_line_color = 'moccasin'
        p.axis.axis_line_color = None
        p.xaxis.major_label_orientation = np.pi / 3

        # return graph to html
        script, div = components(p)
        # show(p)
        return script, div

    # TODO define Trends Word Cloud
    def word_clouds(self, data, graph_title, color='paleturquoise', width=800, height=650):
        colour = color
        data = data
        # data frame takes in 'trends' data from response
        df = pd.DataFrame.from_dict(data, orient='columns')
        print(df)
        # transform data and define x, y attributes
        src = ColumnDataSource(df)
        words = df['value'].values
        counts = df['count'].values

        # build graph
        p = figure(title='Most Frequent Keywords', tools='hover, save, pan, wheel_zoom, reset', x_range=words, y_range=(0, counts.max()))
        p.plot_width = width
        p.plot_height = height
        p.legend.orientation = 'horizontal'
        p.legend.location = 'top_center'
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.xaxis.major_label_text_font_size = '10pt'
        p.xaxis.major_label_orientation = np.pi / 3

        p.vbar(x='value', top='count', width=0.7, source=src, color=colour, legend=graph_title)
        p.select_one(HoverTool).tooltips = [('Word', '@value'), ('count', '@count')]

        # return graph to html
        script, div = components(p)
        #show(p)
        return script, div

    # TODO define Trends overall sentiment vbar
    def overall_sentiment(self, data, graph_title, color='lightsalmon', width=530, height=500):
        colour = color
        data = data  # data must be filtered by 'trend' key as passed as data param
        # transform json response to pandas data frame
        df = pd.DataFrame.from_dict(data, orient='columns')
        print(df)
        # transform data into data source and define x, y attributes
        src = ColumnDataSource(df)
        sentiments = df['value'].values
        sentiment_count = df['count'].values

        # build graph
        p = figure(x_range=sorted(sentiments, reverse=True), y_range=(0, (sum(sentiment_count))),
                   plot_width=width, plot_height=height, title=graph_title, tools='hover, save, pan, wheel_zoom, reset',
                   toolbar_location='below'
                   )
        p.vbar(x='value', top='count', width=0.8, color=colour, legend='Sentiments', source=src)
        p.select_one(HoverTool).tooltips = [('value', '@value'), ('count', '@count')]
        p.legend.orientation = 'horizontal'
        p.legend.location = 'top_center'

        # return graph to html
        script, div = components(p)
        # show(p)
        return script, div


if __name__ == '__main__':

    # import story and time classes
    from News import Time, Trend
    # init graph class
    g = Visualise()

    time = Time.Series()
    trends = Trend.Trends()
    startdate = '10/06/2018'
    enddate = '21/06/2018'

    # - Visualise Trends Data
    tesla_title_trends = trends.advanced_search_sentiments('Tesla', startdate, enddate, sent_title=True)
    tesla_content_trends = trends.advanced_search_sentiments('Tesla', startdate, enddate, sent_body=True)

    # g.overall_sentiment(tesla_title_trends, graph_title='Overall Title Sentiment Trends for Tesla')
    # g.overall_sentiment(tesla_content_trends, graph_title='Overall Content Sentiment Trends for Tesla', color='lightcoral')


    # - Visualise Time Series Data

    # simple content time series
    tes_p, tes_neg, tes_neu = time.quick_search_sentiments_content('Tesla')
    g.time_series_sentiment(tes_p, graph_title='Positive Content Articles', legend='Positive Articles Per Day', color='palegreen', width=1000)


    # advanced content time series
    # tesla_con_pos, tesla_con_neg, tesla_con_neu = time.advanced_search_sentiments_content('Tesla', startdate, enddate)
    # tes_pos = g.time_series_sentiment(tesla_con_pos, graph_title='Positive Content Time Series', legend='Positive Articles Per Day', color='palegreen')

    # tesla_ap, tesla_aneg, tesla_aneu = time.advanced_search_sentiments_title('Tesla', startdate, enddate)
    # qteslap, qteslaneg, qteslaneut = time.quick_search_sentiments_title('Tesla')
    # print(tesla_ap)
    # print(tesla_aneg)
    # print(tesla_aneu)
    #
    # #neg_bar = g.time_series_sentiment(tesla_aneu, graph_title='Title Negative Time Series', legend='Title Negative Articles per Day', color='crimson')
    # pos_bar = g.time_series_sentiment(tesla_ap, graph_title='Title Positive Time Series', legend='Positive Titled Articles per Day', color='palegreen', width=1000, height=700)
    #neu_bar = g.time_series_sentiment(tesla_aneu, graph_title='Title Neutral Time Series', legend='Title Neutral Articles per Day', color='moccasin')










import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

netflix_df = pd.read_csv('netflix_titles.csv')
netflix_df['date_added'] = pd.to_datetime(netflix_df['date_added'])
netflix_df['date_added_year'] = netflix_df.date_added.dt.year


def added_to_netflix_per_year_line():
    added_per_year = netflix_df.groupby(['date_added_year']).size().reset_index(name='counts')
    added_per_year['date_added_year'] = [round(x) for x in added_per_year['date_added_year']]
    fig = px.line(
        data_frame=added_per_year,
        x='date_added_year',
        y='counts',
        labels={
            "date_added_year": "Year added to Netflix",
            "counts": "Content count",
        }
    )

    fig.show()


def released_per_year_line():
    released_per_year = netflix_df.groupby(['release_year']).size().reset_index(name='counts')
    fig = px.line(
        data_frame=released_per_year,
        x='release_year',
        y='counts',
        labels={
            "release_year": "Release year",
            "counts": "Content count",
        },
    )

    fig.show()


def genres_per_year_bar():
    # create column for each genre
    genres = netflix_df['listed_in'].str.get_dummies(sep=', ')
    df = pd.concat([netflix_df[['date_added_year']], genres], axis=1)

    # count the number of movies/tv shows for each genre
    grouped_by_year = df.pivot_table(index=['date_added_year'], values=genres.columns.tolist(), aggfunc=np.sum)
    grouped_by_year.index = [round(x) for x in grouped_by_year.index.tolist()]

    # combine genre counts into one column
    grouped_by_year['counts'] = grouped_by_year.values.tolist()
    grouped_by_year = grouped_by_year[['counts']]

    bars = []
    for i, row in grouped_by_year.iterrows():
        bars.append(
            go.Bar(
                name=i,
                x=genres.columns.tolist(),
                y=row.counts)
        )

    fig = go.Figure(data=bars)
    fig.update_layout(
        title="Content per genre",
        xaxis_title="Genres",
        yaxis_title="Content count",
        legend_title="Year added to Netflix",
        barmode='stack',
        xaxis={'categoryorder': 'total descending'}
    )
    fig.show()


def movie_duration_bar():
    # select the movies
    movies = netflix_df[netflix_df['type'] == 'Movie']
    # extract minutes from string
    movies['duration'] = movies['duration'].str.extract('(\d+)').astype(int)
    # create duration bins with a 30 minute interval
    bins = [x * 30 for x in range(0, 12)]
    movies['duration_bin'] = pd.cut(movies['duration'], bins=bins)
    # count movies per bin
    movies = movies.groupby('duration_bin').size().reset_index(name='counts')
    movies['duration_bin'] = movies['duration_bin'].astype('str')

    fig = px.bar(
        data_frame=movies,
        x='duration_bin',
        y='counts'
    )
    fig.update_layout(
        title="Movie Duration",
        xaxis_title="Duration in minutes",
        yaxis_title="Number of movies",
    )
    fig.show()


movie_duration_bar()
genres_per_year_bar()
added_to_netflix_per_year_line()
released_per_year_line()

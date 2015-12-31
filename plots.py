import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns


def plot_candidate_percentages(df, candidates):
    outlets = np.array(['nyt', 'npr', 'foxnews', 'guardian', 'wsj'])
    ind = np.arange(5)
    c = ['#4e73ad', '#c12e1d', '#ebc844', '#a2b86b']
    width = 0.25
    for i, candidate in enumerate(candidates):
        percentages = np.array([df.loc[df['source'] == outlet, 'article_text'].str.contains(candidate.lower()).sum() / float(len(df[df['source'] == outlet])) for outlet in outlets])
        # idx = np.argsort(percentages)[::-1]
        # outlets, percentages = outlets[idx], percentages[idx]
        plt.bar(ind + i*width, percentages, width, color=c[i], label=candidate)
    plt.title('Coverage By News Outlet')
    plt.xticks(ind + (width/2.) * len(candidates), outlets)
    plt.ylabel('Percentage of Articles Mentioning Candidate')
    plt.xlabel('News Outlet')
    plt.legend(loc='best')
    plt.show()


def article_count_by_time(df, searchterm=None, topic=None, source=False, freq='W', normalize=False, show=True, marker='o', year=False, fig=None, label=None):
    outlets = [('nyt', 'New York Times'), ('foxnews', 'Fox News'), ('npr', 'NPR'), ('guardian', 'The Guardian'), ('wsj', 'Wall Street Journal')]
    outlet_sizes = [len(df.loc[df['source'] == outlet]) for outlet in zip(*outlets)[0]]
    if topic:
        labels, label = topic
        df = df.loc[labels == label]
    if not searchterm and not source:
        ts = pd.Series([1], index=df['date_published']).resample(freq, how='sum')
        if not fig:
            fig = plt.figure(figsize=(12, 8))
        plt.subplots_adjust(left=0.08, bottom=0.12, right=0.95, top=0.92)
        ts.plot(marker=marker, label=label)
        plt.xlabel('Date Published')
        plt.ylabel('Article Count (freq={})'.format(freq))
    elif not searchterm and source:
        timeseries = [pd.Series([1], index=df.loc[df['source'] == outlet, 'date_published']).resample(freq, how='sum') for outlet in zip(*outlets)[0]]
        if normalize:
            timeseries = [ts / outlet_size for ts, outlet_size in zip(timeseries, outlet_sizes)]
        if not fig:
            fig = plt.figure(figsize=(12, 8))
        plt.subplots_adjust(left=0.08, bottom=0.12, right=0.95, top=0.92)
        for idx, ts in enumerate(timeseries):
            if len(ts):
                ts.plot(marker=marker, label=outlets[idx][1])
        plt.xlabel('Date Published', fontsize=12)
        if normalize:
            plt.ylabel('Article Frequency (freq = {})'.format(freq), fontsize=12)
        else:
            plt.ylabel('Article Count (Freq = {})'.format(freq), fontsize=12)
        plt.legend(loc='best')
    elif searchterm and not source:
        ts = pd.Series(df['lemmatized_text'].str.contains(searchterm).astype('int').values, index=df['date_published']).resample(freq, how='sum')
        if not fig:
            fig = plt.figure(figsize=(12, 8))
        plt.subplots_adjust(left=0.08, bottom=0.12, right=0.95, top=0.92)
        ts.plot(marker=marker)
        plt.xlabel('Date Published', fontsize=12)
        plt.ylabel('Article Count (freq={})'.format(freq), fontsize=12)
        plt.title("Articles Containing '{}'".format(searchterm), fontsize=14)
    elif searchterm and source:
        timeseries = [pd.Series(df.loc[df['source'] == outlet, 'lemmatized_text'].str.contains(searchterm).astype('int').values, index=df.loc[df['source'] == outlet, 'date_published']).resample(freq, how='sum') for outlet in zip(*outlets)[0]]
        if normalize:
            timeseries = [ts / outlet_size for ts, outlet_size in zip(timeseries, outlet_sizes)]
        if not fig:
            fig = plt.figure(figsize=(12, 8))
        plt.subplots_adjust(left=0.08, bottom=0.12, right=0.95, top=0.92)
        for idx, ts in enumerate(timeseries):
            if len(ts):
                ts.plot(marker=marker, label=outlets[idx][1])
        plt.xlabel('Date Published', fontsize=12)
        if normalize:
            plt.ylabel('Article Frequency (freq = {})'.format(freq), fontsize=12)
        else:
            plt.ylabel('Article Count (Freq = {})'.format(freq), fontsize=12)
        plt.legend(loc='best')
        plt.title("Articles Containing '{}'".format(searchterm), fontsize=14)
        plt.legend(loc='best')
    if year:
        plt.xlim((date(2014, 12, 20), date(2016, 1, 15)))
        if not normalize:
            axis = plt.axis()
            plt.ylim((0, axis[3] + 1))
    if show:
        plt.show()





if __name__=='__main__':
    df = pd.read_pickle('election_data.pkl')

    # Plot % of articles mentioning candidate accross all news sources
    # plot_candidate_percentages(df, ['Clinton', 'Trump', 'Bush'])
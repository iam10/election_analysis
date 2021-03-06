from bs4 import BeautifulSoup
from requests import get
from load_data import get_keywords_2016, get_dates, get_file_name
import json
import os
import datetime
from sys import argv


def single_query(date):
    url = 'http://www.wsj.com/public/page/archive-{0}.html'.format(date)
    response = get(url)
    if response.status_code != 200:
        print('WARNING', response.status_code)
        print(date)
    else:
        return response


def get_urls(date, urls):
    html = single_query(date)
    try:
        soup = BeautifulSoup(html.content, 'html.parser')
    except:
        return urls

    # This will create a list of Tag elements for each story on the page
    articles = soup.find('ul', attrs={'class': 'newsItem'}).findAll('li')

    for article in articles:
        # add_url = False
        # for keyword in keywords:
        #     # Check the title and summary of the article for the presence of each searchterm.  If found, set the add_url flag to add the link to the urls set
        #     if keyword in article.find('a').text.lower():
        #         add_url = True
        #     elif keyword in article.text.lower():
        #         add_url = True
        # if add_url:
        #     urls.add(article.find('a').get('href'))
        urls.add(article.find('a').get('href'))
    print(len(urls))
    return urls


if __name__=='__main__':
    ''' This script should be called in the following way:
    $ python wsj_article_urls.py 'startdate' 'enddate'
    '''

    start_date, end_date = argv[1], argv[2]
    start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    while True:
        print('Scraping WSJ URLs from {0} to {1}'.format(start_date, end_date))

        # Get dates to search over
        dates = get_dates(start_date, end_date)

        urls = set()

        for date in dates:
            print(date)
            urls = get_urls(date, urls)

        # Convert urls set to a list and write to a txt file
        file_path = '../url_files/{0}'.format(get_file_name('wsj', start_date, end_date))
        with open(file_path, 'w') as f:
            f.write(json.dumps(list(urls)))
            f.close()

        start_datetime = start_datetime - datetime.timedelta(days=7)
        end_datetime = end_datetime - datetime.timedelta(days=7)
        start_date = start_datetime.strftime('%Y-%m-%d')
        end_date = end_datetime.strftime('%Y-%m-%d')

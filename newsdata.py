#!/usr/bin/env python3

''' module prints out data for newsdata db'''

import psycopg2


def get_query_results(query):
    ''' DB helper that handles interaction with the database'''
    try:
        db = psycopg2.connect(database="news")
        c = db.cursor()
        c.execute(query)
        result = c.fetchall()
        db.close()
        return result
    except psycopg2.Error as e:
        print(e)
        exit(1)


def three_articles_of_all_time():
    '''
        fetch and print the most popular three articles of all time
        based on number of the views
    '''
    query = '''select articles.title, count(*) as num
                    from log, articles
                    where log.status = '200 OK'
                    and log.path != '/'
                    and articles.slug = substring(log.path, 10)
                    group by articles.title
                    order by num desc
                    limit 3;
    '''
    top_articles = get_query_results(query)
    print('\nWhat are the most popular three articles of all time?\n')
    for title, views in top_articles:
        print('"{}" - {} views'.format(title, views))
    return


def all_time_authors():
    '''
        fetch and print the most popular authors of all time
        based on the sum of the views for all the articles
        each author has written
    '''
    query = '''select authors.name, sum(subq.num) as summer
        from authors,
            (select articles.title, articles.author, count(*) as num
            from log, articles
            where log.status = '200 OK'
            and log.path != '/'
            and articles.slug = substring(log.path, 10)
            group by articles.title, articles.author
            order by num desc
            ) as subq
        where authors.id =subq.author
        group by authors.name
        order by summer desc;
    '''
    top_authors = get_query_results(query)
    print('\nWho are the most popular article authors of all time?\n')
    for author, views in top_authors:
        print('{} - {} views'.format(author, views))
    return


def req_err_stats():
    '''
        fetch error statistics for each date and log the specific day
        when more then 1% of request failed
    '''
    query = '''select form_date, round(100.0 * failed_reqs / reqs, 2)
     as perc from
        (select  time::timestamp::date as form_date,
        count(*) as reqs,
        sum(case when log.status != '200 OK' then 1 else 0 end)
        as failed_reqs from log
        group by form_date
        ) as stats_by_date
        where ( 100.0 * failed_reqs / reqs ) > 1;
    '''
    days = get_query_results(query)
    print('\nOn which days did more than 1% of requests lead to errors?\n')
    for day in days:
        print(day[0].strftime("%B %d, %Y") +
              ' - ' + str(day[1]) + '% errors\n')
    return


three_articles_of_all_time()
all_time_authors()
req_err_stats()

#!/usr/bin/env python3
import psycopg2


def connect(database_name="new"):
    ''' 
    Establish connection with datebase and return db and cursor,
    takes news database as default parametar
    '''
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except psycopg2.Error as e:
        print("Can't connect to " + database_name + " database")
        print(e)


def printMessage(message):
    '''
    Prints appropriate message
    '''
    print('')
    print(message)
    print('')
    return


def three_articles_of_all_time():
    '''
        fetch and print the most popular three articles of all time
        based on number of the views
    '''
    db = connect()[0]
    c = connect()[1]
    c.execute('''select articles.title, count(*) as num
                    from log, articles
                    where log.status = '200 OK' 
                    and log.path != '/'
                    and articles.slug = substring(log.path, 10)
                    group by articles.title
                    order by num desc
                    limit 3;
    ''')
    top_articles = c.fetchall()
    db.close()
    printMessage('What are the most popular three articles of all time?')
    for article in top_articles:
        print('"' + str(article[0]) + '"' + ' - ' + str(article[1]))
    return


def all_time_authors():
    '''
        fetch and print the most popular authors of all time
        based on the sum of the views for all the articles
        each author has written
    '''
    db = connect()[0]
    c = connect()[1]
    c.execute('''select authors.name, sum(subq.num) as summer
        from authors, articles, (
                    select articles.title, count(*) as num
                    from log, articles
                    where log.status = '200 OK' 
                    and log.path != '/'
                    and articles.slug = substring(log.path, 10)
                    group by articles.title
                    order by num desc
                    ) as subq
        where authors.id = articles.author
        group by authors.name
        order by summer desc;
    ''')
    top_authors = c.fetchall()
    db.close()
    printMessage('Who are the most popular article authors of all time?')
    for author in top_authors:
        print(str(author[0]) + ' - ' + str(author[1]))
    return


def req_err_stats():
    '''
        fetch error statistics for each date and log the specific day
        when more then 1% of request failed
    '''
    db = connect()[0]
    c = connect()[1]
    c.execute('''select form_date, round(100.0 * failed_reqs / reqs, 2)
     as perc from
        (select  time::timestamp::date as form_date, 
        sum(case when log.status != '' then 1 else 0 end) as reqs, 
        sum(case when log.status != '200 OK' then 1 else 0 end) 
        as failed_reqs from log 
        group by form_date
        ) as stats_by_date
        where ( 100.0 * failed_reqs / reqs ) > 1;
    ''')

    days = c.fetchall()
    db.close()
    printMessage('On which days did more than 1% of requests lead to errors?')
    for day in days:
        print(day[0].strftime("%B %d, %Y") + ' - ' +
              str(day[1]) + '% errors')
    return


three_articles_of_all_time()
print('')
print('')

all_time_authors()
print('')
print('')

req_err_stats()
print('')

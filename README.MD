# Logs Analysis Project
 
Reporting tool that prints out reports (in plain text) based on the data from PostgreSQL database. Project is the part of Udacity fullstack nano degree curriculum

## PostgreSQL database structure ##
The database contains three tables: articles, authors, and log. The log table contains the contents of a web server request log. The PostgreSQL database was generated with a provided .sql dump, which is not included in the repository due to size limitations, however the readout of the tables, along with the output.txt file should provide a good idea of the database content:

    Table "articles"
     Column |           Type           |                       Modifiers
    --------+--------------------------+-------------------------------------------------------
     author | integer                  | not null
     title  | text                     | not null
     slug   | text                     | not null
     lead   | text                     |
     body   | text                     |
     time   | timestamp with time zone | default now()
     id     | integer                  | not null default nextval('articles_id_seq'::regclass)
    Indexes:
        "articles_pkey" PRIMARY KEY, btree (id)
        "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
    Foreign-key constraints:
        "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)


    Table "authors"
     Column |  Type   |                      Modifiers
    --------+---------+------------------------------------------------------
     name   | text    | not null
     bio    | text    |
     id     | integer | not null default nextval('authors_id_seq'::regclass)
    Indexes:
        "authors_pkey" PRIMARY KEY, btree (id)
    Referenced by:
        TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)


    Table "log"
     Column |           Type           |                    Modifiers
    --------+--------------------------+--------------------------------------------------
     path   | text                     |
     ip     | inet                     |
     method | text                     |
     status | text                     |
     time   | timestamp with time zone | default now()
     id     | integer                  | not null default nextval('log_id_seq'::regclass)
    Indexes:
        "log_pkey" PRIMARY KEY, btree (id)


## Run it locally
  Prerequisites:

  • Python3

  • Vagrant

  • VirtualBox


  Virtual Environment Setup:

  1. Ensure Vagrant, Virtual Box and Python are installed on your machine.
  2. Clone the Udacity fullstack-nanodegree-vm -> https://github.com/udacity/fullstack-nanodegree-vm
  3. Clone (or download) this repo into the /vagrant directory
  4. Download and unzip the newsdata.sql data file -> https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
  5. Extract zip contents into cloned /vagrant/logs-analysis directory
  6. Launch the VM:
    • $ vagrant up
  7. SSH into the VM:
    • On Mac/Linux - $ vagrant ssh
    • Windows use Putty or similar SSH client
  8. In the VM navigate to the /vagrant/logs-analysis directory:
    • $ cd /vagrant/logs-analysis
  9. Load the data into the news database already in the VM:
    • $psql -d news -f newsdata.sql
  10. Run python report script:
    • $ python newsdata.py



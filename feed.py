#!/usr/bin/env python

import feedparser
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText


# your atom feed, format: http://username:password@feedurl
feed="http://gijzelaerr:8gC5mjoM9pqzc4F!@uni101.ogame.org/feed/show.php?feedid=2516103b4af1089fd810a806d4763a0d"

# where to mail the reports
from_mail="ogame@pythonic.nl"
to_mail="gijs@pythonic.nl"

# what smtp server to use
smtp_server="localhost"

# where to store the database
database_file = os.path.join(os.path.dirname(__file__), "history.db")

mailer = smtplib.SMTP(smtp_server)
parsed_feed = feedparser.parse(feed)

database_exists = os.path.exists(database_file)
database = sqlite3.connect(database_file)

if not database_exists:
    database.execute("create table entry (id text)")

for entry in parsed_feed.entries:
    id = entry['id']
    title = entry['title']
    updated = entry['updated_parsed']
    summary = entry['summary']

    x = database.execute("SELECT count(*) FROM entry WHERE id=(?)", (id,))
    if x.fetchall()[0][0] == 0:
        #print("new message: ", title)
        msg = MIMEText(summary.encode('utf-8'), 'html', 'UTF-8')
        msg['Subject'] = title
        msg['From'] = from_mail
        msg['To'] = to_mail
        mailer.sendmail(from_mail, [to_mail], msg.as_string())
        database.execute("insert into entry values (?)", (id,))

mailer.quit()
database.commit()
database.close()


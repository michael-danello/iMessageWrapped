def total_texts_sent(year):
    return """
SELECT count(text), date, datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as message_date
FROM message
WHERE
    text NOT NULL
AND
    message_date >= '{year}-01-01'
AND
    message_date < '{next_year}-01-01'
AND
    is_from_me = 1
ORDER BY
    message_date DESC
""".format(year = year, next_year = year + 1)

def total_texts_received(year):
    return """
SELECT count(text), date, datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as message_date
FROM message
WHERE
    text NOT NULL
AND
    message_date >= '{year}-01-01'
AND
    message_date < '{next_year}-01-01'
AND
    is_from_me = 0
ORDER BY
    message_date DESC
""".format(year = year, next_year = year + 1)

def non_gc_non_automated(year):
    return """
SELECT count(text), date, datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as chat_message_date, chat.chat_identifier
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_message_date >= '{year}-01-01'
AND
    chat_message_date < '{next_year}-01-01'
AND
    is_from_me = 0
AND NOT
    chat.chat_identifier REGEXP '\+\d{11}'
ORDER BY
    chat_message_date DESC
""".format(year = year, next_year = year + 1)

def total_chars(year):
    return """
SELECT sum(length(text)), datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as chat_message_date
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_message_date >= '{year}-01-01'
AND
    chat_message_date < '{next_year}-01-01'
ORDER BY
    chat_message_date DESC
""".format(year = year, next_year = year + 1)

def all_chats(year):
    return """
SELECT COUNT(chat.chat_identifier) as total_chats, SUM(CASE WHEN message.is_from_me=1 THEN 1 ELSE 0 END) as from_me, SUM(CASE WHEN message.is_from_me=0 THEN 1 ELSE 0 END) as to_me,  chat.chat_identifier as name
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") >= '{year}-01-01'
AND
    datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") < '{next_year}-01-01'
AND
    chat_identifier REGEXP '\+1\d{{10}}'
GROUP BY
    chat.chat_identifier
ORDER BY
    total_chats DESC
""".format(year = year, next_year = year + 1)

def top_chats(year):
    return all_chats(year) + "LIMIT 10;"

ALL_CONTACTS = """
select record.ZFIRSTNAME as first_name, record.ZLASTNAME as last_name, numbers.ZFULLNUMBER as number
from ZABCDRECORD record
join ZABCDPHONENUMBER numbers on numbers.ZOWNER = record.Z_PK;
"""

def day_query(year):
    return """
SELECT
COUNT(chat.chat_identifier) as total_chats,
SUM(CASE WHEN message.is_from_me=1 THEN 1 ELSE 0 END) as from_me,
SUM(CASE WHEN message.is_from_me=0 THEN 1 ELSE 0 END) as to_me,
date (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as day,
datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as datetime
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_identifier REGEXP '\+1\d{{10}}'
AND
    day >= '{year}-01-01'
AND
    day < '{next_year}-01-01'
GROUP BY
    day
""".format(year = year, next_year = year + 1)


def first_text_of_day(year):
    return """
SELECT
COUNT(chat.chat_identifier) as total_chats,
SUM(CASE WHEN message.is_from_me=1 THEN 1 ELSE 0 END) as from_me,
SUM(CASE WHEN message.is_from_me=0 THEN 1 ELSE 0 END) as to_me,
date (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as day,
MIN(datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime")) as full_datetime,
time (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as full_time
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_identifier REGEXP '\+1\d{{10}}'
AND
    day > '{year}-01-01'
AND
    day < '{next_year}-01-01'
AND
    full_time > '06'
GROUP BY
    day
""".format(year = year, next_year = year + 1)

def all_days_query(year):
    return day_query(year) + """
ORDER BY
    day DESC
"""

def top_days(year):
    return day_query(year) + """
ORDER BY
    total_chats DESC
LIMIT 5;
"""

def all_hours_query(year):
    return """
SELECT
COUNT(chat.chat_identifier) as total_chats,
SUM(CASE WHEN message.is_from_me=1 THEN 1 ELSE 0 END) as from_me,
SUM(CASE WHEN message.is_from_me=0 THEN 1 ELSE 0 END) as to_me,
strftime('%H',datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime")) as time,
date (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as day
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_identifier REGEXP '\+1\d{{10}}'
AND
    day >= '{year}-01-01'
AND
    day < '{next_year}-01-01'
GROUP BY
    time
ORDER BY
    time DESC
""".format(year = year, next_year = year + 1)

def u_up(year):
    return """
SELECT
SUM(CASE WHEN message.is_from_me=1 THEN 1 ELSE 0 END) as from_me,
strftime('%H',datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime")) as time,
chat.chat_identifier as number,
date (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as day
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_identifier REGEXP '\+1\d{{10}}'
AND
    day >= '{year}-01-01'
AND
    day < '{next_year}-01-01'
AND
    time < '03'
GROUP BY
    time, chat.chat_identifier
ORDER BY
    from_me DESC
LIMIT 1;
""".format(year = year, next_year = year + 1)

def all_text(year):
    return """
SELECT
    message.text,
    datetime (message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
    message.is_from_me,
    chat.chat_identifier as number,
    date (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as day
FROM
    message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    chat_identifier REGEXP '\+1\d{{10}}'
AND
    day >= '{year}-01-01'
AND
    day < '{next_year}-01-01'
AND
    text not NULL
AND
    message.is_from_me = 1
ORDER BY
    message_date DESC;
""".format(year = year, next_year = year + 1)

GHOSTED_WINDOW = """
SELECT
    datetime (message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
    chat.chat_identifier as number,
    LEAD(datetime(message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime", "3 hours"), 1, "NA") OVER (ORDER BY message_date DESC) ghosted,
    to_me,
    from_me
FROM
    message
JOIN
    chat_message_join cmj on cmj.message_id = message.ROWID
JOIN
    chat on chat.ROWID = cmj.chat_id
WHERE
    number = '+12022887321'
AND
    message_date > ghosted
ORDER BY
    message_date DESC;
"""

def avg_message_length(year):
    return """
SELECT
    AVG(LENGTH(message.text)),
    datetime (message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
    message.is_from_me,
    chat.chat_identifier as number,
    date (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as day
FROM
    message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    chat_identifier REGEXP '\+1\d{{10}}'
AND
    text not NULL
AND
    day >= '{year}-01-01'
AND
    day < '{next_year}-01-01'
AND
    message.is_from_me = 1
ORDER BY
    message_date DESC;
""".format(year = year, next_year = year + 1)

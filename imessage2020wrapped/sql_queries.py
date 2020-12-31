TOTAL_TEXTS_SENT = """
SELECT count(text), date, datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as message_date
FROM message
WHERE
    text NOT NULL
AND
    message_date > '2020-01-01'
AND
    is_from_me = 1
ORDER BY
    message_date DESC
"""

TOTAL_TEXTS_RECIEVED = """
SELECT count(text), date, datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as message_date
FROM message
WHERE
    text NOT NULL
AND
    message_date > '2020-01-01'
AND
    is_from_me = 0
ORDER BY
    message_date DESC
"""

NON_GC_NON_AUTOMATED = """
SELECT count(text), date, datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as chat_message_date, chat.chat_identifier
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_message_date > '2020-01-01'
AND
    is_from_me = 0
AND NOT
    chat.chat_identifier REGEXP '\+\d{11}'
ORDER BY
    chat_message_date DESC
"""

TOTAL_CHARS = """
SELECT sum(length(text)), datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") as chat_message_date
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_message_date > '2020-01-01'
ORDER BY
    chat_message_date DESC
"""

ALL_CHATS = """
SELECT COUNT(chat.chat_identifier) as total_chats, SUM(CASE WHEN message.is_from_me=1 THEN 1 ELSE 0 END) as from_me, SUM(CASE WHEN message.is_from_me=0 THEN 1 ELSE 0 END) as to_me,  chat.chat_identifier as name
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") > '2020-01-01'
AND
    chat_identifier REGEXP '\+1\d{10}'
GROUP BY
    chat.chat_identifier
ORDER BY
    total_chats DESC
"""

TOP_CHATS = ALL_CHATS + "LIMIT 10;"

ALL_CONTACTS = """
select record.ZFIRSTNAME as first_name, record.ZLASTNAME as last_name, numbers.ZFULLNUMBER as number
from ZABCDRECORD record
join ZABCDPHONENUMBER numbers on numbers.ZOWNER = record.Z_PK;
"""

DAY_QUERY = """
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
    chat_identifier REGEXP '\+1\d{10}'
AND
    day > '2020-01-01'
AND
    day < '2021-01-01'
GROUP BY
    day
"""


FIRST_TEXT_OF_DAY = """
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
    chat_identifier REGEXP '\+1\d{10}'
AND
    day > '2020-01-01'
AND
    day < '2021-01-01'
AND
    full_time > '06'
GROUP BY
    day
"""

ALL_DAYS = DAY_QUERY + """
ORDER BY
    day DESC
"""

TOP_DAYS = DAY_QUERY + """
ORDER BY
    total_chats DESC
LIMIT 5;
"""

ALL_HOURS = """
SELECT
COUNT(chat.chat_identifier) as total_chats,
SUM(CASE WHEN message.is_from_me=1 THEN 1 ELSE 0 END) as from_me,
SUM(CASE WHEN message.is_from_me=0 THEN 1 ELSE 0 END) as to_me,
strftime('%H',datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime")) as time
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_identifier REGEXP '\+1\d{10}'
GROUP BY
    time
ORDER BY
    time DESC
"""

U_UP = """
SELECT
SUM(CASE WHEN message.is_from_me=1 THEN 1 ELSE 0 END) as from_me,
strftime('%H',datetime (date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime")) as time,
chat.chat_identifier as number
FROM message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    text NOT NULL
AND
    chat_identifier REGEXP '\+1\d{10}'
AND
    time < '03'
GROUP BY
    time, chat.chat_identifier
ORDER BY
    from_me DESC
LIMIT 1;
"""
ALL_TEXT = """
SELECT
    message.text,
    datetime (message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
    message.is_from_me,
    chat.chat_identifier as number
FROM
    message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    chat_identifier REGEXP '\+1\d{10}'
AND
    text not NULL
AND
    message.is_from_me = 1
ORDER BY
    message_date DESC;
"""

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

AVG_MESSAGE_LENGTH = """
SELECT
    AVG(LENGTH(message.text)),
    datetime (message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
    message.is_from_me,
    chat.chat_identifier as number
FROM
    message
JOIN chat_message_join cmj on cmj.message_id = message.ROWID
JOIN chat on chat.ROWID = cmj.chat_id
WHERE
    chat_identifier REGEXP '\+1\d{10}'
AND
    text not NULL
AND
    message.is_from_me = 1
ORDER BY
    message_date DESC;
"""

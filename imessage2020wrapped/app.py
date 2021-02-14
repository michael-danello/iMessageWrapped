# External Imports
import sqlite3
from flask import g, Flask, render_template, request, jsonify
import pandas.io.sql as sqlio
import pandas as pd
import emoji
import zipcodes
import nltk
# Standard Library
import os
import re
import sys
import functools
import subprocess
import getpass
from collections import Counter
# Local Imports
from .sql_queries import *
from .nlp_utils import *

def get_user():
    username = getpass.getuser()
    return username


def get_chat_db_path():
    username = get_user()
    return f"/Users/{username}/Library/Messages/chat.db"

def get_address_db_path():
    """
    iterate through address books and return all contact database paths
    """
    username = get_user()
    path = os.path.abspath(f"/Users/{username}/Library/Application Support/AddressBook/Sources")

    contact_db_paths = []
    # walking through the entire folder,
    # including subdirectories

    for folder, subfolders, files in os.walk(path):
        # checking the size of each file
        for file in files:
            if file == "AddressBook-v22.abcddb" and folder != path:
                contact_db_paths.append(os.path.join( folder, file))

    print(contact_db_paths)
    return contact_db_paths


app = Flask(__name__)

CHAT_DATABASE = get_chat_db_path()
CONTACTS_DATABSES = get_address_db_path()

#  Estiamte Taken from Here (and obviously rough) https://www.anycount.com/word-count-news/how-many-words-in-one-page/#:~:text=Just%20to%20keep%20in%20mind,600%20words%20(academic%20book).
CHARS_IN_PAGE = 3000

# regex is not loaded as default function in SQLite, so it must be manually added
def re_fn(expr, item):
    reg = re.compile(expr, re.I)
    return reg.search(item) is not None

class Wrapped():
    pass


def get_db(source):
    db = g._database = sqlite3.connect(source)
    db.create_function("REGEXP", 2, re_fn)
    return db


def db_to_json(query, conn):
    """execute query on connection, and return data as a dict"""

    df = pd.read_sql(query, conn)
    df_dict = df.to_dict(orient='list')

    return df_dict


def format_number(number):
    """standardizes numbers in contacts"""

    chars_to_remove = " ()-"

    for char in chars_to_remove:
        number = number.replace(char, "")
    if number[0:2] != '+1':
        number = '+1' + number

    return number


def format_contacts(contacts):
    """format firstname, lastname and number of contacts"""

    contacts['number'] = contacts['number'].apply(format_number)
    contacts = contacts.fillna("")
    contacts = contacts.set_index('number')
    contacts_dict = contacts.to_dict()
    full_name_contacts_dict = {}

    for key, value in contacts_dict['first_name'].items():
        full_name_contacts_dict[key] = value + " " + contacts_dict['last_name'][key]

    return full_name_contacts_dict


def get_contacts():
    """ A user may mantain multiple local contacts databases. Iterate through
    all of these databaes, extract all contacts from each and update the contact
    dict with results. Return the contacts dict"""

    contacts_dict = {}
    for contacts_db in CONTACTS_DATABSES:

        contacts_conn = get_db(contacts_db)
        contacts_cur = contacts_conn.cursor()
        all_contacts = pd.read_sql(ALL_CONTACTS, contacts_conn)
        print(all_contacts)
        contacts_dict.update(format_contacts(all_contacts))
        print(contacts_dict)

    return contacts_dict

def extract_emojis(s):
    """
    extract all emojis in a string
    :param s: a string containing emojis to be extracted
    """
    return ''.join(c for c in s if c in emoji.UNICODE_EMOJI)

def count_emojis(text):
    """
    counts emojis in a str
    :param text: emojis to be extracted
    return: dict of emojis by frequency
    """

    emojis = text.apply(extract_emojis)
    emoji_str = "".join(list(emojis))

    emoji_cnt = Counter('emojis')
    for emoji in emoji_str:
        emoji_cnt[emoji] += 1

    return emoji_cnt

def avg_datetime(series):
    """
    calculutes average time (in hours and minutes) for a pandas
    series.
    :param series: pd dt series
    :return the time as as string (HH:MM)
    """
    avg_hour = sum([time.hour for time in series])/len(series)
    avg_minute = sum([time.minute for time in series])/len(series)
    avg_time = avg_hour + avg_minute/60

    return str(int(avg_time)) + ":" + str(int(avg_time % 1 * 60))

def get_text_totals(wrapped, chat_cur, year):
    wrapped.total_texts_sent = chat_cur.execute(total_texts_sent(year)).fetchone()[0]
    wrapped.total_texts_recieved = chat_cur.execute(total_texts_received(year)).fetchone()[0]
    wrapped.total_pages = round(chat_cur.execute(total_chars(year)).fetchone()[0]/CHARS_IN_PAGE)

def get_text(year):
    chat_conn = get_db(CHAT_DATABASE)
    text_df = pd.read_sql(all_text(year), chat_conn)
    text = " ".join(text_df['text'])
    return text

def get_tokenized_text(text):
    tokens = nltk.word_tokenize(text)
    tokens_clean = [word.lower() for word in tokens if word.isalnum()]
    return tokens_clean

def get_initiator(chat_conn, year):
    all_contacts = pd.read_sql(all_chats(year), chat_conn)
    all_close_contacts = all_contacts[all_contacts['from_me'] > 25]
    initiated = all_close_contacts.query('from_me > to_me')
    return len(initiated.index)/len(all_contacts.index)

def get_who_data(wrapped, chat_conn, contacts_dict, year):
    top_contacts = pd.read_sql(top_chats(year), chat_conn)
    top_contacts = top_contacts.replace({'name':contacts_dict})
    wrapped.top_contacts = top_contacts.to_dict(orient='index')


def get_when_data(wrapped, chat_conn, chat_cur, contacts_dict, year):
    top_days_raw = pd.read_sql(top_days(year), chat_conn, parse_dates='day')['day']
    top_days_formatted = [str(day.month_name()) + " " + str(day.day) for day in top_days_raw]
    wrapped.top_days = top_days_formatted
    time = pd.read_sql(first_text_of_day(year), chat_conn, parse_dates=["full_time"])['full_time']
    wrapped.wake_up_avg = avg_datetime(time)
    u_up_raw = chat_cur.execute(u_up(year)).fetchone()
    wrapped.u_up = {'total_sent':u_up_raw[0], 'name':contacts_dict[u_up_raw[2]]}


def get_what_data(wrapped, chat_conn, year):
    all_text_df = pd.read_sql(all_text(year), chat_conn, parse_dates=["message_date"])
    wrapped.emojis = count_emojis(all_text_df['text']).most_common(8)

def get_how_data(wrapped, chat_conn, chat_cur, year):
    wrapped.avg_message_len = chat_cur.execute(avg_message_length(year)).fetchone()[0]
    wrapped.initator= int(get_initiator(chat_conn, year)*100)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/data/week_days', methods=['POST','GET'])
def all_week_days():
    """
    calculuate frequency by day of week
    return: dict with days of the week as values and frequency as keys
    """

    chat_conn = get_db(CHAT_DATABASE)
    year = int(request.args.get('year') or 2020)

    all_days =  pd.read_sql(all_days_query(year), chat_conn, parse_dates=["day"])
    all_days['to_me'] = (all_days['to_me']/52).astype(int)
    all_days['from_me'] = (all_days['from_me']/52).astype(int)
    # hacky fix since days needed to be grouped and then sorted
    all_days['day'] = all_days['day'].dt.dayofweek

    all_days_sum = all_days.groupby(['day']).sum().sort_values(by="day")
    all_days_sum['day'] = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    return all_days_sum.to_dict(orient='list')

@app.route('/data/all_days', methods=['POST','GET'])
def all_days():
    """
    api-ish route: calculuates frequency by day of the year
    """
    year = int(request.args.get('year') or 2020)
    chat_conn = get_db(CHAT_DATABASE)

    return db_to_json(all_days_query(year), chat_conn)

@app.route('/data/all_hours', methods=['POST','GET'])
def all_hours():

    """api-ish route: retrieves, structures, and labels frequency data by hour"""

    chat_conn = get_db(CHAT_DATABASE)

    year = int(request.args.get('year') or 2020)
    df = pd.read_sql(all_hours_query(year), chat_conn)

    df = df.sort_values(by="time")

    formatted_hours = [str(int(hour) % 12) +":00" for hour in df['time']]
    ams = [hour + "AM" for hour in formatted_hours[1:12]]
    pms = [hour + "PM" for hour in formatted_hours[13:]]
    formatted_hours = ["Midnight"] + ams + ["Noon"] + pms
    df['time'] = formatted_hours

    return df.to_dict(orient='list')

@app.route('/data/contact_map', methods=['POST','GET'])
def contact_locations():
    """api-ish route: returns lat/long positions of all contacts texted"""


    all_contacts = get_contacts()
    chat_conn = get_db(CHAT_DATABASE)
    year = int(request.args.get('year') or 2020)
    cur_contacts = pd.read_sql(all_chats(year), chat_conn)

    contacts = {k:v for (k,v) in all_contacts.items() if k in list(cur_contacts['name'])}

    people_map = {}
    for number, name in contacts.items():
        area_code = number[2:5]

        if people_map.get(area_code) != None:
            people_map[area_code]['people'].append(name)
            continue

        zipcode = zipcodes.filter_by(area_codes=[area_code])
        if len(zipcode) == 0:
            continue
        else:
            people_map[area_code] = {
                "place":[zipcode[0]['lat'],zipcode[0]['long']],
                "people": [name]
            }

    return people_map

@app.route('/data/common_words', methods=['POST','GET'])
def common_pos():
    """api-ish route: returns most frequent parts of speech in sent text corpus"""

    year = int(request.args.get('year') or 2020)

    pos_list = [
        {
        'name':'Adjectives',
        'code':'JJ',
        'data': None
        },
        {
        'name':'Nouns',
        'code':'NN',
        'data': None
        },
        {
        'name':'Superlatives',
        'code':'JJS',
        'data': None
        },
        {
        'name':'Verbs',
        'code':'VB',
        'data': None
        },
    ]

    tf_idf_list = [
        {
            'name': 'Single',
            'data': None
        },
        {
            'name':'Bigram',
            'data': None
        }
    ]

    text = get_text(year)
    tagged = tag_text(get_tokenized_text(text))

    for pos in pos_list:
        pos['data'] = common_word_dict(count_pos(pos['code'], tagged))

    # this was going to take too long load + it's huge. shame. the data is cool

    return {'pos':pos_list, 'tfidf': tf_idf_list}

@app.route('/', methods=['POST','GET'])
def index():
    contacts_dict = get_contacts()
    wrapped = Wrapped()

    chat_conn = get_db(CHAT_DATABASE)
    chat_cur = chat_conn.cursor()
    year = int(request.args.get('year') or 2020)

    get_text_totals(wrapped, chat_cur, year)
    get_who_data(wrapped, chat_conn, contacts_dict, year)
    get_when_data(wrapped, chat_conn, chat_cur, contacts_dict, year)
    get_what_data(wrapped, chat_conn, year)
    get_how_data(wrapped, chat_conn, chat_cur, year)

    return render_template("wrapped.html", wrapped=wrapped, year=year)

@app.route('/share', methods=['POST','GET'])
def share():
    return render_template("share.html")

def run_app():
     app.run(debug=True)

import datetime
import random

from flask import Flask, render_template, request, session, url_for, redirect
from flask_uploads import UploadSet, IMAGES, configure_uploads
from google.cloud import datastore
from google.cloud import storage
from requests import Session


from bucket import Bucket
from forumForm import ForumForm
from registerForm import RegisterForm
from bigquery import bigquery_check

import os

from google.cloud import bigquery

PATH = os.path.join(os.getcwd(), 'chengccassgn1-ce7fd57eac11.json')
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH
# BASEPATH = os.path.abspath(os.path.dirname(__file__))

datastore_client = datastore.Client()
storage_client = storage.Client()

bucket_name = 'ass1forimages'

app = Flask(__name__)

user_dict = {}

app.config['UPLOADED_IMAGES_DEST'] = './Image'
PATH_BASE = 'Image/'


app.config['SECRET_KEY'] = 'god'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)


def bigquery_check(sql_clause):
    client = bigquery.Client(project='chengccassgn1')
    query_job = client.query(sql_clause)  # Make an API request.
    print("The query data:")
    # print(query_job)

    output = ''
    temp_list = []
    for row in query_job:
    # Row values can be accessed by field name or index.
        for step, _ in enumerate(row):
            output = output + " "+str(row[step])
        temp_list.append(output)
        # print("country_code={}".format(row[1]))
        output = ''

    output = '\n'.join(temp_list)

    return output

def store_user(id, un, pw, url):
    kind = 'user'
    task_key = datastore_client.key(kind, id)
    task = datastore.Entity(task_key)

    task.update({
        'id': id,
        'user_name': un,
        'password': pw,
        'url': url
    })

    datastore_client.put(task)

def delete_user():
    pass

def get_property_query():
    query = datastore_client.query(kind= 'user')
    usern = []

    for entity in query.fetch():
        # if id == entity["user"] and test_password == entity["password"]:
        #     return

        usern.append((entity['id'], entity['password']))
    # print(usern)
    return usern


# def fetch_times(limit):
#     query = datastore_client.query(kind='user')
#     query.order = ['-id']
#     times = query.fetch(limit=limit)
#     return times


def __random_password():
    str = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch
    return str

@app.route("/bigquery", methods=["GET", 'POST'])
def big_query():
    if request.method == 'POST':
        sql = request.form['textarea']
        output = bigquery_check(sql)
        return render_template('bigqueryres.html', output=output)

    return render_template('bigquery.html')


def __generate_users():
    base_id = 's3803990'
    base_name = 'Qixiang_Cheng'

    base_image_post_name = '.jpg'

    # image_url = bucket(bucket_name, source_file_name).image_url

    for i in range(10):
        source_file_name = PATH_BASE + str(i) + base_image_post_name

        temp_list = []
        temp_list.append(base_id+str(i))
        temp_list.append(base_name+str(i))
        temp_list.append(__random_password())
        temp_list.append(Bucket(bucket_name, source_file_name).image_url)
        user_dict[i] = temp_list

# def fetch_recorder(limit):
#     query = datastore_client.query(kind='recorder')
#
# def store_times(limit):



def __judge_db():
    if len(get_property_query())!= 0:
        print("I have db")
        return True
    else:
        print("do not have db")
        return False

#TODO
@app.route('/')
def root():
    # Store the current access time in Datastore.
    if not __judge_db():
        __generate_users()
        for i in range(10):
            store_user(user_dict[i][0], user_dict[i][1], user_dict[i][2], user_dict[i][3])

    if 'username' in session:
        forum_form = ForumForm()
        return render_template('forum_page.html', form = forum_form, name=session['username'], url=session['url'])
    #
    # get_property_query()
    # times = fetch_times(10)
    return render_template(
        'index.html')



def __judge_status(id, pd):
    query = datastore_client.query(kind='user')


    # print(get_property_query())
    # print('rid', id, 'rpd', pd)
    for entity in query.fetch():
        # print('id',entity['id'], 'pd', entity['password'])
        if str(id) == entity["id"] and str(pd) == entity["password"]:
            # print(id, pd)


            session['username']= str(entity['user_name'])
            # print('entity', entity['url'])
            session['url'] = str(entity['url'])
            session['password'] = str(entity['password'])
            session['id'] = str(entity['id'])

            # print(session['url'])
            # print('session name', session['username'])
            # print('entity', str(entity['user_name']))
            return True

    return False

@app.route('/login', methods=['POST'])
def login():
    if 'username' in session:

        output = display_forum(10)
        return render_template('forum_page.html', name = session['username'], output = output)

    curr_id = request.form['ID']
    curr_pd = request.form['password']
    error = None
    #TODO:

    if __judge_status(curr_id, curr_pd):
        form = ForumForm()
        # print(session['url'])
        # flash("Login Successfully!")
        output = display_forum(10)
        return render_template('forum_page.html', name = session['username'],form= form, url = session['url'], output = output)
    else:
        error = "ID or password is invalid"
        return render_template('index.html', error = error)

def delete_userinfo():
    pass

@app.route('/change_password', methods=['POST'])
def change_password():
    error = None
    if 'username' in session:

        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if str(old_password) != str(session['password']):
            error = 'The old password is incorrect'
            return render_template('user_page.html', name = session['username'],error = error)

        session['password'] = new_password

        with datastore_client.transaction():
            key = datastore_client.key('user', session['id'])
            task = datastore_client.get(key)

            task['password'] = str(new_password)

            print(1)

            datastore_client.put(task)


    return redirect(url_for('logout'))

    # store_user(,1,1,1)

@app.route('/register', methods=['POST','GET'])
def register():
    error = None
    register_from = RegisterForm()

    if request.method == 'POST':
        # print(request.form)
        if register_from.validate_on_submit():
        # if True:
            ID = request.form.get('id')
            username = request.form.get('username')
            password = request.form.get('password1')
            password2 = request.form.get('password2')
            # f = form.photo.data


            filename = images.save(register_from.photo.data)

            print(ID, username, password, password2)
    # ID = request.form['ID']
    # username = request.form['username']
    # password = request.form['password']

    # f.save(f.filename)
            query = datastore_client.query(kind='user')

            for entity in query.fetch():
                # print('id',entity['id'], 'pd', entity['password'])
                if str(ID) == entity["id"]:
                    error = "The ID already exists"
                    return render_template('register.html',form = register_from, error= error)
                elif str(username) == entity['user_name']:
                    error = "The username already exists"
                    return render_template('register.html',form = register_from, error=error)


            temp_uploaded_url = Bucket(bucket_name, PATH_BASE+str(filename)).image_url
            store_user(ID, username, password, temp_uploaded_url)
            render_template('index.html', error=error)
        else:
            return render_template('register.html', form=register_from, error=error)

        return render_template('index.html')
    else:

        return render_template('register.html', form=register_from, error=error)


@app.route('/forum_page', methods=['POST', 'GET'])
def forum():
    forum_form = ForumForm()
    limit = 10

    if request.method == 'POST':
        subject = ''
        message_text = ''
        if forum_form.validate_on_submit():
            subject = request.form.get('subject')
            message_text = request.form.get('message_text')
            filename = images.save(forum_form.photo.data)
            forum_save(filename, subject, message_text)

            # return render_template('forum_page.html', form = forum_form, message = message_text, subject = subject,
            #                        name=session['username'], url=session['url'])
            output = display_forum(limit)
            return render_template('forum_page.html', form=forum_form,
                                   name=session['username'], url=session['url'], output = output)

def forum_save(filename,subject, message):
    temp_url = Bucket(bucket_name, PATH_BASE+str(filename)).image_url
    kind1 = 'user'

    parent_key = datastore_client.key(kind1, session['id'])
    task_key = datastore_client.key('message', parent = parent_key)

    task = datastore.Entity(task_key)
    dt = datetime.datetime.now()

    task.update({
        'subject': subject,
        'message': message,
        'url': temp_url,
        'timestamp': dt
    })

    datastore_client.put(task)

def display_forum(limit):
    kind = 'message'
    # parent_key = datastore_client.key('user', session['id'])
    # my_query = datastore_client.query(ancestor=parent_key)

    query = datastore_client.query(kind = kind)
    query.order = ['-timestamp']
    output = query.fetch(limit = limit)
    return output


    # subject_set = set()
    # for entity in list(my_query.fetch()):
    #     if 'subject' in entity:
    #
    #         subject_set.add(entity['subject'])
    #
    # for i in subject_set:
    #     final_query = datastore_client.query(kind = i, ancestor = parent_key)
    #     output.extend(final_query.fetch)
    # #
    # #     for entity in list(final_query.fetch()):
    # #         output.extend(entity)
    #
    # for i in subject_set:
    #     my_query.add_filter('subject', '=', i)
    #
    #
    # for k in my_query.fetch():
    #     print(k)
    #
    # my_query.order = ['-timestamp']
    # output = my_query.fetch(limit = limit)
    # for i in output:
    #     print(i['message'])
    # return output






# parent_key = datastore_client.key('user', 's38039909')
# my_query = datastore_client.query(ancestor = parent_key)
#
# for entity in list(my_query.fetch()):
#     if 'subject' in entity:
#         print(entity['subject'])
#
#         print(entity['message'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('url', None)
    session.pop('password', None)
    session.pop('id', None)
    return render_template('index.html')

@app.route('/user_page')
def user_page():

    return render_template('user_page.html', name= session['username'])

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)

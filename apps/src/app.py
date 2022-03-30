import os
from datetime import datetime
from flask import Flask, render_template, make_response, request
import re
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='192.168.1.72',
                            database='sgndb',
                            port=5434,
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn
  
  


def get_app_debug_info():
    cfg_items = {k: v for k, v in os.environ.items()}
    cfg_items['datetime'] = datetime.now().isoformat()
    return cfg_items


@app.route('/')
def welcome():
    return {
        'msg': 'Hello World! This is a simple Python app using Flask! But wait there is more!',
        'endpoints': ['/', '/ping', '/debug', '/debug/ui', '/register']
    }

@app.route('/sgn')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    book=[]
    cur.close()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/update', methods =['GET', 'POST'])
def update():
    msg = ''
    posts=""
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST' and 'id' in request.form :
        post = request.form['post']
        firstname = request.form['firstname']
        id=int(request.form['id'])
        cur.execute("update posts set firstname=%s,post=%s where id=%s",(firstname,post,str(id)))
        cur.connection.commit()
        cur.execute('SELECT * FROM posts')
        posts = cur.fetchall()
        print(posts)
        msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    cur.execute('SELECT * FROM posts')
    posts = cur.fetchall()
    return render_template('view.html', msg = msg , posts=posts)



@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    posts=""
    if request.method == 'POST' and 'post' in request.form :
        post = request.form['post']
        firstname = request.form['firstname']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("insert into posts (post,firstname) values ( %s,%s )",(post,firstname))
        cur.connection.commit()
        cur.execute('SELECT * FROM posts')
        posts = cur.fetchall()
        print(posts)
        conn.close()
        msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('view.html', msg = msg , posts=posts)
  


@app.route('/ping')
def ping():
    return {'msg': 'pong!'}


@app.route('/debug', methods=['GET'])
def debug():
    cfg_items = get_app_debug_info()
    response = make_response(cfg_items, 200)

    # Enable CORS: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    response.headers['Access-Control-Allow-Origin'] = '*'  # allow all domains for now
    response.headers['Access-Control-Allow-Methods'] = "GET"

    return response


@app.route('/debug/ui', methods=['GET'])
def debug_ui():
    cfg_map = get_app_debug_info()
    # sort items by key
    cfg_items = sorted([{'k': k, 'v': v} for k, v in cfg_map.items()], key=lambda x: x['k'].upper())
    return render_template('debug.html', cfg_items=cfg_items, title='Hello Python Debug!')


@app.errorhandler(404)
def not_found(e):
    return {'err': 'Not found!'}, 404


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)

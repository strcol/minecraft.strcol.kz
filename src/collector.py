'''
Copyright 2021, Kaletise

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Contact me via Telegram, VK, Reddit or Twitter: @kaletise
'''

import json
import smtplib
import sqlite3
import time
import traceback

import flask
import gevent.pywsgi

import config


last_submit = {}


def get_database():
    return sqlite3.connect('database.db', check_same_thread=False)


def main():
    app = flask.Flask(__name__, root_path = '', template_folder = '')

    _config = config.Config('config.json', default = {
        'SMTP_HOST': 'xxxx.xxxxxx.xx',
        'SMTP_PORT': 465,
        'SMTP_USERNAME': 'xxxx@xxxxxx.xx',
        'SMTP_PASSWORD': 'xxxxxxxx'
    })

    database = get_database()
    cursor = database.cursor()
    cursor.execute(
        ('CREATE TABLE IF NOT EXISTS applications (unixtime LONG, '
         'ip TINYTEXT, nickname TINYTEXT, fullname TINYTEXT, '
         'school TINYTEXT, class TINYTEXT, phone TINYTEXT, email TINYTEXT)')
    )
    database.commit()
    database.close()

    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route('/logo.png', methods=['GET'])
    def logo():
        return flask.send_file('static/logo.png')

    @app.route('/submit', methods=['POST'])
    def submit_handler():
        try:
            data = flask.request.form
            ip = flask.request.remote_addr
            current_time = int(time.time() * 1000)
            if 'nickname' not in data or 'fullname' not in data or \
                    'school' not in data or 'class' not in data or \
                    'phone' not in data or 'email' not in data or \
                    len(data['nickname']) > 16 or \
                    len(data['fullname']) > 64 or \
                    len(data['school']) > 32 or len(data['class']) > 16 or \
                    len(data['phone']) > 16 or len(data['email']) > 64:
                return json.dumps({'status': -1})
            if ip in last_submit and last_submit[ip] > current_time:
                last_submit[ip] += 10000
                return json.dumps({'status': -2})
            database = get_database()
            cursor = database.cursor()
            if cursor.execute(
                        ('SELECT 1 FROM applications WHERE nickname=? OR '
                         'email=?'),
                        (data['nickname'], data['email'])
                    ).fetchone():
                database.close()
                last_submit[ip] = current_time + 10000
                return json.dumps({'status': 2})
            cursor.execute(
                'INSERT INTO applications VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    int(time.time() * 1000), ip, data['nickname'],
                    data['fullname'], data['school'], data['class'],
                    data['phone'], data['email']
                )
            )
            with open('templates/email.html', 'r', encoding='utf-8') as file:
                email_rendered = flask.render_template_string(
                    file.read(), nickname=data['nickname'],
                    fullname=data['fullname'], school=data['school'],
                    _class=data['class'], phone=data['phone'],
                    email=data['email']
                )
            database.commit()
            database.close()
            server = smtplib.SMTP_SSL(
                _config.get('SMTP_HOST'), _config.get('SMTP_PORT')
            )
            server.ehlo()
            server.login(
                _config.get('SMTP_USERNAME'), _config.get('SMTP_PASSWORD')
            )
            server.sendmail(
                _config.get('SMTP_USERNAME'), data['email'],
                ('From: Костанайский Строительный Колледж <admin@strcol.kz>\n'
                 'To: ' + data['email'] + '\n'
                 'Subject: Подтверждение заявки - '
                 'Костанайский Строительный Колледж\n'
                 'Content-type: text/html\n\n' + email_rendered
                ).encode('utf-8')
            )
            server.quit()
            last_submit[ip] = current_time + 60000
            return json.dumps({'status': 1})
        except Exception:
            traceback.print_exc()
            return json.dumps({'status': -3})

    gevent.pywsgi.WSGIServer(
        ('0.0.0.0', 443), app,
        keyfile='ssl/server.key', certfile='ssl/server.crt'
    ).serve_forever()


if __name__ == '__main__':
    main()

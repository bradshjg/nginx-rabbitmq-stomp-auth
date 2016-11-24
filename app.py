#!/usr/bin/env python
import base64
import os

from flask import abort, Flask, redirect, request, url_for
import flask_login


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = 'fake secret key'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'bob': {'pw': 'changeme'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username

    user.is_authenticated = request.form['pw'] == users[username]['pw']

    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return """
               <form action='' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               """

    username = request.form['username']
    if request.form['pw'] == users[username]['pw']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('ws_test'))

    return 'Bad login'


@app.route('/')
@flask_login.login_required
def ws_test():
    return open(os.path.join(CURRENT_DIR, 'ws-test.html')).read()


@app.route('/auth')
def auth():
    if not flask_login.current_user.is_authenticated:
        abort(401)
    return (
        'OK',
        {'Authorization': 'Basic %s' % base64.b64encode('bob:changeme')}
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

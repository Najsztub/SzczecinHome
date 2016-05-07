# coding: utf-8
'''
MN: 04/05/16
Flask tutorial: https://blog.openshift.com/build-your-app-on-openshift-using-flask-sqlalchemy-and-postgresql-92/
And here: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
And here: http://charlesleifer.com/blog/saturday-morning-hacks-building-an-analytics-app-with-flask/
'''
from app import app

@app.route('/')
@app.route('/hello')
def index():
    return "Hello world!"

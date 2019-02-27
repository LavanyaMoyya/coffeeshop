from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Coffeeshop, MenuItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from functools import wraps
from flask import Flask, render_template, \
                  url_for, request, redirect,\
                  flash, jsonify

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Coffeeshop Menu Application"


'''Connect to Database and create database session'''
engine = create_engine('sqlite:///coffeeshopmenuwithusers.db', connect_args={
    'check_same_thread': False}, echo=True)
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


'''Decorator function for login'''


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


'''Create anti-forgery state token'''


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''Validate state token'''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    '''Obtain authorization code'''
    code = request.data

    try:
        '''Upgrade the authorization code into a credentials object'''
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Check that the access token is valid.'''
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    '''Submit request, parse response - Python3 compatible'''
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    '''If there was an error in the access token info, abort.'''
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Verify that the access token is used for the intended user.'''
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Verify that the access token is valid for this app.'''
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        '''return response'''

    '''Store the access token in the session for later use.'''
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    '''Get user info'''
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    '''ADD PROVIDER TO LOGIN SESSION'''
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    '''see if user exists, if it doesn't make a new one'''
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px; \
                            -webkit-border-radius: 150px;-moz-border-radius: \
                                150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


'''User Helper Functions'''


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


'''DISCONNECT - Revoke a current user's token and reset their login_session'''


@app.route('/gdisconnect')
def gdisconnect():
    '''Only disconnect a connected user.'''
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        '''Reset the user's sesson.'''
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        login_session.clear()

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        '''return response'''
        return redirect(url_for('showCoffeeshops'))
    else:
        '''For whatever reason, the given token was invalid.'''
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


'''JSON APIs to view Coffeeshop Information'''


@app.route('/coffeeshop/<int:coffeeshop_id>/menu/JSON')
def coffeeshopMenuJSON(coffeeshop_id):
    coffeeshop = session.query(Coffeeshop).filter_by(id=coffeeshop_id).one()
    items = session.query(MenuItem).filter_by(
        coffeeshop_id=coffeeshop_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/coffeeshop/<int:coffeeshop_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(coffeeshop_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/coffeeshop/JSON')
def coffeeshopsJSON():
    coffeeshops = session.query(Coffeeshop).all()
    return jsonify(coffeeshops=[r.serialize for r in coffeeshops])


'''Show all coffeeshops'''


@app.route('/')
@app.route('/coffeeshop/')
def showCoffeeshops():
    coffeeshops = session.query(Coffeeshop).distinct(Coffeeshop.name).group_by(Coffeeshop.name)
    if 'username' not in login_session:
        return render_template('publiccoffeeshops.html',
                               coffeeshops=coffeeshops)
    else:
        return render_template('coffeeshops.html', coffeeshops=coffeeshops)


'''Create a new coffeeshop'''  


@app.route('/coffeeshop/new/', methods=['GET', 'POST'])
@login_required
def newCoffeeshop():
    if request.method == 'POST':
        newCoffeeshop = Coffeeshop(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCoffeeshop)
        flash('New Coffeeshop %s Created Successfully' % newCoffeeshop.name)
        session.commit()
        return redirect(url_for('showCoffeeshops'))
    else:
        return render_template('newCoffeeshop.html')


'''Edit a coffeeshop'''


@app.route('/coffeeshop/<int:coffeeshop_id>/edit/', methods=['GET', 'POST'])
@login_required
def editCoffeeshop(coffeeshop_id):
    editedCoffeeshop = session.query(
        Coffeeshop).filter_by(id=coffeeshop_id).one()
    if editedCoffeeshop.user_id != login_session['user_id']:
        return "<script>function myFunction()" \
               "{alert('You are not authorized to edit this coffeeshop." \
               "Please create your own coffeeshop in order to edit.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedCoffeeshop.name = request.form['name']
            flash('Coffeeshop Successfully Edited %s' % editedCoffeeshop.name)
            return redirect(url_for('showCoffeeshops'))
    else:
        return render_template('editCoffeeshop.html',
                               coffeeshop=editedCoffeeshop)


'''Delete a coffeeshop'''


@app.route('/coffeeshop/<int:coffeeshop_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCoffeeshop(coffeeshop_id):
    coffeeshopToDelete = session.query(
        Coffeeshop).filter_by(id=coffeeshop_id).one()
    if coffeeshopToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction()" \
               "{alert('You are not authorized to delete this coffeeshop." \
               "Please create your own coffeeshop in order to delete.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(coffeeshopToDelete)
        flash('%s Successfully Deleted' % coffeeshopToDelete.name)
        session.commit()
        return redirect(url_for('showCoffeeshops',
                                coffeeshop_id=coffeeshop_id))
    else:
        return render_template('deleteCoffeeshop.html',
                               coffeeshop=coffeeshopToDelete)


'''Show a coffeeshop menu'''


@app.route('/coffeeshop/<int:coffeeshop_id>/')
@app.route('/coffeeshop/<int:coffeeshop_id>/menu/')
def showMenu(coffeeshop_id):
    coffeeshop = session.query(Coffeeshop).filter_by(id=coffeeshop_id).one()
    creator = getUserInfo(coffeeshop.user_id)
    items = session.query(MenuItem).filter_by(
        coffeeshop_id=coffeeshop_id).all()
    if 'username' not in login_session or \
       creator.id != login_session.get('user_id'):
        return render_template('publicmenu.html', items=items,
                               coffeeshop=coffeeshop, creator=creator)
    else:
        return render_template('menu.html', items=items,
                               coffeeshop=coffeeshop, creator=creator)


'''Create new menu item'''


@app.route('/coffeeshop/<int:coffeeshop_id>/menu/new/',
           methods=['GET', 'POST'])
@login_required
def newMenuItem(coffeeshop_id):
    coffeeshop = session.query(Coffeeshop).filter_by(id=coffeeshop_id).one()
    if login_session['user_id'] != coffeeshop.user_id:
        return "<script>function myFunction()" \
               "{alert('You are not authorized to add menu items to this" \
               "coffeeshop. Please create your own coffeeshop in order to" \
               "add items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
                           description=request.form['description'],
                           price=request.form['price'],
                           picture=request.form['picture'],
                           variety=request.form['variety'],
                           coffeeshop_id=coffeeshop_id,
                           user_id=coffeeshop.user_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', coffeeshop_id=coffeeshop_id))
    else:
        return render_template('newmenuitem.html', coffeeshop_id=coffeeshop_id)


'''Edit menu item'''


@app.route('/coffeeshop/<int:coffeeshop_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editMenuItem(coffeeshop_id, menu_id):
    editItem = session.query(MenuItem).filter_by(id=menu_id).one()
    coffeeshop = session.query(Coffeeshop).filter_by(id=coffeeshop_id).one()
    if login_session['user_id'] != coffeeshop.user_id:
        return "<script>function myFunction()" \
               "{alert('You are not authorized to edit menu items to this" \
               "coffeeshop. Please create your own coffeeshop in order to" \
               "edit items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['price']:
            editItem.price = request.form['price']
        if request.form['picture']:
            editItem.picture = request.form['picture']
        if request.form['variety']:
            editItem.variety = request.form['variety']
        session.add(editItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu',
                                coffeeshop_id=coffeeshop_id))
    else:
        return render_template('editmenuitem.html',
                               coffeeshop_id=coffeeshop_id,
                               menu_id=menu_id, item=editItem)


'''Delete menu item'''


@app.route('/coffeeshop/<int:coffeeshop_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteMenuItem(coffeeshop_id, menu_id):
    coffeeshop = session.query(Coffeeshop).filter_by(id=coffeeshop_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if login_session['user_id'] != coffeeshop.user_id:
        return "<script>function myFunction()" \
               "{alert('You are not authorized to delete menu items to this" \
               "coffeeshop. Please create your own coffeeshop in order to" \
               "delete items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', coffeeshop_id=coffeeshop_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)


'''Disconnect based on provider'''


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            login_session.clear()
            flash("You have successfully been logged out.")
            return redirect(url_for('showCoffeeshops'))
        else:
            flash("You were not logged in")
            return redirect(url_for('showCoffeeshops'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

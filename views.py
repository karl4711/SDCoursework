import httpcodes
import json
from services import *
from framework import app, _login_required, base_troops, base_items, base_specialisms
from flask import request, Blueprint,render_template, redirect, g, send_from_directory, session, abort, url_for, jsonify
from pdb import set_trace

views = Blueprint('views', __name__,
                        template_folder = 'templates',
                        static_folder = 'static')

@views.route('/', methods=['GET'])
def welcome_page():
    return app.send_static_file('index.html'), httpcodes.OK

@views.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html'), httpcodes.OK
    if request.method == 'POST':
        app.logger.warn('login')
        username = request.form['username']
        user = query_user(username)
        if not user:
            return render_template('login.html', username = username, username_error = True)
        if not user[1] == request.form['password']:
            return render_template('login.html', username = username, password_error = True)
        session["current_user"] = username
        # {
        #         "username" : username,
        #     }
        return redirect(url_for('views.bandlist',username = username))

@views.route('/logout', methods=['GET'])
def logout():
    session.pop('current_user',None)
    return redirect(url_for("views.login"))


def sumband(createdband):
    total = 0;
    for item in createdband['Captain']['Items']:
        total = total + app.cost[item]
    if 'Ensign' in createdband.keys():
        total = total + 250
        for item in   createdband['Captain']['Items']:
            total = total + app.cost[item]
    for troop in createdband['Troops']:
        total = total + app.troops[troop]['Cost']
    return total

def validate_band(createdband):
    ''' Need to write the validation '''
    return True

def validate_band(oldband,newband):
    return True

@views.route('/new', methods=['GET','POST'])
@_login_required
def new_warband():
    result = {}
    if request.method == 'GET':
        print base_items
        return render_template('editband.html', troops=base_troops, specialisms = base_specialisms, items = base_items, band=None, captain=None, ensign=None, username=session["current_user"]), httpcodes.OK
    if request.method == 'POST':
        band = eval(request.form['band'])
        exist_band = query_band(band["name"])

        if len(exist_band)>0:
            result["reason"] = "Band name has been used!"
            return jsonify(result = result)

        captain = eval(request.form['captain'])
        ensign = eval(request.form['ensign'])

        captain_id = insert_member(captain,"captain")
        ensign_id = 0
        if len(ensign) > 0:
          ensign_id = insert_member(ensign,"ensign")

        band["username"] = session["current_user"]
        band["captainId"] = captain_id
        band["ensignId"] = ensign_id
        
        insert_result = insert_band(band)
        if insert_result > 0:
          result["success"] = True
          result["url"] = url_for("views.bandlist",username=session["current_user"])

        return jsonify(result = result)


@views.route('/bandlist/<username>', methods=['GET'])
@_login_required
def bandlist(username):
    if session['current_user'] != username:
        abort(401)
    own_bands = query_own_band_list(username)
    others_bands = query_others_band_list(username)

    return render_template('bandlist.html', own_bands=own_bands, others_bands=others_bands, username=username), httpcodes.OK


@views.route('/update_public', methods=['POST'])
@_login_required
def update_public():
    band_name = request.form['band_name']
    is_public = request.form['is_public']

    result = update_public_status(band_name, is_public)

    return jsonify(result = result)


@views.route('/edit/<band>', methods=['GET','POST'])
@_login_required
def edit_warband(band):
    if request.method == 'GET':
        band, captain, ensign = query_band_detail(band)
        if not band["username"] == session["current_user"] :
            abort(401);
        return render_template('editband.html', troops=base_troops, specialisms = base_specialisms, items = base_items, band=band, captain=captain, ensign=ensign, username=session["current_user"]), httpcodes.OK

    if request.method == 'POST':
        result = {}

        band = eval(request.form['band'])
        captain = eval(request.form['captain'])
        ensign = eval(request.form['ensign'])

        update_result = 1

        update_result *= update_band(band)
        update_result *= update_member(captain,band["captainId"])
        if len(ensign) > 0:
          update_result *= update_member(ensign,band["ensignId"])

        if update_result == 1:
          result["success"] = True

        return jsonify(result = result)

@views.route('/look/<band>', methods=['GET'])
@_login_required
def look_warband(band):
    band, captain, ensign = query_band_detail(band)
    return render_template('editband.html', troops=base_troops, specialisms = base_specialisms, items = base_items, band=band, captain=captain, ensign=ensign, username=session["current_user"], look=True), httpcodes.OK


@views.route('/delete/<band>', methods=['GET'])
@_login_required
def delete_given_warband(band):
    os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands",band))
    if os.path.isdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands")):
       bands = os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands"))
    else:
       os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands"))
       bands = None
    if request.method == 'GET':
       return render_template('bandlist.html', bands=bands), httpcodes.OK


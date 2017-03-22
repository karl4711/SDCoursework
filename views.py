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

    if request.method == 'GET':
        print base_items
        return render_template('blankband.html', troops=base_troops, specialisms = base_specialisms, items = base_items, band=None, captain=None, ensign=None), httpcodes.OK
    if request.method == 'POST':
      #TODO DEAL WITH JSON
        set_trace()
        print request

        return "ok"


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
def edit_given_warband(band):

    loadedband = pickle.load(open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands"),band), "rb"))
    if request.method == 'GET':
       return render_template('editband.html', band=loadedband,  people=app.troops, wizard=app.wizard, apprentice=app.apprentice, specs = app.specialisms, skills = app.skillsets, weaps = app.weapon), httpcodes.OK
    if request.method == 'POST':
       
       bandname = request.form['bandname']
       capspec = request.form['capspec']
       #capskill = request.form['capskill']
       skills = json.loads(request.form['capskill'])
       capweap = request.form['capweap']
       troops = json.loads(request.form['troops'])
       capmov = request.form['capmove']
       capfig = request.form['capfight']
       capsho = request.form['capshoot']
       capshi = request.form['capshield']
       capmor = request.form['capmorale']
       caphea = request.form['caphealth']
       capexp = request.form['capexperience']
       createdband = dict()
       createdband['Name'] = bandname
       createdband['Captain'] = dict(app.wizard['Captain'])
       createdband['Captain']['Specialism'] = capspec
       createdband['Captain']['Skillset'].extend(skills)
       createdband['Captain']['Items'].append(capweap)
       createdband['Captain']['Move'] = capmov
       createdband['Captain']['Fight'] = capfig
       createdband['Captain']['Shoot'] = capsho
       createdband['Captain']['Shield'] = capshi
       createdband['Captain']['Morale'] = capmor
       createdband['Captain']['Health'] = caphea
       createdband['Captain']['Experience'] = capexp
       if 'hasensign' in request.form.keys():

           ensspec = request.form['ensspec']
           #ensskill = request.form['ensskill']
           eskills = json.loads(request.form['ensskill'])
           ensmov = request.form['ensmove']
           ensfig = request.form['ensfight']
           enssho = request.form['ensshoot']
           ensshi = request.form['ensshield']
           ensmor = request.form['ensmorale']
           enshea = request.form['enshealth']
           ensexp = request.form['ensexperience']
           ensweap = request.form['ensweap']
           createdband['Ensign'] = dict(app.apprentice['Ensign'])
           createdband['Ensign']['Specialism'] = ensspec
           createdband['Ensign']['Skillset'].extend(eskills)
           createdband['Ensign']['Items'].append(ensweap)
           createdband['Ensign']['Move'] = ensmov 
           createdband['Ensign']['Fight'] = ensfig
           createdband['Ensign']['Shoot'] = enssho 
           createdband['Ensign']['Shield'] = ensshi 
           createdband['Ensign']['Morale'] = ensmor 
           createdband['Ensign']['Health'] = enshea 
           createdband['Ensign']['Experience'] = ensexp 
       createdband['Troops'] = []
       for item in troops:
           if item != "Empty":
              createdband['Troops'].append(item)
       if len(createdband['Troops']) > 9 :
           return render_template('blankband.html', people=app.troops, wizard=app.wizard, apprentice=app.apprentice, specs = app.specialisms, skills = app.skillsets, weaps = app.weapon), httpcodes.OK
       if validate_band(loadedband,createdband):
           createdband['Treasury'] = 500 - sumband(createdband)
           pickle.dump(createdband, open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands"),bandname), "wb"))
           return render_template('editband.html', band=createdband, people=app.troops, wizard=app.wizard, apprentice=app.apprentice, specs = app.specialisms, skills = app.skillsets, weaps = app.weapon),httpcodes.OK
       else:
           return render_template('editband.html', band=loadedband,  people=app.troops, wizard=app.wizard, apprentice=app.apprentice, specs = app.specialisms, skills = app.skillsets, weaps = app.weapon), httpcodes.BAD_REQUEST

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


from utilities import *
from pdb import set_trace

def query_troops():
	"""
	query all troops
	"""
	sql = "SELECT * FROM TROOPS"
	res = execute_query(sql)
	
	troops = dict()
	for r in res:
		troops[r[0]] = {'move':r[1], 'fight':r[2], 'shoot':r[3], 'shield':r[4], 'morale':r[5], 'health':r[6], 'cost':r[7], 'notes':r[8]}

	return troops

def query_user(username):
	"""
	query a user
	"""
	sql = "SELECT * FROM USERS WHERE USERNAME = ?"
	params = (username, )

	res = execute_query(sql, params)

	return res[0]


def query_items():
	"""
	query all items
	"""
	sql = "SELECT * FROM ITEMS"
	res = execute_query(sql)
	
	items = dict()
	for r in res:
		items[r[0]] = {'type':r[1], 'cost':r[2]}

	return items

def query_specialisms():
	"""
	query all specialisms and corresponding skills
	"""
	sql = "SELECT * FROM SPECIALISMS"
	res = execute_query(sql)
	
	specialisms = dict()
	for r in res:
		specialisms[r[0]] = [r[1],r[2],r[3]]

	return specialisms

def query_own_band_list(username):
	"""
	query the player's own band list
	"""
	sql = "SELECT NAME,PUBLIC FROM BANDS WHERE USERNAME = ?"
	params = (username,)
	res = execute_query(sql, params)
	return res


def query_others_band_list(username):
	"""
	query others band list except the player's
	"""
	sql = "SELECT NAME,USERNAME FROM BANDS WHERE USERNAME != ? AND PUBLIC = 1"
	params = (username,)
	res = execute_query(sql, params)
	return res

def query_band(name):
	"""
	query a band
	"""
	band_sql = "SELECT * FROM BANDS WHERE NAME = ?"
	band_params = (name,)
	band_res = execute_query(band_sql, band_params)
	return band_res

def query_band_detail(name):
	"""
	query the detail of a band , including data bout the captain and ensign
	"""
	band_sql = "SELECT * FROM BANDS WHERE NAME = ?"
	band_params = (name,)
	band_results = execute_query(band_sql, band_params)
	band_res = band_results[0]

	band = {'name':band_res[0], 'username':band_res[1], 'public':band_res[2], 'captainId':band_res[3], 'ensignId':band_res[4], 'currency':band_res[5], 'soldiers':eval(band_res[6])}

	captain_sql = "SELECT * FROM MEMBERS WHERE ID = ?"
	captain_params = (band["captainId"],)
	captain_results = execute_query(captain_sql, captain_params)
	captain_res = captain_results[0]

	captain = {'move':captain_res[2], 'fight':captain_res[3], 'shoot':captain_res[4], 'shield':captain_res[5], 'morale':captain_res[6], 'health':captain_res[7], 'specialism':captain_res[8], 'skills':eval(captain_res[9]), 'experience':captain_res[10], 'weapons':captain_res[11], 'items':captain_res[12]}

	ensign = None
	if not band['ensignId'] == 0: 
		ensign_sql = "SELECT * FROM MEMBERS WHERE ID = ?"
		ensign_params = (band["ensignId"],)
		ensign_results = execute_query(ensign_sql, ensign_params)
		ensign_res = ensign_results[0]

		ensign = {'move':ensign_res[2], 'fight':ensign_res[3], 'shoot':ensign_res[4], 'shield':ensign_res[5], 'morale':ensign_res[6], 'health':ensign_res[7], 'specialism':ensign_res[8], 'skills':eval(ensign_res[9]), 'experience':ensign_res[10], 'weapons':ensign_res[11], 'items':ensign_res[12]}

	return band, captain, ensign


def update_public_status(band_name, public_status):
	"""
	update the is_public status of a band
	"""
	sql = "UPDATE BANDS SET PUBLIC = ? WHERE NAME = ?"
	params = (public_status, band_name)

	result = execute_update(sql, params)
	return result


def insert_member(member, type):
	"""
	insert a new member(captain or ensign)
	"""
	sql = "INSERT INTO MEMBERS (TYPE, MOVE, FIGHT, SHOOT, SHIELD, MORALE, HEALTH, SPECIALISM, SKILLS, WEAPONS, ITEMS) VALUES(?,?,?,?,?,?,?,?,?,?,?)"
	params = (type, member["move"],member["fight"],member["shoot"],member["shield"],member["morale"],member["health"],member["specialism"],str(member["skills"]),member["weapons"],member["items"])

	return execute_insert(sql, params)


def insert_band(band):
	"""
	insert a new band
	"""
	sql = "INSERT INTO BANDS VALUES(?,?,?,?,?,?,?)"
	params = (band["name"], band["username"], 0, band["captainId"], band["ensignId"], band["currency"], str(band["soldiers"]))

	return execute_insert(sql, params)


def update_member(member,id):
	"""
	update an existing member
	"""
	sql = "UPDATE MEMBERS SET MOVE=?,FIGHT=?,SHOOT=?,SHIELD=?,MORALE=?,HEALTH=?,SPECIALISM=?,SKILLS=?,EXPERIENCE=?,WEAPONS=?,ITEMS=? WHERE ID=?"
	params = (member["move"],member["fight"],member["shoot"],member["shield"],member["morale"],member["health"],member["specialism"],str(member["skills"]),member["experience"],member["weapons"],member["items"],id)

	return execute_update(sql, params)

def update_band(band):
	"""
	update an existing band
	"""
	sql = "UPDATE BANDS SET CURRENCY=?,SOLDIERS=? WHERE NAME = ?"
	params = (band["currency"], str(band["soldiers"]), band["name"])

	return execute_update(sql, params)


def delete_band(band):
	"""
	delete a band
	"""
	band_res = execute_query("SELECT * FROM BANDS WHERE NAME = ?", (band,))

	captain_id = band_res[0][3]
	ensign_id = band_res[0][4]

	delete_member_res = execute_update("DELETE FROM MEMBERS WHERE ID=? or ID=?",(captain_id,ensign_id))
	if delete_member_res == 0:
		return 0
	else:
		return execute_update("DELETE FROM BANDS WHERE NAME=?",(band,))




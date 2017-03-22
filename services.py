from utilities import *

def query_troops():
	sql = "SELECT * FROM TROOPS"
	res = execute_query(sql)
	
	troops = dict()
	for r in res:
		troops[r[0]] = {'move':r[1], 'fight':r[2], 'shoot':r[3], 'shield':r[4], 'morale':r[5], 'health':r[6], 'cost':r[7], 'notes':r[8]}

	return troops

def query_user(username):
	sql = "SELECT * FROM USERS WHERE USERNAME = ?"
	params = (username, )

	res = execute_query(sql, params)

	return res[0]


def query_items():
	sql = "SELECT * FROM ITEMS"
	res = execute_query(sql)
	
	items = dict()
	for r in res:
		items[r[0]] = {'type':r[1], 'cost':r[2]}

	return items

def query_specialisms():
	sql = "SELECT * FROM SPECIALISMS"
	res = execute_query(sql)
	
	specialisms = dict()
	for r in res:
		specialisms[r[0]] = [r[1],r[2],r[3]]

	return specialisms


def query_own_band_list(username):
	sql = "SELECT NAME,PUBLIC FROM BANDS WHERE USERNAME = ?"
	params = (username,)
	res = execute_query(sql, params)
	return res


def query_others_band_list(username):
	sql = "SELECT NAME,USERNAME FROM BANDS WHERE USERNAME != ? AND PUBLIC = 1"
	params = (username,)
	res = execute_query(sql, params)
	return res

def query_band(name):
	band_sql = "SELECT * FROM BANDS WHERE NAME = ?"
	band_params = (name,)
	band_res = execute_query(band_sql, band_params)

	band = {'name':band_res[1], 'username':band_res[2], 'public':band_res[3], 'captainId':band_res[4], 'ensignId':band_res[5], 'currency':band_res[6], 'soldiers':eval(band_res[7])}

	captain_sql = "SELECT * FROM MEMBERS WHERE ID = ?"
	captain_params = (band["captainId"],)
	captain_res = execute_query(captain_sql, captain_params)

	captain = {'move':captain_res[2], 'fight':captain_res[3], 'shoot':captain_res[4], 'shield':captain_res[5], 'morale':captain_res[6], 'health':captain_res[7], 'specialism':captain_res[8], 'skills':eval(captain_res[9]), 'experience':captain_res[10], 'weapons':eval(captain_res[11]), 'items':eval(captain_res[12])}

	ensign = None
	if not band[4] == 0: 
		ensign_sql = "SELECT * FROM MEMBERS WHERE ID = ?"
		ensign_params = (band["ensignId"],)
		ensign_res = execute_query(ensign_sql, ensign_params)

		ensign = {'move':ensign_res[2], 'fight':ensign_res[3], 'shoot':ensign_res[4], 'shield':ensign_res[5], 'morale':ensign_res[6], 'health':ensign_res[7], 'specialism':ensign_res[8], 'skills':eval(ensign_res[9]), 'experience':ensign_res[10], 'weapons':eval(ensign_res[11]), 'items':eval(ensign_res[12])}

	return band, captain, ensign


def update_public_status(band_name, public_status):
	sql = "UPDATE BANDS SET PUBLIC = ? WHERE NAME = ?"
	params = (public_status, band_name)

	result = execute_update(sql, params)
	return result

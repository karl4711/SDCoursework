import sqlite3
import configs


# -------------------
# database operation utilities
# -------------------

def execute_query(sql, param = None):
	"""
	execute query sql, return the query result
	"""
	try:
		conn = sqlite3.connect(configs.SQLITE_FILE)
		if param == None:
			cu = conn.execute(sql)
		else:
			cu = conn.execute(sql, param)
		res = cu.fetchall()
		return res
	except Exception, e:
		print e
		return None
	finally:
		if conn is not None:
			conn.close()

def execute_update(sql, param = None):
	"""
	execute update sql, return the total changes
	"""
	try:
		conn = sqlite3.connect(configs.SQLITE_FILE)
		if param == None:
			conn.execute(sql)
		else:
			if not type(param) == tuple:
				param = tuple(param)
			conn.execute(sql, param)
		conn.commit()
		return conn.total_changes
	except Exception, e:
		print e
		return 0
	finally:
		if conn is not None:
			conn.close()


def execute_insert(sql, param = None):
	"""
	execute the insert sql, return the lastrowid
	"""
	try:
		conn = sqlite3.connect(configs.SQLITE_FILE)
		cursor=conn.cursor()
		if param == None:
			cursor.execute(sql)
		else:
			if not type(param) == tuple:
				param = tuple(param)
			cursor.execute(sql, param)
		conn.commit()
		return cursor.lastrowid
	except Exception, e:
		print e
		return 0
	finally:
		if conn is not None:
			conn.close()
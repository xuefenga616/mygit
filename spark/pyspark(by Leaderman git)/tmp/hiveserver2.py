import logging
import traceback
import pyhs2

class HiveServer2Client(object):

	def __init__(self, host, port, user, passwd, db):
		self._host = host
		self._port = port
		self._user = user
		self._passwd = passwd
		self._db = db

		self._conn = pyhs2.connect(host = self._host, port = self._port, authMechanism = "PLAIN", user = self._user, password = self._passwd, database = self._db)

		self._cur = self._conn.cursor()
	
	def execute(self, sql):
		if sql:
			self._cur.execute(sql)
	
	def getTableColumns(self, table):
		self._cur.execute("show columns in " + table)

		return [cols[0] for cols in self._cur.fetch()]

	def getTableLocation(self, table):
		self._cur.execute("desc formatted " + table)

		return [cols[1] for cols in self._cur.fetch() if cols[0].strip() == "Location:"][0]

	def getPartitions(self, table):
		self._cur.execute("show partitions " + table)

		return [cols[0] for cols in self._cur.fetch()]

	def isExistedPartition(self, table, partition):
		return "log_dir=" + partition in self.getPartitions(table)

	def dropPartitionIfExisted(self, table, partition):
		self._cur.execute("alter table " + table + " drop if exists partition (log_dir = " + partition + ")")

	def close(self):
		if self._cur:
			try:
				self._cur.close()
			except Exception:
				pass
		
		if self._conn:
			try:
				self._conn.close()
			except Exception:
				pass
			

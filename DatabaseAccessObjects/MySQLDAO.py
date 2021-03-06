import MySQLdb as msq
import MySQLdb.cursors


class BaseDAO:
    """
    Base data access object.
    Inherited by all classes that need to access the mysql database. For data analysis tasks, use pandas and sql alchemy

    Attributes:
        db: The mysql connection
        dbc: The mysql cursor
        cnt: Count of rows affected (default None)
        query: Query string to run
        val: Array holding the values to insert into query
        vals: Array alias for val
        results: List of dictionaries holding results of query
        status: String of the format 'connected to: %s' % databaseName
        test: DEPRECATED legacy string
        local: DEPRECATED legacy string
    """

    def __init__(self, credentials, test=False, local=False):
        """
        Args:
            test: No longer used; still here for legacy code
            local: No longer used; still here for legacy code
        """
        self.credentials = credentials
        self.test = test
        self.local = local
        self.mysqlError = MySQLdb.Error
        self.cnt = None
        self.query = ""
        self.val = []
        self.vals = []
        self.results = []
        self.status = "Not connected"

    def connect(self, credentials):
        """
        Loads in a credential object for connecting to db

        Arguments:
            credentials: SQL_Credentials.Credentials
        """
        try:
            self.db = msq.connect(credentials.host(),
                                  credentials.username(),
                                  credentials.password(),
                                  credentials.database(),
                                  cursorclass=MySQLdb.cursors.DictCursor)
            self.db.autocommit(True)
            self.dbc = self.db.cursor()
            self.status = 'Connected to: %s' % credentials.database()
        except MySQLdb.Error as e:
            print "Connection error : %s" % e
            raise

    def executeQuery(self):
        """
        Prepares and executes the query stored in self.query with the variables in self.val
        Usually used for insert, update, and other functions which don't require a return
        """
        try:
            # self.checkValName()
            self.dbc.execute(self.query, self.val)
            self.cnt = self.dbc.rowcount
        except MySQLdb.Error as e:
            print "Query failed: %s" % e

    def returnOne(self):
        """
        Executes the query stored in self.query with the vals in self.val.
        Returns the first row in an array called self.results
        """
        try:
            # self.checkValName()
            self.dbc.execute(self.query, self.val)
            self.results = self.dbc.fetchone()
        except MySQLdb.Error, e:
            print "Query failed: %s " % e

    # raise

    def returnAll(self):
        """
        Executes the query stored in self.query with the vals in self.val.
        Return the results in an array called self.results
        """
        try:
            # self.checkValName()
            self.dbc.execute(self.query, self.val)
            self.results = self.dbc.fetchall()
        except MySQLdb.Error as e:
            print "Query failed: %s " % e
            raise

    def checkValName(self):
        """
        Since I sometimes may use self.val and othertimes use self.vals, this will check which is used and proceed appropriately
        """
        valLength = len(self.val)
        if valLength == 0:
            try:
                valsLength = len(self.val)
                if valsLength == 0:
                    self.val = self.vals
            except Exception:
                print "No value set"

    def returnInsertID(self):
        """
        Returns the id of the last insert statement. Also sets self.insertedid with this value
        """
        try:
            return self.db.insert_id()
        except MySQLdb.Error as e:
            print "Error getting insert id %s " % e
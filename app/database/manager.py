import databases
import sqlalchemy

class DatabaseManager:
    def __init__(self, DATABASE_URL):
        self.database = databases.Database(DATABASE_URL)
        self.metadata = sqlalchemy.MetaData()

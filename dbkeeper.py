from . import mysqlite
from datetime import datetime


class DBKeeper:

    def __init__(self, folder_path: str):
        """
        Stock Split Database Keeper manage the dividend data.
        Keeper will save the .db in the folder_path.
        """
        self.db_path = folder_path + "/stocksplit.db"
        self.__initialize()

    def update(self, symbol: str, data: dict, skipUpdated: bool = True):
        """
        Update the stock split data to database.
        If skipUpdated is True, keeper will skip the symbol had been updated today.
        """
        # create table if not exists
        if not symbol in self.mastertb:
            # duoble check
            self.mastertb = self.master.query()
            if not symbol in self.mastertb:
                self.__create_stocksplit_table(symbol)
        self.tb = self.db.TB(symbol)
        # skip if updated
        today = self.__get_today()
        self.config = self.master.query(
            "*", 'WHERE table_name = "{}"'.format(symbol))
        lastupdate = self.config[symbol]["last_update"]
        if skipUpdated == True and today == lastupdate:
            return
        # insert new data
        updates = {}
        last_date = self.config[symbol]["last_date"]
        for date in data:
            if date > last_date:
                updates[date] = data[date]
        self.tb.update(updates)
        # update lastupdate
        self.config[symbol]["last_update"] = today
        if self.config[symbol]["first_date"] == 0:
            self.config[symbol]["first_date"] = min(list(data.keys()))
        self.config[symbol]["last_date"] = max(list(data.keys()))
        if self.config[symbol]["data_points"] == 0:
            self.config[symbol]["data_points"] = len(data)
        else:
            self.config[symbol]["data_points"] += len(updates)
        self.master.update(self.config)
        self.db.commit()

    def query_stocksplit(self, symbol: str) -> dict:
        """
        1:5 | 5 shares -> 1 share | origin price x (1 / 5)
        5:1 | 1 share -> 5 shares | origin price x (5 / 1)
        """
        if not symbol in self.mastertb:
            # duoble check
            self.mastertb = self.master.query()
            if not symbol in self.mastertb:
                return False
        self.tb = self.db.TB(symbol)
        query = self.tb.query()
        return query

    def query_master_info(self, symbol: str) -> dict:
        if not symbol in self.mastertb:
            # duoble check
            self.mastertb = self.master.query()
            if not symbol in self.mastertb:
                return False
        info = self.mastertb[symbol]
        return info

    def query_full_master_info(self) -> dict:
        self.mastertb = self.master.query()
        return self.mastertb

    def __initialize(self):
        self.db = mysqlite.DB(self.db_path)
        if not "master" in self.db.listTB():
            self.master = self.db.createTB("master", "table_name", "CHAR(100)")
            self.master.addCol("last_update", "INT")
            self.master.addCol("first_date", "INT")
            self.master.addCol("last_date", "INT")
            self.master.addCol("data_points", "INT")
        else:
            self.master = self.db.TB("master")
        self.mastertb = self.master.query()

    def __create_stocksplit_table(self, symbol: str):
        self.tb = self.db.createTB(symbol, "date", "INT")
        self.tb.addCol("stocksplit", "CHAR(30)")
        self.master.update({
            symbol: {
                "last_update": 0,
                "first_date": 0,
                "last_date": 0,
                "data_points": 0
            }})
        self.db.commit()

    def __get_today(self) -> int:
        now = datetime.now()
        now = datetime(now.year, now.month, now.day)
        return int(now.timestamp())

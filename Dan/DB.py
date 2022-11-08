import sqlite3
import datetime
from datetime import timezone


class DB:
    def __init__(self, filename):
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()
        self.db_name = 'user'

        newTable = True
        for row in self.cur.execute("SELECT name FROM sqlite_master"):
            if row == (self.db_name,):
                newTable = False
        if newTable:
            self.cur.execute("CREATE TABLE user(name, school, start, stop)")
            print("New Table Created")
        else:
            print("Table Exists")

    def AddMany(self, size, data, duplicate=False):
        # build SQL command
        string = "INSERT INTO user VALUES("
        for i in range(size - 1):
            string = string + "?, "
        string = string + "?)"

        if (not duplicate):
            indices = []
            for i in range(len(data)):
                if data[i] in self.cur.execute("SELECT name, school, start, stop FROM user"):
                    indices.append(i)

            indices.reverse()
            for i in indices:
                data.remove(data[i])

        self.cur.executemany(string, data)
        self.con.commit()

    def Display(self):
        for row in self.cur.execute("SELECT name, school, start, stop FROM user"):
            print(row)


if __name__ == "__main__":
    myDB = DB("Chronos.db")

    data = [("Jack", "UMBC", 5, 10), ("Joe", "UMBC", 1, 100)]
    myDB.AddMany(len(data[0]), data, True)

    myDB.Display()

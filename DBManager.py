#!/usr/bin/python2
#vim: fileencoding=utf-8
import sqlite3
import datetime

def decorate_with_line(function):
    def wrapper(*args, **kwargs):
        print('-' * 8 + function.__name__ + '-' * 8)
        result = function(*args, **kwargs)
        print('-' * 8 + 'end: ' + function.__name__ + '-' * 8)
        return result

    return wrapper

TABLES = {0: 'user_data', 1: 'todo_data'}

class DBManager():
    @decorate_with_line
    def __init__(self):
        self._user_db_name = 'user_data'
        self._todo_db_name = 'todo_data'

        self._conn = sqlite3.connect('./Todo.db')
        self._cur = self._conn.cursor()

        #create user_data table query
        query = 'create table ' + self._user_db_name
        query = query + '(id integer primary key not null, '
        query = query + 'name text not null, key text not null, '
        query = query + 'secret text not null);'

#         print(query)

        try:
            self._cur.execute(query)
        except Exception as e:
#            raise e
            print(e)

        #create todo_data table query
        query = 'create table ' + self._todo_db_name
        query = query + '(id integer not null, task_id integer not null,'
        query = query + 'classified text,'
        query = query + 'context text not null, rimit text not null)'
#         print(query)

        try:
            self._cur.execute(query)
        except Exception as e:
#            raise e
            print(e)

    """TODO DATA """

    @decorate_with_line
    def insert_todo_data(self, user_id, classified, context, rimit):
        query = 'insert into ' + self._todo_db_name + ' values(?, ?, ?, ?, ?);'
        print(query)

        date = datetime.datetime.today()
        task_id = str(date.year) + str(date.month) + str(date.day)
        task_id = task_id + str(date.hour) + str(date.minute) + str(date.second)
        print('task_id: ' + task_id)
        try:
           self._cur.execute(query, [user_id, task_id, classified, context, rimit])
        except Exception as e:
            print(e)

        self._conn.commit()

    @decorate_with_line
    def find_todo_data(self, user_id):
        query = 'select * from ' + self._todo_db_name
        query = query + ' where id = ' + str(user_id)
        query = query + ' order by rimit;'

        print(query)

        try:
            self._cur.execute(query)
        except Exception as e:
            print(e)

        return self._cur.fetchall()


    @decorate_with_line
    def get_todo_divide_data(self, user_id):
        alldata = self.find_todo_data(user_id)

        nonull=[]
        null=[]
        for d in alldata:
            if d[4]:
                print(d[4])
                nonull.append(d)
            else:
                print('null rimit')
                null.append(d)

#   add dammy
#        dmy = ['', '', '', '', '']
#        dif = len(nonull) - len(null)
#        if dif > 0:
#            for i in range(dif):
#                null.append(dmy)
#        else:
#            for i in range(dif):
#                nonull.append(dmy)


        return { 'nonull': nonull, 'null': null}


    @decorate_with_line
    def delete_todo_data(self, user_id, task_id):
        query = 'delete from ' + self._todo_db_name
        query = query + ' where id = ' + str(user_id) + ' and '
        query = query + 'task_id = ' + str(task_id) + ';'

        print(query)

        try:
            self._cur.execute(query)
        except Exception as e:
            print(e)

        data = self.find_todo_data(user_id)

#        for i, entry in enumerate(data):
#            query = 'update ' + self._todo_db_name
#            query = query + ' set task_id = ' + str(i)
#            query = query + ' where task_id = ' + str(entry[1]) + ';'
#            print(query)

#            try:
#                self._cur.execute(query)
#            except Exception as e:
#                print(e)
        self._conn.commit()


    """USER DATA """

    @decorate_with_line
    def insert_user_data(self, user_id, name, key, secret):
        query = 'insert into ' + self._user_db_name + ' values(?, ?, ?, ?);'

        print(query)
        try:
            self._cur.execute(query,[ user_id, name, key, secret])
        except Exception as e:
            print(e)
        self._conn.commit()


    @decorate_with_line
    def find_user_data(self, user_id):
        query = 'select * from ' +  self._user_db_name
        query = query + ' where id = ' + str(user_id) + ';'

        print(query)

        try:
            self._cur.execute(query)
        except Exception as e:
            print(e)

#        for data in self._cur.fetchall():
#            print(data)
        data = self._cur.fetchall()
        if not data:
            return ()
        else:
            data = data[0]
            dic = {'id':data[0], 'name': data[1], 'key':data[2], 'secret':data[3]}
            return dic


    #TODO: make user delete method

    @decorate_with_line
    def print_data(self, table_name):
        query = 'select * from ' + table_name + ';'
        print(query)

        self._cur.execute(query)
        for data in self._cur.fetchall():
            print(data)

    @decorate_with_line
    def close(self):
        self._conn.commit()
        self._conn.close()


if __name__ == '__main__':

    db = DBManager()
#    db.insert_user_data(1, 'donmai', 'key', 'secret')


#    print(TABLES[0],TABLES[1])
    db.print_data(TABLES[0])
#     db.print_data(TABLES[1])

#    data = db.find_user_data(0)
#    print(data)

#     for a in db.find_todo_data(182691245):
#        print(a)
#    db.insert_todo_data(182691245, 'classified', 'context', 20131231)
#    db.delete_todo_data(182691245, 0)
#     div = db.get_todo_divide_data(182691245)

#     for a in div['nonull']:
#         print(a)
#     print('\n')
#     for a in div['null']:
#         print(a)
#    db.print_data(TABLES[1])
#    db.print_data(TABLES[1])

    db.close()


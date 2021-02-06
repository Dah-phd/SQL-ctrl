import mysql.connector as mc
import pandas
import tkinter as tk


def f_date(date):
    # formats date from investing to MySQL format
    if 'e' in date or 'a' in date or 'o' in date or 'c' in date or 'u' in date or 'p' in date:
        months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
                  'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
        date = date.replace(',', '')
        date = date.lower()
        date = date.split(' ')
        date = date[2]+'-'+months[date[0]]+'-'+date[1]
    elif '/' in date:
        date = date.split('/')
        date = '20'+str(date[2])+'-'+str(date[0])+'-'+str(date[1])
    return date


class DATABASE():
    def __init__(self, name, table, user, passwd):
        self.name = name
        self.table = table
        self.user = user
        self.passwd = passwd
        self.db = mc.connect(
            host='localhost',
            user=str(self.user),
            password=str(self.passwd),
            database=str(self.name)
        )
        self.cursor = self.db.cursor()

    def drop_column(self, data_string):
        # burns the data
        self.cursor.execute(
            f'ALTER TABLE {self.table} DROP COLUMN {data_string}'
        )
        print(data_string, ' dropped!')

    def create_table(self):
        self.cursor.execute(
            f'CREATE TABLE {self.table} (date_ DATE, PRIMARY KEY(date_))'
        )
        print(f'{self.table} was created!')

    def drop_table(self):
        self.cursor.execute(
            f'DROP TABLE {self.table}'
        )
        print('Table destroyed!')

    def name_bases(self):
        self.cursor.execute('SHOW DATABASES')
        result = []
        for t in self.cursor:
            result.append(t[0])
            print(t[0])
        return result

    def freeze(self):
        self.cursor.execute('SHOW TABLES')
        result = []
        for t in self.cursor:
            result.append(t[0])
            print(t[0])
        return result

    def freeze_tab(self):
        self.cursor.execute(f'DESC {self.table}')
        result = []
        for t in self.cursor:
            result.append(t[0])
            print(t[0])
        return result

    def q_all(self, print_=0):
        self.cursor.execute(
            f'SELECT * FROM {self.table}'
        )
        if print_ != 0:
            for t in self.cursor:
                print(t)
        else:
            quarry = [t for t in self.cursor]
            return quarry

    def fix_dates(self, date, table):
        # function that lightens the check of the dates it will stop as soon as eq is reached
        for t in table:
            if str(t[0]) == date:
                return
        self.cursor.execute(
            "INSERT INTO " + self.table + " (date_) VALUES (%s)", (date,))

    def import_csv(self, data_string):
        # data string is the location of the csv from witch to import
        name = data_string.split('.')
        name = name[-2]
        name = name.split('/')
        name = name[-1]
        # MAKE THAT PRETTY
        try:
            self.cursor.execute(
                f'ALTER TABLE {self.table} ADD {name} float'
            )
            print('ADDING column')
        except:
            print('CORRECTING/ADDING to existing entry')
        data_frame = pandas.read_csv(data_string)
        df_str = [t for t in data_frame]
        dates = [f_date(t) for t in data_frame[df_str[0]]]
        val = [(data_frame[df_str[1]][x], t)
               for x, t in enumerate(dates)]
        self.cursor.execute(f'SELECT date_ FROM {self.table}')
        temp = [t for t in self.cursor]
        for t in dates:
            self.fix_dates(t, temp)
        self.cursor.executemany(
            "UPDATE " + self.table +
            " SET " + name + " = (%s) WHERE date_ = (%s)", val
        )
        self.db.commit()

    def check_data(self):
        tabs = self.freeze_tab()
        tabs.pop(0)
        for t in tabs:
            print('Checking column: ', t)
            self.cursor.execute(
                "SELECT date_, " + t +
                " FROM " + self.table
            )
            n_val = 0
            column = [t for t in self.cursor]
            for t1 in column:
                if not t1[1]:
                    print('For date: ', t1[0], '\n The value is: None')
                    self.cursor.execute(
                        "UPDATE " + self.table +
                        " SET " + t + " = (%s) WHERE date_ = (%s)",
                        (n_val, t1[0])
                    )
                    print('REPLACED WITH PREVIOUS: ', n_val)
                    self.db.commit()
                else:
                    n_val = t1[1]
            print(t, ' is checked!')


print(
    "Useful variables:\n", "_initial_name_ = Controler.DATABASE('database','table','user','password') / entry into database \n",
    "_initial_name_.table = table_name / change table \n",
    "_initial_name_.name = database_name / change database in use\n\n",
    "Useful methods:\n", ".freeze() / shows the tables into the database\n",
    ".freeze_tab() / shows the columns into the table (data_) is primery key\n",
    ".import_csv(data_string) / imports data from csv, data_string file location\n",
    "the data should include Date column with dates (investing format) and corresponding values \n",
    "the name of the file is used to name the column\n",
    ".check_data() / checks for missing data points and interpolate them using previous observation \n",
    ".drop_table(data_string) / destroys the column specified into the data_string\n",
    ".q_all(print=0) / if no value is given returns a list with all the date, else it only prints it"

)

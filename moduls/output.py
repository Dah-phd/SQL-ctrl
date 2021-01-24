import pandas

if __name__ == '__main__':
    import datetime
    import Controler


def export_csv(self, name, list=[]):
    if list == '':
        names = self.freeze_tab()
    else:
        names = list.split(',')
        names.insert(0, 'date_')
    self.cursor.execute(f'SELECT * FROM {self.table}')
    data = [t for t in self.cursor]
    df = {}
    for x, t in enumerate(names):
        list = [t[x] for t in data]
        df[t] = list
    df = pandas.DataFrame(df)
    print(df)
    if name != 'File name':
        name = str(name) + '.csv'
    else:
        name = 'export.csv'
    df.to_csv(name, index=False)


def export(self, list=[]):
    if list == '':
        names = self.freeze_tab()
    else:
        names = list.split(',')
        names.insert(0, 'date_')
    self.cursor.execute(f'SELECT * FROM {self.table}')
    data = [t for t in self.cursor]
    df = {}
    for x, t in enumerate(names):
        list = [t[x] for t in data]
        df[t] = list
    df = pandas.DataFrame(df)
    pandas.set_option("display.max_rows", None,
                      "display.max_columns", None)
    return df

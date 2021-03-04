import pandas
import os

if __name__ == '__main__':
    import datetime
    import Controler


def export_csv(self, name, _list=''):
    base = self.freeze_tab()
    if _list == '':
        names = base.copy()
    else:
        names = _list.split(',')
        names.insert(0, 'date_')
    self.cursor.execute(f'SELECT * FROM {self.table}')
    data = [t for t in self.cursor]
    df = {}
    for t in names:
        _list = [t1[base.index(t)] for t1 in data]
        df[t] = _list
    df = pandas.DataFrame(df)
    print(df)
    if name != 'File name':
        name = str(name) + '.csv'
    else:
        name = 'export.csv'
    while os.path.isfile(name):
        if not n:
            n = 0
            name = name[:-4]+str(n)+name[-4:]
            position = 1
        else:
            n += 1
            name = name[:-(4+position)]+str(n)+name[-4:]
            position = len(str(n))
    else:
        df.to_csv(name, index=False)


def export(self, _list=''):
    base = self.freeze_tab()
    if _list == '':
        names = base.copy()
    else:
        names = _list.split(',')
        names.insert(0, 'date_')
    self.cursor.execute(f'SELECT * FROM {self.table}')
    data = [t for t in self.cursor]
    df = {}
    for t in names:
        _list = [t1[base.index(t)] for t1 in data]
        df[t] = _list
    return df

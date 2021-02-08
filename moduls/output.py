import pandas

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
    df = pandas.DataFrame(df)
    pandas.set_option("display.max_rows", None,
                      "display.max_columns", None)
    return df

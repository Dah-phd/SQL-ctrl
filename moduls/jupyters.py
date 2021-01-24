import os


def j_load():
    old_path = os.getcwd()
    path = old_path + '\jupyter'
    if os.path.exists(path):
        os.chdir(path)
    else:
        os.system('md jupyter')
        os.chdir(path)
    os.system('jupyter notebook')
    os.chdir(old_path)


def file_name(path):
    name = 'new_jupyter.ipynb'
    n = 1
    while os.path.exists(path+'/'+name):
        name = 'new_jupyter'+str(n)+'.ipynb'
        n += 1
    return name


def j_nload(self, list=[]):
    columns = "['date_"
    if list == '':
        for t in self.freeze_tab()[1:]:
            columns = columns + '\', \'' + t
        columns = columns + "']"
    else:
        list = list.split(',')
        for t in list:
            columns = columns + '\', \'' + t
        columns = columns + "']"
    print(columns)
    old_path = os.getcwd()
    path = old_path + '\jupyter'
    if os.path.exists(path):
        os.chdir(path)
    else:
        os.system('md jupyter')
        os.chdir(path)
    text = r"""{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas\n",
    "import mysql.connector as mc"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "db = mc.connect(\n",
    "            host='localhost',\n",
    "            user='"""+self.user+r"""',\n",
    "            password='"""+self.passwd+r"""',\n",
    "            database='"""+self.name+r"""')\n",
    "Cursor = db.cursor()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "names = """+columns+r"""\n",
    "Cursor.execute(f'SELECT * FROM """+self.table+r"""')\n",
    "# data contains the full table unstructured (list of tuples)\n",
    "data = [t for t in Cursor]\n",
    "df = {}\n",
    "for x, t in enumerate(names):\n",
    "    list = [t[x] for t in data]\n",
    "    df[t] = list\n",
    "# FULL DATA IS NAMED df\n",
    "df = pandas.DataFrame(df)\n",
    "print(df)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
"""
    print(self.db)
    notebook = file_name(path)
    with open(notebook, 'w') as file:
        file.write(text)
    os.system('jupyter notebook '+notebook)
    os.chdir(old_path)

from moduls import Controler, output, jupyters, mt_dialog
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import ImageTk, Image


### functions ###
def est_conn():
    if e_db.get():
        conn = Controler.DATABASE(e_db.get(), 'root', e_u.get(), e_p.get())
        client_list.append(conn)
        l_scond.configure(text='CONNECTED', fg='green')
        l_db_n1.configure(text=e_db.get(), fg='green')
        dropmenu_table(client_list[-1])
    else:
        conn = Controler.DATABASE('world', 'root', e_u.get(), e_p.get())
        poppers = ['information_schema', 'mysql',
                   'performance_schema', 'sakila', 'sys', 'world']
        list = conn.name_bases()
        for t in poppers:
            list.remove(t)
        text = f'No database is selected! \nSelect one from the following list: {list} \n First will be entered automatically.'
        messagebox.showinfo(title='DATABASES', message=text)
        e_db.insert(0, list[0])


def dropmenu_table(self):
    global l_scond, l_db_n1, table_var
    optinos = [t for t in self.freeze()]
    table_var = tk.StringVar(root)
    t_menu = ttk.Combobox(mod_frame, textvariable=table_var,
                          values=optinos, width=9)
    t_menu.configure(font=myfont)
    table_var.trace('w', select_table)
    t_menu.grid(row=0, column=1)


def dropmenu_columns(self):
    global column_var
    optinos = {t for t in self.freeze_tab()}
    optinos.remove('date_')
    column_var = tk.StringVar(root)
    t_menuc = tk.OptionMenu(export_frame, column_var, *optinos)
    t_menuc.configure(font=myfont, width=10)
    column_var.trace('w', print_columns)
    t_menuc.grid(row=2, column=1)


def conn_check():
    if not e_u.get():
        messagebox.showinfo(
            'USER!', message='No user is connected, you ca use viewer as base!')
    elif not e_db.get():
        messagebox.showinfo(
            'Data base!', message='Data base is not selected!')
    elif not table_var.get():
        messagebox.showinfo(
            'Table!', message='Table is no selected')
    else:
        return True


def select_table(*Dah):
    global table_var, l_table1
    client_list[-1].table = table_var.get()
    l_table1.configure(fg='green', text=table_var.get())
    dropmenu_columns(client_list[-1])


def print_columns(*Dah):
    global column_var, e_columns
    if e_columns.get():
        e_columns.insert('end', ','+column_var.get())
    else:
        e_columns.insert(0, column_var.get())


def create_table():
    client_list[-1].table = c_table.get()
    client_list[-1].create_table()


def explore():
    if conn_check():
        global eimport_csv
        csv = filedialog.askopenfilename(
            initialdir='/',
            title='Open file:',
            filetypes=(('excel', '*.csv'), ('all files', '*.*'))
        )
        eimport_csv.insert(0, csv)


def export_clipboard():
    if conn_check():
        result = output.export(client_list[-1], e_columns.get())
        root.clipboard_clear()
        root.clipboard_append(result)
        messagebox.showinfo(title='Data send!',
                            message='Data has been added to clipboard!')


def datacheck():
    if client_list[-1].table == 'root':
        messagebox.showerror('MISSING TABLE', message='Please select table!')
    else:
        client_list[-1].check_data()
        messagebox.showinfo(
            'Data fixed!', message='Missing data has been filled!')


def delete_table():
    if conn_check():
        sq_check = messagebox.askyesno(
            title='Confirm', message='Confirm data destruction:')
        if sq_check:
            client_list[-1].drop_table()


def delete_column():
    if conn_check():
        columns = client_list[-1].freeze_tab()
        target = mt_dialog.OptionDialog(
            root, 'Select column', 'Select column to delete:', columns)
        client_list[-1].drop_column(target.result)
        print('COLUMN '+target.result+' has been deleted!')


def new_jupyter():
    if conn_check():
        jupyters.j_nload(client_list[-1], list=e_columns.get())


### initialization ###
root = tk.Tk()
root.geometry('800x850')
root.title('SQL mainframe')

### base variables ###
client_list = []
myfont = 'calibri 20'
separater = 'calibri 10 bold'

### defin base widgets ###
conn_frame = tk.Frame(root, bd=4, relief='sunken')
stat_frame = tk.Frame(root, bd=4, relief='sunken', cursor='plus')
mod_frame = tk.Frame(root, bd=4, relief='sunken')
export_frame = tk.Frame(root, bd=4, relief='sunken')
# export frame
exp_title = tk.Label(export_frame, text='Data export', bd=4, bg='gray',
                     font=myfont, relief='raised', padx=130)
e_filename = tk.Entry(export_frame, font=myfont, width=10, bd=4)
e_filename.insert(0, 'File name')
b_exportcsv = tk.Button(export_frame, text='Export csv', font=myfont, bd=4, bg='lightgray',
                        command=lambda: output.export_csv(client_list[-1], e_filename.get(), e_columns.get()))
b_exprotclipboard = tk.Button(export_frame, text='Clipboard', bd=4, bg='lightgray',
                              font=myfont, command=export_clipboard)
l_columns = tk.Label(export_frame, text='COLUMN SELECTION (,)',
                     bd=6, relief='raised', font=separater)
e_columns = tk.Entry(export_frame, font=myfont, width=10, bd=4)
l_jupyter = tk.Label(export_frame, text='JUPYTER NOTEBOOK',
                     bd=6, relief='raised', font=separater)
b_jupyter = tk.Button(export_frame, text='Run in new Jupyter',
                      font=myfont, fg='green', bd=4, bg='lightgray', command=new_jupyter)
b_jupyterload = tk.Button(export_frame, text='View existing Jupyter',
                          font=myfont, fg='green', bd=4, bg='lightgray', command=jupyters.j_load)
# mod frame
mod_title = tk.Label(mod_frame, text='Database modification', bd=4, bg='gray',
                     font=myfont, relief='raised', padx=71)
sel_tl = tk.Label(mod_frame, text='Select table:', font=myfont)
c_table = tk.Entry(mod_frame, font=myfont, text='Talbe name', width=10, bd=4)
c_tableb = tk.Button(mod_frame, font=myfont, bd=4, bg='lightgray',
                     text='Create table', command=create_table)
l_importcsv = tk.Label(mod_frame, text='IMPORT CSV',
                       bd=6, relief='raised', font=separater)
l_global = tk.Label(mod_frame, text='GLOBAL FUNCTIONS',
                    bd=6, relief='raised', font=separater)
check = tk.Button(mod_frame, text='Fill missing data', bd=4, bg='lightgray',
                  fg='green', font=myfont, command=datacheck)
drop_table = tk.Button(mod_frame, fg='red', font=myfont, bg='lightgray',
                       bd=4, text='DELETE TABLE', command=delete_table)
eimport_csv = tk.Entry(mod_frame, font=myfont, width=10, bd=4)
bsimport_csv = tk.Button(mod_frame, font=myfont, bd=4, bg='lightgray',
                         text='Select file', command=explore)
bimport_csv = tk.Button(mod_frame, text='IMPORT FILE', bd=4, bg='lightgray',
                        font=myfont, command=lambda: client_list[-1].import_csv(eimport_csv.get()))
b_coldelete = tk.Button(mod_frame, fg='red', font=myfont, bg='lightgray',
                        bd=4, text='DELETE COLUMN (select)', command=delete_column)
# status frame
l_sname1 = tk.Label(stat_frame, text='CURRENT STATUS',
                    font=myfont, relief='raised', padx=98, pady=9, bd=4, bg='gray')
l_sname2 = tk.Label(stat_frame, text='Connection:', font=myfont)
l_scond = tk.Label(stat_frame, text='AWAIT CONNECTION', fg='red', font=myfont)
l_db_n = tk.Label(stat_frame, text='Database:', font=myfont)
l_table = tk.Label(stat_frame, text='Table:', font=myfont)
l_db_n1 = tk.Label(stat_frame, text='Load database', font=myfont, fg='red')
l_table1 = tk.Label(stat_frame, text='Load table', font=myfont, fg='red')
# conn_frame
l_u = tk.Label(conn_frame, text="*User:", font=myfont)
l_p = tk.Label(conn_frame, text="*Pass:", font=myfont)
l_db = tk.Label(conn_frame, text="Database", font=myfont)
l_status = tk.Label()
b_conn = tk.Button(conn_frame, text='CONNECT', bd=4, bg='lightgray',
                   command=est_conn, font=myfont)
e_u = tk.Entry(conn_frame, font=myfont, bd=4)
e_p = tk.Entry(conn_frame, font=myfont, show='*', bd=4)
e_db = tk.Entry(conn_frame, font=myfont, bd=4)
e_t = tk.Entry(conn_frame, font=myfont, bd=4)

### place them ###
conn_frame.grid(row=0, column=0)
stat_frame.grid(row=0, column=1)
mod_frame.grid(row=1, column=0)
export_frame.grid(row=1, column=1)
# export frame
exp_title.grid(pady=5, row=0, column=0, columnspan=2)
l_columns.grid(pady=5, row=1, column=0, columnspan=2, sticky='EW')
e_columns.grid(pady=5, row=2, column=0)
e_filename.grid(pady=5, row=2, column=0)
b_exportcsv.grid(pady=5, row=3, column=1)
b_exprotclipboard.grid(pady=5, row=3, column=0)
l_jupyter.grid(pady=5, row=4, column=0, columnspan=2, sticky='EW')
b_jupyter.grid(pady=5, row=5, column=0, columnspan=2, sticky='EW')
b_jupyterload.grid(pady=5, row=6, column=0, columnspan=2, sticky='EW')
# mod frame
sel_tl.grid(pady=5, row=0, column=0)
mod_title.grid(pady=5, row=1, column=0, columnspan=2)
c_table.grid(pady=5, row=2, column=0)
c_tableb.grid(pady=5, row=2, column=1)
l_importcsv.grid(pady=5, row=3, column=0, columnspan=2, sticky='EW')
eimport_csv.grid(pady=5, row=4, column=0)
bsimport_csv.grid(pady=5, row=4, column=1)
bimport_csv.grid(pady=5, row=5, column=0, columnspan=2, sticky='EW')
l_global.grid(pady=5, row=80, column=0, columnspan=2, sticky='EW')
b_coldelete.grid(pady=5, row=98, column=0, columnspan=2, sticky='EW')
check.grid(pady=5, row=99, column=0, columnspan=2, sticky='EW')
drop_table.grid(pady=5, row=100, column=0, columnspan=2, sticky='EW')
# stat frame
l_sname1.grid(row=0, column=0, columnspan=2, sticky='NEWS')
l_sname2.grid(row=1, column=0)
l_scond.grid(row=1, column=1)
l_db_n.grid(row=2, column=0)
l_db_n1.grid(row=2, column=1)
l_table.grid(row=3, column=0)
l_table1.grid(row=3, column=1)
# conn frame
l_u.grid(row=0, column=0)
l_p.grid(row=1, column=0)
l_db.grid(row=2, column=0)
b_conn.grid(row=3, column=0, columnspan=2)
e_u.grid(row=0, column=1)
e_p.grid(row=1, column=1)
e_db.grid(row=2, column=1)

### mainloop ###
root.mainloop()

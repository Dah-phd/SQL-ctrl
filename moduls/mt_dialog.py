import tkinter as tk
from tkinter import messagebox


class OptionDialog(tk.Toplevel):
    """
        This dialog accepts a list of options.
        If an option is selected, the results property is to that option value
        If the box is closed, the results property is set to zero
    """

    def __init__(self, parent, title, question, options):
        tk.Toplevel.__init__(self, parent)
        self.title(title)
        self.question = question
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.options = options
        self.result = '_'
        self.createWidgets()
        self.grab_set()
        # wait.window ensures that calling function waits for the window to
        # close before the result is returned.
        self.wait_window()

    def createWidgets(self):
        frmQuestion = tk.Frame(self)
        tk.Label(frmQuestion, text=self.question).grid()
        frmQuestion.grid(row=1)
        frmButtons = tk.Frame(self)
        frmButtons.grid(row=2)
        column = 0
        for option in self.options:
            btn = tk.Button(frmButtons, text=option,
                            command=lambda x=option: self.setOption(x))
            btn.grid(column=column, row=0)
            column += 1

    def setOption(self, optionSelected):
        self.result = optionSelected
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()


if __name__ == '__main__':
    # test the dialog
    root = tk.Tk()

    def run():
        values = ['Red', 'Green', 'Blue', 'Yellow']
        dlg = OptionDialog(root, 'TestDialog', "Select a color", values)
        print(dlg.result)
    tk.Button(root, text='Dialog', command=run).pack()
    root.mainloop()

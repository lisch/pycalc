"""Calculator view and controller.

This module contains the view and controller in an MVC-architecture calculator.

The view is a tk window. The controller is a set of callbacks
to the model.

"""

import tkinter
import model

class StatusBar(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tkinter.Label(self, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
        self.label.pack(fill=tkinter.X)

    def set(self, fmt, *args, **kwargs):
        self.label.config(text=fmt.format(*args, **kwargs))
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
        
class View:
    def __init__(self, configuration, root=None, controller=None):
        self.configuration = configuration
        self.model = model.Calculator()
        self.root = root or tkinter.Tk()
        self.controller = controller or Controller(self, self.model)
        self.current = tkinter.StringVar()
        self.initialize()
        
    def initialize(self):
        """Initialize the view according to the configuration."""
        self.root.wm_title("Calculator")
        outer = tkinter.Frame(self.root)
        outer.bind("<Key>", self.controller.key)

        frame = tkinter.Frame(outer)
        scroll = tkinter.Scrollbar(frame)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        
        self.history = tkinter.Text(frame,
                                    bd=2,
                                    yscrollcommand=scroll.set,
                                    height=4,
                                    width=40,
                                    )
        self.history.pack(expand=True, side=tkinter.LEFT, fill=tkinter.BOTH)
        scroll.config(command=self.history.yview)
        frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)

        self.current_label = tkinter.Label(outer,
                                textvariable=self.current,
                                bd=2,
                                bg=self.history["bg"],
                                font=self.history["font"],
                                relief=tkinter.FLAT,
                                justify=tkinter.RIGHT,
                                )
        self.current_label.pack(expand=True, side=tkinter.TOP, fill=tkinter.X)

        buttons = tkinter.Frame(outer)
        for row in self.configuration.splitlines():
            if not row.strip():
                continue
            row_frame = tkinter.Frame(buttons)
            for label in row.split('|'):
                label = label.strip()
                if not label:
                    continue
                button = tkinter.Button(row_frame,
                                        text=label,
                                        height=3,
                                        width=3,
                                        command=self.controller.command(label))
                button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
            row_frame.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)
        buttons.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)

        self.status = StatusBar(outer)
        self.status.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        outer.pack(expand=True, fill=tkinter.BOTH)

    def all_clear(self):
        self.clear()
        self.history.delete(1.0, tkinter.END)
        
    def clear(self):
        self.current.set('')
        
    def backspace(self):
        self.current.set(self.text[ : -1 ])
        
    def insert(self, text):
        self.set_text(self.text + text)

    def add_history(self, text):
        self.history.insert(tkinter.END, text + '\n')
        
    def set_text(self, text):
        self.current.set(text)
        self.current_label.update_idletasks()

    def function(self, name):
        self.set_text(name + "(" + self.text + ")")
        
    @property
    def text(self):
        return self.current.get()
    
    def mainloop(self):
        self.root.mainloop()

    def update_idletasks(self):
        self.history.update_idletasks()
        
class Controller:
    def __init__(self, view=None, model=None):
        self.view = view
        self.model = model

    def all_clear(self):
        self.view.all_clear()
        self.model.all_clear()

    def clear(self):
        self.view.clear()

    def backspace(self):
        self.view.backspace()

    def change_sign(self):
        text = self.view.text
        if not text:
            negative = False
        elif text[0] == '-':
            negative = True
            text = text[1:]
        else:
            negative = False
            if text[0] == '+':
                text = text[1:]

        if not negative:
            text = '-' + text

        self.view.set_text(text)

    def insert(self, text):
        self.view.insert(text)

    def function(self, name):
        self.view.function(name)
        
    def equal(self):
        try:
            value = self.model.evaluate(self.view.text)
            print("value", value)
        except Exception as ex:
            self.view.status.set(str(ex))
        else:
            value_text = str(value)
            self.view.add_history(self.view.text + ' = ' + value_text)
            self.view.set_text(value_text)
    
    COMMANDS = {
        "0": lambda self : self.insert('0'),
        "1": lambda self : self.insert('1'),
        "2": lambda self : self.insert('2'),
        "3": lambda self : self.insert('3'),
        "4": lambda self : self.insert('4'),
        "5": lambda self : self.insert('5'),
        "6": lambda self : self.insert('6'),
        "7": lambda self : self.insert('7'),
        "8": lambda self : self.insert('8'),
        "9": lambda self : self.insert('9'),
        "*": lambda self : self.insert('*'),
        "/": lambda self : self.insert('/'),
        "+": lambda self : self.insert('+'),
        "-": lambda self : self.insert('-'),
        "x^y": lambda self : self.insert('**'),
        ".": lambda self : self.insert('.'),
        "(": lambda self : self.insert('('),
        ")": lambda self : self.insert(')'),
        "+/-": lambda self : self.change_sign(),
        "AC": lambda self : self.all_clear(),
        "C": lambda self : self.clear(),
        "Bksp": lambda self : self.backspace(),
        "=": lambda self : self.equal(),
        "sqrt": lambda self : self.function("sqrt"),
        "pi": lambda self : self.insert("pi"),
        "cos": lambda self : self.function("cos"),
        "sin": lambda self : self.function("sin"),
        "tan": lambda self : self.function("tan"),
        "arccos": lambda self : self.function("acos"),
        "arcsin": lambda self : self.function("asin"),
        "arctan": lambda self : self.function("atan"),
        "exp": lambda self : self.function("exp"),
    }

    def command(self, label):
        function = self.COMMANDS[label]
        return lambda : self.call_function(label, function)

    def call_function(self, label, function):
        print("command", label)
        function(self)
        self.view.update_idletasks()

    def key(self, event):
        function = self.COMMANDS.get(event.char, None)
        if function is not None:
            print("key", key) or function(self)
        self.view.update_idletasks()

#!/usr/bin/env python

"""Calculator model.

This module is the model in an MVC-architecture calculator.

The model implements a history of expressions and results,
an unlimited number of registers and variables,
and a current expression.

The current expression is a string that is evaluated
by python's eval() function.
"""

import sympy

class Variable:
    def __init__(self, name, value = 0.0, readonly=False):
        self.name = name
        self.value = value
        self.readonly = readonly

def Constant(Variable):
    def __init__(self, name, value):
        super().__init__(name, value, True)
        
class Calculator:
    def __init__(self):
        self.history = []
        self.registers = []
        self.variables = {}
        #variables['pi'] = Constant('pi', sympy.pi)
        #variables['e']  = Constant('e',  sympy.E)

    def evaluate(self, text):
        return sympy.sympify(text).evalf()

    def all_clear(self):
        self.history = []
        self.registers = []
        self.variables = {}

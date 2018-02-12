#!/usr/bin/env python3

"""Calculator view and controller.

This module contains the main program.

"""

import view_control
        
CONFIGURATION = """
        sqrt|x^y| pi|*|AC
         7  | 8 | 9 |/|C
         4  | 5 | 6 |+|Bksp
         1  | 2 | 3 |-|(
         .  | 0 |+/-|=|)
    """

if __name__ == "__main__":
    v = view_control.View(CONFIGURATION)
    v.mainloop()

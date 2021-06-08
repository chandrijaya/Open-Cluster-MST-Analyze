# -*- coding: utf-8 -*-
"""
Chandra Aldiwijaya
chandra.aldiwijaya.694@gmail.com

Created on Fri Mar 16 21:08:05 2018

@author: Chandrijaya
"""

import sys

class execute:
    program = ""
    def __init__(self, program=''):
        self.program = program

    def newline(self):
        sys.stdout.write('\r\n\r')

    def bar(self, count, total, status=""):
        bar_len = 40
        filled_len = int(round(bar_len * count / float(total)))
    
        percents = round(100.0 * count / float(total), 3)
        load = '=' * filled_len + '-' * (bar_len - filled_len)
    
        sys.stdout.write('\r[%s] %s%s ... %s:%s       \r' %(load, 
                         percents, '%', self.program, status))
        sys.stdout.flush()
        if count == total:
            sys.stdout.write('\r\n\r')
    
    def spin(self, count, status=''):
        animation = "|/-\\"
        stat = ("\r%s:%s ... " %(self.program, status))
        sys.stdout.write(str(stat) + animation[count % len(animation)])
        sys.stdout.flush()
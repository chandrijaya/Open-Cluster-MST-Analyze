#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 07:53:03 2021

@author: chandrijaya
"""

def start():
    import program.work as wrk
    
    def cls():
        from os import system, name
        system('cls' if name=='nt' else 'clear')
    
    #open cluster on database
    ocName = ["Collinder 135", "IC 2391", "NGC 2632", "NGC 752", "NGC 869", "NGC 2244"]
    #parameter ((average pmRA, average pmDE), distance, colour excess)
    ocParameter = [[[-9.33, 5.26], 381, 0.042],
                   [[-24.2, 23.42], 165, 0.052],
                   [[-36.54, -13.36], 187, 0.01],
                   [[8.36, -12.1], 450, 0.04],
                   [[-2.81, 0.05], 2300, 0.521],
                   [[-0.84, -0.94], 1532, 0.541]]
    #parameter (e_pm, pmRA-, pmRA+, pmDE-, pmDE+)
    readParameter = [[2.9, -30, 30, -30, 30],
                     [3.6, -35, 25, -25, 35],
                     [1.5, -50, 30, -30, 30],
                     [1.9, -30, 30, -30, 30],
                     [1.7, -25, 25, -25, 25],
                     [3.7, -25, 25, -25, 25]]
    

    iNumber = 0
    check = 0
    while not iNumber in range(1, len(ocName)+1, 1):
        cls()
        print("Choose the open cluster on our demo:")
        count = 1
        for i in ocName:
            print("%i. %s" %(count, i))
            count += 1
        
        if check != 0:
            print("Error! Please input the right number")

        try:
            iNumber = int(input("Choose the option number: "))
        
        except:
            continue
        
        check += 1
        
    
    cls()
    print("You choose %s open cluster to analyze the MST." %(ocName[iNumber-1]))
    print("Database Parameter:")
    print("limit error pm = %i\n%i < pmRA < %i\n%i < pmDE < %i" %(readParameter[iNumber][0],
                                                                  readParameter[iNumber][1],
                                                                  readParameter[iNumber][2],
                                                                  readParameter[iNumber][3],
                                                                  readParameter[iNumber][4]))
    
    run = wrk.program(ocName[0], ocParameter[0], readParameter[0])
    run.mstAnalyze()
    run.graphOutput()
    print("Operation completed. Please check on output folder.")

if __name__ == "__main__":
    start() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 10:15:40 2021

@author: chandrijaya
"""
import program.loading as ld

class execute:
    rawPath = ""; dbPath = ""
    rawDataCount = 0; inputedData = 0
    removedInput = 0; conflictedInput = 0
    
    def __init__(self, db, raw):
        import sqlite3
 
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        self.createMainDB(connection, cursor)
        self.inputFromRaw(connection, cursor, raw)
        self.delWasteData(connection, cursor)

        cursor.close()
        connection.close()
        
        del sqlite3

    def inputFromRaw(self, db, cur, path):
        import csv
        
        dbLoad = ld.execute("Database")
        with open(path) as test:
            self.rawDataCount = sum(1 for i in test)
        
        print("Program detect total %i data on raw input." %(self.rawDataCount))
        with open(path) as data:
            rows = csv.reader(data, delimiter='\t')
            count = 0
            for row in rows:
                if count == 0:
                    id_ind = row.index("2MASS")
                    RA_ind = row.index("RAhour")
                    DE_ind = row.index("DEdeg")
                    B_ind = row.index("Bmag")
                    V_ind = row.index("Vmag")
                    J_ind = row.index("Jmag")
                    H_ind = row.index("Hmag")
                    K_ind = row.index("Ksmag")
                    pmRA_ind = row.index("pmRA")
                    pmDE_ind = row.index("pmDE")
                    epm_ind = row.index("e_pm")
                    Pkin_ind = row.index("Pkin")
        
                if (count > 2):
                    if not (float(row[pmRA_ind]) < 9999.) and (float(row[pmDE_ind]) < 9999.):
                        self.removedInput += 1
                        continue
                    
                    if not (float(row[B_ind]) > -99) and  (float(row[V_ind]) > -99):
                        self.removedInput += 1
                        continue
                        
                    if not (float(row[J_ind]) > -99) and  (float(row[H_ind]) > -99):
                        self.removedInput += 1
                        continue
                    
                    if not (float(row[K_ind]) > -99):
                        self.removedInput += 1
                        continue
                            
                    input_db = (row[id_ind],
                                row[RA_ind],row[DE_ind],
                                row[B_ind],row[V_ind],
                                row[J_ind],row[H_ind],
                                row[K_ind],
                                row[pmRA_ind],row[pmDE_ind],
                                row[epm_ind],row[Pkin_ind])

                    try:
                        self.inputMainDB(db, cur, input_db)
                        self.inputedData += 1
                        
                    except:
                        print("The %i star has already on database." %(int(row[id_ind])))
                        self.conflictedInput += 1

                    
                count += 1
                dbLoad.bar(count, self.rawDataCount, "Building")
                
        
        del dbLoad; del csv
        print("Database created successfully. Total %i has inputed, %i has removed, %i conflicted data"
              %(self.inputedData, self.removedInput, self.conflictedInput))
    
    def inputMainDB(self, db, cur, inList):
        crud_query = '''INSERT INTO stars (id, RA, DE, B, V, J, H, K, pmRA, pmDE, epm, Pkin) 
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?);'''

        cur.execute(crud_query, inList)
        db.commit()

    def createMainDB(self, db, cur):
        create_stars_table = '''CREATE TABLE IF NOT EXISTS stars (
                                 id INTEGER NOT NULL PRIMARY KEY,
                                 RA INTEGER NOT NULL,
                                 DE INTEGER NOT NULL,
                                 B INTEGER NOT NULL,
                                 V INTEGER NOT NULL,
                                 J INTEGER NOT NULL,
                                 H INTEGER NOT NULL,
                                 K INTEGER NOT NULL,
                                 pmRA INTEGER NOT NULL,
                                 pmDE INTEGER NOT NULL,
                                 epm INTEGER NOT NULL,
                                 Pkin INTEGER NOT NULL,
                                 selected INTEGER DEFAULT 0,
                                 reduced INTEGER DEFAULT 0,
                                 choosen INTEGER DEFAULT 0);'''
        

        cur.execute(create_stars_table)
        db.commit()
    
    def delWasteData(self, db, cur):
        deleteValue1 = '''DELETE FROM stars WHERE pmRA > 9999'''
        cur.execute(deleteValue1)
        db.commit()
        
        deleteValue2 = '''DELETE FROM stars WHERE pmDE > 9999'''
        cur.execute(deleteValue2)
        db.commit()
        
        deleteValue3 = '''DELETE FROM stars WHERE B < -99'''
        cur.execute(deleteValue3)
        db.commit()
        
        deleteValue4 = '''DELETE FROM stars WHERE V < -99'''
        cur.execute(deleteValue4)
        db.commit()
        
        deleteValue5 = '''DELETE FROM stars WHERE J < -99'''
        cur.execute(deleteValue5)
        db.commit()
        
        deleteValue6 = '''DELETE FROM stars WHERE H < -99'''
        cur.execute(deleteValue6)
        db.commit()
        
        deleteValue7 = '''DELETE FROM stars WHERE K < -99'''
        cur.execute(deleteValue7)
        db.commit()
        
        
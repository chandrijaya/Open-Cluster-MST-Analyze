#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 04:35:50 2021

@author: chandrijaya
"""
import sqlite3

class execute:
    def __init__(self, path):
        self.dbPath = path
        
    def createBackupTable(self, reset=False):
        if reset:
            self.delBackupTable()
            
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        create_stars__backup_table = '''CREATE TABLE IF NOT EXISTS stars_backup (
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
        cursor.execute(create_stars__backup_table)
        connection.commit()
        
        insert_backup_table = '''INSERT INTO stars_backup SELECT * FROM stars'''
        cursor.execute(insert_backup_table)
        connection.commit()
        
        cursor.close()
        connection.close()
    
    def checkTableExist(self, table):
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        
        check_backup_table = ("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s'" %(table))
        cursor.execute(check_backup_table)
        check = cursor.fetchone()[0]
        
        return bool(check)
    
    def retreiveBackupTable(self, recreate=False):
        check = self.checkTableExist("stars_backup")
        if check:
            connection = sqlite3.connect(self.dbPath)
            cursor = connection.cursor()
            
            drop_mst_edges_table = '''DROP TABLE IF EXISTS stars'''
            cursor.execute(drop_mst_edges_table)
            connection.commit()
            
            rename_backup_table = '''ALTER TABLE stars_backup RENAME TO stars'''
            cursor.execute(rename_backup_table)
            connection.commit()
            if recreate:
                self.createBackupTable()
            
            cursor.close()
            connection.close()
        
        else:
            print("Warning! No backup has detected. Operation will be aborted.")
            
            return
    
    def delBackupTable(self):
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        
        drop_stars_backup_table = '''DROP TABLE IF EXISTS stars_backup'''
        cursor.execute(drop_stars_backup_table)
        connection.commit()
            
        cursor.close()
        connection.close()
    
    def initSelectData(self, parameter):
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        
        cursor = connection.cursor()
        readId = '''SELECT id
                       FROM STARS 
                       WHERE epm <= ? 
                       AND pmRA BETWEEN ? AND ? 
                       AND pmDE BETWEEN ? AND ?'''
        
        cursor.execute(readId, parameter)
        tempId = cursor.fetchall()
        tempId = list(j for row in tempId for j in row)
        
        cursor.close()
        connection.close()
        
        return tempId
    
    def readDB(self, selcol, concol="id", conval=0, 
               table="stars", nocon=False, doubleCol=False):
        import program.loading as ld
        import numpy as np
        
        readLoad = ld.execute(selcol)
        
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        read = ("SELECT %s FROM %s WHERE %s = ?" %(selcol, table, concol))
        if nocon:
            read = ("SELECT %s FROM %s" %(selcol, table))
            
        if np.isscalar(conval):
            if nocon:
                cursor.execute(read)
                
            else:
                cursor.execute(read, (conval,))
                
            get = list(cursor.fetchall())
            if not doubleCol:
                get = list(j for row in get for j in row)
            
            temp = get
            
        else:
            temp = []; count = 0
            for i in conval:
                cursor.execute(read, (i,))
                get = list(cursor.fetchall()[0])
                if not doubleCol:
                    get = get[0]
                
                temp.append(get)
                count += 1
                readLoad.bar(count, len(conval), "Getting Data")
        
        cursor.close()
        connection.close()
        del readLoad
        del ld
        return temp
    
    def createExtendTable(self, reset=False):
        if reset:
            self.delExtendTable()
            
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        
        create_mst_edges_table = '''CREATE TABLE IF NOT EXISTS mst_edges (
                                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                     Vert_1 INTEGER NOT NULL,
                                     Vert_1_id INTEGER NOT NULL,
                                     Vert_2 INTEGER NOT NULL,
                                     Vert_2_id INTEGER NOT NULL,
                                     distance INTEGER NOT NULL,
                                     reduced INTEGER DEFAULT 0);'''
        cursor.execute(create_mst_edges_table)
        connection.commit()
        
        cursor.close()
        connection.close()
    
    def inputExtendTable(self, sd, si, se, re=[]):
        import program.loading as ld
        
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        
        crud_query = '''INSERT INTO mst_edges (Vert_1, Vert_1_id, Vert_2, Vert_2_id, distance, reduced) 
                            VALUES (?,?,?,?,?,?);'''
        
        inputLoad = ld.execute("Extend Table")
        
        if re != []:
            temp = []
            count = 0
            for i in re:
                temp.append(str(list(i)))
                count += 1
                inputLoad.bar(count, len(re), "Initiate RedEdg")
                
            re = temp
        
        count = 0
        for row, d in zip(se, sd):
            v1, v2 = row
            status = 0
            if str(list(row)) in re:
                status = 1
            
            inputData = (int(v1), si[v1], int(v2), si[v2], d, status)
            cursor.execute(crud_query, inputData)
            connection.commit()
            count += 1
            inputLoad.bar(count, len(sd), "Input Data")
        
        del inputLoad
        del ld
        cursor.close()
        connection.close()
    
    def delExtendTable(self):
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        
        drop_mst_edges_table = '''DROP TABLE IF EXISTS mst_edges'''
        cursor.execute(drop_mst_edges_table)
        connection.commit()
        
        cursor.close()
        connection.close()
        
    def updateExtendTable(self, re):
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        
        update_selected = '''UPDATE mst_edges SET reduced = 1 WHERE Vert_1 = ? AND Vert_2 = ?'''
        for row in re:
            cursor.execute(update_selected, row)
            connection.commit()
        
        cursor.close()
        connection.close()
        
    def updateStatCol(self, si, ri=[], ci=[], reset=False):
        if reset:
            self.resetStatCol()
            
        import program.loading as ld
        
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        
        updateLoad = ld.execute("Extend Column")
        count = 0
        for i in si:
            update_selected = '''UPDATE stars SET selected = 1 WHERE id = ?'''
            cursor.execute(update_selected, (i,))
            connection.commit()
            
            if i in ri:
                update_reduced = '''UPDATE stars SET reduced = 1 WHERE id = ?'''
                cursor.execute(update_reduced, (i,))
                connection.commit()
            
            if i in ci:
                update_choosen = '''UPDATE stars SET choosen = 1 WHERE id = ?'''
                cursor.execute(update_choosen, (i,))
                connection.commit()
            
            count += 1
            updateLoad.bar(count, len(si), "Update Data")
        
        del updateLoad
        del ld
        cursor.close()
        connection.close()
    
    def resetStatCol(self, task=3):
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()
        
        if task == 0 or task == 3:
            reset_selected_col = '''UPDATE stars SET selected = 0 where selected = 1'''
            cursor.execute(reset_selected_col)
            connection.commit()
        
        if task == 1 or task == 3:
            reset_selected_col = '''UPDATE stars SET reduced = 0 where selected = 1'''
            cursor.execute(reset_selected_col)
            connection.commit()
            
        if task == 2 or task == 3:    
            reset_selected_col = '''UPDATE stars SET choosen = 0 where selected = 1'''
            cursor.execute(reset_selected_col)
            connection.commit()
        
        cursor.close()
        connection.close()

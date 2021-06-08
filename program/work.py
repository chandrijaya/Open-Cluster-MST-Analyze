# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 23:17:29 2018

@author: Chandrijaya
"""

import numpy as np
import program.analyze.mstree as mst
import program.analyze.area as area
import program.output_generator.plot as plt
import program.database_management as dbm
import program.database_creator as dbc
from scipy.spatial.distance import pdist, squareform


class program:
    openClusterName = ""
    muPm=[]
    errorPm = 0
    starId = []
    reducedId = []
    choosenId = []
    dbPath = ""
    rawPath = ""
    dbLoadSuccess = False
    def __init__(self, ocName, ocParameter, readParameter, savedData=True):
        self.muPm, self.distance, self.esc = ocParameter;
        self.errorPm = readParameter[0]
        self.openClusterName = ocName
        self.dbPath = ("input/db/%s%s" %(ocName.replace(" ","_"), (".db")))
        self.rawPath = ("input/raw/%s%s" %(ocName.replace(" ","_"), (".csv")))
        self.initData(readParameter, savedData)
        
    def initData(self, parameter, savedData=True):
        if not savedData:
            dbc.execute(self.dbPath, self.rawPath)
            
        from os import path
        
        if not path.isfile(self.dbPath):
            print("Error! Possibly no database had built. Try to rebuild database.")
            try:
                print("Warning! This will be take a while.")
                dbc.execute(self.dbPath, self.rawPath)
            
            except:
                print("Error! Possibly no raw data detected or wrong raw data input. Please input data correctly")
                return
        
        initDB = dbm.execute(self.dbPath)      
        self.starId = initDB.initSelectData(parameter)
        if len(self.starId) > 0:
            self.dbLoadSuccess = True
        
        del initDB
        del path
    
    def mstAnalyze(self, l=1, n=10, reduce=True):
        dbManag = dbm.execute(self.dbPath)
        properMotion = dbManag.readDB("pmRA, pmDE", conval=self.starId, doubleCol=True)
        matDist = squareform(pdist(properMotion))
        mstBuild = mst.execute(matDist)
        Edges, DistEdg = mstBuild.prim()
        if reduce:
            RedEdg, RedDistEdg, Sub = mstBuild.reduction(Edges, DistEdg, l, n)
            if Sub[0] == []:
                raise ValueError('Reduction Error! No MST reduction formed.')
            
            print('Program detect %s sub-tree from reduction' %(len(Sub)))
            RedVert = np.sort(np.concatenate(Sub))
            for v in RedVert:
                self.reducedId.append(self.starId[v])

            count = 1
            testDistCen = []
            DefClt = area.execute(self.muPm)
            for sub in Sub:
                temp_sub = []
                for v in sub:
                    temp_sub.append(properMotion[v])
                        
                r, c = DefClt.radcen(temp_sub, count)
                cx, cy = c
                d = np.sqrt(((cy-self.muPm[1])**2)+((cx-self.muPm[0])**2))
                testDistCen.append(d)
                count += 1
            
            testSub = np.argmin(testDistCen);
            ChoosenVert = np.sort(Sub[testSub])
            for v in ChoosenVert:
                self.choosenId.append(self.starId[v])
        
        dbManag.createBackupTable(True)
        dbManag.updateStatCol(self.starId, self.reducedId, self.choosenId, True)
        dbManag.createExtendTable(True)
        dbManag.inputExtendTable(DistEdg, self.starId, Edges, RedEdg)
        del dbManag

    def graphOutput(self, task=4):
        dbRead = dbm.execute(self.dbPath)
        image = plt.execute(self.dbPath, self.openClusterName, self.muPm, self.errorPm)
        if (task == 0) or (task == 4):
            print('Plotting Cluster . . . . ')
            coor = np.vstack(dbRead.readDB("RA, DE", conval=self.starId, doubleCol=True))
            redCoor = np.vstack(dbRead.readDB("RA, DE", conval=self.reducedId, doubleCol=True))
            choosenCoor = np.vstack(dbRead.readDB("RA, DE", conval=self.choosenId, doubleCol=True))
            choosenVmag = dbRead.readDB("V", conval=self.choosenId)
            choosenPkin = dbRead.readDB("Pkin", conval=self.choosenId)
            image.cluster(coor, redCoor, choosenCoor, choosenVmag, choosenPkin, True)
            
        if (task == 1) or (task == 4):
            print('Plotting MST . . . . ')
            pm = np.vstack(dbRead.readDB("pmRA, pmDE", conval=self.starId, doubleCol=True))
            redPm = np.vstack(dbRead.readDB("pmRA, pmDE", conval=self.reducedId, doubleCol=True))
            choosenPm = np.vstack(dbRead.readDB("pmRA, pmDE", conval=self.choosenId, doubleCol=True))
            Edges = dbRead.readDB("Vert_1, Vert_2", table="mst_edges", nocon=True, doubleCol=True)
            RedEdg = dbRead.readDB("Vert_1, Vert_2", "reduced", 1, "mst_edges", doubleCol=True)
            image.vpdraw(pm)
            image.vpdraw(pm, redPm, red=True)
            image.vpdraw(pm, redPm, choosenPm, red=True, choosen=True)
            image.vpdmst(pm, Edges)
            image.vpdmst(pm, Edges, RedEdg, red=True)
        
        if (task == 2) or (task == 4):
            print('Plotting Pkin Histogram . . . . ')
            memProb = dbRead.readDB("Pkin", conval=self.starId)
            redMemProb = dbRead.readDB("Pkin", conval=self.reducedId)
            choosenMemProb = dbRead.readDB("Pkin", conval=self.choosenId)
            image.histogram(memProb, redMemProb, choosenMemProb)
            image.histogram(memProb, redMemProb, choosenMemProb, choosen=True)
            image.histogram(memProb, redMemProb, choosenMemProb, com=True, choosen=True)
            image.histogram(memProb, redMemProb, choosenMemProb, red=True)
            image.histogram(memProb, redMemProb, choosenMemProb, com=True, red=True)
            image.histogram(memProb, redMemProb, choosenMemProb, com=True, red=True, choosen=True)
    
        if (task == 3) or (task == 4):
            print('Plotting HR Diagram  . . . . ')
            bvDat = dbRead.readDB("id, B, V, Pkin", conval=self.starId, doubleCol=True)
            jkDat = dbRead.readDB("id, J, K, Pkin", conval=self.starId, doubleCol=True)
            jhDat = dbRead.readDB("id, J, H, Pkin", conval=self.starId, doubleCol=True)
            image.hr(bvDat, self.reducedId, self.choosenId, 0)
            image.hr(jkDat, self.reducedId, self.choosenId, 1)
            image.hr(jhDat, self.reducedId, self.choosenId, 2)
            if self.distance != "" and self.esc != "":
                print('Plotting Isochrone Fitting . . . . ')
                image.hr(bvDat, self.reducedId, self.choosenId, 0, self.distance, self.esc, iso=True)
                image.hr(jkDat, self.reducedId, self.choosenId, 1, self.distance, self.esc, iso=True)
                image.hr(jhDat, self.reducedId, self.choosenId, 2, self.distance, self.esc, iso=True)
    
            else:
                print('Warning! One or more isochrone parameter has no value. No isochrone fitting created')

        del dbRead
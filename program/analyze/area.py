# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 00:43:12 2018

@author: Chandrijaya
"""

import numpy as np
import program.loading as ld

class execute:
    Radius = 0; Center = []
    Rsub = []; Csub = []
    MuPM = []; DistMuC = []
    def __init__(self, mupm):
        self.MuPM = mupm
    
    def sortR(self):
        if len(self.Rsub) > 1:
            print('Sorting Sub Area')
            r = np.argsort(self.Rsub)
            temp_R = []; temp_C = []
            for i in r:
                cx, cy = self.Csub[i]
                temp_R.append(self.Rsub[i]); temp_C.append([cx, cy])
        
            self.Rsub = temp_R; self.Csub = temp_C
    
    def radcen(self, p, suba=[], whole=False): #m=0,
        if whole is True:
            pName = 'Area VPD'
        
        else:
            if suba == []:
                pName = 'Area Sub'
            
            else:
                pName = ('Area Sub ' + str(suba))
        
        x_list = []; y_list = []; temp_R = []
        n = len(p)
        loadArea = ld.execute(program=pName)
        for point, cek in zip(p, range(n)):
            i, j = point
            x_list.append(i); y_list.append(j)
            loadArea.bar(cek+1, n, status='Initializing')
             

        xmax = np.max(x_list); xmin = np.min(x_list)
        ymax = np.max(y_list); ymin = np.min(y_list)
        xc = round((xmax + xmin)/2.,2); yc = round((ymax + ymin)/2.,2)     
        for point, cek in zip(p, range(n)):
            i, j = point
            rx = (i - xc)**2; ry = (j - yc)**2
            r = np.sqrt(rx + ry)
            temp_R.append(round(r,2))
            loadArea.bar(cek+1, n, status='Finalizing')
            
        del loadArea
        return np.max(temp_R), [xc, yc]

'''
    def convex(self, Z): #jarvismarch
        def orientation(A,B,C):
            x32 = C[0]-B[0]; x21 = B[0]-A[0]
            y32 = C[1]-B[1]; y21 = B[1]-A[1]
            return (y21)*(x32)-(y32)*(x21)
        
        def area(H):
            A = 0
            for i in range(len(H)):
                Temp_A =(1./2.)*((H[i-1][0]*H[i][1]) - (H[i][0]*H[i-1][1]))
                A += Temp_A
            return A
    
        Temp_Hull = []; temp = []
        n = len(Z)
        P = range(n)
        # start point
        for i in range(1,n):#periksa titik yang paling kiri
            a = Z[P[i]][0]; b = Z[P[0]][0]
            if (a < b): 
                P[i], P[0] = P[0], P[i]
            
            if self.Loading is True:
                bar(i+1, n, status='con:cek')

        
        temp.append(P[0]) #titik awal
        del P[0]
        P.append(temp[0]) #membuat titik awal sebagai titik akhir
        vert=1
        while True:
            right = 0
            for i in range(1,len(P)):
                p = Z[temp[-1]]; r = Z[P[i]]; q = Z[P[right]]
                rotate = orientation(p,r,q)
                if rotate < 0:
                    right = i
                
                if self.Loading is True:
                    bar(i+1, len(P), status='con:h' + str(vert))
            
            
            
            if P[right] == temp[0]: #cek jika sudah kembali ke titik awal
                break
        
            else:
                temp.append(P[right])
                vert += 1
                del P[right] 
        
    
        for i in range(len(temp)):
            x = Z[temp[i]][0]
            y = Z[temp[i]][1]
            Temp_Hull.append([x,y])
            if self.Loading is True:
                bar(i+1, len(temp), status='con:fin')
    
    
        Temp_Area = area(Temp_Hull)/(1.0 - float(len(Temp_Hull)/n))
        Temp_R = np.sqrt(Temp_Area/np.pi)
        return Temp_Hull, Temp_Area, Temp_R
'''
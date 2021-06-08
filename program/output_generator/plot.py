# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:51:22 2018

@author: Chandrijaya
"""

import numpy as np
import matplotlib.pyplot as plt

class execute:
    def __init__(self, db, ocName='', mupm='', epm=''):
        self.dbPath = db
        self.Name = ocName
        self.muPm = mupm
        #Menambah folder pada directory file program
        #Folder untuk menyimpan hasil program
        self.outputPath = ("output/%s/original/graph" %(ocName))
        if epm != '':
            self.outputPath = ("output/%s/error limit %s/graph/" %(ocName, str(epm)))
            
        from os import path, makedirs
        
        if not path.isdir(self.outputPath):
            makedirs(self.outputPath)
            
        del path; del makedirs
    
    def cluster(self, C, RC=[], CC=[], CM=[], CP=[], reduced=False):    
        plt.figure(figsize=(8,8))
        plt.scatter(C[:,0], C[:,1], s=1, c='k', label='Awal')
        if reduced:
            CMC = []; S = []
            for c, m, p in zip(CC, CM, CP):
                if p >= 60:
                    CMC.append(c)
                    s = divmod(m,0.5)
                    ma = 21.
                    pa = 2.0 - 0.8
                    if m <=6:
                        S.append(175*((ma/s[0])**pa))
                
                    else:
                        S.append(125*((ma/s[0])**pa))
                        
            CMC = np.vstack(CMC)
            plt.scatter(RC[:,0], RC[:,1], s=4, c='r', label='Reduksi')
            plt.scatter(CC[:,0], CC[:,1], s=15, c='b', label='Akhir')
            plt.scatter(CMC[:,0], CMC[:,1], s=S, c='g', marker='*', label='P'+r'$\geq$'+'60%')
        
        plt.legend(loc=0, borderaxespad=0., facecolor='k', framealpha=0.175, fontsize=17 , labelspacing=0.1)
        plt.xlabel('RA J2000 (deg)', fontsize=19); plt.ylabel('DE J2000 (deg)', fontsize=19)
        plt.title('Plot Gugus ' + str(self.Name), fontsize=22)
        plt.tight_layout()
        plt.savefig(self.outputPath + 'Plot Gugus ' + str(self.Name) + '.png')
        plt.close()
    
    def vpdraw(self, PM, RPM=[], CPM=[], red=False, choosen=False):
        plt.figure(figsize = (8,8))
        plt.scatter(PM[:,0], PM[:,1], s=1, c='k', label='Awal', zorder=0)
        if red is False:
            name = ('VPD Raw ' + str(self.Name))
        
        else:
            plt.scatter(RPM[:,0], RPM[:,1], s=3, c='r', label='Reduksi', zorder=1)
            if choosen is False:
                name = ('VPD Raw Reduksi ' + str(self.Name))
            
            else:
                name = ('VPD Raw Akhir ' + str(self.Name))
                plt.scatter(CPM[:,0], CPM[:,1], s=10, c='b', label='Akhir', zorder=2)
                
        if self.muPm != '':
            plt.scatter(self.muPm[0], self.muPm[1], s=200, edgecolors='g', facecolors='g', marker='*', 
                        label=(r"$\overline{\mu_{\alpha}}=$" + str(self.muPm[0]) + 
                               r"$,  \overline{\mu_{\delta}}=$" + str(self.muPm[1])), zorder=2)
            plt.legend(loc=0, borderaxespad=0., facecolor='k', 
                             framealpha=0.175, fontsize=17 , labelspacing=0.1)
        

        plt.xlabel(r'$\mu_{\alpha}$ (mas/thn)', fontsize=19); plt.ylabel(r'$\mu_{\delta}$ (mas/thn)', fontsize=19)
        plt.suptitle(name, fontsize = 22)
        plt.tight_layout()
        plt.savefig(self.outputPath + str(name) + '.png')
        plt.close()
    
    def vpdmst(self, point, E, rE=[], red=False):        
        import program.loading as ld
        
        plt.figure(figsize = (8,8))
        if red is False:
            state = 'VPD'
        
        else:
            state = 'VPD Reduction'
            
        reload = ld.execute(state)
        for edge, count in zip(E, range(len(E))):
            i, j = edge
            plt.plot([point[i, 0], point[j, 0]], 
                     [point[i, 1], point[j, 1]], c='k', linewidth=0.8, zorder=0)
            reload.bar(count+1, len(E), status='Initial')
        
        if red is False:
            name = ('VPD MST ' + str(self.Name))
            
        else:
            name = ('VPD MST Reduksi ' + str(self.Name))
            for edge, count in zip(rE, range(len(rE))):
                i, j = edge
                plt.plot([point[i, 0], point[j, 0]], 
                         [point[i, 1], point[j, 1]], c='r', linewidth=1.9, zorder=1)
                reload.bar(count+1, len(rE), 'Reduction')
                
            
            
        if len(self.muPm) > 0:
            plt.scatter(self.muPm[0], self.muPm[1], s=200, edgecolors='g', facecolors='g', marker='*', 
                        label=(r"$\overline{\mu_{\alpha}}=$" + str(self.muPm[0]) + 
                               r"$,  \overline{\mu_{\delta}}=$" + str(self.muPm[1])), zorder=2)
            plt.legend(loc=0, borderaxespad=0., facecolor='k', 
                             framealpha=0.175, fontsize=17 , labelspacing=0.1)  

        plt.xlabel(r'$\mu_{\alpha}$ (mas/thn)'); plt.ylabel(r'$\mu_{\delta}$ (mas/thn)')
        plt.suptitle(name, fontsize = 22)
        plt.tight_layout()
        plt.savefig(self.outputPath + str(name) + '.png')
        plt.close()
        del reload; del ld
        
    def histogram(self, pk, rpk, cpk, com=False, red=False, choosen=False):
        bine = [0,10,20,30,40,50,60,70,80,90,100]
        lim = np.histogram(rpk, bins=bine)
        plt.figure(figsize = (7,7))
        if red is False:
            if choosen is False:
                name = ('Histogram Awal ' + str(self.Name))
                plt.hist(pk, bins=bine, edgecolor='w', facecolor='k', alpha=0.8, label='Awal')
                
                
            else:
                name = ('Histogram Akhir ' + str(self.Name))
                plt.hist(cpk, bins=bine, edgecolor='k', facecolor='b', alpha=0.8, label='Akhir')
                if com is True:
                    name = ('Histogram Awal-Akhir ' + str(self.Name))
                    plt.hist(pk, bins=bine, edgecolor='w', facecolor='k', alpha=0.325, label='Awal')
                    plt.ylim(0, np.max(lim[0])+(np.max(lim[0])/5))
                    
            
        
        else:
            if com is True:
                name = ('Histogram Awal-Reduksi ' + str(self.Name))
                plt.hist(pk, bins=bine, edgecolor='w', facecolor='k', alpha=0.325, label='Awal')
                plt.hist(rpk, bins=bine, edgecolor='r', fill=False, label='Reduksi')
                if choosen is True:
                    name = ('Histogram Lengkap ' + str(self.Name))
                    plt.hist(cpk, bins=bine, edgecolor='b', fill=False, label='Akhir')
                
                plt.ylim(0, np.max(lim[0])+(np.max(lim[0])/5))
            
            else:
                name = ('Histogram Reduksi ' + str(self.Name))
                plt.hist(rpk, bins=bine, edgecolor='k', facecolor='r', alpha=0.8, label='Reduksi')
        
        plt.legend(loc=0, borderaxespad=0., facecolor='k', framealpha=0.175, fontsize=17 , labelspacing=0.1)
        plt.xlabel(r'$P_{kin}$ (%)', fontsize=19); plt.ylabel('Jumlah Bintang', fontsize=19)
        plt.suptitle(name, fontsize = 22)
        plt.tight_layout()
        plt.savefig(self.outputPath + str(name) + '.png')
        plt.close()
    

    def hr(self, mag, ri, ci, dat=0, dist=0, Esc=0, iso=False):
        def isochrone(dist, Esc, bench, dt=0, point=[]):
            def modulus(M, d, K):
                return M - 5 + (5*np.log10(d) + K)
    
            R = 3.1; Av = R*Esc
            Rat = 1.29719; RatJ = 0.29553; RatH = 0.18201; RatK = 0.11554;
            if dt == 0:
                Ax = Rat*Av
                Ay = Av
    
            else:
                Ax = RatJ*Av
                if dt == 1:
                    Ay = RatK*Av
        
                else:
                    Ay = RatH*Av
        
        
            Axis = [[24,25],[28,30],[28,29]]
            i, j = Axis[dt]
            temp = []
            for MMX, MMY in zip(bench[i], bench[j]):
                mX = modulus(MMX, dist, Ax); mY = modulus(MMY, dist, Ay)
                if dt == 0:
                    if mY <= np.max(point[:,1])+3:
                        temp.append([(mX-mY), mY])
        
                else:
                    if mY <= np.max(point[:,1])+3:
                        temp.append([(mX-mY), mX])
                

    
            return np.vstack(temp)

        temp = []; tempr = []; tempc = []; tempm = []
        for i, x, y, p in mag:
            if dat == 0:
                j = y
                
            else:
                j = x
                
            temp.append([(x-y), j])
            if i in ri:
                tempr.append([(x-y), j])
            
            if i in ci:
                tempc.append([(x-y), j])
                if p >= 60:
                    tempm.append([(x-y), j])
                    
            
            else:
                temp.append([(x-y), x])
                
        
        point = np.vstack(temp); pointr = np.vstack(tempr); pointc = np.vstack(tempc)
        pointm = np.vstack(tempm)
        
        listName = ["Diagram BV ", "Diagram JK ", "Diagram JH "]
        listLabel = [["B-V", "V"],["J-K", "J"],["J-H", "J"]]
        
        plt.figure(figsize=(7,7))
        plt.scatter(point[:,0], point[:,1], s=1, c='k', label='Awal')
        plt.scatter(pointr[:,0], pointr[:,1], s=4, c='r', label='Reduksi')
        plt.scatter(pointc[:,0], pointc[:,1], s=10, c='b', label='Akhir')
        plt.scatter(pointm[:,0], pointm[:,1], s=50, c='g', marker='*', label='P'+r'$\geq$'+'60%')
        
        plus = 'Only '
        if iso is True:
            from os import path
    
            if path.isfile("input/bench/%s%s" %(self.Name.replace(" ","_"), ".txt")):
                benchFile = np.transpose(np.loadtxt("input/bench/%s%s" %(self.Name.replace(" ","_"), ".txt")))
                bench = isochrone(dist, Esc, benchFile, dat, point)
                plt.plot(bench[:,0], bench[:,1], 'b', linewidth=0.9, label='Model')
                plus = 'Isochrone Fitting '
            
            else:
                print("Warning! No bench file has detected. The program will plot HR diagram only.")
            
            del path
        
        name = (listName[dat] + str(plus) + str(self.Name))
    
        plt.legend(loc=0, borderaxespad=0., facecolor='k', framealpha=0.175, fontsize=17 , labelspacing=0.1)
        plt.gca().invert_yaxis()
        plt.xlabel(listLabel[dat][0], fontsize=19); plt.ylabel(listLabel[dat][1], fontsize=19)
        plt.title(name, fontsize=22)
    
        plt.xlim(-0.25, 2.25)
        plt.tight_layout()
        plt.savefig(self.outputPath + str(name) + '.png')              
        plt.close()
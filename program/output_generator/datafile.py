# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 01:46:45 2018

@author: Chandrijaya
"""
import os
import numpy as np
import program.loading as ld

class txtfile:
    def __init__(self, DIR, cluster='Cluster', load=False):
        self.Name = cluster
        self.Loading = load
        #Menambah folder pada directory file program
        #Folder untuk menyimpan hasil program
        final_path = os.path.join(DIR, r'Data')
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        
        os.chdir(str(final_path))

    def data(self, data, vertices=[], red=False, choosen=False):
        if vertices == []:
            vertices = range(len(data[0]))
            
        if red is True:
            state = 'Reduction'
            name1 = (str(self.Name) + ' Reduksi, N = ' + 
                     str(len(vertices)) + '.txt')
                
        elif choosen is True:
            state = 'Final'
            name1 = (str(self.Name) + ' Akhir, N = ' + 
                     str(len(vertices)) + '.txt')
            
        else:
            state = 'Initial'
            name1 = (str(self.Name) + ' Input,  N = ' + 
                     str(len(vertices)) + '.txt')
        
        fl = open(name1, 'w')
        fl.write('#Vertice' + '\t' + 'RAhour' + '\t' + 'DEdeg' + '\t' + 
                'Bmag' + '\t' + 'Vmag' + '\t' + 'Pkin' + '\t' + 'pmRA' + '\t' + 
                'pmDE' + '\t' + 'e_pm' + '\t' + 'PJKs' + '\t' + 'PJH' + '\t' + 
                'Jmag' + '\t' + 'Hmag' + '\t' + 'Ksmag' + '\n')
        fl.write('#' + '\t' + 'h' + '\t' + 'deg' + '\t' + 'mag' + '\t' + 
                'mag' + '\t' + '%' + '\t' + 'mas/yr' + '\t' + 'mas/yr' + '\t' + 
                'mas/yr' + '\t' + '%' + '\t' + '%' + '\t' + 'mag' + '\t' + 
                'mag' + '\t' + 'mag' + '\n')
        fl.write('#v' + '\t' + 'ra' + '\t' + 'de' + '\t' + 'B' + '\t' + 
                'V' + '\t' + 'Pk' + '\t' + 'pRA' + '\t' + 'pDE' + '\t' + 
                'ep' + '\t' + 'Pjk' + '\t' + 'Pjh' + '\t' + 'J' + '\t' + 
                'H' + '\t' + 'K' + '\n')
        count = 0     
        load = ld.execute(program='Write')
        for v in vertices:
            a, b, c = data[0][int(v)], data[1][int(v)], data[2][int(v)]
            fl.write(str(int(a)) + '\t' + str(b) + '\t' + str(c) + '\t')
            
            d, e, f = data[3][int(v)], data[4][int(v)], data[5][int(v)]
            fl.write(str(d) + '\t' + str(e) + '\t' + str(f) + '\t') 

            g, h, i = data[6][int(v)], data[7][int(v)], data[8][int(v)]
            fl.write(str(g) + '\t' + str(h) + '\t' + str(i) + '\t') 
            
            j, k, l = data[9][int(v)], data[10][int(v)], data[11][int(v)] 
            fl.write(str(j) + '\t' + str(k) + '\t' + str(l) + '\t') 
            
            m, n = data[12][int(v)], data[13][int(v)]
            fl.write(str(m) + '\t' + str(n) + '\n')
            if self.Loading is True:
                load.bar(count+1, len(vertices), status=state)
                count += 1
        
        fl.close()
        load.newline()
        
    def hist(self, pk, rpk, cpk):
        bine = [0,10,20,30,40,50,60,70,80,90,100]
        cek1 = np.histogram(pk, bins=bine)
        cek2 = np.histogram(rpk, bins=bine)
        cek3 = np.histogram(cpk, bins=bine)
        
        f = open('Histogram ' + str(self.Name) + '.txt', 'w')
        f.write('Data' + '\t' + '0<P<10' + '\t' + '10<P<20' + '\t' + 
                '20<P<30' + '\t' + '30<P<40' + '\t' + '40<P<50' + '\t' + 
                '50<P<60' + '\t' + '60<P<70' + '\t' + '70<P<80' + '\t' + 
                '80<P<90' + '\t' + '90<P<100' + '\t' + 'Ntot' + '\n')
        f.write('Input' + '\t')
        for ck in cek1[0]:
            f.write(str(ck) + '\t')
        
        f.write(str(len(pk)) + '\n')
        f.write('Reduksi' + '\t')
        for ck in cek2[0]:
            f.write(str(ck) + '\t')
        
        f.write(str(len(rpk)) + '\n')
        f.write('Akhir' + '\t')
        for ck in cek3[0]:
            f.write(str(ck) + '\t')
            
        f.write(str(len(cpk)))
        f.close()
    
    def sub(self, r, c, whole=False):
        if whole is False:
            name = ('Area Sub-Pohon Reduksi ' + str(self.Name) + '.txt')
    
        else:
            name = ('Area Sub-Pohon ' + str(self.Name) + '.txt')
        
        f = open(name, 'w')
        f.write('#[No]' + '\t' + '[Rc]' + '\t' + '[Cx]' + '\t' + '[Cy]' '\n')
        if type(r) is list:
            for i, R, C in zip(range(len(r)), r, c):
                cx, cy = C
                f.write(str(i+1) + '\t' + str(R) + '\t' + 
                        str(cx) + '\t' + str(cy) + '\n')
        
        else:
            cx, cy = C
            f.write(str(r) + '\t' + str(cx) + '\t' + str(cy) + '\n')
        
        f.close()
        
    
    
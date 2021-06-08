# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 22:06:23 2018

@author: Chandrijaya
"""
import numpy as np
import program.loading as ld

class execute:
    Edges = []; DistEdg = []
    RedEdg = []; RedDistEdg = []; RedVert = []; Sub = []
    matDist = []
    def __init__(self, M):
        self.matDist = M
    
    def prim(self): #Membuat MST
        if self.matDist.shape[0] != self.matDist.shape[1]:
            raise ValueError("MST error! Matrix not in 1:1 ratio.")
        
        n_vertices = self.matDist.shape[0]
        diag_indices = np.arange(n_vertices)
        #ubah poin (n,n) = inf, sisi menuju vertices yang sama
        self.matDist[diag_indices, diag_indices] = np.inf                                                                 
        visited_vertices = [0] #titik awal proses pembuatan MST
        num_visited = 1
        Temp_Edg = []; Temp_Dist = []
        mstLoad = ld.execute("MST")
        while num_visited != n_vertices:
            new_edge = np.argmin(self.matDist[visited_vertices], axis=None)
            #Mencari bobot terkecil                                                   
            new_edge = divmod(new_edge, n_vertices)
            new_edge = [visited_vertices[new_edge[0]], new_edge[1]]                                                       
            #identifikasi vertices yang dihubungkan dari titik awal dengan bobot terkecil
            p,q = new_edge
            Temp_Edg.append([p, q])
            visited_vertices.append(new_edge[1])
            #memasukan data bobot sisi-sisi mst
            Temp_Dist.append(self.matDist[p][q])
            self.matDist[visited_vertices, new_edge[1]] = np.inf
            self.matDist[new_edge[1], visited_vertices] = np.inf
            #Menghapus semua vertices yang dilalui oleh vertices yang telah dikunjungi
            num_visited += 1
            mstLoad.bar(num_visited, n_vertices, "Generating")
        
        del mstLoad
        return np.vstack(Temp_Edg), Temp_Dist

    def reduction(self, M, S, L, N):
        def findset(vertex):
            for i in range(len(vertices)):
                for element in vertices[i]:
                    if element == vertex:
                        return i
            
            
            return None

        def union(vertex1, vertex2):
            index1 = vertex1; index2 = vertex2
            for element in vertices[index2]:
                vertices[index1].append(element)
            vertices.pop(index2)
    
        vertices = []; sub = []
        temp_Edg = []; fin_Edg = []
        temp_Dist = []; fin_Dist = []
        lc = L*np.mean(S); Nc = N; n1 = len(M)
        reduceLoad = ld.execute(program="Reduction")
        for i in range(n1 + 1):
            vertices.append([i])
            #identifikasi vertices
            reduceLoad.bar(i+1, n1+1, "Add Vertices")
            
        
        for edge, distance, cek in zip(M, S, range(n1)):
            i, j = edge
            reduceLoad.bar(cek+1, n1, "Separation")
                
            #Cek jarak dengan bobot yang lebih kecil dari lc
            if distance < lc:
                a = findset(i); b = findset(j)
                temp_Edg.append([i,j]); temp_Dist.append(distance)
                union(a,b)
                #Membuat sub-pohon
        
        
        count = 0; n2 = len(vertices)
        #Memilih sub-pohon yang akan dihapus jika anggotanya kurang dari Nc
        while count < n2:
            if len(vertices[count]) < Nc:    
                vertices.remove(vertices[count])
                n2 = len(vertices)
        
            else:
                count += 1
            
            reduceLoad.spin(count, status="Elimination")
            #Kasus di mana tidak ada sub-pohon yang tersisa
            if n2 == 0:
                return [[0, 0]], [0], [0]
        
    
        sub = vertices
        n3 = len(temp_Edg)
        #Identifikasi vertices yang lolos dari proses reduksi
        for edge, distance, cek in zip(temp_Edg, temp_Dist, range(n3)):
            i, j = edge
            for element in vertices:
                if (i in element) and (j in element):
                    fin_Edg.append([i,j]); fin_Dist.append(distance)
            
            
            reduceLoad.bar(cek+1, n3, status='Finalizing')
            
        del reduceLoad
        return np.vstack(fin_Edg), fin_Dist, sub
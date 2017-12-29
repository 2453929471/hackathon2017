# -*- coding: utf-8 -*-
class QuickFind(object):
    id=[]
    count=0

    def __init__(self,n): # n is total number of nodes
        self.count = n
        i=0
        while i<n:
            self.id.append(i)
            i+=1
    #check whether two nodes are in the same component
    def connected(self,p,q):
        return self.find(p) == self.find(q)

    #find which component p belongs to
    def find(self,p):
        return self.id[p]

    #union node p and node q
    def union(self,p,q):
        idp = self.find(p)
        if not self.connected(p,q):
            for i in range(len(self.id)):
                if self.id[i]==idp: # 将p所在组内的所有节点的id都设为q的当前id
                    self.id[i] = self.id[q]
            self.count -= 1

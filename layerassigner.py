from ast import Pass
from math import nan
from os import splice
from socket import MsgFlag

from regex import F
import BusAllocator
import random
import matplotlib.pyplot as plt
import copy


# for package, not the hole board 
class Bus:
    def __init__(self, ID, comps, start, end) -> None:
        self.BusID = ID
        self.comps = comps      #[startcomp,endcomp]
        self.start = start
        self.end = end


class Component:
    def __init__(self, dia0, dia1, busIDs, id) -> None: #dia is absolute pos
        self.dia0 = dia0
        self.dia1 = dia1
        self.buslist = busIDs
        self.compID = id
        
class Package:
    def __init__(self, comps, dia0, dia1, id) -> None: # absolute pos of the left-botton diag
        self.comps = comps
#        self.pos = pos
#        self.sizex = sizex
#        self.sizey = sizey
        self.dia0 = dia0
        self.dia1 = dia1
        self.compsList = []
        self.pkgID = id
        for comp in comps:
            self.compsList.append(comp.compID)
    
#    def sort(self):
#        for comp in self.comps:
#            for bus in comp.buslist:
#                if (bus.comps[0] in self.compsList) & (bus.comps[1] in self.compsList):
        

class LayerAssigner:
    def __init__(self, packages) -> None:
        self.PackageList = packages

    def allocate_boundary(self, bus):  #TODO: add actual path, consider interpkgs
        direct0 = []
        direct1 = []
        if bus.start[0] <= bus.end[0]:
            if bus.start[1] <= bus.end[1]:
                if (bus.comps[0].dia1[0] <= bus.end[0]) & (bus.comps[0].dia1[1] <= bus.end[1]):
                    direct0 = [0,1]
                elif (bus.comps[0].dia1[0] <= bus.end[0]) & (bus.comps[0].dia1[1] > bus.end[1]):
                    direct0 = [1]
                elif (bus.comps[0].dia1[0] > bus.end[0]) & (bus.comps[0].dia1[1] <= bus.end[1]):
                    direct0 = [0]
                if (bus.comps[1].dia0[0] >= bus.start[0]) & (bus.comps[1].dia0[1] >= bus.start[1]):
                    direct1 = [2,3]
                elif (bus.comps[1].dia0[0] >= bus.start[0]) & (bus.comps[1].dia0[1] < bus.start[1]):
                    direct1 = [3]
                elif (bus.comps[1].dia0[0] < bus.start[0]) & (bus.comps[1].dia0[1] >= bus.start[1]):
                    direct1 = [2]
            

                        
            else:
                if (bus.comps[0].dia1[0] <= bus.end[0]) & (bus.comps[0].dia0[1] >= bus.end[1]):
                    direct0 = [1,2]
                elif (bus.comps[0].dia1[0] <= bus.end[0]) & (bus.comps[0].dia0[1] < bus.end[1]):
                    direct0 = [1]
                elif (bus.comps[0].dia1[0] > bus.end[0]) & (bus.comps[0].dia0[1] >= bus.end[1]):
                    direct0 = [2]
                if (bus.comps[1].dia0[0] >= bus.start[0]) & (bus.comps[1].dia1[1] <= bus.start[1]):
                    direct1 = [0,3]
                elif (bus.comps[1].dia0[0] < bus.start[0]) & (bus.comps[1].dia1[1] <= bus.start[1]):
                    direct1 = [0]
                elif (bus.comps[1].dia0[0] >= bus.start[0]) & (bus.comps[1].dia1[1] > bus.start[1]):
                    direct1 = [3]
        else:

            if bus.start[1] > bus.end[1]:
                if (bus.comps[0].dia0[0] >= bus.end[0]) & (bus.comps[0].dia0[1] >= bus.end[1]):
                    direct0 = [2,3]
                elif (bus.comps[0].dia0[0] >= bus.end[0]) & (bus.comps[0].dia0[1] < bus.end[1]):
                    direct0 = [3]
                elif (bus.comps[0].dia0[0] < bus.end[0]) & (bus.comps[0].dia0[1] >= bus.end[1]):
                    direct0 = [2]
                if (bus.comps[1].dia1[0] <= bus.start[0]) & (bus.comps[1].dia1[1] <= bus.start[1]):
                    direct1 = [0,1]
                elif (bus.comps[1].dia1[0] <= bus.start[0]) & (bus.comps[1].dia1[1] > bus.start[1]):
                    direct1 = [1]
                elif (bus.comps[1].dia1[0] > bus.start[0]) & (bus.comps[1].dia1[1] <= bus.start[1]):
                    direct1 = [0]
            

                        
            else:
                if (bus.comps[0].dia0[0] >= bus.end[0]) & (bus.comps[0].dia1[1] <= bus.end[1]):
                    direct0 = [0,3]
                elif (bus.comps[0].dia0[0] >= bus.end[0]) & (bus.comps[0].dia1[1] > bus.end[1]):
                    direct0 = [3]
                elif (bus.comps[0].dia0[0] < bus.end[0]) & (bus.comps[0].dia1[1] <= bus.end[1]):
                    direct0 = [0]
                if (bus.comps[1].dia1[0] <= bus.start[0]) & (bus.comps[1].dia0[1] >= bus.start[1]):
                    direct1 = [1,2]
                elif (bus.comps[1].dia1[0] > bus.start[0]) & (bus.comps[1].dia0[1] >= bus.start[1]):
                    direct1 = [2]
                elif (bus.comps[1].dia1[0] <= bus.start[0]) & (bus.comps[1].dia0[1] < bus.start[1]):
                    direct1 = [1]
        return direct0,direct1



    def EscapeOptimize(self):
        directions = []
        for package in self.PackageList:
            for comp in package.comps:
                for busindex in comp.buslist:
                    bus = buslist[busindex]
                    if (bus.comps[0] in package.comps) & (bus.comps[1] in package.comps):
                        dir1,dir2 = self.allocate_boundary(bus)
                    elif bus.comps[1] not in package.comps:
                        dir1, _ = self.allocate_boundary(bus)
                        dir2 = [4]
                    elif bus.comps[0] not in package.comps:
                        _,dir2 = self.allocate_boundary(bus)
                        dir1 = [4]
                    item = [package.pkgID,bus.BusID,dir1,dir2]
                    if item not in directions:
                        directions.append([package.pkgID,bus.BusID,dir1,dir2])
        return directions
    
    def sort_by_dir(self):
        for package in self.PackageList:
            directions = []
            comps_dir = []
            for comp in package.comps:
                component = {}
                component[0] = []
                component[1] = []
                component[2] = []
                component[3] = []
                for busindex in comp.buslist:
                    bus = buslist[busindex]
                    if (bus.comps[0] in package.comps) & (bus.comps[1] in package.comps):
                        dir1,dir2 = self.allocate_boundary(bus)
                    elif bus.comps[1] not in package.comps:
                        dir1, _ = self.allocate_boundary(bus)
                        dir2 = [4]
                    elif bus.comps[0] not in package.comps:
                        _,dir2 = self.allocate_boundary(bus)
                        dir1 = [4]
                    item = [package.pkgID,bus.BusID,dir1,dir2]
                    if item not in directions:
                        directions.append([package.pkgID,bus.BusID,dir1,dir2])
                        if 0 in dir1 :
                            component[0].append([bus.busID,[bus.start[0],comp.dia1[1]]])
                        if 1 in dir1 :
                            component[1].append([bus.busID,[comp.dia1[0],bus.start[1]]])
                        if 2 in dir1 :
                            component[2].append([bus.busID,[bus.start[0],comp.dia0[1]]])
                        if 3 in dir1 :
                            component[3].append([bus.busID,[comp.dia0[0],bus.start[1]]])
                        if 0 in dir2 :
                            component[0].append([bus.busID,[bus.end[0],comp.dia1[1]]])
                        if 1 in dir2 :
                            component[1].append([bus.busID,[comp.dia1[0],bus.end[1]]])
                        if 2 in dir2 :
                            component[2].append([bus.busID,[bus.end[0],comp.dia0[1]]])
                        if 3 in dir2 :
                            component[3].append([bus.busID,[comp.dia0[0],bus.end[1]]])
                component[0].sort(key = lambda x:x[1][0])
                component[1].sort(key = lambda x:x[1][1],reverse=True)
                component[2].sort(key = lambda x:x[1][0],reverse=True)
                component[3].sort(key = lambda x:x[1][1])
                comps_dir.append(component)
        return comps_dir
    
class Drawer:
        def __init__(self, packages, buslist) -> None:
            self.packages = packages
            self.buslist = buslist


        def draw(self, Bsize_x, Bsize_y, directions):
            fig,ax = plt.subplots(figsize = (Bsize_x/100,Bsize_y/100))
            expand = 0
            busx = []
            busy = []
            plt.xlim(0-expand,Bsize_x+expand)
            plt.ylim(0-expand,Bsize_y+expand)
            for i, pkg in enumerate(self.packages):
                plt.plot([pkg.dia0[0],pkg.dia1[0]], [pkg.dia0[1],pkg.dia0[1]], 'k',linewidth = 0.5, alpha= 1)
                plt.plot([pkg.dia1[0],pkg.dia1[0]], [pkg.dia0[1],pkg.dia1[1]], 'k',linewidth = 0.5, alpha= 1)
                plt.plot([pkg.dia0[0],pkg.dia1[0]], [pkg.dia1[1],pkg.dia1[1]], 'k',linewidth = 0.5, alpha= 1)
                plt.plot([pkg.dia0[0],pkg.dia0[0]], [pkg.dia0[1],pkg.dia1[1]], 'k',linewidth = 0.5, alpha= 1)
                plt.text(pkg.dia0[0], pkg.dia0[1], s=i)
                for j,comp in enumerate(pkg.comps):
                    plt.plot([comp.dia0[0],comp.dia1[0]], [comp.dia0[1],comp.dia0[1]], 'g',linewidth = 0.5, alpha= 1)
                    plt.plot([comp.dia1[0],comp.dia1[0]], [comp.dia0[1],comp.dia1[1]], 'g',linewidth = 0.5, alpha= 1)
                    plt.plot([comp.dia0[0],comp.dia1[0]], [comp.dia1[1],comp.dia1[1]], 'g',linewidth = 0.5, alpha= 1)
                    plt.plot([comp.dia0[0],comp.dia0[0]], [comp.dia0[1],comp.dia1[1]], 'g',linewidth = 0.5, alpha= 1)
                    plt.text(comp.dia0[0], comp.dia0[1], s=j)
                    for bus in comp.buslist:
                        busx.append(self.buslist[bus].start[0])
                        busx.append(self.buslist[bus].end[0])
                        busy.append(self.buslist[bus].start[1])
                        busy.append(self.buslist[bus].end[1])
                        plt.text(self.buslist[bus].start[0], self.buslist[bus].start[1], s=bus)
                        plt.text(self.buslist[bus].end[0], self.buslist[bus].end[1], s=bus)
            plt.scatter(busx, busy,linewidths=0.1)
            for item in directions:
                start = buslist[item[1]].start
                end = buslist[item[1]].end
                stcomp = buslist[item[1]].comps[0]
                edcomp = buslist[item[1]].comps[1]
                dir1 = item[2]
                dir2 = item[3]
                for item in dir1:
                    if item == 0:
                        ax.arrow(start[0],start[1],0,stcomp.dia1[1]-start[1])
                    elif item == 1:
                        ax.arrow(start[0],start[1],stcomp.dia1[0]-start[0],0)
                    elif item == 2:
                        ax.arrow(start[0],start[1],0,stcomp.dia0[1]-start[1])
                    elif item == 3:
                        ax.arrow(start[0],start[1],stcomp.dia0[0]-start[0],0)
                    elif item == 4:
                        ax.arrow(start[0],start[1],0,0)
                for item in dir2:
                    if item == 0:
                        ax.arrow(end[0],end[1],0,edcomp.dia1[1]-end[1])
                    elif item == 1:
                        ax.arrow(end[0],end[1],edcomp.dia1[0]-end[0],0)
                    elif item == 2:
                        ax.arrow(end[0],end[1],0,edcomp.dia0[1]-end[1])
                    elif item == 3:
                        ax.arrow(end[0],end[1],edcomp.dia0[0]-end[0],0)
                    elif item == 4:
                        ax.arrow(end[0],end[1],0,0)

                        
            
            plt.show()
#def isoverlap(comp1,comp2):
def isoverlap(comp1,comp2):
    if comp1[0][0]>=comp2[1][0] or comp1[1][0]<=comp2[0][0] or comp1[0][1]>=comp2[1][1] or comp1[1][1]<=comp2[0][1]:
        return False
    else:
        return True
    
def iscontain(comp1,comp2): #2contains1
    if (comp1[0][0]>=comp2[0][0] and comp1[1][0]<=comp2[1][0] and comp1[0][1]>=comp2[0][1] and comp1[1][1]<=comp2[1][1]):
        return True
    else:
        return False










def Legalization(dialist,target,boundarydiapair, base):
    dia0 = target[0]
    dia1 = target[1]
    size_x = boundarydiapair[1][0] - boundarydiapair[0][0]
    size_y = boundarydiapair[1][1] - boundarydiapair[0][1]
    if dialist:
            for dia_pair in dialist:
                #while (dia_pair[0][0] < dia0[0]) &(dia_pair[1][0] > dia1[0])&(dia_pair[0][1] < dia0[1])&(dia_pair[1][1] > dia1[1]):
                while (isoverlap(dia_pair,[dia0, dia1])) or not iscontain([dia0, dia1], boundarydiapair):
                    dia0 = [random.randint(0,size_x -1),random.randint(0,size_y -1)]
                    #dia1 = [dia0[0] + random.randint(0,Bsize_x - dia0[0]), dia0[1] + random.randint(0,Bsize_y - dia0[1])]
                    edge_length = random.randint(base, base + min(size_x-dia0[0], size_y-dia0[1]))
                    dia1 = [dia0[0] + edge_length, dia0[1] + edge_length]
                    return Legalization(dialist, [dia0, dia1], boundarydiapair, base)
            dialist.append([dia0, dia1])
    else:
        if iscontain([dia0, dia1], [[0, 0], [size_x, size_y]]):
            dialist.append([dia0, dia1])
        else:
            while not iscontain([dia0, dia1], [[0, 0], [size_x, size_y]]):
                dia0 = [random.randint(0,size_x -1),random.randint(0,size_y -1)]
                edge_length = random.randint(base, base + min(size_x-dia0[0], size_y-dia0[1]))
                dia1 = [dia0[0] + edge_length, dia0[1] + edge_length]
            dialist.append([dia0, dia1])


def Legalization2(dialist,target,boundarydiapair, base, devide):
    dia0 = target[0]
    dia1 = target[1]
    size_x = boundarydiapair[1][0] - boundarydiapair[0][0]
    size_y = boundarydiapair[1][1] - boundarydiapair[0][1]
    if dialist:
        flag = 0  
        firstloop = 1
        while flag or firstloop:
            firstloop = 0
            flag = 0
            for dia_pair in dialist:
                if (isoverlap(dia_pair,[dia0, dia1])) or not iscontain([dia0, dia1], boundarydiapair):
                    flag = 1
                    dia0 = [random.randint(boundarydiapair[0][0], boundarydiapair[1][0]),random.randint(boundarydiapair[0][1], boundarydiapair[1][1])]
                    #edge_length = min(random.randint(base, base + min(size_x-dia0[0], size_y-dia0[1])), int(size_x/3))
                    edge_length = int(size_x/devide)
                    dia1 = [dia0[0] + edge_length, dia0[1] + edge_length]
                    break
        dialist.append([dia0, dia1])
    else:
        if iscontain([dia0, dia1], [[0, 0], [size_x, size_y]]):
            dialist.append([dia0, dia1])
        else:
            while not iscontain([dia0, dia1], boundarydiapair):
                dia0 = [random.randint(boundarydiapair[0][0], boundarydiapair[1][0]),random.randint(boundarydiapair[0][1], boundarydiapair[1][1])]
                #edge_length = min(random.randint(base, base + min(size_x-dia0[0], size_y-dia0[1])), int(size_x/3))
                edge_length = int(size_x/devide)
                dia1 = [dia0[0] + edge_length, dia0[1] + edge_length]
            dialist.append([dia0, dia1])
class VitualWall:
    def __init__(self,point1, point2, comp1, comp2, nb, crossbus):
        self.comps = [comp1,comp2]
        self.point = [point1,point2]
        self.nb = nb
        self.crossbus = crossbus

def evaluate(vitualwall, ):
    Pass

def isadjacent(comppair)->int: #TODO consider other comp between comppair (over)
    comp1 = comppair[0]
    comp2 = comppair[1]
    if (comp2.dia0[0]>=comp1.dia1[0]) and comp2.dia0[1] < comp1.dia1[1] and comp2.dia1[1] > comp1.dia0[1]:
        dir = 1
    elif (comp2.dia0[1]<=comp1.dia1[1]) and comp2.dia0[0] < comp1.dia1[0] and comp2.dia1[1] > comp1.dia0[1]:
        dir = 2
    elif (comp2.dia1[0]<=comp1.dia0[0]) and comp2.dia0[1] < comp1.dia1[1] and comp2.dia1[1] > comp1.dia0[1]:
        dir = 3
    elif (comp2.dia0[1]>=comp1.dia1[1]) and comp2.dia0[0] < comp1.dia1[0] and comp2.dia1[0] > comp1.dia0[0]:
        dir = 0
    else:
        return 4 
    for comp in comp_list: 
        dias = [comp.dia0, comp.dia1]
        if dir == 0:
            if comp2.dia1[0] <= comp1.dia1[0]:
                if comp2.dia0[0] <= comp1.dia0[0]:
                    zone = [comp1.dia0,comp2.dia1]
                else:
                    zone = [[comp2.dia0[0],comp1.dia1[1]],[comp2.dia1[0],comp2.dia0[1]]]
            else:
                if comp2.dia0[0] <= comp1.dia0[0]:
                    zone = [[comp1.dia0[0],comp1.dia1[1]],[comp1.dia1[0],comp2.dia0[1]]]
                else:
                    zone = [[comp2.dia0[0],comp1.dia1[1]],[comp1.dia1[0],comp2.dia0[1]]]
        elif dir == 1:
            if comp2.dia1[1] <= comp1.dia1[1]:
                if comp2.dia0[1] <= comp1.dia0[1]:
                    zone = [comp1.dia0,comp2.dia1]
                else:
                    zone = [[comp1.dia1[0],comp2.dia0[1]],[comp2.dia0[0],comp2.dia1[1]]]
            else:
                if comp2.dia0[1] <= comp1.dia0[1]:
                    zone = [[comp1.dia1[0],comp1.dia0[1]],[comp2.dia1[0],comp1.dia1[1]]]
                else:
                    zone = [[comp1.dia1[0],comp2.dia0[1]],[comp2.dia1[0],comp1.dia1[1]]]
        elif dir == 2:
            if comp2.dia1[0] <= comp1.dia1[0]:
                if comp2.dia0[0] <= comp1.dia0[0]:
                    zone = [[comp1.dia0[0],comp2.dia1[1]],[comp2.dia1[0],comp1.dia0[1]]]
                else:
                    zone = [[comp2.dia0[0],comp2.dia1[1]],[comp2.dia1[0],comp1.dia0[1]]]
            else:
                if comp2.dia0[0] <= comp1.dia0[0]:
                    zone = [[comp1.dia0[0],comp2.dia1[1]],[comp1.dia1[0],comp1.dia0[1]]]
                else:
                    zone = [[comp2.dia0[0],comp2.dia1[1]],[comp1.dia1[0],comp1.dia0[1]]]
        elif dir == 3:
            if comp2.dia1[1] <= comp1.dia1[1]:
                if comp2.dia0[1] <= comp1.dia0[1]:
                    zone = [[comp2.dia1[0],comp1.dia0[1]],[comp1.dia0[0],comp2.dia1[1]]]
                else:
                    zone = [[comp2.dia1[0],comp2.dia0[1]],[comp1.dia0[0],comp2.dia1[1]]]
            else:
                if comp2.dia0[1] <= comp1.dia0[1]:
                    zone = [[comp2.dia1[0],comp2.dia0[1]],[comp1.dia0[0],comp1.dia1[1]]]
                else:
                    zone = [[comp2.dia1[0],comp1.dia0[1]],[comp1.dia0[0],comp1.dia1[1]]]
        if isoverlap(dias,zone):
            return 4
        else:
            return dir


def localminimization(comppair, directions) -> VitualWall:   #can use comp_dirs instead of directions
    dir = isadjacent(comppair)
    if dir == 4:
        return None
    else:
        edge1 = []
        edge2 = []

        if dir == 0:
            for item in directions:     # TODO:optimize:   just use directions of buses in comppair
                if item[1] in comppair[0].buslist:
                    bus = buslist[item[1]]
                    
                    if bus.comps[0].compID == comppair[0].compID:   #to figure out start 0 /end comp 1
                        if 0 in item[2]:
                            edge1.append([bus,0,bus.start[0],comppair[0].dia1[1]])
                    elif bus.comps[1].compID == comppair[0].compID:
                        if 0 in item[3]:
                            edge1.append([bus,1,bus.end[0],comppair[0].dia1[1]])
                
                if item[1] in comppair[1].buslist:
                    bus = buslist[item[1]]
                    
                    if bus.comps[0].compID == comppair[1].compID:   #to figure out start/end comp
                        if 2 in item[2]:
                            edge2.append([bus,0,bus.start[0],comppair[1].dia0[1]])
                    elif bus.comps[1].compID == comppair[1].compID:
                        if 2 in item[3]:
                            edge2.append([bus,1,bus.end[0],comppair[1].dia0[1]])
     

        if dir == 1:
            for item in directions:
                if item[1] in comppair[0].buslist:
                    bus = buslist[item[1]]
                    
                    if bus.comps[0].compID == comppair[0].compID:   #to figure out start/end comp
                        if 1 in item[2]:
                            edge1.append([bus,0,comppair[0].dia1[0],bus.start[1]])
                    elif bus.comps[1].compID == comppair[0].compID:
                        if 1 in item[3]:
                            edge1.append([bus,1,comppair[0].dia1[0],bus.end[1]])
                
                if item[1] in comppair[1].buslist:
                    bus = buslist[item[1]]
                    
                    if bus.comps[0].compID == comppair[1].compID:   #to figure out start/end comp
                        if 3 in item[2]:
                            edge2.append([bus,0,comppair[1].dia0[0],bus.start[1]])
                    elif bus.comps[1].compID == comppair[1].compID:
                        if 3 in item[3]:
                            edge2.append([bus,1,comppair[1].dia0[0],bus.end[1]])                                                   
        if dir == 2:
            for item in directions:
                if item[1] in comppair[0].buslist:
                    bus = buslist[item[1]]
                    
                    if bus.comps[0].compID == comppair[0].compID:   #to figure out start/end comp
                        if 2 in item[2]:
                            edge1.append([bus,0,bus.start[0],comppair[0].dia0[1]])
                    elif bus.comps[1].compID == comppair[0].compID:
                        if 2 in item[3]:
                            edge1.append([bus,1,bus.end[0],comppair[0].dia0[1]])
                
                if item[1] in comppair[1].buslist:
                    bus = buslist[item[1]]
                    
                    if bus.comps[0].compID == comppair[1].compID:   #to figure out start/end comp
                        if 0 in item[2]:
                            edge2.append([bus,0,bus.start[0],comppair[1].dia1[1]])
                    elif bus.comps[1].compID == comppair[1].compID:
                        if 0 in item[3]:
                            edge2.append([bus,1,bus.end[0],comppair[1].dia1[1]])
     

        if dir == 3:
            for item in directions:
                if item[1] in comppair[0].buslist:
                    bus = buslist[item[1]]
                    
                    if bus.comps[0].compID == comppair[0].compID:   #to figure out start/end comp
                        if 3 in item[2]:
                            edge1.append([bus,0,comppair[0].dia0[0],bus.start[1]])
                    elif bus.comps[1].compID == comppair[0].compID:
                        if 3 in item[3]:
                            edge1.append([bus,1,comppair[0].dia0[0],bus.end[1]])
                
                if item[1] in comppair[1].buslist:
                    bus = buslist[item[1]]
                    
                    if bus.comps[0].compID == comppair[1].compID:   #to figure out start/end comp
                        if 1 in item[2]:
                            edge2.append([bus,0,comppair[1].dia1[0],bus.start[1]])
                    elif bus.comps[1].compID == comppair[1].compID:
                        if 1 in item[3]:
                            edge2.append([bus,1,comppair[1].dia1[0],bus.end[1]])                                                   
    if dir == 0 or dir ==2:
        type = 0
        nb0 = 0
        edge1.sort(key= lambda x:x[2])  #may change edge unit from list to tuple 
        edge2.sort(key= lambda x:x[2])
        for net in edge1:
            busid = net[0]
            ids = [buslist[busid].comps[1].compID,buslist[busid].comps[0].compID]
            if comppair[1].compID not in ids:
                if net[1]:
                    if buslist[busid].end[0] >= buslist[busid].start[0]:
                        nb0 +=1
                else:
                    if buslist[busid].end[0] < buslist[busid].start[0]:
                        nb0 +=1
        for net in edge2:
            busid = net[0]
            ids = [buslist[busid].comps[1].compID,buslist[busid].comps[0].compID]
            if comppair[0].compID not in ids:
                if net[1]:
                    if buslist[busid].end[0] >= buslist[busid].start[0]:
                        nb0 +=1
                else:
                    if buslist[busid].end[0] < buslist[busid].start[0]:
                        nb0 +=1





    if dir == 1 or dir ==3:
        type = 1
        nb0 = 0
        edge1.sort(key= lambda x:x[3])
        edge2.sort(key= lambda x:x[3])
        for net in edge1:
            busid = net[0]
            ids = [buslist[busid].comps[1].compID,buslist[busid].comps[0].compID]
            if comppair[1].compID not in ids:
                if net[1]:
                    if buslist[busid].end[1] >= buslist[busid].start[1]:
                        nb0 +=1
                else:
                    if buslist[busid].end[1] < buslist[busid].start[1]:
                        nb0 +=1
        for net in edge2:
            busid = net[0]
            ids = [buslist[busid].comps[1].compID,buslist[busid].comps[0].compID]
            if comppair[0].compID not in ids:
                if net[1]:
                    if buslist[busid].end[1] >= buslist[busid].start[1]:
                        nb0 +=1
                else:
                    if buslist[busid].end[1] < buslist[busid].start[1]:
                        nb0 +=1
    
    vitualwall = findwall2(comppair,edge1, edge2,type)
    return vitualwall


def findwall(comppair,edge1,edge2,walls,nb0,type):  #walls must be null list.  type ==0 horizontal/ ==1 vertical
    
    if not (edge1 or edge2):
        return min 
    else:
        e1 = copy.deepcopy(edge1)
        e2 = copy.deepcopy(edge2)
        v1 = e1[0]
        v2 = e2[0]
        bus1 = v1[0]
        bus2 = v2[0]
        if type == 0:
            if v1[1]:                    
                if v1[1] and buslist[bus1].end[0] >= buslist[bus1].start[0]:
                    pass
                if buslist[bus1].end[0] < buslist[bus1].start[0]:
                    pass
                if bus1 == bus2:
                    del e1[0]
                    del e2[0]
    pass 

def findwall2(comppair,edge1,edge2,type):
    for a in range(len(edge1)): #a,b to the west or south of actual indexed point
        for b in range(len(edge2)):
            cross = 0 
            min = float('inf')
            if type == 0:
                crossbus = []
                for i,item1 in enumerate(edge1):
                    for j,item2 in enumerate(edge2):
                        if i < a :
                            if item1[1] == 0:
                                if not item1[0].comps[1].compID == comppair[1].compID:  #global
                                    if  item1[0].end[0] >= item1[0].start[0]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                                else:  #locaal
                                    if  item1[0].end[0] >= edge2[b][2]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                            else:
                                if not item1[0].comps[0].compID == comppair[1].compID:  #global
                                    if  item1[0].start[0] >= item1[0].end[0]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                                else:  #locaal
                                    if  item1[0].start[0] >= edge2[b][2]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                        else:
                            if item1[1] == 0:
                                if not item1[0].comps[1].compID == comppair[1].compID:  #global
                                    if  item1[0].end[0] < item1[0].start[0]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                                else:  #locaal
                                    if  item1[0].end[0] < edge2[b][2]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                            else:
                                if not item1[0].comps[0].compID == comppair[1].compID:  #global
                                    if  item1[0].start[0] < item1[0].end[0]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                                else:  #locaal
                                    if  item1[0].start[0] < edge2[b][2]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                        if j < b :
                            if item2[1] == 0:
                                if not item2[0].comps[1].compID == comppair[0].compID:  #global
                                    if  item2[0].end[0] >= item2[0].start[0]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                                else:  #locaal
                                    if  item2[0].end[0] >= edge2[a][2]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                            else:
                                if not item2[0].comps[0].compID == comppair[0].compID:  #global
                                    if  item2[0].start[0] >= item2[0].end[0]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                                else:  #locaal
                                    if  item2[0].start[0] >= edge2[a][2]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                        else:
                            if item2[1] == 0:
                                if not item2[0].comps[1].compID == comppair[0].compID:  #global
                                    if  item2[0].end[0] < item2[0].start[0]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                                else:  #locaal
                                    if  item2[0].end[0] < edge2[a][2]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                            else:
                                if not item2[0].comps[0].compID == comppair[0].compID:  #global
                                    if  item2[0].start[0] < item2[0].end[0]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                                else:  #locaal
                                    if  item2[0].start[0] < edge2[a][2]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
            elif type ==1:
                crossbus = []
                for i,item1 in enumerate(edge1):
                    for j,item2 in enumerate(edge2):
                        if i < a :
                            if item1[1] == 0:
                                if not item1[0].comps[1].compID == comppair[1].compID:  #global
                                    if  item1[0].end[1] >= item1[0].start[1]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                                else:  #locaal
                                    if  item1[0].end[1] >= edge2[b][3]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                            else:
                                if not item1[0].comps[0].compID == comppair[1].compID:  #global
                                    if  item1[0].start[1] >= item1[0].end[1]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                                else:  #locaal
                                    if  item1[0].start[1] >= edge2[b][3]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                        else:
                            if item1[1] == 0:
                                if not item1[0].comps[1].compID == comppair[1].compID:  #global
                                    if  item1[0].end[1] < item1[0].start[1]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                                else:  #locaal
                                    if  item1[0].end[1] < edge2[b][3]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                            else:
                                if not item1[0].comps[0].compID == comppair[1].compID:  #global
                                    if  item1[0].start[1] < item1[0].end[1]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                                else:  #locaal
                                    if  item1[0].start[1] < edge2[b][3]:
                                        cross +=1
                                        crossbus.append(item1[0].busID)
                        if j < b :
                            if item2[1] == 0:
                                if not item2[0].comps[1].compID == comppair[0].compID:  #global
                                    if  item2[0].end[1] >= item2[0].start[1]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                                else:  #locaal
                                    if  item2[0].end[1] >= edge2[a][3]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                            else:
                                if not item2[0].comps[0].compID == comppair[0].compID:  #global
                                    if  item2[0].start[1] >= item2[0].end[1]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                                else:  #locaal
                                    if  item2[0].start[1] >= edge2[a][3]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                        else:
                            if item2[1] == 0:
                                if not item2[0].comps[1].compID == comppair[0].compID:  #global
                                    if  item2[0].end[1] < item2[0].start[1]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                                else:  #locaal
                                    if  item2[0].end[1] < edge2[a][3]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                            else:
                                if not item2[0].comps[0].compID == comppair[0].compID:  #global
                                    if  item2[0].start[1] < item2[0].end[1]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)
                                else:  #locaal
                                    if  item2[0].start[1] < edge2[a][3]:
                                        cross +=1
                                        crossbus.append(item2[0].busID)

        if cross<= min:
            min = cross
            w1 = a
            w2 = b
            crossbus_real = crossbus
    point1 = [edge1[w1][2],edge1[w1][3]]
    point2 = [edge2[w2][2],edge2[w2][3]]

    wall = VitualWall(point1,point2,comppair[0],comppair[1],min,crossbus_real)  #to the left of two points
    return wall
        
'''
minimum spanning tree
'''
class MGragh:
    def __init__(self,vertex, edge): #edge [vw,weight]
        self.v = vertex
        self.e = edge.sort(key= lambda x:x[1])


def Find(parent, f):
    while( parent[f] > 0 ):
        f = parent[f]
    return f
 


def MiniSpanTree_Kruskal(G:MGragh):
    parent = [0 for _ in range(len(G.v))]
    e_count = 0
    edges = G.e
    actualwall =[]

    for i in range(len(G.e)):
        n = Find(parent, edges[i][0].comppair[0].compID)
        m = Find(parent, edges[i][0].comppair[1].compID)
        if m!=n:
            parent[n] = m
            actualwall.append(edges[i][0])
            e_count +=1
            if e_count == (len(G.e)-1) :
                break
    return actualwall


def CriticalPoint(actualwalls,comps_dir): #return sorted index of edge points of all walls 
    comps=[[[] for _ in range(4)] for _ in range(len(comp_list))]

    for wall in actualwalls:
        dir1 = isadjacent(wall.comps)
        dir2 = dir1+2 if dir1+2<4 else dir1-2
        comp1 = wall.comps[0]
        comp2 = wall.comps[1]
        for i,point in enumerate(comps_dir[comp1.compID][dir1]):
            if wall.points[0] == point:
                comps[comp1.compID][dir1].extend([i])
        for i,point in enumerate(comps_dir[comp2.compID][dir2]):
            if wall.points[2] == point:
                comps[comp2.compID][dir2].extend([i])
    cpts_in_comps = []
    
    for comp in comps:
        temp =[]
        for dir in range(4):
            pts =  comp[dir].sort()
            temp.extend(pts)
        cpts_in_comps.append(temp)

    return cpts_in_comps
            
        


def constructcircle(complist,directions, comps_dir):
    vw_list = []
    for i in range(len(complist)):
        for j in range(i+1,len(complist)):
            comppair = [complist[i], complist[j]]
            vw = localminimization(comppair, directions)
            if vw is not None:
                vw_list.append([vw, vw.nb])

    gragh = MGragh(comp_list, vw_list)
    MST = MiniSpanTree_Kruskal(gragh)
    FanoutsCircle =[]
    cpts = CriticalPoint(MST,comps_dir)
    if len(cpts[0]) ==1:
        split0 = split1(cpts,comps_dir,0)
    else:
        split0,_ = split2(cpts,comps_dir,0)
    
    FanoutsCircle.append(split0)

    
            

        

    return FanoutsCircle
        

def edge_switch(edgenum,shift):
    if edgenum+shift >3:
        return edgenum +shift -4
    else:
        return edgenum+shift
        
def split1(criticalpoints,comps_dir,compid):
    split =[]
    for i,point in enumerate(criticalpoints):
        if i == compid and len(point) == 1:
            dir = point[0]
            index = point[1]
            split.append(comps_dir[i][dir][index])
            count = 0
            for x in range(index+1,len(comps_dir[i][dir])):
                split.append(comps_dir[i][dir][x])

            for count in range(1,4):
                m = edge_switch(index,count)
                for item in comps_dir[i][m]:
                    split.append(item)

            for y in range(0,index):
                split.append(comps_dir[i][dir][y])
            return split
        else: return None
def split2(criticalpoints,comps_dir,compid):
    split1 =[]
    split2 =[]
    for i,point in enumerate(criticalpoints):
        if i == compid and len(point) == 2:
            dir1 = point[0][0]
            index1 = point[0][1]
            dir2 = point[1][0]
            index2 = point[1][1]
            maxcount = dir2 -dir1
            for x in range(index1,len(comps_dir[i][dir1])):
                split1.append(comps_dir[i][dir1][x])

            for count in range(1,maxcount):
                m = edge_switch(dir1,count)
                for item in comps_dir[i][m]:
                    split1.append(item)

            for y in range(0,index1):
                split1.append(comps_dir[i][dir2][y])
        
            for x in range(index2,len(comps_dir[i][dir2])):
                split2.append(comps_dir[i][dir2][x])

            for count in range(1,4-maxcount):
                m = edge_switch(dir2,count)
                for item in comps_dir[i][m]:
                    split2.append(item)

            for y in range(0,index2):
                split2.append(comps_dir[i][dir2][y])
            
            return [split1,split2]


        else: return None
def split(criticalpoints,comps_dir,compid):
            i = compid
            point = criticalpoints[i]
            split= [[] for _ in range(len(point))]          
            for x in range(0,len(point) - 1):
                dir1 = point[x][0]
                index1 = point[x][1]
                dir2 = point[x+1][0]
                index2 = point[x+1][1]
                maxcount = dir2 -dir1

                if maxcount == 0:
                    split[x] = comps_dir[i][dir1][index1:index2-1]
                    
                else:
                    split[x] = comps_dir[i][dir1][index1:]
                    for count in range(1,maxcount):
                        m = edge_switch(dir1,count)
                        for item in comps_dir[i][m]:
                            split[x].extend(item)
                    split[x].extend(comps_dir[i][dir2][0:index2])
            dir_end = point[len(point) - 1][0]
            index_end = point[len(point) - 1][1]
            dir_0 = point[0][0]
            index_0 = point[0][1]
            split[-1]=comps_dir[i][dir_end][index_end:]
            maxcount = dir_end - dir_0
            for count in range(1,4-maxcount):
                m = edge_switch(dir_end,count)
                for item in comps_dir[i][m]:
                    split[-1].extend(item)
            split[-1].extend(comps_dir[i][dir_0][0:index_0])
            return split




    
if __name__ == '__main__':
    Bsize_x = 1000
    Bsize_y = 1000
    packagenum = 1
    busnum = 15
    compnum = 5
    comppair_in_bus = {}
    buslist_in_comp = {}
    comps_in_pkg = {}

    pkg_of_com = []
    for i in range(compnum):
        buslist_in_comp[i] = []
        index = random.randint(0,packagenum - 1)
        pkg_of_com.append(index)


    
    for i in range(busnum):
        comppair_in_bus[i] = []

    pkg_dialist = []
    for i in range(packagenum):
        comps_in_pkg[i] = []
        dia0 = [random.randint(0,Bsize_x-1),random.randint(0,Bsize_y-1)]
        base = int(Bsize_x/100)
        #edge_length = random.randint(base, base + min(Bsize_x-dia0[0], Bsize_y-dia0[1]))
        edge_length = int((Bsize_x+Bsize_y)/(2*packagenum))
#        dia1 = [dia0[0] + random.randint(0,Bsize_x - dia0[0]), dia0[1] + random.randint(0,Bsize_y - dia0[1])]
        dia1 = [dia0[0] + edge_length, dia0[1] + edge_length]
        Legalization2(pkg_dialist,[dia0, dia1],[[0,0],[Bsize_x, Bsize_y]], edge_length,packagenum)







    for i in range(busnum):
        index = random.sample(range(0,compnum),2)
        a = index[0]#startcmop
        b = index[1]#endcomp
        buslist_in_comp[a].append(i)
        buslist_in_comp[b].append(i)
        comppair_in_bus[i].append(index)
    
    dialist = []
    comp_list = []
    for i in range(compnum):
        pkgindex = pkg_of_com[i]
        pkgsize_x = pkg_dialist[pkgindex][1][0] - pkg_dialist[pkgindex][0][0]
        pkgsize_y = pkg_dialist[pkgindex][1][1] - pkg_dialist[pkgindex][0][1]
        comp_base = int((pkgsize_x + pkgsize_y)/200)
        dia0 = [random.randint(pkg_dialist[pkgindex][0][0], pkg_dialist[pkgindex][1][0]), random.randint(pkg_dialist[pkgindex][0][1], pkg_dialist[pkgindex][1][1])]
        #comp_edge = random.randint(comp_base, comp_base + min(pkg_dialist[pkgindex][1][0] - dia0[0], pkg_dialist[pkgindex][1][1] - dia0[1]))
        comp_edge = int((pkgsize_x +pkgsize_y)/(2*compnum))
#        dia1 = [dia0[0] + random.randint(0,pkg_dialist[pkgindex][1][0] - dia0[0]), dia0[1] + random.randint(0,pkg_dialist[pkgindex][1][1] - dia0[1])]
        dia1 = [dia0[0] + comp_edge, dia0[1] + comp_edge]
        Legalization2(dialist,[dia0, dia1],pkg_dialist[pkgindex], comp_edge, compnum)
        dia0 = dialist[i][0]
        dia1 = dialist[i][1]        
        comp = Component(dia0, dia1, buslist_in_comp[i], i)
        comp_list.append(comp)
        temp = pkg_of_com[i]
        comps_in_pkg[temp].append(comp)

    buslist=[]
    for i in range(busnum):
        start_comp = comppair_in_bus[i][0][0]
        end_comp = comppair_in_bus[i][0][1]
        start_x =  random.randint(comp_list[start_comp].dia0[0], comp_list[start_comp].dia1[0])
        end_x =  random.randint(comp_list[end_comp].dia0[0], comp_list[end_comp].dia1[0])
        start_y =  random.randint(comp_list[start_comp].dia0[1], comp_list[start_comp].dia1[1])
        end_y =  random.randint(comp_list[end_comp].dia0[1], comp_list[end_comp].dia1[1])
        bus = Bus(i, [comp_list[start_comp], comp_list[end_comp]], [start_x, start_y], [end_x, end_y])
        buslist.append(bus)

    packagelist = []
    for i in range(packagenum):
        dia0 = pkg_dialist[i][0]
        dia1 = pkg_dialist[i][1]
        pkg = Package(comps_in_pkg[i], dia0, dia1, i)
        packagelist.append(pkg) 



assigner = LayerAssigner(packagelist)
directions = assigner.EscapeOptimize()
pic = Drawer(packagelist,buslist)
pic.draw(Bsize_x, Bsize_y,directions)




        
        



    





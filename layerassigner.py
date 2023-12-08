from ast import Pass
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
    def __init__(self,point1, point2, comp1, comp2, nb):
        self.comps = [comp1,comp2]
        self.point = [point1,point2]
        self.nb = nb

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


def localminimization(comppair, directions) -> VitualWall:
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
                    
                    if bus.comps[0].compID == comppair[0].compID:   #to figure out start/end comp
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
    for 

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
                if buslist[bus1].end[0] >= buslist[bus1].start[0]:
                    
            else:
                if buslist[bus1].end[0] < buslist[bus1].start[0]:
            
            if bus1 == bus2:
                e1.del()
                e2.del




    
    



    
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




        
        



    





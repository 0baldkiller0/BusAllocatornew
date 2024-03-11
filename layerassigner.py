
from enum import EnumType
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
        directions.sort(key = lambda x:x[1])
        return directions
    
    def sort_by_dir(self,comp_list):
        for package in self.PackageList:
            directions = []
            comps_dir = []
            component = [{} for _ in range(len(comp_list))]
            for i in range(len(comp_list)):
                
                component[i][0] = []
                component[i][1] = []
                component[i][2] = []
                component[i][3] = []
            for comp in package.comps:
                for busindex in comp.buslist:
                    bus = buslist[busindex]
                    comp1 = bus.comps[0].compID
                    comp2 = bus.comps[1].compID
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
                    if comp.compID == comp1:

                        if 0 in dir1 :
                            component[comp1][0].append([bus.BusID,[bus.start[0],comp.dia1[1]],0])
                        if 1 in dir1 :
                            component[comp1][1].append([bus.BusID,[comp.dia1[0],bus.start[1]],0])
                        if 2 in dir1 :
                            component[comp1][2].append([bus.BusID,[bus.start[0],comp.dia0[1]],0])
                        if 3 in dir1 :
                            component[comp1][3].append([bus.BusID,[comp.dia0[0],bus.start[1]],0])
                    if comp.compID == comp2:
                    
                        if 0 in dir2 :
                            component[comp2][0].append([bus.BusID,[bus.end[0],comp.dia1[1]],1])
                        if 1 in dir2 :
                            component[comp2][1].append([bus.BusID,[comp.dia1[0],bus.end[1]],1])
                        if 2 in dir2 :
                            component[comp2][2].append([bus.BusID,[bus.end[0],comp.dia0[1]],1])
                        if 3 in dir2 :
                            component[comp2][3].append([bus.BusID,[comp.dia0[0],bus.end[1]],1])

            for i in range(len(comp_list)):
            
                component[i][0].sort(key = lambda x:x[1][0])
                component[i][1].sort(key = lambda x:x[1][1],reverse=True)
                component[i][2].sort(key = lambda x:x[1][0],reverse=True)
                component[i][3].sort(key = lambda x:x[1][1])
            comps_dir = component
        return comps_dir
    




    def EscapePairs(self,buslist):
        escapepairs = []
        dirs = self.EscapeOptimize()
        for dir in dirs:
            bus = buslist[dir[1]]
            temp = [dir[1]]
            dir1 =  dir[2]
            dir2 =  dir[3]
            for i in dir1:
                for j in dir2:
                    temp.append([i,j])

            if (len(dir1) == 2) and (len(dir2) == 2):
                d = edgeoverlap(bus.comps[0],bus.comps[1])
                if  d!=4:
                    if [edge_switch(d,1),edge_switch(d,3)] in temp:
                        temp.remove([edge_switch(d,1),edge_switch(d,3)])
                    if [edge_switch(d,3),edge_switch(d,1)] in temp:
                        temp.remove([edge_switch(d,3),edge_switch(d,1)])
            escapepairs.append(temp)
        return escapepairs



                

            


    
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
                    plt.text(comp.dia0[0], comp.dia0[1], s=j, c='g')
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

                        
            

        def draw_walls(self,vws):
            for vw in vws:
                p0 = vw.points[0]
                p1 = vw.points[1]
                if vw.comps[0] is None:
                    id1 = -1
                else:
                    id1 = vw.comps[0].compID
                if vw.comps[1] is None:
                    id2 = -1
                else:
                    id2 = vw.comps[1].compID
                
                plt.plot([p0[0],p1[0]], [p0[1],p1[1]], 'r',linewidth = 0.5, alpha= 1)
                plt.text(p0[0],p0[1],s='{},{}'.format(id1,id2))
                plt.text(p0[0]/2 +p1[0]/2,p0[1]/2 +p1[1]/2,s='{}'.format(vw.nb))
                

        def show(self):
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




def comps_dirbus(comps_dir):
    comps_dirbus = [{} for _ in range(len(comps_dir))]
    for i in range(len(comps_dir)):
        
        comps_dirbus[i][0] = []
        comps_dirbus[i][1] = []
        comps_dirbus[i][2] = []
        comps_dirbus[i][3] = []
    for m in range(len(comps_dir)):
        for n in range(4):
            for item in comps_dir[m][n]:
                comps_dirbus[m][n].append(item[0])

    return comps_dirbus


def add_points(actualwalls,comps_dir):
    comps_dir2 = copy.deepcopy(comps_dir)
    pt_in_v0 = [[] for _ in range(4)]
    for wall in actualwalls:
        point1 = wall.points[1]#point on boardboundary can only in points[1]
        comp1 = wall.comps[1]
        if point1[1] == comp1.dia1[1]:
            dir = 0
        elif point1[0] == comp1.dia1[0]:                                         
            dir = 1
        elif point1[1] == comp1.dia0[1]:
            dir = 2
        elif point1[0] == comp1.dia0[0]:
            dir = 3
        if comp1.compID == len(comps_dir):
            pt_in_v0[dir].append([-1,point1,-1])
    
        else:
            if len(comps_dir[comp1.compID][dir]) == 0:
                comps_dir2[comp1.compID][dir].append([[-1,point1,-1]])
    pt_in_v0[0].sort(key = lambda x:x[1][0],reverse=True)
    pt_in_v0[1].sort(key = lambda x:x[1][1],reverse=False)
    pt_in_v0[2].sort(key = lambda x:x[1][0],reverse=False)
    pt_in_v0[3].sort(key = lambda x:x[1][1],reverse=True)
    comps_dir2.append(pt_in_v0)
    return comps_dir2
                






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
        self.points = [point1,point2]
        self.nb = nb
        self.crossbus = crossbus
def isadjacent(comppair)->int: #TODO consider other comp between comppair (over)
    comp1 = comppair[0]
    comp2 = comppair[1]
    if (comp2.dia0[0]>=comp1.dia1[0]) and comp2.dia0[1] < comp1.dia1[1] and comp2.dia1[1] > comp1.dia0[1]:
        dir = 1
    elif (comp2.dia1[1]<=comp1.dia0[1]) and comp2.dia0[0] < comp1.dia1[0] and comp2.dia1[0] > comp1.dia0[0]:
        dir = 2
    elif (comp2.dia1[0]<=comp1.dia0[0]) and comp2.dia0[1] < comp1.dia1[1] and comp2.dia1[1] > comp1.dia0[1]:
        dir = 3
    elif (comp2.dia0[1]>=comp1.dia1[1]) and comp2.dia0[0] < comp1.dia1[0] and comp2.dia1[0] > comp1.dia0[0]:
        dir = 0
    else:
        return 4 
    flag = 0
    for comp in comp_list: 
        dias = [comp.dia0, comp.dia1]
        if dir == 0:
            if comp2.dia1[0] <= comp1.dia1[0]:
                if comp2.dia0[0] <= comp1.dia0[0]:
                    zone = [[comp1.dia0[0],comp1.dia1[1]],[comp2.dia1[0],comp2.dia0[1]]]
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
                    zone = [[comp1.dia1[0],comp1.dia0[1]],[comp2.dia0[0],comp2.dia1[1]]]
                else:
                    zone = [[comp1.dia1[0],comp2.dia0[1]],[comp2.dia0[0],comp2.dia1[1]]]
            else:
                if comp2.dia0[1] <= comp1.dia0[1]:
                    zone = [[comp1.dia1[0],comp1.dia0[1]],[comp2.dia0[0],comp1.dia1[1]]]
                else:
                    zone = [[comp1.dia1[0],comp2.dia0[1]],[comp2.dia0[0],comp1.dia1[1]]]
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
            flag = 1
    if flag:
        return 4           
    else:
        return dir
def edgeoverlap(comppair)->int:
    comp1 = comppair[0]
    comp2 = comppair[1]
    if (comp2.dia0[0]>=comp1.dia1[0]) and comp2.dia0[1] < comp1.dia1[1] and comp2.dia1[1] > comp1.dia0[1]:
        return 1
    elif (comp2.dia1[1]<=comp1.dia0[1]) and comp2.dia0[0] < comp1.dia1[0] and comp2.dia1[0] > comp1.dia0[0]:
        return 2
    elif (comp2.dia1[0]<=comp1.dia0[0]) and comp2.dia0[1] < comp1.dia1[1] and comp2.dia1[1] > comp1.dia0[1]:
        return 3
    elif (comp2.dia0[1]>=comp1.dia1[1]) and comp2.dia0[0] < comp1.dia1[0] and comp2.dia1[0] > comp1.dia0[0]:
        return 0
    else:
        return 4         

def to_boundary(comp,comp_list,pkg):

    bdys = [0,1,2,3]
    for component in comp_list:
        if isoverlap([[comp.dia0[0],comp.dia1[1]],[comp.dia1[0],pkg.dia1[1]]], [component.dia0,component.dia1]):
            if 0 in bdys:
                bdys.remove(0)
        if isoverlap([[comp.dia1[0],comp.dia0[1]],[pkg.dia1[0],comp.dia1[1]]], [component.dia0,component.dia1]):
            if 1 in bdys:
                bdys.remove(1)
        if isoverlap([[comp.dia0[0],pkg.dia0[1]],[comp.dia1[0],comp.dia0[1]]], [component.dia0,component.dia1]):
            if 2 in bdys:
                bdys.remove(2)
        if isoverlap([[pkg.dia0[0],comp.dia0[1]],[comp.dia0[0],comp.dia1[1]]], [component.dia0,component.dia1]):
            if 3 in bdys:
                bdys.remove(3)
    return bdys




        



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
            busid = net[0].BusID
            ids = [buslist[busid].comps[1].compID,buslist[busid].comps[0].compID]
            if comppair[1].compID not in ids:
                if net[1]:
                    if buslist[busid].end[0] >= buslist[busid].start[0]:
                        nb0 +=1
                else:
                    if buslist[busid].end[0] < buslist[busid].start[0]:
                        nb0 +=1
        for net in edge2:
            busid = net[0].BusID
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
            busid = net[0].BusID
            ids = [buslist[busid].comps[1].compID,buslist[busid].comps[0].compID]
            if comppair[1].compID not in ids:
                if net[1]:
                    if buslist[busid].end[1] >= buslist[busid].start[1]:
                        nb0 +=1
                else:
                    if buslist[busid].end[1] < buslist[busid].start[1]:
                        nb0 +=1
        for net in edge2:
            busid = net[0].BusID
            ids = [buslist[busid].comps[1].compID,buslist[busid].comps[0].compID]
            if comppair[0].compID not in ids:
                if net[1]:
                    if buslist[busid].end[1] >= buslist[busid].start[1]:
                        nb0 +=1
                else:
                    if buslist[busid].end[1] < buslist[busid].start[1]:
                        nb0 +=1
    
    vitualwall = findwall3(comppair,edge1, edge2,type)
    return vitualwall
def localminimization2(comp_dirs, comp1, comp2):
    dir = isadjacent([comp1,comp2])
    if dir == 4:
        return None
    else:
        wall =findwall3(comp_dirs,comp1,dir,comp2)

    return wall

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

def findwall2(comppair,edge1,edge2,dir):
    if dir == 0 or dir == 2:
        type = 0
    elif dir == 1 or dir == 3:
        type = 1
    
    comp1 = comppair[0]
    comp2 = comppair[1]

    if edge1 is None:

        flag1 = 1
        if dir == 0:
            point1 = [comp1.dia0[0]/2 +comp1.dia1[0]/2 ,comp1.dia1[1]]
        if dir == 1:
            point1 = [comp1.dia1[0],comp1.dia0[1]/2 +comp1.dia1[1]/2 ]
        if dir == 2:
            point1 = [comp1.dia0[0]/2 +comp1.dia1[0]/2 ,comp1.dia0[1]]
        if dir == 3:
            point1 = [comp1.dia0[0],comp1.dia0[1]/2 +comp1.dia1[1]/2 ]

    else:
        flag1 = 0

        
    if edge2 is None:

        flag2 = 1
        if dir == 0:
            point2 = [comp2.dia0[0]/2 +comp2.dia1[0]/2 ,comp2.dia0[1]]
        if dir == 1:
            point2 = [comp2.dia0[0],comp2.dia0[1]/2 +comp2.dia1[1]/2 ]
        if dir == 2:
            point2 = [comp2.dia0[0]/2 +comp2.dia1[0]/2 ,comp2.dia1[1]]
        if dir == 3:
            point2 = [comp2.dia1[0],comp2.dia0[1]/2 +comp2.dia1[1]/2 ]
    else:
        flag2 = 0

    


    

    for a in range(1 if flag1 else len(edge1)): #a,b to the west or south of actual indexed point
        for b in range(1 if flag2 else len(edge2)):
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
                                        crossbus.append(item1[0].BusID)
                                else:  #locaal
                                    if  item1[0].end[0] >= edge2[b][2]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                            else:
                                if not item1[0].comps[0].compID == comppair[1].compID:  #global
                                    if  item1[0].start[0] >= item1[0].end[0]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                                else:  #locaal
                                    if  item1[0].start[0] >= edge2[b][2]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                        else:
                            if item1[1] == 0:
                                if not item1[0].comps[1].compID == comppair[1].compID:  #global
                                    if  item1[0].end[0] < item1[0].start[0]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                                else:  #locaal
                                    if  item1[0].end[0] < edge2[b][2]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                            else:
                                if not item1[0].comps[0].compID == comppair[1].compID:  #global
                                    if  item1[0].start[0] < item1[0].end[0]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                                else:  #locaal
                                    if  item1[0].start[0] < edge2[b][2]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                        if j < b :
                            if item2[1] == 0:
                                if not item2[0].comps[1].compID == comppair[0].compID:  #global
                                    if  item2[0].end[0] >= item2[0].start[0]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                                else:  #locaal
                                    if  item2[0].end[0] >= edge1[a][2]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                            else:
                                if not item2[0].comps[0].compID == comppair[0].compID:  #global
                                    if  item2[0].start[0] >= item2[0].end[0]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                                else:  #locaal
                                    if  item2[0].start[0] >= edge1[a][2]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                        else:
                            if item2[1] == 0:
                                if not item2[0].comps[1].compID == comppair[0].compID:  #global
                                    if  item2[0].end[0] < item2[0].start[0]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                                else:  #locaal
                                    if  item2[0].end[0] < edge1[a][2]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                            else:
                                if not item2[0].comps[0].compID == comppair[0].compID:  #global
                                    if  item2[0].start[0] < item2[0].end[0]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                                else:  #locaal
                                    if  item2[0].start[0] < edge1[a][2]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
            elif type ==1:
                crossbus = []
                for i,item1 in enumerate(edge1):
                    for j,item2 in enumerate(edge2):
                        if i < a :
                            if item1[1] == 0:
                                if not item1[0].comps[1].compID == comppair[1].compID:  #global
                                    if  item1[0].end[1] >= item1[0].start[1]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                                else:  #locaal
                                    if  item1[0].end[1] >= edge2[b][3]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                            else:
                                if not item1[0].comps[0].compID == comppair[1].compID:  #global
                                    if  item1[0].start[1] >= item1[0].end[1]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                                else:  #locaal
                                    if  item1[0].start[1] >= edge2[b][3]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                        else:
                            if item1[1] == 0:
                                if not item1[0].comps[1].compID == comppair[1].compID:  #global
                                    if  item1[0].end[1] < item1[0].start[1]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                                else:  #locaal
                                    if  item1[0].end[1] < edge2[b][3]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                            else:
                                if not item1[0].comps[0].compID == comppair[1].compID:  #global
                                    if  item1[0].start[1] < item1[0].end[1]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                                else:  #locaal
                                    if  item1[0].start[1] < edge2[b][3]:
                                        cross +=1
                                        crossbus.append(item1[0].BusID)
                        if j < b :
                            if item2[1] == 0:
                                if not item2[0].comps[1].compID == comppair[0].compID:  #global
                                    if  item2[0].end[1] >= item2[0].start[1]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                                else:  #locaal
                                    if  item2[0].end[1] >= edge1[a][3]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                            else:
                                if not item2[0].comps[0].compID == comppair[0].compID:  #global
                                    if  item2[0].start[1] >= item2[0].end[1]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                                else:  #locaal
                                    if  item2[0].start[1] >= edge1[a][3]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                        else:
                            if item2[1] == 0:
                                if not item2[0].comps[1].compID == comppair[0].compID:  #global
                                    if  item2[0].end[1] < item2[0].start[1]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                                else:  #locaal
                                    if  item2[0].end[1] < edge1[a][3]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                            else:
                                if not item2[0].comps[0].compID == comppair[0].compID:  #global
                                    if  item2[0].start[1] < item2[0].end[1]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
                                else:  #locaal
                                    if  item2[0].start[1] < edge1[a][3]:
                                        cross +=1
                                        crossbus.append(item2[0].BusID)
            if cross<= min:
                global w1,w2
                point1,point2
                min = cross
                w1 = a
                w2 = b
                crossbus_real = crossbus
            point1 = [edge1[w1][2],edge1[w1][3]]
            point2 = [edge2[w2][2],edge2[w2][3]]
                
    wall = VitualWall(point1,point2,comppair[0],comppair[1],min,crossbus_real)  #to the left of two points
    return wall


def findwall3(comp_dirs, comp1:Component, dir:int, comp2:Component):
    edge1 = comp_dirs[comp1.compID][dir]
    dir2 = edge_switch(dir,2)
    edge2 = comp_dirs[comp2.compID][dir2]
    if (len(edge1) == 0) and (len(edge2) == 0):
       if dir == 0:
           point1 = [comp1.dia0[0]/2 +comp1.dia1[0]/2 ,comp1.dia1[1]]
           point2 = [comp2.dia0[0]/2 +comp2.dia1[0]/2 ,comp2.dia0[1]]
           wall = VitualWall(point1,point2,comp1,comp2,0,None)
       if dir == 1:
           point1 = [comp1.dia1[0],comp1.dia0[1]/2 +comp1.dia1[1]/2 ]
           point2 = [comp2.dia0[0],comp2.dia0[1]/2 +comp2.dia1[1]/2 ]
           wall = VitualWall(point1,point2,comp1,comp2,0,None)
       if dir == 2:
           point1 = [comp1.dia0[0]/2 +comp1.dia1[0]/2 ,comp1.dia0[1]]
           point2 = [comp2.dia0[0]/2 +comp2.dia1[0]/2 ,comp2.dia1[1]]
           wall = VitualWall(point1,point2,comp1,comp2,0,None)
       if dir == 3:
           point1 = [comp1.dia0[0],comp1.dia0[1]/2 +comp1.dia1[1]/2 ]
           point2 = [comp2.dia1[0],comp2.dia0[1]/2 +comp2.dia1[1]/2 ]
           wall = VitualWall(point1,point2,comp1,comp2,0,None)
        
        

    if (len(edge1) == 0) and (len(edge2) != 0):
        wall = SingleEdge(comp_dirs,comp2,dir2,comp1)
    if (len(edge1) != 0) and (len(edge2) == 0):
        wall = SingleEdge(comp_dirs,comp1,dir,comp2)
    if (len(edge1) != 0) and (len(edge2) != 0):
        wall = DoubleEdge(comp_dirs,comp1,dir,comp2)
    return wall

        

def SingleEdge(comp_dirs, component:Component, dir, component2:Component): #component edge of dir must not be null
    i = component.compID
    min = float('inf')
    if dir == 0 or dir == 2: #with crosswall , no need to consider dir,also in doubleedge
        for a in range(len(comp_dirs[i][dir]) + 1):
            cross = 0 
            crossbus = []
            for j,point in enumerate(comp_dirs[i][dir]):
                #if j<a:
                #    if point[2] == 0:
                #        if  point[1][0] <= buslist[point[0]].end[0]:
                #            cross +=1
                #            crossbus.append(point[0])
                #    elif point[2] == 1:
                #        if  point[1][0] <= buslist[point[0]].start[0]:
                #            cross +=1
                #            crossbus.append(point[0])
                #elif j>=a:
                #    if point[2] == 0:
                #        if  point[1][0] >= buslist[point[0]].end[0]:
                #            cross +=1
                #            crossbus.append(point[0])
                #    elif point[2] == 1:
                #        if  point[1][0] >= buslist[point[0]].start[0]:
                #            cross +=1
                #
                #             crossbus.append(point[0])
                if crosswall2(j,a,dir,point):
                    cross +=1
                    crossbus.append(point[0])
            if cross<= min:
                min = cross
                w = a
                crossbus_real = crossbus
    elif dir == 1 or dir == 3:
        for a in range(len(comp_dirs[i][dir]) + 1):
            cross = 0 
            crossbus = []
            for j,point in enumerate(comp_dirs[i][dir]):
                #if j<a:
                #    if point[2] == 0:
                #        if  point[1][1] <= buslist[point[0]].end[1]:
                #            cross +=1
                #            crossbus.append(point[0])
                #    elif point[2] == 1:
                #        if  point[1][1] <= buslist[point[0]].start[1]:
                #            cross +=1
                #            crossbus.append(point[0])
                #elif j>=a:
                #    if point[2] == 0:
                #        if  point[1][1] >= buslist[point[0]].end[1]:
                #            cross +=1
                #            crossbus.append(point[0])
                #    elif point[2] == 1:
                #        if  point[1][1] >= buslist[point[0]].start[1]:
                #            cross +=1
                #            crossbus.append(point[0])
                if crosswall2(j,a,dir,point):
                    cross +=1
                    crossbus.append(point[0])
            if cross<= min:
                    min = cross
                    w = a
                    crossbus_real = crossbus

    if w ==  len(comp_dirs[i][dir]) :
        point1 = comp_dirs[i][dir][w - 1][1]
    else:
        point1 = comp_dirs[i][dir][w][1]
    
    if dir == 0:
        point2 = [component2.dia0[0]/2 +component2.dia1[0]/2 ,component2.dia0[1]]
    if dir == 1:
        point2 = [component2.dia0[0],component2.dia0[1]/2 +component2.dia1[1]/2 ]
    if dir == 2:
        point2 = [component2.dia0[0]/2 +component2.dia1[0]/2 ,component2.dia1[1]]
    if dir == 3:
        point2 = [component2.dia1[0],component2.dia0[1]/2 +component2.dia1[1]/2 ]
    
    wall = VitualWall(point1,point2,component,component2,min,crossbus_real)
    return wall

def DoubleEdge(comp_dirs, component1:Component, dir, component2:Component): #edge must not be null
    i = component1.compID
    j = component2.compID
    dir2 = edge_switch(dir,2)
    dirbus = comps_dirbus(comp_dirs)
    min = float('inf')
    if dir == 0 or dir == 2:
        for a in range(len(comp_dirs[i][dir]) + 1):
            for b in range(len(comp_dirs[j][dir2]) + 1):
                cross = 0 
                crossbus = []
                for m,point in enumerate(comp_dirs[i][dir]):
                    if crosswall(m,a,b,dir,i,j,point,dirbus):
                        cross +=1
                        crossbus.append(point[0])

                for n, point2 in enumerate(comp_dirs[j][dir2]):
                    if crosswall(n,b,a,dir2,j,i,point2,dirbus):
                        if point[0] not in crossbus:
                            cross +=1
                            crossbus.append(point[0])    
                if cross<= min:
                    min = cross
                    w1 = a
                    w2 = b
                    crossbus_real = crossbus
    elif dir == 1 or dir == 3:
        for a in range(len(comp_dirs[i][dir])+1):
            for b in range(len(comp_dirs[j][dir2])+1):
                cross = 0
                crossbus = []
                for m,point in enumerate(comp_dirs[i][dir]):
                    if crosswall(m,a,b,dir,i,j,point,dirbus):
                        cross +=1
                        crossbus.append(point[0])
                for n, point in enumerate(comp_dirs[j][dir2]):
                    if crosswall(n,b,a,dir2,j,i,point,dirbus):
                        if point[0] not in crossbus:
                            cross +=1
                            crossbus.append(point[0])    
                if cross<= min:
                    min = cross
                    w1 = a
                    w2 = b
                    crossbus_real = crossbus
    if w1 == len(comp_dirs[i][dir]):
        point1 = comp_dirs[i][dir][w1-1][1]
    else:                  
        point1 = comp_dirs[i][dir][w1][1]
    if w2 == len(comp_dirs[j][dir2]):
        point2 = comp_dirs[j][dir2][w2-1][1]
    else:
        point2 = comp_dirs[j][dir2][w2][1]
    wall = VitualWall(point1,point2,component1,component2,min,crossbus_real)
    return wall

def crosswall(m,a,b,dir,comp1,comp2,point,dirbus):
    i = comp1
    j = comp2
    dir2 = edge_switch(dir,2)
    cross = False
    if dir == 1 or dir == 2:
        reverse = True
    else:
        reverse = False
    if dir == 0 or dir == 2:
        d = 0
    elif dir == 1 or dir == 3:
        d = 1

    if not reverse:
        if m<a:
            if j not in [buslist[point[0]].comps[0].compID, buslist[point[0]].comps[1].compID]:
                if point[2] == 0:
                    if  point[1][d] <= buslist[point[0]].end[d]:
                        cross = True
                elif point[2] == 1:
                    if  point[1][d] <= buslist[point[0]].start[d]:
                        cross = True
            else:
                if point[0] not in dirbus[j][dir2]:
                    if point[2] == 0:
                        if  point[1][d] <= buslist[point[0]].end[d]:
                            cross = True
                    elif point[2] == 1:
                        if  point[1][d] <= buslist[point[0]].start[d]:
                            cross = True
                else:
                    if dirbus[j][dir2].index(point[0]) < b:
                        cross = True
                    
        elif m>=a:  #to the right or top of a
            if j not in [buslist[point[0]].comps[0].compID, buslist[point[0]].comps[1].compID]:
                if point[2] == 0:
                    if  point[1][d] >= buslist[point[0]].end[d]:
                        cross = True
                elif point[2] == 1:
                    if  point[1][d] >= buslist[point[0]].start[d]:
                        cross = True
            else:
                if point[0] not in dirbus[j][dir2]:
                    if point[2] == 0:
                        if  point[1][d] >= buslist[point[0]].end[d]:
                            cross = True
                    elif point[2] == 1:
                        if  point[1][d] >= buslist[point[0]].start[d]:
                            cross = True
                else:
                    if dirbus[j][dir2].index(point[0]) >= b:
                        cross = True
    else:
        if m<a:   #to the right or top of a
            if j not in [buslist[point[0]].comps[0].compID, buslist[point[0]].comps[1].compID]:
                if point[2] == 0:
                    if  point[1][d] >= buslist[point[0]].end[d]:
                        cross = True
                elif point[2] == 1:
                    if  point[1][d] >= buslist[point[0]].start[d]:
                        cross = True
            else:
                if point[0] not in dirbus[j][dir2]:
                    if point[2] == 0:
                        if  point[1][d] >= buslist[point[0]].end[d]:
                            cross = True
                    elif point[2] == 1:
                        if  point[1][d] >= buslist[point[0]].start[d]:
                            cross = True
                else:
                    if dirbus[j][dir2].index(point[0]) < b:
                        cross = True
                    
        elif m>=a:
            if j not in [buslist[point[0]].comps[0].compID, buslist[point[0]].comps[1].compID]:
                if point[2] == 0:
                    if  point[1][d] <= buslist[point[0]].end[d]:
                        cross = True
                elif point[2] == 1:
                    if  point[1][d] <= buslist[point[0]].start[d]:
                        cross = True
            else:
                if point[0] not in dirbus[j][dir2]:
                    if point[2] == 0:
                        if  point[1][d] <= buslist[point[0]].end[d]:
                            cross = True
                    elif point[2] == 1:
                        if  point[1][d] <= buslist[point[0]].start[d]:
                            cross = True
                else:
                    if dirbus[j][dir2].index(point[0]) >= b:
                        cross = True
    return cross


        
    


def find_bdwall(component, comp_dirs,comp_list,pkg):
    dirs = to_boundary(component,comp_list,pkg)
    bdwalls = []
    w=0
    i = component.compID
    for dir in dirs:
        if len(comp_dirs[i][dir]) == 0:
            w = 0
            cross = 0
            min = 0
            crossbus_real = []
            if dir == 0:
                point1 = [component.dia0[0]/2 +component.dia1[0]/2 ,component.dia1[1]]
            if dir == 1:
                point1 = [component.dia1[0],component.dia0[1]/2 +component.dia1[1]/2 ]
            if dir == 2:
                point1 = [component.dia0[0]/2 +component.dia1[0]/2 ,component.dia0[1]]
            if dir == 3:
                point1 = [component.dia0[0],component.dia0[1]/2 +component.dia1[1]/2 ]
        else:
            min = float('inf')
            if dir == 0 or dir == 2:
                for a in range(len(comp_dirs[i][dir])+1):
                    cross = 0 
                    crossbus = []
                    for j,point in enumerate(comp_dirs[i][dir]):
                        #if j<a:
                        #    if point[2] == 0:
                        #        if  point[1][0] <= buslist[point[0]].end[0]:
                        #            cross +=1
                        #            crossbus.append(point[0])
                        #    elif point[2] == 1:
                        #        if  point[1][0] <= buslist[point[0]].start[0]:
                        #            cross +=1
                        #            crossbus.append(point[0])
                        #elif j>=a:
                        #    if point[2] == 0:
                        #        if  point[1][0] >= buslist[point[0]].end[0]:
                        #            cross +=1
                        #            crossbus.append(point[0])
                        #    elif point[2] == 1:
                        #        if  point[1][0] >= buslist[point[0]].start[0]:
                        #            cross +=1
                        #            crossbus.append(point[0])
                        if crosswall2(j,a,dir,point):
                            cross +=1
                            crossbus.append(point[0])
                    if cross<= min:
                        min = cross
                        w = a
                        crossbus_real = crossbus

            if dir == 1 or dir == 3:
                for a in range(len(comp_dirs[i][dir])+1):
                    cross = 0 
                    crossbus = []
                    for j,point in enumerate(comp_dirs[i][dir]):
                        #if j<a:
                        #    if point[2] == 0:
                        #        if  point[1][1] <= buslist[point[0]].end[1]:
                        #            cross +=1
                        #            crossbus.append(point[0])
                        #    elif point[2] == 1:
                        #        if  point[1][1] <= buslist[point[0]].start[1]:
                        #            cross +=1
                        #            crossbus.append(point[0])
                        #elif j>=a:
                        #    if point[2] == 0:
                        #        if  point[1][1] >= buslist[point[0]].end[1]:
                        #            cross +=1
                        #            crossbus.append(point[0])
                        #    elif point[2] == 1:
                        #        if  point[1][1] >= buslist[point[0]].start[1]:
                        #            cross +=1
                        #            crossbus.append(point[0])
                        if crosswall2(j,a,dir,point):
                            cross +=1
                            crossbus.append(point[0])
                    if cross<= min:
                            min = cross
                            w = a
                            crossbus_real = crossbus

            if w == len(comp_dirs[i][dir]):
                point1 = comp_dirs[i][dir][w-1][1]
            else:
                point1 = comp_dirs[i][dir][w][1]
        if dir == 0:
            point2 = [component.dia0[0]/2 +component.dia1[0]/2 ,pkg.dia1[1]]
        if dir == 1:
            point2 = [pkg.dia1[0],component.dia0[1]/2 +component.dia1[1]/2 ]
        if dir == 2:
            point2 = [component.dia0[0]/2 +component.dia1[0]/2 ,pkg.dia0[1]]
        if dir == 3:
            point2 = [pkg.dia0[0],component.dia0[1]/2 +component.dia1[1]/2 ]

        v0 = Component([0,0],[Bsize_x,Bsize_x],[],len(comp_list))
        bdwall = VitualWall(point1,point2,component,v0,min,crossbus_real)  #to the left of two points
        bdwalls.append(bdwall)
    return bdwalls

def crosswall2(m,a,dir,point):
    cross = False
    if dir == 1 or dir == 2:
        reverse = True
    else:
        reverse = False
    if dir == 0 or dir == 2:
        d = 0
    elif dir == 1 or dir == 3:
        d = 1

    if not reverse:
        if m<a:

                if point[2] == 0:
                    if  point[1][d] <= buslist[point[0]].end[d]:
                        cross = True
                elif point[2] == 1:
                    if  point[1][d] <= buslist[point[0]].start[d]:
                        cross = True

        elif m>=a:  #to the right or top of a
                if point[2] == 0:
                    if  point[1][d] >= buslist[point[0]].end[d]:
                        cross = True
                elif point[2] == 1:
                    if  point[1][d] >= buslist[point[0]].start[d]:
                        cross = True

    else:
        if m<a:   #to the right or top of a
                if point[2] == 0:
                    if  point[1][d] >= buslist[point[0]].end[d]:
                        cross = True
                elif point[2] == 1:
                    if  point[1][d] >= buslist[point[0]].start[d]:
                        cross = True

                    
        elif m>=a:
                if point[2] == 0:
                    if  point[1][d] <= buslist[point[0]].end[d]:
                        cross = True
                elif point[2] == 1:
                    if  point[1][d] <= buslist[point[0]].start[d]:
                        cross = True

    return cross
        
'''
minimum spanning tree
'''
class MGragh:
    def __init__(self,vertex, edge): #edge [vw,weight]
        self.v = vertex
        self.e = edge


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
        n = Find(parent, edges[i][0].comps[0].compID)
        m = Find(parent, edges[i][0].comps[1].compID)
        if m!=n:
            parent[n] = m
            actualwall.append(edges[i][0])
            e_count +=1
            if e_count == (len(G.e)-1) :
                break
    return actualwall


def CriticalPoint(actualwalls,comps_dir,comps_dir2): #return sorted index of edge points of all walls 
    #comps_dir-> nets only,comps_dir2 -> nets &critical points
    comps=[[[] for _ in range(4)] for _ in range(len(comp_list))]

    for wall in actualwalls:
        comp1 = wall.comps[0]
        point1 = wall.points[0]
        comp2 = wall.comps[1]
        point2 = wall.points[1]
        if isadjacent(wall.comps) !=4 :
            dir1 = isadjacent(wall.comps)
            dir2 = dir1+2 if dir1+2<4 else dir1-2
            if len(comps_dir[comp1.compID][dir1]) != 0:
                for i,point in enumerate(comps_dir[comp1.compID][dir1]):
                    if wall.points[0] == point:
                        index1 = i
            else:
                index1 = 0 
            if len(comps_dir[comp2.compID][dir2]) != 0:
                for i,point in enumerate(comps_dir[comp2.compID][dir2]):
                    if wall.points[1] == point:
                        index2 = i
            else:
                index2 = 0
            comps[comp1.compID][dir1].append([index1,[comp2.compID,dir2,index2]])
            comps[comp2.compID][dir2].append([index2,[comp1.compID,dir1,index1]])
        else:
            if point1[1] == comp1.dia1[1]:
                dir1 = 0
            elif point1[0] == comp1.dia1[0]:                                         
                dir1 = 1
            elif point1[1] == comp1.dia0[1]:
                dir1 = 2
            elif point1[0] == comp1.dia0[0]:
                dir1 = 3
            if len(comps_dir[comp1.compID][dir1]) != 0:
                for i,point in enumerate(comps_dir[comp1.compID][dir1]):
                    if wall.points[0] == point[1]:
                        index1 = i
            else:
                index1 = 0
            
            boardID = len(comps_dir)
            for i,pt in enumerate(comps_dir2[-1][dir1]):
                if pt[1] == point2:
                    index2 = i
            comps[comp1.compID][dir1].append([index1,[boardID,dir1,index2]])
            comps[boardID][dir1].append([index2,[comp1.compID,dir1,index1]])        
            #sorted because comps_dir is sorted
    cpts_in_comps = []
    
    for i,comp in enumerate(comps):
        temp =[]
        if i ==(len(comps) -1):# SORT board boundary directions
            for dir in range(4):
                pts =  comp[3-dir]
                edge = []
                for pt in pts:
                    edge.append([3-dir,pt])
                edge.sort(key = lambda x:x[1][0],reverse=False)
                temp.extend(edge)

        else:                   
            for dir in range(4):
                pts =  comp[dir]
                for pt in pts:
                    temp.append([dir,pt])
        cpts_in_comps.append(temp)

    return comps,cpts_in_comps
            
        


def find_tree(comp_list, walls):
    vw_list = []
    v0 = Component([0,0],[Bsize_x,Bsize_x],[],len(comp_list))
    comp_list.append(v0)
    for wall in walls:
        vw_list.append([wall,wall.nb])
    vw_list.sort(key =lambda x:x[1])
    gragh = MGragh(comp_list, vw_list)
    MST = MiniSpanTree_Kruskal(gragh)
    #FanoutsCircle =[]
    #cpts = CriticalPoint(MST,comps_dir)
    #if len(cpts[0]) ==1:
    #    split0 = split1(cpts,comps_dir,0)
    #else:
    #    split0,_ = split2(cpts,comps_dir,0)
    #
    #FanoutsCircle.append(split0)
    return MST

        
def constructcircle2(segments,cp_dirs,criticalpoints): #criticalpoint [dir,[index,[nextcomp,nextdir,nextindex]]]
    dir0 = criticalpoints[0][0][0]
    index0 = criticalpoints[0][0][1][0]
    if len(criticalpoints[0]) == 1:
        nextcomp = criticalpoints[0][0][1][1][0]
        nextdir = criticalpoints[0][0][1][1][1]
        nextindex = criticalpoints[0][0][1][1][2]
    else:
        nextcomp = criticalpoints[0][1][1][1][0]
        nextdir = criticalpoints[0][1][1][1][1]
        nextindex = criticalpoints[0][1][1][1][2]
    

    circle = segments[0][dir0][index0]
    while (nextcomp != 0) or (nextdir != dir0) or (nextindex != index0):
        if nextcomp != (len(criticalpoints) - 1):
            circle.extend(segments[nextcomp][nextdir][nextindex])
        temp1 = nextcomp
        index = findindex(nextcomp,nextdir,nextindex,criticalpoints)

#        if (nextcomp == (len(criticalpoints) - 1)) and (index == (len(criticalpoints[nextcomp]) - 1)):
#            nextcomp = len(criticalpoints) - 1
#            nextdir = 3
#            nextindex = 0          

        if index < (len(criticalpoints[temp1]) - 1): 
            nextcomp = criticalpoints[temp1][index+1][1][1][0]
            nextdir = criticalpoints[temp1][index+1][1][1][1]
            nextindex = criticalpoints[temp1][index+1][1][1][2]
        elif index == (len(criticalpoints[temp1]) - 1):
            nextcomp = criticalpoints[temp1][0][1][1][0]
            nextdir = criticalpoints[temp1][0][1][1][1]
            nextindex = criticalpoints[temp1][0][1][1][2]

    return circle
def findindex(comp,dir,index,criticalpoints):
    for i,cpt in enumerate(criticalpoints[comp]):
        if dir == cpt[0]:
            if  index == cpt[1][0]:
                return i



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


class Section:
    def __init__(self,section,next) -> None:
        self.section = section
        self.next = next



def split(criticalpoints,comps_dir): #split buses by criticalpoints -> segs:[[bus,bus_pos,dir1,i], ... ]
        segments = [[{} for _ in range(4)] for _ in range(len(comps_dir))]        
        for i in range(len(comps_dir)):    
            points = criticalpoints[i]
            split= [[] for _ in range(len(points))]          
            for x in range(0,len(points) - 1):
                dir1 = points[x][0]
                index1 = points[x][1][0]
                dir2 = points[x+1][0]
                index2 = points[x+1][1][0]
                maxcount = abs(dir2 -dir1)
                segments[i][dir1][index1] = []

                if maxcount == 0:
                    split[x] = comps_dir[i][dir1][index1:index2-1]
#                    segments[i][dir1][index1] = comps_dir[i][dir1][index1:index2-1]
                    for item in range(index1,index2):
                        segments[i][dir1][index1].append([comps_dir[i][dir1][item][0],comps_dir[i][dir1][item][1],dir1,i])

                    
                else:
                    if (len(comps_dir[i][dir1]) != 0) :
                        split[x] = comps_dir[i][dir1][index1:]
#                        segments[i][dir1][index1] = comps_dir[i][dir1][index1:]
                        for item in range(index1,len(comps_dir[i][dir1])):
                            segments[i][dir1][index1].append([comps_dir[i][dir1][item][0],comps_dir[i][dir1][item][1],dir1,i])
                        for count in range(1,maxcount):
                            m = edge_switch(dir1,count)
#                            for item in comps_dir[i][m]:
#                                split[x].extend(item)
#                                segments[i][dir1][index1].extend(item)
                            for item in range(0,len(comps_dir[i][dir1])):
                                segments[i][dir1][index1].append([comps_dir[i][m][item][0],comps_dir[i][m][item][1],m,i])
                    if (len(comps_dir[i][dir2]) != 0):
                        split[x].extend(comps_dir[i][dir2][0:index2])
#                        segments[i][dir1][index1].extend(comps_dir[i][dir2][0:index2])
                        for item in range(0,index2):
                            segments[i][dir1][index1].append([comps_dir[i][dir2][item][0],comps_dir[i][dir2][item][1],dir2,i])
                   
            dir_end = points[len(points) - 1][0]
            index_end = points[len(points) - 1][1][0]
            dir_0 = points[0][0]
            index_0 = points[0][1][0]
            segments[i][dir_end][index_end]=[]
            if (len(comps_dir[i][dir_end]) != 0) :
                split[-1]=comps_dir[i][dir_end][index_end:]
#                segments[i][dir_end][index_end]=comps_dir[i][dir_end][index_end:]
                for item in range(index_end,len(comps_dir[i][dir_end])):
                    segments[i][dir_end][index_end].append([comps_dir[i][dir_end][item][0],comps_dir[i][dir_end][item][1],dir_end,i])

            maxcount = dir_end - dir_0
            for count in range(1,4-maxcount):
                m = edge_switch(dir_end,count)
#                for item in comps_dir[i][m]:
#                    split[-1].extend(item)
#                    segments[i][dir_end][index_end].extend(item)
                for item in range(0,len(comps_dir[i][m])):
                        segments[i][dir_end][index_end].append([comps_dir[i][m][item][0],comps_dir[i][m][item][1],m,i])
            if (len(comps_dir[i][dir_0]) != 0) :        
                split[-1].extend(comps_dir[i][dir_0][0:index_0])
#                segments[i][dir_end][index_end].extend(comps_dir[i][dir_0][0:index_0])
                for item in range(0,index_0):
                    segments[i][dir_end][index_end].append([comps_dir[i][dir_0][item][0],comps_dir[i][dir_0][item][1],dir_0,i])
        return segments

def init_layer(circle,comp_list):
    layers = []
    circle2 = copy.deepcopy(circle)
    while(len(circle2) != 0):
        for bus1 in circle2:
            pass

def process_circle(circle,comp_list,buslist): #add next and its direcion
    circle2 = copy.deepcopy(circle)
    for i in range(len(buslist)):
        temp = []
        for j,item in enumerate(circle2):
            if item[0] == i:
                temp.append([j,item])
#        if len(temp) == 2:
#            if 2*(temp[1][0] - temp[0][0]) <= len (circle):
#                circle2[temp[0][0]].extend([1,temp[1][0]]) #(its direcion,next)
#                circle2[temp[1][0]].extend([0,temp[0][0]])
#            else:
#                circle2[temp[0][0]].extend([0,temp[1][0]])
#                circle2[temp[1][0]].extend([1,temp[0][0]])
        lenth = len(temp)
        for m in range(lenth):
            for n in range(m+1,lenth):
                if len(circle2[temp[m][0]]) == 4:
                    circle2[temp[m][0]].append([])
                if len(circle2[temp[n][0]]) == 4:
                    circle2[temp[n][0]].append([])
                if circle2[temp[m][0]][3] == circle2[temp[n][0]][3]:
                    if 2*(temp[n][0] - temp[m][0]) <= len (circle):
                        circle2[temp[m][0]][4].append([1,temp[n][0]])# 1 -> forward, 0 -> backward
                        circle2[temp[n][0]][4].append([0,temp[m][0]])
                    else:
                        circle2[temp[m][0]][4].append([0,temp[n][0]])
                        circle2[temp[n][0]][4].append([1,temp[m][0]])
        for m in range(lenth):
            for n in range(m+1,lenth):                
                dir = isadjacent(comp_list[circle2[temp[m][0]][3]],comp_list[circle2[temp[n][0]][3]])
                if (len(temp) == 4) and (dir != 4):
                    for next in circle2[temp[m][0]][4]:
                        if ((circle2[next[1]][2] == edge_switch(dir,1)) or (circle2[next[1]][2] == edge_switch(dir,3))) and ((circle2[temp[m][0]][2] == edge_switch(dir,1)) or (circle2[temp[m][0]][2] == edge_switch(dir,3))):
                            circle2[temp[m][0]][4].remove(next)
                    for next in circle2[temp[n][0]][4]:
                        if ((circle2[next[1]][2] == edge_switch(dir,1)) or (circle2[next[1]][2] == edge_switch(dir,3))) and ((circle2[temp[n][0]][2] == edge_switch(dir,1)) or (circle2[temp[n][0]][2] == edge_switch(dir,3))):
                            circle2[temp[n][0]][4].remove(next)
    for i,item in enumerate(circle2):
        item.append(i)
    

    return circle2


def cross_state(a1,a2,b1,b2):#format: [bus,pos,dir,comp,next([0(1),nextindex])]
    if b2[4][1] > b1[4][1]:
        if a1[4][1] <= b1[4][1]:
            if a2[4][1] >= b2[4][1]:
                return 0
            else:
                return 1
        else:
            if a2[4][1] <= b2[4][1]:
                return 0
            else:
                return 1
    else:
        if a1[4][1] <= b2[4][1]:
            if a2[4][1] >= b1[4][1]:
                return 0
            else:
                return 1
        else:
            if a2[4][1] <= b1[4][1]:
                return 0
            else:
                return 1        

def find_in_circle(item,circle):
    for i,point in enumerate(circle):
        if item == point[0:3]:
            return i

def assign_layer(processed_circle):
    layers = []
    circle = copy.deepcopy(processed_circle)
    while(len(circle) != 0):

        temp = [circle[0]]
        next = circle[0][4][0][1] #须用链表，index会变, 多向链表？
        dir = circle[0][4][0][0]
        del circle[0][4][0]
        if dir == 1:
            flag = 1
            while(flag and (processed_circle[next][5] > temp[-1][5])):
                index = find_in_circle(processed_circle[next][0:3],circle)
                temp.append(circle[index])
                if circle[index][4][0][0] == 1:
                    next = circle[index][4][0][1]
                    del circle[index][4][0]
                else:
                    flag = 0
                    for i in range(index + 1, len(circle)):
                        if circle[i][4][0][0] == 1:
                            next = circle[i][4][0][1]
                            del circle[index][4][0]
                            flag = 1
                            break
                
                if  circle[index][4] == []:
                    del circle[index]
        elif dir == 0:
            flag = 1
            while(flag and (processed_circle[next][5] > temp[-1][5])):
                index = find_in_circle(processed_circle[next][0:3],circle)
                temp.append(circle[index])
                if circle[index][4][0][0] == 0:
                    next = circle[index][4][0][1]
                    del circle[index][4][0]
                else:
                    flag = 0
                    for i in range(1, index):
                        if circle[index - i][4][0][0] == 0:
                            next = circle[index - i][4][0][1]
                            del circle[index][4][0]
                            flag = 1
                            break
                
                if  circle[index][4] == []:
                    del circle[index]




    

        
    
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
    comp_dirs = assigner.sort_by_dir(comp_list)
    pic = Drawer(packagelist,buslist)
    walls = []
    
    for i, pkg in enumerate(packagelist):
        for comp in comps_in_pkg[i]:
            bdwall = find_bdwall(comp,comp_dirs,comp_list,pkg)
            walls.extend(bdwall)
    
    relatedirs = []
    for i, comp1 in enumerate(comp_list):
        for j in range(i+1, len(comp_list)):
            comp2 = comp_list[j]
            if isadjacent([comp1,comp2]) != 4:
    #        wall = localminimization([comp1,comp2],directions)
                relatedirs.append([i,j,isadjacent([comp1,comp2])])
                wall = localminimization2(comp_dirs,comp1,comp2)
    
                if wall is not None:
                    walls.extend([wall])
    pic.draw(Bsize_x, Bsize_y,directions)
    pic.draw_walls(walls)
    pic.show()
    
    actual_walls = find_tree(comp_list,walls)
    pic.draw(Bsize_x, Bsize_y,directions)
    pic.draw_walls(actual_walls)
    pic.show()
    comps_dir2 = add_points(actual_walls,comp_dirs)
    comps,cpts = CriticalPoint(actual_walls,comp_dirs,comps_dir2)
    segs = split(cpts,comp_dirs)
    circle = constructcircle2(segs,comps,cpts)
    print(circle)
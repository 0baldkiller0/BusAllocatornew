import BusAllocator
import random
import matplotlib.pyplot as plt


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
    def __init__(self, comps, dia0, dia1) -> None: # absolute pos of the left-botton diag
        self.comps = comps
#        self.pos = pos
#        self.sizex = sizex
#        self.sizey = sizey
        self.dia0 = dia0
        self.dia1 = dia1
        self.compsList = []
        for comp in comps:
            self.compsList.append(comp.compID)
    
#    def sort(self):
#        for comp in self.comps:
#            for bus in comp.buslist:
#                if (bus.comps[0] in self.compsList) & (bus.comps[1] in self.compsList):
        

class LayerAssigner:
    def __init__(self, packages) -> None:
        self.PackageList = packages

    def allocate_boundary(self, bus):  #TODO: add actual path
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
                    direct0 = [2]
                elif (bus.comps[0].dia1[0] > bus.end[0]) & (bus.comps[0].dia0[1] >= bus.end[1]):
                    direct0 = [1]
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
                    direct0 = [0]
                elif (bus.comps[0].dia0[0] < bus.end[0]) & (bus.comps[0].dia1[1] <= bus.end[1]):
                    direct0 = [3]
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
                    directions.append([bus.BusID,dir1,dir2])
        return directions
    
class Drawer:
        def __init__(self, packages) -> None:
            self.packages = packages


        def draw(self, Bsize_x, Bsize_y):
            fig,ax = plt.subplots(figsize = (Bsize_x/100,Bsize_y/100))
            expand = 0
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
            
            plt.show()
#def isoverlap(comp1,comp2):
def isoverlap(comp1,comp2):
    if comp1[0][0]>=comp2[1][0] or comp1[1][0]<=comp2[0][0] or comp1[0][1]>=comp2[1][1] or comp1[1][1]<=comp2[0][1]:
        return False
    else:
        return True
    
def iscontain(comp1,comp2): #2contains1
    return (comp1[0][0]>=comp2[0][0] and comp1[1][0]<=comp2[1][0] and comp1[0][1]>=comp2[0][1] and comp1[1][1]<=comp2[1][1])










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
                    return Legalization(dialist, [dia0, dia1], boundarydiapair)
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















    
if __name__ == '__main__':
    Bsize_x = 1000
    Bsize_y = 1000
    packagenum = 5
    busnum = 30
    compnum = 18
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
        base = int(Bsize_x/10)
        edge_length = random.randint(base, base + min(Bsize_x-dia0[0], Bsize_y-dia0[1]))
#        dia1 = [dia0[0] + random.randint(0,Bsize_x - dia0[0]), dia0[1] + random.randint(0,Bsize_y - dia0[1])]
        dia1 = [dia0[0] + edge_length, dia0[1] + edge_length]
        if pkg_dialist:
            for dia_pair in pkg_dialist:
                #while (dia_pair[0][0] < dia0[0]) &(dia_pair[1][0] > dia1[0])&(dia_pair[0][1] < dia0[1])&(dia_pair[1][1] > dia1[1]):
                while (isoverlap(dia_pair,[dia0, dia1])) or not iscontain([dia0, dia1], [[0, 0], [Bsize_x, Bsize_y]]):
                    dia0 = [random.randint(0,Bsize_x -1),random.randint(0,Bsize_y -1)]
                    #dia1 = [dia0[0] + random.randint(0,Bsize_x - dia0[0]), dia0[1] + random.randint(0,Bsize_y - dia0[1])]
                    edge_length = random.randint(base, base + min(Bsize_x-dia0[0], Bsize_y-dia0[1]))
                    dia1 = [dia0[0] + edge_length, dia0[1] + edge_length]
            pkg_dialist.append([dia0, dia1])
        else:
            if iscontain([dia0, dia1], [[0, 0], [Bsize_x, Bsize_y]]):
                pkg_dialist.append([dia0, dia1])
            else:
                while not iscontain([dia0, dia1], [[0, 0], [Bsize_x, Bsize_y]]):
                    dia0 = [random.randint(0,Bsize_x -1),random.randint(0,Bsize_y -1)]
                    edge_length = random.randint(base, base + min(Bsize_x-dia0[0], Bsize_y-dia0[1]))
                    dia1 = [dia0[0] + edge_length, dia0[1] + edge_length]
                pkg_dialist.append([dia0, dia1])







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
        comp_base = int((pkgsize_x + pkgsize_y)/20)
        dia0 = [random.randint(pkg_dialist[pkgindex][0][0], pkg_dialist[pkgindex][1][0]), random.randint(pkg_dialist[pkgindex][0][1], pkg_dialist[pkgindex][1][1])]
        comp_edge = random.randint(comp_base, comp_base + min(pkg_dialist[pkgindex][1][0] - dia0[0], pkg_dialist[pkgindex][1][1] - dia0[1]))
#        dia1 = [dia0[0] + random.randint(0,pkg_dialist[pkgindex][1][0] - dia0[0]), dia0[1] + random.randint(0,pkg_dialist[pkgindex][1][1] - dia0[1])]
        dia1 = [dia0[0] + comp_edge, dia0[1] + comp_edge]
        if dialist:
            for dia_pair in dialist:
#                while (dia_pair[0][0] < dia0[0]) &(dia_pair[1][0] > dia1[0])&(dia_pair[0][1] < dia0[1])&(dia_pair[1][1] > dia1[1]):
                while (isoverlap(dia_pair,[dia0, dia1])) or not iscontain([dia0, dia1], pkg_dialist[pkgindex]):
                    dia0 = [random.randint(pkg_dialist[pkgindex][0][0], pkg_dialist[pkgindex][1][0]),random.randint(pkg_dialist[pkgindex][0][1], pkg_dialist[pkgindex][1][1])]
                    #dia1 = [dia0[0] + random.randint(0,pkg_dialist[pkgindex][1][0] - dia0[0]), dia0[1] + random.randint(0,pkg_dialist[pkgindex][1][1] - dia0[1])]
                    comp_edge = random.randint(comp_base, comp_base + min(pkg_dialist[pkgindex][1][0] - dia0[0], pkg_dialist[pkgindex][1][1] - dia0[1]))
                    dia1 = [dia0[0] + comp_edge, dia0[1] + comp_edge]
            dialist.append([dia0, dia1])
        else:
            if iscontain([dia0, dia1], pkg_dialist[pkgindex]):
                dialist.append([dia0, dia1])
            else:
                while not iscontain([dia0, dia1], pkg_dialist[pkgindex]):
                    dia0 = [random.randint(pkg_dialist[pkgindex][0][0], pkg_dialist[pkgindex][1][0]),random.randint(pkg_dialist[pkgindex][0][1], pkg_dialist[pkgindex][1][1])]
                    comp_edge = random.randint(comp_base, comp_base + min(pkg_dialist[pkgindex][1][0] - dia0[0], pkg_dialist[pkgindex][1][1] - dia0[1]))
                    dia1 = [dia0[0] + comp_edge, dia0[1] + comp_edge]
                
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
        pkg = Package(comps_in_pkg[i], dia0, dia1)
        packagelist.append(pkg) 



assigner = LayerAssigner(packagelist)
directions = assigner.EscapeOptimize()
pic = Drawer(packagelist)
pic.draw(Bsize_x, Bsize_y)




        
        



    





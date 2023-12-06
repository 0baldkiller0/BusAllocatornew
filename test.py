import random
import matplotlib.pyplot as plt

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






Bsize_x = 1000
Bsize_y = 1000
packagenum = 1
compnum = 5
pkg_dialist = []
dialist = []
base = int(Bsize_x/100)

for _ in range(packagenum):
    dia0 = [random.randint(0,Bsize_x-1),random.randint(0,Bsize_y-1)]
    #edge_length = random.randint(base, base + min(Bsize_x-dia0[0], Bsize_y-dia0[1]))
    edge_length = int(Bsize_x/packagenum)
    dia1 = [dia0[0] + edge_length, dia0[1] + edge_length]
    Legalization2(pkg_dialist,[dia0, dia1],[[0,0],[Bsize_x, Bsize_y]], edge_length, packagenum)

for _ in range(compnum):
    i = random.randint(0,packagenum-1)
    pkgsize_x = pkg_dialist[i][1][0] - pkg_dialist[i][0][0]
    pkgsize_y = pkg_dialist[i][1][1] - pkg_dialist[i][0][1]
    dia0 = [random.randint(pkg_dialist[i][0][0], pkg_dialist[i][1][0]), random.randint(pkg_dialist[i][0][1], pkg_dialist[i][1][1])]
    comp_edge = int((pkgsize_x +pkgsize_y)/(2*compnum))
    dia1 = [dia0[0] + comp_edge, dia0[1] + comp_edge]
    Legalization2(dialist,[dia0, dia1],pkg_dialist[i], comp_edge, compnum)  

fig,ax = plt.subplots(figsize = (Bsize_x/100,Bsize_y/100))
expand = 0
plt.xlim(0-expand,Bsize_x+expand)
plt.ylim(0-expand,Bsize_y+expand)
for i, pkg in enumerate(pkg_dialist):
    plt.plot([pkg[0][0],pkg[1][0]], [pkg[0][1],pkg[0][1]], 'k',linewidth = 0.5, alpha= 1)
    plt.plot([pkg[1][0],pkg[1][0]], [pkg[0][1],pkg[1][1]], 'k',linewidth = 0.5, alpha= 1)
    plt.plot([pkg[0][0],pkg[1][0]], [pkg[1][1],pkg[1][1]], 'k',linewidth = 0.5, alpha= 1)
    plt.plot([pkg[0][0],pkg[0][0]], [pkg[0][1],pkg[1][1]], 'k',linewidth = 0.5, alpha= 1)
    plt.text(pkg[0][0], pkg[0][1], s=i)
for j,comp in enumerate(dialist):
    plt.plot([comp[0][0],comp[1][0]], [comp[0][1],comp[0][1]], 'g',linewidth = 0.5, alpha= 1)
    plt.plot([comp[1][0],comp[1][0]], [comp[0][1],comp[1][1]], 'g',linewidth = 0.5, alpha= 1)
    plt.plot([comp[0][0],comp[1][0]], [comp[1][1],comp[1][1]], 'g',linewidth = 0.5, alpha= 1)
    plt.plot([comp[0][0],comp[0][0]], [comp[0][1],comp[1][1]], 'g',linewidth = 0.5, alpha= 1)
    plt.text(comp[0][0], comp[0][1], s=j)
x = [0,100,200,300,400]
y = [0,100,200,300,400]
plt.scatter(x,y)
plt.show()
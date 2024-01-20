

import copy


def isoverlap(comp1,comp2):
    if comp1[0][0]>=comp2[1][0] or comp1[1][0]<=comp2[0][0] or comp1[0][1]>=comp2[1][1] or comp1[1][1]<=comp2[0][1]:
        return False
    else:
        return True
    

print (isoverlap([[1,3],[2,4]],[[1,3],[8,9]]))


a = [0,1,2,[3,4]]
if 1 in a:
    a.remove(1)
print(a[-1])

a = []
print(len(a) == 0)


def add(a):
    b = copy.deepcopy(a)
    b.append(1)
    print(b)
add(a)
print(a)

a = [2,3]
b = [2,3]
print(a == b)

c = [1 for i in range(5)]
print(c)

d = [[1,2],[3,4],[5,6]]
e = d[0][:]
f = copy.deepcopy(d)
f.extend([[1,1]])
print(e)
print(f)
a= [[1,2],[2,'b'],[3,4]]
b= [[1,2],[2,'b'],[3,3]]
print(a[0:1] == b[0:1])
del a[0][0]
print(a[-1])
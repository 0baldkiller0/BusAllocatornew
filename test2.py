

def isoverlap(comp1,comp2):
    if comp1[0][0]>=comp2[1][0] or comp1[1][0]<=comp2[0][0] or comp1[0][1]>=comp2[1][1] or comp1[1][1]<=comp2[0][1]:
        return False
    else:
        return True
    

print (isoverlap([[1,3],[2,4]],[[1,3],[8,9]]))


a = [0,1,2,3,4]
if 1 in a:
    a.remove(1)
print(a)

a = []
print(len(a) is 0)
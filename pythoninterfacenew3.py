from dataclasses import dataclass
from os import path
from typing import Optional

import re
# 这些最后收集了ELEMENT类的数据，并且保存为一个栈
BusList_list = []
Components_list = []
BoundaryPoints_list = []
PathList_list = []

# 由于没有BoardSetting和NetSetting的具体实现，这里我先注释掉这两行
# from BoardSetting import BoardSetting
# from NetSetting import NetSetting

out = []

term_regex = r'''(?mx) 
    \s*(?:
        (?P<roundl>\()|
        (?P<roundr>\))|
        (?P<num>[+-]?\d+\.\d+(?=[\ \]|\-?\d+(?=[\ \]]))|
        (?P<s>[^(^)\s]+)
        )'''
dbg = False
def parse_sexp(sexp):
    stack = []
    out = []
    if dbg: print("%-6s %-14s %-44s %-s" % tuple("term value out stack".split()))
    for termtypes in re.finditer(term_regex, sexp):
        term, value = [(t, v) for t, v in termtypes.groupdict().items() if v][0]
        if dbg: print("%-7s %-14s %-44r %-r" % (term, value, out, stack))
        if term == 'roundl':
            stack.append(out)
            out = []
        elif term == 'roundr':
            assert stack, "Trouble with nesting of brackets"
            tmpout, out = out, stack.pop(-1)
            out.append(tmpout)
        elif term == 'num':
            v = float(value)
            if v.is_integer(): v = int(v)
            out.append(v)
        elif term == 'sq':
            out.append(value[1:-1].replace(r'\"', '"'))
        elif term == 's':
            out.append(value)
        else:
            raise NotImplementedError("Error: %r" % (term, value))
    assert not stack, "Trouble with nesting of brackets"
    return out[0]

class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Element:
    def __init__(self,x1 = None,y1 = None,x2 = None,y2 = None):
        super().__init__()
        self.start = Position(x1,y1)
        self.end = Position(x2,y2)

"还需要一个判断两个点谁是start，谁是end的函数，总得来说需要两个点的xy引入才能判断它的全部参数"

class Bus(Element):
    def __init__(self,filePath: str, encoding: Optional[str] = None,width=None):
        self.filePath = filePath
        self.Bus_start = []
        self.Bus_end = []
        self.BusWidth = width
        self.netsID = []
    @classmethod
    def from_sexpr(cls,exp:list):
        # 其接受了out列表，0，1，2，3分别是其四个数据
        read = exp[0]# read这里是没问题的
        # read[1]->bus1,read[2]->bus2
        BusList = []
        # 对bus1到n
        for i in range(1, len(read)):
            item = Element()
            item.start.x = read[i][1][1][1]
            item.start.y = read[i][1][2][1]
            item.Bus_start = [read[i][1][1][1],read[i][1][2][1]]
            item.end.x = read[i][2][1][1]
            item.end.y = read[i][2][2][1]
            item.Bus_end = [read[i][2][1][1],read[i][2][2][1]]
            item.BusWidth = read[i][3][1]
            item.netsID = [item[1] for item in read[i][4][1:]]
            #            for j in range(1,len(read[i][4])):
             #   BusList[i].netsID.append(read[i][4][j][1])
            BusList.append(item)
            # 成功输入，buslist[0]是bus1输入的item，是board类型。
        return BusList
    # 现在接受的是一个字符串,不需要board类型，既然element类型已经存在列表元素中，直接提取就好
    # 可以在不创造实例的情况下对类名起作用
    @classmethod
    def from_file(cls,filepath:str,encoding:Optional[str] = None):
        if not path.isfile(filepath):
            raise Exception("Given path is not a file!")
        # 接受file中内容变成Board中的量
        with open(filepath,'r',encoding=encoding) as infile:
            item = cls.from_sexpr(parse_sexp(infile.read()))
            # 先不管它的filepath，让它直接输出list
            # 我认为它是向from_sexp中调file中的数据
            return item
            "现在item是一个存着element类型的列表"
    @staticmethod
    def to_sexpr(BusList=None,indent=0,newline=True):
        result = ""
        if newline:
            result += "\n" + " " * indent
        result += f"((Bus"
        for i,bus in enumerate(BusList):
            result += f"(Bus{str(i)}(start(x {bus.Bus_start[0]})(y {bus.Bus_start[1]}))(end(x {bus.Bus_end[0]})(y {bus.Bus_end[1]}))(width {bus.BusWidth})(nets" ## TODO：可能还要加上Bus里排序好的netID
            for n,netid in enumerate(bus.netsID):
                result += f"(net{n} {netid})"
            result += f"))"
            if newline:
                result += "\n" + " " * indent
            else:
                result += " "
        result += f")"
        return result.strip()
    def to_file(self,input=None,filepath = None,encoding:Optional[str] = None):
        if filepath is None:
            raise ValueError("Filepath cannot be None.")

            # 处理编码方式参数，默认为None
        if encoding is None:
            encoding = 'utf-8'  # 默认使用UTF-8编码
#        filepath = r"output.txt"
        #上面是测试用地址
        with open(filepath,'w') as file:
            file.write(Bus.to_sexpr(input))


class BoundaryPoints(Element):
    def __init__(self,filePath: str, encoding: Optional[str] = None):
        self.filePath = filePath
    @classmethod
#TODO: 第163行进行了参数数目的改动，所以from_sexpr相应的也要重写
    def from_sexpr(cls,exp:list):
        read = exp[1]#read这里是没问题的
        BoundaryPoints = []#
        for i in range(1, len(read) - 1):
            item = Element()#这里没有问题
            item.start.x = read[1][1][1]
            item.start.y = read[1][2][1]
            item.end.x = read[2][1][1]
            item.end.y = read[2][2][1]

            BoundaryPoints.append(item)
        return BoundaryPoints
    @classmethod
    def from_file(cls,filepath:str,encoding:Optional[str] = None):
        if not path.isfile(filepath):
            raise Exception("Given path is not a file!")
        #接受file中内容变成Board中的量
        with open(filepath,'r',encoding=encoding) as infile:
            item = cls.from_sexpr(parse_sexp(infile.read()))
            #先不管它的filepath，让它直接输出list
            #我认为它是向from——sexp中调file中的数据
            return item
            "现在item是一个存着element类型的列表"

    @staticmethod
    def to_sexpr(BoundaryPoints=None, indent=0, newline=True):
        result = ""
        if newline:
            result += "\n" + " " * indent
        result += f"(BoundaryPoints"
        for i, boundarypoints in enumerate(BoundaryPoints):
            result += f"(start (x {boundarypoints.start.x})(y {boundarypoints.start.y}))(end (x {boundarypoints.end.x})(y {boundarypoints.end.y}))" #boundary points只有两个，分别记录其xy就行
            if newline:
                result += "\n" + " " * indent
            else:
                result += " "
        result += f")"
        return result.strip()

    def to_file(self, input=None, filepath=None, encoding: Optional[str] = None):
        if filepath is None:
            raise ValueError("Filepath cannot be None.")

            # 处理编码方式参数，默认为None
        if encoding is None:
            encoding = 'utf-8'  # 默认使用UTF-8编码
#        filepath = r"E:\output\1.txt"
        # 上面是测试用地址
        with open(filepath, 'a') as file:
            file.write(BoundaryPoints.to_sexpr(input))


class Components(Element):
    def __init__(self,filePath: str, encoding: Optional[str] = None,type = None):
        self.filePath = filePath
        self.type = type
        self.pad_dia0 = None
        self.pad_dia1 = None
    @classmethod
    def from_sexpr(cls,exp:list):
        #其接受了out列表，0，1，2，3分别是其四个数据
        read = exp[2]#read这里是没问题的
        #read[1]->bus1,read[2]->bus2
        Components = []
        #对bus1到n
        for i in range(1, len(read)):
            item = Element()
            item.start.x = read[i][2][1][1]
            item.start.y = read[i][2][2][1]
            item.end.x = read[i][3][1][1]
            item.end.y = read[i][3][2][1]
            item.type = read[i][1][1]
            item.pad_dia0 = read[i][2][1][1], read[i][2][2][1]
            item.pad_dia1 = read[i][3][1][1], read[i][3][2][1]
            Components.append(item)
            #成功输入，buslist[0]是bus1输入的item，是board类型。
        return Components
        "现在接受的是一个字符串,不需要board类型，既然element类型已经存在列表元素中，直接提取就好"
    #可以在不创造实例的情况下对类名起作用
    @classmethod
    def from_file(cls,filepath:str,encoding:Optional[str] = None):
        if not path.isfile(filepath):
            raise Exception("Given path is not a file!")
        #接受file中内容变成Board中的量
        with open(filepath,'r',encoding=encoding) as infile:
            item = cls.from_sexpr(parse_sexp(infile.read()))
            #先不管它的filepath，让它直接输出list
            #我认为它是向from——sexp中调file中的数据
            return item
            "现在item是一个存着element类型的列表"

    @staticmethod
    def to_sexpr(Components=None, indent=0, newline=True):
        result = ""
        if newline:
            result += "\n" + " " * indent
        result += f"(Components"
        for i, components in enumerate(Components):
            result += f"(Component{str(i)}(type {components.type})(start(x {components.pad_dia0[0]})(y {components.pad_dia0[1]}))(end(x {components.pad_dia1[0]})(y {components.pad_dia1[1]})))"
            if newline:
                result += "\n" + " " * indent
            else:
                result += " "
        result += f")"
        return result.strip()

    def to_file(self, input=None, filepath=None, encoding: Optional[str] = None):
        if filepath is None:
            raise ValueError("Filepath cannot be None.")

            # 处理编码方式参数，默认为None
        if encoding is None:
            encoding = 'utf-8'  # 默认使用UTF-8编码
#        filepath = r"E:\output\1.txt"
        # 上面是测试用地址
        with open(filepath, 'a') as file:
            file.write(Components.to_sexpr(input))



class PathList(Element):
    def __init__(self,filePath: str, encoding: Optional[str] = None):
        self.filePath = filePath
    @classmethod
    def from_sexpr(cls,exp:list):
        #其接受了out列表，0，1，2，3分别是其四个数据
        read = exp[3]#read这里是没问题的
        #read[1]->bus1,read[2]->bus2
        PathList = []
        #对bus1到n
        for i in range(1, len(read)):
            #对于path1到n
            CellList = []
            for j in range(1,len(read[1])):
                #低于cell1到n
                item = Element()
                item.start.x = read[i][j][1][1][1]
                item.start.y = read[i][j][1][2][1]
                item.end.x = read[i][j][2][1][1]
                item.end.y = read[i][j][2][2][1]
                CellList.append(item)
            PathList.append(CellList)
            #PathList[0][0]是path1的cell1
            #成功输入，buslist[0]是bus1输入的item，是board类型。
        return PathList
        "现在接受的是一个字符串,不需要board类型，既然element类型已经存在列表元素中，直接提取就好"
    #可以在不创造实例的情况下对类名起作用
    @classmethod
    def from_file(cls,filepath:str,encoding:Optional[str] = None):
        if not path.isfile(filepath):
            raise Exception("Given path is not a file!")
        #接受file中内容变成Board中的量
        with open(filepath,'r',encoding=encoding) as infile:
            item = cls.from_sexpr(parse_sexp(infile.read()))
            #先不管它的filepath，让它直接输出list
            #我认为它是向from——sexp中调file中的数据
            return item
            "现在item是一个存着element类型的列表"

    @staticmethod
    def to_sexpr(PathList=None, indent=0, newline=True):
        result = ""

        if newline:
            result += "\n" + " " * indent
        result += f"(PathList"
        for i, pathlist in enumerate(PathList):
            result += f"(path{str(i + 1)}"
            for j,cell in enumerate(pathlist):
                result += f"(cell{str(j + 1)}(start(x {cell.start.x})(y {cell.start.y}))(end(x {cell.end.x})(y {cell.end.y})))"
                if newline:
                    result += "\n" + " " * indent
                else:
                    result += " "
            result += f")"
        result += f"))"
        return result.strip()

    def to_file(self, input=None, filepath=None, encoding: Optional[str] = None):
        if filepath is None:
            raise ValueError("Filepath cannot be None.")

            # 处理编码方式参数，默认为None
        if encoding is None:
            encoding = 'utf-8'  # 默认使用UTF-8编码
#        filepath = r"E:\pythonstudy\check\mytext.txt"
        # 上面是测试用地址
        with open(filepath, 'a') as file:
            file.write(PathList.to_sexpr(input))


if __name__ == '__main__':
    #Todo：接受txt文件的地址在这里
    filePath = r"mytext3.txt"

    with open(filePath, 'r') as infile:
        read = []
        bus = Bus(filePath)
        read.append(bus.from_sexpr(parse_sexp(infile.read())))
        for i in range(len(read[0])):
            BusList_list.append(read[0][i])

    #这里是读入文件测试
        bus = Bus(filePath)
        bus.to_file(read[0],filepath=r"output\2.txt")
    #Todo：输出的txt文件地址在这里

        for i in range(len(read[0])):
            print("bus{}的开始坐标({},{}),结束坐标({},{}),线宽：{},线网：{}".format(i+1,read[0][i].start.x,read[0][i].start.y,read[0][i].end.x,read[0][i].end.y,read[0][i].BusWidth, read[0][i].netsID))
        #问题在 list index out of range

    with open(filePath, 'r') as infile:
        read = []
        boundarypoints = BoundaryPoints(filePath)
        read.append(boundarypoints.from_sexpr(parse_sexp(infile.read())))
        for i in range(len(read[0])):
            BoundaryPoints_list.append(read[0][i])

        boundarypoints.to_file(read[0], filepath=r"output\2.txt")


        for i in range(len(read[0])):
            print("Boundary Points{}的开始坐标({},{}),结束坐标({},{})".format(i + 1, read[0][i].start.x, read[0][i].start.y,
                                                                              read[0][i].end.x, read[0][i].end.y))

    with open(filePath, 'r') as infile:
        read = []
        components = Components(filePath)
        read.append(components.from_sexpr(parse_sexp(infile.read())))
        for i in range(len(read[0])):
            Components_list.append(read[0][i])

        components.to_file(read[0], filepath=r"output\2.txt")


        for i in range(len(read[0])):
            print("Component{}的开始坐标({},{}),结束坐标({},{}),类型：{}".format(i + 1, read[0][i].start.x, read[0][i].start.y,
                                                                              read[0][i].end.x, read[0][i].end.y,read[0][i].type))

    with open(filePath, 'r') as infile:
        read = []
        pathlist = PathList(filePath)
        read.append(pathlist.from_sexpr(parse_sexp(infile.read())))
        for i in range(len(read[0])):
            PathList_list.append(read[0][i])

        pathlist.to_file(read[0], filepath=r"output\2.txt")



        for i in range(len(read[0])):
            for j in range(len(read[0][0])):
                print("Path{}的Cell{}的开始坐标为({},{}),终止坐标为({},{})".format(i+1,j+1,read[0][i][j].start.x,read[0][i][j].start.y,read[0][i][j].end.x,read[0][i][j].end.y))


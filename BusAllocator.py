from GridParameters import GridParameters
import argparse
import matplotlib.pyplot as plt


class Bus:
    def __init__(self, BusID, Bus_start, StartPads, Bus_end, EndPads, BusWidth):
        self.BusID = BusID
        self.Bus_start = Bus_start
        self.StartPads = StartPads
        self.Bus_end = Bus_end
        self.EndPads = EndPads
        self.BusWidth = BusWidth

class BusAllocator:
    def __init__(self, grid_parameter: GridParameters):
        self.netclass = grid_parameter.netClass
        self.NetList = grid_parameter.netList
        self.FootprintList = grid_parameter.footprint_list
        self.parameters = grid_parameter
        self.BusList = []

        
    def is_near(self,pad1, pad2, MaxDistance):
        dx = pad1.position.X - pad2.position.X
        dy = pad1.position.Y - pad2.position.Y
        distance = (dx**2+dy**2)**0.5
        return distance <= MaxDistance
    
    def AllocZone(self, dia0, dia1, points):
        zone = [[None]]*4
        centralpoint = ((dia0[0]+dia1[0])/2, (dia0[1]+dia1[1])/2)
        for point in points:
            tanx = abs((point[1]-centralpoint[1])/(point[0]-centralpoint[0]))
            tan0 = (dia1[1]-dia0[1])/(dia1[0]-dia0[0])
            if tanx>=tan0 :
                if point[1]>centralpoint[1]:
                    zone[0].append(point)
                else:
                    zone[2].append(point)
            else:
                if point[0]>centralpoint[0]:
                    zone[1].append(point)
                else:
                    zone[3].append(point)
        return zone
    

    def GenerateMultipadFPList(self):
        MultipadFPList = []
        for i in range(len(self.FootprintList)):
            if len(self.FootprintList[i].pads) > 2:
                MultipadFPList.append(self.FootprintList[i])
        return MultipadFPList
    
        

    
    def NetsInFP(self, footprint):
        PadAndNet = []
        for pad in footprint.pads:
            if pad.netID is not None:
                PadAndNet.append((pad, pad.netID))
        return PadAndNet
    
#    def AllocateBoundary(self, pos, footprint) ->int:
        



    def allocate(self):
        """
        disregard multipinnets

        1. add Footprint with over 2 pads to MFPList
        2. search each Footprint pair to find the same net number,sort and  store by netclass
        3. if there are over 2 nets in the same netclass between Footprint pair:
            

        """

        MFPList=self.GenerateMultipadFPList()
        BusID = 0
        with open('debug.txt', 'w') as file:
            file.write('')

        for i in range(len(MFPList)):
            PadNet1 = self.NetsInFP(MFPList[i])

            for j in range(len(MFPList)-1-i):
                PadNet2 = self.NetsInFP(MFPList[i+j+1])

                classes = {}  #classes in the same Fp
                StartBusPins_temp = {}
                EndBusPins_temp = {}
                StartID_temp = {}
                EndID_temp = {}
                BusWidth_temp = {}
                for n in  range(len(PadNet2)):  #initialize the dict
                    padnetclass = self.parameters.netid_to_net[PadNet2[n][1]].netClass
                    if padnetclass not in classes.keys():
                        classes[padnetclass] = []
                        StartBusPins_temp[padnetclass] = []
                        EndBusPins_temp[padnetclass] = []
                        StartID_temp[padnetclass] = []
                        EndID_temp[padnetclass] = []
                        BusWidth_temp[padnetclass] = 0

                with open('debug.txt', 'a') as file:
                    file.write('({},{},{},{})'.format(MFPList[i].fpname, MFPList[i].position, MFPList[i+j+1].fpname, MFPList[i+j+1].position))

                for m in range(len(PadNet1)):
                    net1 = PadNet1[m][1]
                    netclass1 = self.parameters.netid_to_class[net1]
                    for n in  range(len(PadNet2)):
                        net2 = PadNet2[n][1]
                        with open('debug.txt' ,'a') as file:
                            file.write('({},{})'.format(self.parameters.id_to_name[net1],self.parameters.id_to_name[net2]))
                        if (net1 == net2) & (net1 not in StartID_temp) & (net2 not in EndID_temp) :
                            if len(self.parameters.netid_to_net[net1].padList) != 2 :
                                continue
                            else:
                                classes[self.parameters.netid_to_net[net1].netClass].append(net1)
                                clearance_with_track = netclass1.clearance + netclass1.track_width
                                StartID_temp[self.parameters.netid_to_net[net1].netClass].append(net1)
                                EndID_temp[self.parameters.netid_to_net[net1].netClass].append(net2)
                                StartBusPins_temp[self.parameters.netid_to_net[net1].netClass].append(PadNet1[m][0])
                                EndBusPins_temp[self.parameters.netid_to_net[net1].netClass].append(PadNet2[n][0])
                                BusWidth_temp[self.parameters.netid_to_net[net1].netClass] += clearance_with_track

                                break
                with open('debug.txt' ,'a') as file:
                            file.write('\n')
                for netclass in classes:
                    if len(classes[netclass]) >= 2:   #pad number in the same class is over 2
                        with open('debug.txt' ,'a') as file:
                            file.write('the same net:')
                        for pin in StartBusPins_temp[netclass]:
                            with open('debug.txt' ,'a') as file:
                                file.write('{} '.format(self.parameters.id_to_name[pin.netID]))
                            with open('debug.txt' ,'a') as file:
                                file.write('\n')
                        start_sum_x = 0
                        start_sum_y = 0
                        end_sum_x = 0
                        end_sum_y = 0
#                        startpoints = []
                        for pin in StartBusPins_temp[netclass]:
                            start_sum_x += pin.position[0]
                            start_sum_y += pin.position[1]
                            #startpoints.append((pin.position[0],pin.position[1]))

                        Bus_start_x = start_sum_x/len(StartBusPins_temp[netclass])
                        Bus_start_y = start_sum_y/len(StartBusPins_temp[netclass])

                        for pin in EndBusPins_temp[netclass]:

                            end_sum_x += pin.position[0]
                            end_sum_y += pin.position[1]
                        
                        Bus_end_x = end_sum_x/len(EndBusPins_temp[netclass])
                        Bus_end_y = end_sum_y/len(EndBusPins_temp[netclass]) 
                        Bus_start_tmp = (Bus_start_x,Bus_start_y)
                        Bus_end_tmp = (Bus_end_x, Bus_end_y)
                        allocated_sp = self.AllocZone(MFPList[i].dia_pos_0,MFPList[i].dia_pos_1, [Bus_start_tmp])
                        allocated_ep = self.AllocZone(MFPList[j+i+1].dia_pos_0,MFPList[j+i+1].dia_pos_1, [Bus_end_tmp])
                        for i in range(4):
                            if allocated_sp[i] is not None:
                                if i == 0:
                                    Bus_start = (Bus_start_tmp[0],MFPList[i].dia_pos_1[1])
                                elif i == 1:
                                    Bus_start = (MFPList[i].dia_pos_1[0],Bus_start_tmp[1])
                                elif i == 2:
                                    Bus_start = (Bus_start_tmp[0],MFPList[i].dia_pos_0[1])
                                elif i == 3:
                                    Bus_start = (MFPList[i].dia_pos_0[0],Bus_start_tmp[1])
                        
                        for i in range(4):
                            if allocated_ep[i] is not None:
                                if i == 0:
                                    Bus_end = (Bus_end_tmp[0],MFPList[j+i+1].dia_pos_1[1])
                                elif i == 1:
                                    Bus_end = (MFPList[j+i+1].dia_pos_1[0],Bus_end_tmp[1])
                                elif i == 2:
                                    Bus_end = (Bus_end_tmp[0],MFPList[j+i+1].dia_pos_0[1])
                                elif i == 3:
                                    Bus_end = (MFPList[j+i+1].dia_pos_0[0],Bus_end_tmp[1])

                        BusWidth = BusWidth_temp[netclass]
                        bus = Bus(BusID,Bus_start,StartBusPins_temp[netclass],Bus_end,EndBusPins_temp[netclass],BusWidth)
                        self.BusList.append(bus)
                        BusID +=1

def allocator_arguments():
    parser = argparse.ArgumentParser('BusAllocator')
    parser.add_argument('--kicad_pcb', type=str, dest='kicad_pcb', default="bench1/bm1.unrouted.kicad_pcb")
    parser.add_argument('--kicad_pro', type=str, dest='kicad_pro', default="bench1/bm1.unrouted.kicad_pro")
    parser.add_argument('--save_file', type=str, dest='save_file', default="bench1/bm1.routed.kicad_pcb")
    return parser.parse_args()

class Drawer():
    def __init__(self, buslist, gridparameters:GridParameters):
        self.buslist = buslist
        self.gridparameters = gridparameters
    
    def draw(self):
        sizex = abs(self.gridparameters.dia_pos_1[0] - self.gridparameters.dia_pos_0[0])
        sizey = abs(self.gridparameters.dia_pos_1[1] - self.gridparameters.dia_pos_0[1])
        #bench1 1200,650 bench2 700,300 bench4 500,500
#        sizex = 700
#        sizey = 300
        print(sizex,sizey)
        fig,ax = plt.subplots(figsize = (sizex/100,sizey/100))
        padx = []
        pady = []
        for fp in self.gridparameters.footprint_list:
            for pad in fp.pads:
                padx.append(pad.position[0])
                pady.append(pad.position[1])

        plt.scatter(padx,pady,marker='.',linewidths= 0.1)

        for bus in self.buslist:
            busx = [bus.Bus_start[0],bus.Bus_end[0]]
            busy = [bus.Bus_start[1],bus.Bus_end[1]]
            plt.plot(busx,busy, linewidth = bus.BusWidth, alpha = 0.5)
#        plt.xlim((self.gridparameters.dia_pos_0[0],self.gridparameters.dia_pos_1[0]))
#        plt.ylim((self.gridparameters.dia_pos_1[1],self.gridparameters.dia_pos_0[1]))



        plt.savefig('figs/new/bench1.png')
        plt.show()




if __name__ == '__main__':
    arg = allocator_arguments()
    benchmark_file = arg.kicad_pcb
    project_file = arg.kicad_pro
    save_file = arg.save_file
    gridParameters = GridParameters(benchmark_file, project_file, save_file)
    busallocator = BusAllocator(gridParameters)
    busallocator.allocate()
    for Bus in busallocator.BusList:
        print(Bus.BusID,Bus.Bus_start,Bus.Bus_end,Bus.BusWidth)
    drawer = Drawer(busallocator.BusList, gridParameters)
    drawer.draw()





                    
                




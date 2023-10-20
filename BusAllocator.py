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
#        self.clearance = clearance
#        self.trackwidth = trackwidth
        self.BusList = []

        
    def is_near(self,pad1, pad2, MaxDistance):
        dx = pad1.position.X - pad2.position.X
        dy = pad1.position.Y - pad2.position.Y
        distance = (dx**2+dy**2)**0.5
        return distance <= MaxDistance
    

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



    def allocate(self):
        """
        1. add Footprint with over 2 pads to MFPList
        2. search each Footprint pair to find the same net number
        3. if there are over 2 nets between Footprint pair ,record pads and set Bus parameters
        """

        MFPList=self.GenerateMultipadFPList()
#        StartBusPins = []
#        EndBusPins = []
#        BusWidth = 0
        BusID = 0

        for i in range(len(MFPList)):
            PadNet1 = self.NetsInFP(MFPList[i])
            for j in range(len(MFPList)-1-i):
                StartBusPins_temp = []
                EndBusPins_temp = []
                BusWidth_temp = 0
                count = 0

                PadNet2 = self.NetsInFP(MFPList[i+j+1])
#                for pad in MFPList[i].pads:
#                    if pad.net in

                for m in range(len(PadNet1) - 1):
                    net1 = PadNet1[m][1]
                    for n in  range(len(PadNet2) - 1):
                        net2 = PadNet2[n][1]
                        if net1 == net2 :
                            netclass = self.parameters.netid_to_class[net1]
                            clearance_with_track = netclass.clearance_with_track
                            StartBusPins_temp.append(PadNet1[m][0])
                            EndBusPins_temp.append(PadNet2[n][0])
                            BusWidth_temp += clearance_with_track
                            count +=1
                if count >= 2:
                    start_sum_x = 0
                    start_sum_y = 0
                    end_sum_x = 0
                    end_sum_y = 0
                    for pin in StartBusPins_temp:
                        start_sum_x += pin.position[0]
                        start_sum_y += pin.position[1]

                    Bus_start_x = start_sum_x/len(StartBusPins_temp)
                    Bus_start_y = start_sum_y/len(StartBusPins_temp)
                    for pin in EndBusPins_temp:

                        end_sum_x += pin.position[0]
                        end_sum_y += pin.position[1]

                    Bus_end_x = end_sum_x/len(EndBusPins_temp)
                    Bus_end_y = end_sum_y/len(EndBusPins_temp) 
                    Bus_start = (Bus_start_x,Bus_start_y)
                    Bus_end = (Bus_end_x, Bus_end_y)
                    BusWidth = BusWidth_temp
                    bus = Bus(BusID,Bus_start,StartBusPins_temp,Bus_end,EndBusPins_temp,BusWidth)
                    self.BusList.append(bus)
                    BusID +=1

def allocator_arguments():
    parser = argparse.ArgumentParser('BusAllocator')
    parser.add_argument('--kicad_pcb', type=str, dest='kicad_pcb', default="bench4/bm4.unrouted.kicad_pcb")
    parser.add_argument('--kicad_pro', type=str, dest='kicad_pro', default="bench4/bm4.unrouted.kicad_pro")
    parser.add_argument('--save_file', type=str, dest='save_file', default="bench4/bm4.routed.kicad_pcb")
    return parser.parse_args()

class Drawer():
    def __init__(self, buslist, gridparameters:GridParameters):
        self.buslist = buslist
        self.gridparameters = gridparameters
    
    def draw(self):
        sizex = abs(self.gridparameters.dia_pos_1[0] - self.gridparameters.dia_pos_0[0]) * self.gridparameters.gridSize[0]
        sizey = abs(self.gridparameters.dia_pos_1[1] - self.gridparameters.dia_pos_0[1]) * self.gridparameters.gridSize[1] 
        print(sizex,sizey)
        fig,ax = plt.subplots(figsize = (5,5))
        plt.axis((0,500,500,0)) #bench1 1200,650 bench2 700,300 bench4 500,500
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


#        ax.axis('off')
#        ax.plot([0,0], [0,8], color = 'black')
        plt.savefig('figs/bench4.png')
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





                    
                




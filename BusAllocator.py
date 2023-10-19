from GridParameters import GridParameters
import argparse



class Bus:
    def __init__(self, BusID, Bus_start, StartPads, Bus_end, EndPads, BusWidth):
        self.BusID = BusID
        self.Bus_start = Bus_start
        self.StartPads = StartPads
        self.Bus_end = Bus_end
        self.EndPads = EndPads
        self.BusWidth = BusWidth

class BusAllocator:
    def __init__(self, clearance, trackwidth, grid_parameter: GridParameters):
        self.NetList = grid_parameter.netList
        self.FootprintList = grid_parameter.footprint_list
        self.clearance = clearance
        self.trackwidth = trackwidth
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
            if pad.net is not None:
                PadAndNet.append((pad, pad.net.number))
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
                            StartBusPins_temp.append(PadNet1[m][0])
                            EndBusPins_temp.append(PadNet2[n][0])
                            BusWidth_temp += self.clearance + self.trackwidth
                            count +=1
                if count >= 2:
                    start_sum_x = 0
                    start_sum_y = 0
                    end_sum_x = 0
                    end_sum_y = 0
                    for pin in StartBusPins_temp:
                        start_sum_x += pin.position.X
                        start_sum_y += pin.position.Y

                    Bus_start_x = start_sum_x/len(StartBusPins_temp)
                    Bus_start_y = start_sum_y/len(StartBusPins_temp)
                    for pin in EndBusPins_temp:

                        end_sum_x += pin.position.X
                        end_sum_y += pin.position.Y

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
    parser.add_argument('--kicad_pcb', type=str, dest='kicad_pcb', default="bench1/bm1.unrouted.kicad_pcb")
    parser.add_argument('--kicad_pro', type=str, dest='kicad_pro', default="bench1/bm1.unrouted.kicad_pro")
    parser.add_argument('--save_file', type=str, dest='save_file', default="bench1/bm1.routed.kicad_pcb")
    return parser.parse_args()



if __name__ == '__main__':
    clearance = 100 
    trackwidth = 23
    arg = allocator_arguments()
    benchmark_file = arg.kicad_pcb
    project_file = arg.kicad_pro
    save_file = arg.save_file
    gridParameters = GridParameters(benchmark_file, project_file, save_file)
    busallocator = BusAllocator(clearance, trackwidth, gridParameters)
    busallocator.allocate()
    for Bus in busallocator.BusList:
        print(Bus.BusID,Bus.Bus_start,Bus.Bus_end,Bus.BusWidth)





                    
                




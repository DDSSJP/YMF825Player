class YMF825Parameter():
    # Clock Enable
    CLKE = "CLKE" # 0,1/Disable,Enable
    # Reset
    ALRST = "ALRST" # 0,1/OFF,ON
    # AnalogBlockPowerDown
    AP3 = "AP3" # 0,1/OFF,ON  DAC
    AP2 = "AP2" # 0,1/OFF,ON  SPAMP, SPOUT2
    AP1 = "AP1" # 0,1/OFF,ON  SPAMP, SPOUT1
    AP0 = "AP0" # 0,1/OFF,ON  VREF, IREF
    # SpeakerAmplifireGain
    GAIN = "GAIN" # 0-3
    # HardwareID
    HardwareID = "HardwareID"
    # Interrupt
    EMP_DW = "EMP_DW" # 0,1/clear,set         empty data write ?
    FIFO = "FIFO" # 0,1/clear,set             FIFO ...?
    SQ_STP = "SQ_STP" # 0,1/clear,set         Sequencer stopping ?
    EIRQ = "EIRQ" # 0,1/Disable,Enable        Enable IRQ
    EEMP_DW = "EEMP_DW" # 0,1/Disable,Enable  Enable EMP Interrupt
    EFIFO = "EFIFO" # 0,1/Disable,Enable      Enable FIFO Interrupt
    ESQ_STP = "ESQ_STP" # 0,1/Disable,Enable  Enable Sequencer Stopping Interrupt
    # ContentsDataWrite
    ContentsDataWrite = "ContentsDataWrite" # burst write to FIFO
    # Sequencer
    AllKeyOff = "AllKeyOff" # 0,1/OFF,ON
    AllMute = "AllMute" # 0,1/OFF,ON
    AllEGRst = "AllEGRst" # 0,1/OFF,ON
    R_FIFOR = "R_FIFOR" # 0,1/OFF,ON  Reset FIFO Read point ?
    REP_SQ = "REP_SQ" # 0,1/OFF,ON    Repeat Sequencer ?
    R_SEQ = "R_SEQ" # 0,1/OFF,ON      Reset Sequencer ?
    R_FIFO = "R_FIFO" # 0,1/OFF,ON    Reset FIFO ?
    START = "START" # 0,1/OFF,ON      Sequencer Start ?
    SEQ_Vol = "SEQ_Vol" # 0-31
    DIR_SV = "DIR_SV" # 0,1/Enable,Disable Sequence Volume Interpolation
    SIZE = "SIZE" # 0-511/1-512 Sequence data size
    MS_S = "MS_S" # 0-16383/1-16384 ms ?
    # Synthesizer
    CRGD_VNO = "CRGD_VNO" # 0-15 Control Register Voice NO
    VoVol = "VoVol" # 0-31 Voice Volume
    BLOCK = "BLOCK" # 0-7 Octave
    FNUM = "FNUM" # 0-1023 Frequency
    KeyOn = "KeyOn" # 0,1/OFF,ON
    Mute = "Mute" # 0,1/OFF,ON
    EG_RST = "EG_RST" # 0,1/OFF,ON  Emergency Rest
    ToneNum = "ToneNum" # 0-15 Tone Number
    ChVol = "ChVol" # 0-31 Channel Volume
    DIR_CV = "DIR_CV" # 0,1/Enable,Disable Channel Volume Interpolation
    XVB = "XVB" # 0,1,2,4,6/OFF,DVB,2x(DVB+1),4x(DVB+2),8x(DVB+3) Vibrato Extension
    INT = "INT" # 0-3 Audio frequency multiplier Integer part
    FRAC = "FRAC" # 0-511 Audio frequency multiplier Fraction part
    DIR_MT = "DIR_MT" # 0,1/Enable,Disable Master Volume Interpolation
    # ControlRegister
    RDADR_CRG = "RDADR_CRG" # 0-255 Read Address Control Register
    RDDATA_CRG = "RDDATA_CRG" # 0-127 Read Data Control Register
    # MasterVolume
    MASTER_VOL = "MASTER_VOL" # 0-63 Master Volume
    # SoftReset
    SFTRST = "SFTRST" # 0-255
    # VolumeInterpolation
    DADJT = "DADJT" # 0,1/OFF,ON  Sequencer Delay Adjust ?
    MUTE_ITIME = "MUTE_ITIME" # 0-3    Mute Interpolation Time
    CHVOL_ITIME = "CHVOL_ITIME" # 0-3  Channel Volume Interpolation Time
    MVOL_ITIME = "MVOL_ITIME" # 0-3    Master Volumne Interpolation Time
    # LFOReset
    LFO_RST = "LFO_RST" # 0,1/off,on
    # PowerRailSelection
    DRV_SEL = "DRV_SEL" # 0,1
    # Equalizer
    W_CEQ0 = "W_CEQ0" # 0-255
    W_CEQ1 = "W_CEQ1" # 0-255
    W_CEQ2 = "W_CEQ2" # 0-255
    CEQ00 = "CEQ00" # 0-16777215
    CEQ01 = "CEQ01" # 0-16777215
    CEQ02 = "CEQ02" # 0-16777215
    CEQ03 = "CEQ03" # 0-16777215
    CEQ04 = "CEQ04" # 0-16777215
    CEQ10 = "CEQ10" # 0-16777215
    CEQ11 = "CEQ11" # 0-16777215
    CEQ12 = "CEQ12" # 0-16777215
    CEQ13 = "CEQ13" # 0-16777215
    CEQ14 = "CEQ14" # 0-16777215
    CEQ20 = "CEQ20" # 0-16777215
    CEQ21 = "CEQ21" # 0-16777215
    CEQ22 = "CEQ22" # 0-16777215
    CEQ23 = "CEQ23" # 0-16777215
    CEQ24 = "CEQ24" # 0-16777215
    # SoftwareCommunicationCheck
    COMM = "COMM" # 0-255

class YMF825Register():
    def __init__(self):
        self._reg = [0] * 81
        self._ctrl = [0] * 256 # 128?
        self._fifo = [0] * 512
        self._fifo_write_point = 0
        self._eq_temp = [[0] * 15] * 3
        self._eq_write_point = [0] * 3
        self._not_read = [7, 12, 13, 14, 15, 16, 7, 18, 19, 20, 30, 31]
        self._not_write = [4, 22, 30, 31]
        self._not_write.extend([35 + i for i in range(15*3)])
        self.hardware_reset()

    @staticmethod
    def diff(new_obj, old_obj):
        reg = []
        for i in range(len(new_obj._reg)):
            if i in new_obj._not_write:
                continue
            if new_obj._reg[i] != old_obj._reg[i]:
                reg.append((i, new_obj._reg[i]))
        
        ctrl = []
        for i in range(len(new_obj._ctrl)):
            if new_obj._ctrl[i] != old_obj._ctrl[i]:
                ctrl.append((i, new_obj._ctrl[i]))
        
        size = (new_obj._reg[9] & 0b0000_0001) * 256 + new_obj._reg[10] + 1
        p = 0
        for i in range(size):
            if new_obj._fifo[i] != old_obj._fifo[i]:
                p = i+1
        fifo = [0] * p
        for k in range(p):
            fifo[k] = new_obj._fifo[k]
        
        return reg, ctrl, fifo

    @staticmethod
    def copy(to_obj, from_obj):
        for i in range(len(to_obj._reg)):
            to_obj._reg[i] = from_obj._reg[i]
        for i in range(len(to_obj._ctrl)):
            to_obj._ctrl[i] = from_obj._ctrl[i]
        for i in range(len(to_obj._fifo)):
            to_obj._fifo[i] = from_obj._fifo[i]
        to_obj._fifo_write_point = from_obj._fifo_write_point
        for band in range(3):
            for i in range(15):
                to_obj._eq_temp[band][i] = from_obj._eq_temp[band][i]
            to_obj._eq_write_point[band] = from_obj._eq_write_point[band]

    def hardware_reset(self):
        for i in range(len(self._reg)):
            self._reg[i] = 0x00
        self._reg[ 1] = 0x80
        self._reg[ 2] = 0x0f
        self._reg[ 3] = 0x01
        self._reg[ 4] = 0x01
        self._reg[35] = 0x10
        self._reg[50] = 0x10
        self._reg[65] = 0x10
        for i in range(len(self._ctrl)):
            self._ctrl[i] = 0x00
        for i in range(16):
            self._ctrl[i*8 + 4] = 0x60
            self._ctrl[i*8 + 6] = 0x08
        for i in range(len(self._fifo)):
            self._fifo[i] = 0x00

    def all_reset(self):
        back_00 = self._reg[ 0]
        back_01 = self._reg[ 1]
        back_01 = self._reg[ 2]
        back_29 = self._reg[29]
        back_80 = self._reg[80]
        self.hardware_reset()
        self._reg[ 0] = back_00
        self._reg[ 1] = back_01
        self._reg[ 2] = back_01
        self._reg[29] = back_29
        self._reg[80] = back_80

    def write(self, adr, data):
        if adr in self._not_write:
            raise Exception(f"not write address. -> {adr}")

        # ALRST
        if adr == 1 and (data & 0x80) != 0:
            self.all_reset()

        # Contents Data Write Port
        if adr == 7:
            self._fifo[self._fifo_write_point] = data
            self._fifo_write_point += 1
            if self._fifo_write_point >= len(self._fifo):
                self._fifo_write_point = 0
            return

        if adr == 8:
            # AllKeyOff
            if data & 0b0100_0000 != 0:
                for i in range(16):
                    self._ctrl[i*8 + 3] &= 0b1011_1111 # KeyOn=0
            # AllMute
            if data & 0b0010_0000 != 0:
                for i in range(16):
                    self._ctrl[i*8 + 3] &= 0b1101_1111 # Mute=0
            # AllEGRst
            if data & 0b0001_0000 != 0:
                for i in range(16):
                    self._ctrl[i*8 + 3] &= 0b1110_1111 # EG_RST=0
            # R_FIFO
            if data & 0b0000_0010 != 0:
                for i in range(len(self._fifo)):
                    self._fifo[i] = 0x00
                self._fifo_write_point = 0

        # Control Register
        if 12 <= adr and adr <= 19:
            vno = self._reg[11] & 0b0000_1111 # CRGD_VNO
            self._ctrl[vno*8 + adr-12] = data
            return
        
        # EQ
        if 32 <= adr and adr <= 34:
            band = adr - 32
            self._eq_temp[band][self._eq_write_point[band]] = data
            self._eq_write_point[band] += 1
            if self._eq_write_point[band] >= 15:
                self._eq_write_point[band] = 0
                for i in range(15):
                    self._reg[35 + band*15 + i] = self._eq_temp[band][i]

        self._reg[adr] = data

    def read(self, adr):
        if adr in self._not_read:
            raise Exception(f"not read address. -> {adr}")

        # Control Register
        if adr == 22:
            rdadr = self._reg[21] # RDADR_CRG
            return self._ctrl[rdadr]

        return self._reg[adr]

def write_parameter_to_register(reg, prm, value):
    p = YMF825Parameter
    if prm == p.CLKE:
        reg.write(0, value & 0b0000_0001)
    elif prm == p.ALRST:
        reg.write(1, (value & 0b0000_0001) << 7)
    elif prm == p.AP3:
        reg.write(2, (reg.read(2) & 0b1111_0111) | (value & 0b0000_0001) << 3)
    elif prm == p.AP2:
        reg.write(2, (reg.read(2) & 0b1111_1011) | (value & 0b0000_0001) << 2)
    elif prm == p.AP1:
        reg.write(2, (reg.read(2) & 0b1111_1101) | (value & 0b0000_0001) << 1)
    elif prm == p.AP0:
        reg.write(2, (reg.read(2) & 0b1111_1110) | (value & 0b0000_0001))
    elif prm == p.GAIN:
        reg.write(3, value & 0b0000_0011)
    elif prm == p.EMP_DW:
        reg.write(5, (reg.read(5) & 0b1110_1111) | (value & 0b0000_0001) << 4)
    elif prm == p.FIFO:
        reg.write(5, (reg.read(5) & 0b1111_1011) | (value & 0b0000_0001) << 2)
    elif prm == p.SQ_STP:
        reg.write(5, (reg.read(5) & 0b1111_1110) | (value & 0b0000_0001))
    elif prm == p.EIRQ:
        reg.write(6, (reg.read(6) & 0b1011_1111) | (value & 0b0000_0001) << 6)
    elif prm == p.EEMP_DW:
        reg.write(6, (reg.read(6) & 0b1110_1111) | (value & 0b0000_0001) << 4)
    elif prm == p.EFIFO:
        reg.write(6, (reg.read(6) & 0b1111_1011) | (value & 0b0000_0001) << 2)
    elif prm == p.ESQ_STP:
        reg.write(6, (reg.read(6) & 0b1111_1110) | (value & 0b0000_0001))
    elif prm == p.ContentsDataWrite:
        reg.write(7, value & 0b1111_1111)
    elif prm == p.AllKeyOff:
        reg.write(8, (reg.read(8) & 0b0111_1111) | (value & 0b0000_0001) << 7)
    elif prm == p.AllMute:
        reg.write(8, (reg.read(8) & 0b1011_1111) | (value & 0b0000_0001) << 6)
    elif prm == p.AllEGRst:
        reg.write(8, (reg.read(8) & 0b1101_1111) | (value & 0b0000_0001) << 5)
    elif prm == p.R_FIFOR:
        reg.write(8, (reg.read(8) & 0b1110_1111) | (value & 0b0000_0001) << 4)
    elif prm == p.REP_SQ:
        reg.write(8, (reg.read(8) & 0b1111_0111) | (value & 0b0000_0001) << 3)
    elif prm == p.R_SEQ:
        reg.write(8, (reg.read(8) & 0b1111_1011) | (value & 0b0000_0001) << 2)
    elif prm == p.R_FIFO:
        reg.write(8, (reg.read(8) & 0b1111_1101) | (value & 0b0000_0001) << 1)
    elif prm == p.START:
        reg.write(8, (reg.read(8) & 0b1111_1110) | (value & 0b0000_0001))
    elif prm == p.SEQ_Vol:
        reg.write(9, (reg.read(9) & 0b0000_0111) | (value & 0b0001_1111) << 3)
    elif prm == p.DIR_SV:
        reg.write(9, (reg.read(9) & 0b1111_1011) | (value & 0b0000_0001) << 2)
    elif prm == p.SIZE:
        vh = (value & 0b0000_0001_0000_0000) >> 8
        vl =  value & 0b0000_0000_1111_1111
        reg.write(9, (reg.read(9) & 0b1111_1110) | vh )
        reg.write(10, vl )
    elif prm == p.CRGD_VNO:
        reg.write(11, value & 0b0000_1111)
    elif prm == p.VoVol:
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8)
        reg.write(12, (reg.read(22) & 0b0000_0011) | (value & 0b0011_1111) << 2)
    elif prm == p.BLOCK:
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 1)
        reg.write(13, (reg.read(22) & 0b1111_1000) | (value & 0b0000_0111))
    elif prm == p.FNUM:
        vh = (value & 0b0000_0011_1000_0000) >> 7
        vl =  value & 0b0000_0000_0111_1111
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 2)
        reg.write(13, (reg.read(22) & 0b1100_0111) | vh << 3)
        reg.write(14, vl)
    elif prm == p.KeyOn:
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 3)
        reg.write(15, (reg.read(22) & 0b1011_1111) | (value & 0b0000_0001) << 6)
    elif prm == p.Mute:
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 3)
        reg.write(15, (reg.read(22) & 0b1101_1111) | (value & 0b0000_0001) << 5)
    elif prm == p.EG_RST:
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 3)
        reg.write(15, (reg.read(22) & 0b1110_1111) | (value & 0b0000_0001) << 4)
    elif prm == p.ToneNum:
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 3)
        reg.write(15, (reg.read(22) & 0b1111_0000) | (value & 0b0000_1111))
    elif prm == p.ChVol:
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 4)
        reg.write(16, (reg.read(22) & 0b1000_0011) | (value & 0b0001_1111) << 2)
    elif prm == p.DIR_CV:
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 4)
        reg.write(16, (reg.read(22) & 0b1111_1110) | (value & 0b0000_0001))
    elif prm == p.XVB:
        reg.write(17, value & 0b0000_0111)
    elif prm == p.INT:
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 6)
        reg.write(18, (reg.read(22) & 0b1110_0111) | (value & 0b0000_0011) << 3)
    elif prm == p.FRAC:
        vh = (value & 0b0000_0001_1100_0000) >> 6
        vl = (value & 0b0000_0000_0011_1111)
        vno = reg.read(11) & 0b0000_1111
        reg.write(21, vno*8 + 6)
        reg.write(18, (reg.read(22) & 0b1111_1000) | vh)
        reg.write(19, vl << 1)
    elif prm == p.DIR_MT:
        reg.write(20, value & 0b0000_0001)
    elif prm == p.RDADR_CRG:
        reg.write(21, value & 0b1111_1111)
    elif prm == p.MS_S:
        vh = (value & 0b0011_1111_1000_0000) >> 7
        vl =  value & 0b0000_0000_0111_1111
        reg.write(23, vh)
        reg.write(24, vl)
    elif prm == p.MASTER_VOL:
        reg.write(25, (value & 0b0011_1111) << 2)
    elif prm == p.SoftReset:
        reg.write(26, value & 0b1111_1111)
    elif prm == p.DADJT:
        reg.write(27, (reg.read(27) & 0b1011_1111) | (value & 0b0000_0001) << 6)
    elif prm == p.MUTE_ITIME:
        reg.write(27, (reg.read(27) & 0b1100_1111) | (value & 0b0000_0011) << 4)
    elif prm == p.CHVOL_ITIME:
        reg.write(27, (reg.read(27) & 0b1111_0011) | (value & 0b0000_0011) << 2)
    elif prm == p.MVOL_ITIME:
        reg.write(27, (reg.read(27) & 0b1111_1100) | (value & 0b0000_0011))
    elif prm == p.LFO_RST:
        reg.write(28, value & 0b0000_0001)
    elif prm == p.DRV_SEL:
        reg.write(29, value & 0b0000_0001)
    else:
        raise Exception("Invalid write parameter.")

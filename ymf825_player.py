import time

def sleep_ms(ms):
    time.sleep(ms / 1000.0)

def sleep_us(ms):
    time.sleep(ms / 1000000.0)

class YMF825Player:
    STATUS_PLAYING = "Playing"
    STATUS_STOP = "Stop"
    STATUS_PAUSE= "Pause"

    def __init__(self):
        self._spi = None
        self._song = None
        self._status = YMF825Player.STATUS_STOP

    @property
    def status(self):
        return self._status

    def stop(self):
        self._status = YMF825Player.STATUS_STOP
        self._spi = None
        self._song = None

    def pause(self):
        self._status = YMF825Player.STATUS_PAUSE

    def play(self, spi, song):
        self._spi = spi
        self._song = song
        self._status = YMF825Player.STATUS_PLAYING

        self._init_chip()

        #---------------------------------------
        # debug from sample1

        # system setup
        self._spi.write_single(25, 63 << 2) # MasterVolume 0～63
        self._spi.write_single(27, 0b0011_1111) # mute time
        self._spi.write_single(20, 0b0000_0000) # DIR_MT
        self._spi.write_single(20, 0b0000_0011) # Speaker Amplifier Gain
        self._spi.write_single( 8, 0b1111_0110) # Sequencer Setting Reset/Mute on
        sleep_ms(1)
        self._spi.write_single( 8, 0b0000_0000) # Reset/Mute off
        self._spi.write_single( 9, 0b1111_1000) # SEQ_Vol Max
        self._spi.write_single(10, 0b0000_0000) # SIZE 0
        self._spi.write_single(23, 0b0000_0000) # Sequencer Time unit 0
        self._spi.write_single(24, 0b0000_0000)

        # tone data
        tone_list = [
            [0x01,0x85,0x00,0x7F,0xF4,0xBB,0x00,0x10,0x40,0x00,
             0xAF,0xA0,0x0E,0x03,0x10,0x40,0x00,0x2F,0xF3,0x9B,
             0x00,0x20,0x41,0x00,0xAF,0xA0,0x0E,0x01,0x10,0x40]
        ]
        self._write_tone(tone_list)

        # channel setup
        self._spi.write_single(11, 0) #ChannelNo
        self._spi.write_single(12, 31 << 2) # VoiceVolume 0～31
        self._spi.write_single(15, 0b0011_0000) # 0/KeyOff/Mute1/EGRst1/ToneNum0
        self._spi.write_single(16, 0b0111_1101) # 0/ChVol=Max/0/DIR_CV1
        self._spi.write_single(17, 0b0000_0000) # vibrato off
        self._spi.write_single(18, 0b0000_1000) # int=1 frac=0 1.0time
        self._spi.write_single(19, 0b0000_0000) #

        # sequence
        fnum_list = [
            [0x14,0x65],
            [0x1c,0x11],
            [0x1c,0x42],
            [0x1c,0x5d],
            [0x24,0x17],
        ]
        try:
            for _ in range(10):
                for i in range(len(fnum_list)):
                    self._spi.write_single(13, fnum_list[i][0]) # fnum High
                    self._spi.write_single(14, fnum_list[i][1]) # fnum Low
                    self._spi.write_single(15, 0b0100_0000) # 0/KeyOn/Mute0/EGRst0/ToneNum0
                    sleep_ms(500)
                    self._spi.write_single(15, 0b0000_0000) # 0/KeyOff/Mute0/EGRst0/ToneNum0
                    sleep_ms(200)
        except KeyboardInterrupt:
            self._spi.write_single(15, 0b0000_0000) # 0/KeyOff/Mute0/EGRst0/ToneNum0
            self._spi.send_reset_signal()

        #---------------------------------------

    def _init_chip(self):
        # 1. Supply the power to the device.
        # 2. Wait for 100us after supply voltages rise
        # 3. Set the RST_N pin to "H".
        self._spi.send_reset_signal()

        # Software Communication Check
        self._spi.write_single(80, 0xA5)
        ret = self._spi.read_single(80)
        if ret[0] != 0xA5:
            raise Exception("failed to software communication check.")

        # 4. Set DRV_SEL to "0" when this device is used in single 5-V power supply configuration. Set DRV_SEL to "1" when this device is used in dual power supply configuration.
        self._spi.write_single(29, 0b0000_0000) # output power: used in single 5-V power
        # 5. Set the AP0 to "0". The VREF is powered.
        self._spi.write_single( 2, 0b0000_1110) # analog powered: AP3,AP2,AP1,AP0 (DAC,SP2,SP1,VREF)
        # 6. Wait until the clock becomes stable.
        sleep_ms(1) # Oops, but not implemented!
        # 7. Set the CLKE to "1".
        self._spi.write_single( 0, 0b0000_0001) # clock enable
        # 8. Set the ALRST to "0".
        self._spi.write_single( 1, 0b0000_0000) # all reset Out of the reset state.
        # 9. Set the SFTRST to "A3H".
        self._spi.write_single(26, 0b1010_0011) # soft reset
        # 10. Set the SFTRST to "00H".
        self._spi.write_single(26, 0b0000_0000) # soft reset
        # 11. Wait for 30ms after the step 10.
        sleep_ms(30)
        # 12. Set the AP1 and the AP3 to "0".
        self._spi.write_single( 2, 0b0000_0100) # analog powered: AP3,AP2,AP1,AP0 (DAC,SP2,SP1,VREF)
        # 13. Wait for 10us.
        sleep_us(10)
        # 14. Set the AP2 to "0".
        self._spi.write_single( 2, 0b0000_0000) # analog powered: AP3,AP2,AP1,AP0 (DAC,SP2,SP1,VREF)

    def _write_tone(self, tone_list):
        num = len(tone_list) + 1
        data = [0x80 + num]
        for i in range(len(tone_list)):
            data.extend(tone_list[i])
        data.extend([0x80,0x03,0x81,0x80])
        self._spi.write_burst(7, data)

    def _write_eq(self, qe_data):
        pass

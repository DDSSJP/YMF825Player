class Tone():
    pass

class Command():
    NONE = "none"
    Rest = "rest"
    KeyOn = "key_on"
    KeyOff = "key_off"
    Note = "note"
    Tone = "tone"
    Volume = "volume"
    Detune = "detune"
    Quantize = "quantize"
    Vibrato = "vibrato"
    Modulation = "modulation"
    Envelope = "envelope"
    def __init__(self, cmd):
        pass

class PartData:
    def __init__(self, no):
        self.no = no
        self.ch = 0
        self.volume = 0
        self.tone = 0
        self.note = 0
        self.keyon = 0
        self._data = []
        self._index = 0
        self._tick = 0 # cmd内のtick

    def reset(self):
        self._index = 0
        self._tick = 0

    def add(self, cmd):
        self._data.append(cmd)

    def get_tick_register_data(self, tick):
        for t in range(tick):
            pass
        return []

class SongData():
    def __init__(self):
        self.title = ""
        self.composer = ""
        self.arranger = ""
        self.message = ""
        self.part_data = [PartData(i) for i in range(16)]
        self.master_volume = 0

    def print_information(self):
        print("Title:", self.title)
        print("Composer:", self.composer)
        print("Arranger:", self.arranger)
        print("Message:", self.message)
    
    @staticmethod
    def from_mml(filename):
        return SongData()

    def reset(self):
        for i in range(len(self.part_data)):
            self.part_data[i].reset()

    def get_tick_register_data(self, tick):
        data = []
        for i in range(len(self.part_data)):
            data.extend(self.part_data[i].get_tick_register_data(tick))
        return data

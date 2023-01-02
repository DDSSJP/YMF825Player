import sys
from ymf825_player import YMF825Player
from spi_device import SpiDevice
from song_data import SongData

if len(sys.argv) <= 1:
    print("usage: python play.py song.mml")
    exit()

filename = sys.argv[1]
device_info = SpiDevice.get_device_info()

with SpiDevice.open(device_info) as spi:
    song = SongData.from_mml(filename)
    song.print_information()

    player = YMF825Player()
    player.play(spi, song)

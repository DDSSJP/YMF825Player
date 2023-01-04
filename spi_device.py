# FT232H
# VID 0x0403 PID 0x6014
# GUID {36fc9e60-c465-11cf-8056-444553540000}

import os
import json
import time
import FTD2xx

class DeviceInfo:
    def __init__(self, device:str, id:str, detail:list):
        self.device = device
        self.id = id
        self.detail = detail
    def __str__(self):
        return f"device:{self.device}  id:{self.id}  detail:{self.detail}"

SPI_DEVICE_UNKNOWN = "unknown"
SPI_DEVICE_FTD2xx = "FTD2xx"

class SpiDevice:
    @staticmethod
    def get_device_info():
        filename = "spi_device.json"
        if os.path.exists(filename):
            device_list = SpiDevice.search(show=False)
            info = SpiDevice.load_info(filename)
            use_id = info["use_id"]
        else:
            device_list = SpiDevice.search(show=True)
            use_index = input("Please input a device index number for you play song. >> ")
            use_index = int(use_index)
            print("selected device id:", device_list[use_index].id)
            print()
            use_id = device_list[use_index].id

        SpiDevice.save_info(filename, device_list, use_id)
        info = SpiDevice.load_info(filename)
        use_id = info["use_id"]

        for i in range(len(info["device_list"])):
            if device_list[i].id == use_id:
                use_index = i
                break

        return device_list[use_index]

    @staticmethod
    def search(show=False, save=False):
        device_list = []
        device_list.extend(DeviceFTD2xx._search())

        if show:
            if len(device_list) == 0:
                print("not found spi device.")
                return
            print(f"found spi devices.")
            for idx,i in enumerate(device_list):
                print(f"  index:{idx}  {i}")
            print()

        return tuple(device_list)
    
    @staticmethod
    def save_info(filename, device_list, use_id):
        import datetime
        with open(filename,"w") as f:
            dic = {}
            dic["output datetime"] = str(datetime.datetime.now())
            dic["use_id"] = use_id
            dic["device_list"] = []
            for i in range(len(device_list)):
                info_item = {"device":device_list[i].device,"id":device_list[i].id,"detail":device_list[i].detail}
                dic["device_list"].append(info_item)
            f.write(json.dumps(dic,ensure_ascii=False,indent=4))

    @staticmethod
    def load_info(filename):
        with open(filename,"r") as f:
            info = json.load(f)
        return info

    @staticmethod
    def open(device_info):
        if device_info.device == SPI_DEVICE_FTD2xx:
            spi = DeviceFTD2xx()
        else:
            raise Exception(f"unknown device. -> {device_info}")
        spi._open(device_info)
        return spi

    @staticmethod
    def close(spi):
        spi._close()

class DeviceBase:
    def __init__(self):
        self.opend = False
        self.info = DeviceInfo(SpiDevice.DEVICE_UNKNOWN, None, [])
    @staticmethod
    def _search():
        raise NotImplementedError()
    def _open(self, index):
        raise NotImplementedError()
    def _close(self):
        pass
    def send_reset_signal(self):
        raise NotImplementedError()
    def write_burst(self, adr, data):
        raise NotImplementedError()
    def write_single(self, adr, data):
        raise NotImplementedError()
    def write_multi(self, item_list):
        raise NotImplementedError()
    def read_single(self, adr):
        raise NotImplementedError()
    def read_multi(self, adr_list):
        raise NotImplementedError()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self._close()
    def __str__(self):
        return f"opend:{self.opend}  {self.info}"

class DeviceFTD2xx(DeviceBase):
    def __init__(self):
        self.info = DeviceInfo(SPI_DEVICE_FTD2xx, None, {})
        self.opend = False
        self._handle = None

        # ?,?,?,RST_N,SS,MISO,MOSI,clock SS,RST_N=low-active
        self.pin_rstn_high = 0b0001_1000 
        self.pin_rstn_low  = 0b0000_1000
        self.pin_ss_high   = 0b0001_1000
        self.pin_ss_low    = 0b0001_0000
        self.pin_direction = 0b0001_1011 # 1=out/0=in D0～D7
        self.bytes_ss_high = bytes([0x80, self.pin_ss_high, self.pin_direction])
        self.bytes_ss_low = bytes([0x80, self.pin_ss_low, self.pin_direction])

    @staticmethod
    def _search():
        FTD2xx.load_dll()
        num = FTD2xx.FT_CreateDeviceInfoList()
        if num == 0:
            return []
        device_list = FTD2xx.FT_GetDeviceInfoList(num)
        info = []
        for i in range(len(device_list)):
            di = DeviceInfo(
                SPI_DEVICE_FTD2xx,
                device_list[i][4], # serial number
                {
                    "flag":device_list[i][0],
                    "type":device_list[i][1],
                    "id":device_list[i][2],
                    "locaton":device_list[i][3],
                    "serial number":device_list[i][4],
                    "description":device_list[i][5],
                    "handle":device_list[i][6]
                }
            )
            info.append(di)
        FTD2xx.unload_dll()
        return info

    def _open(self, info):
        if info.device != SPI_DEVICE_FTD2xx:
            raise Exception(f"not match device type. -> {info}")

        FTD2xx.load_dll()
        self._handle = FTD2xx.FT_OpenEx(FTD2xx.FT_OPEN_BY_SERIAL_NUMBER, info.id)

        # setup device
        FTD2xx.FT_ResetDevice(self._handle)
        FTD2xx.FT_SetUSBParameters(self._handle, 0xffff, 0xffff)
        FTD2xx.FT_SetChars(self._handle, 0, 0, 0, 0)
        FTD2xx.FT_SetTimeouts(self._handle, 3000, 0)
        FTD2xx.FT_SetLatencyTimer(self._handle, 1)
        FTD2xx.FT_SetFlowControl(self._handle, FTD2xx.FT_FLOW_RTS_CTS, 0, 0)
        FTD2xx.FT_SetBitMode(self._handle, 0x00, FTD2xx.FT_BITMODE_RESET)
        FTD2xx.FT_SetBitMode(self._handle, 0x00, FTD2xx.FT_BITMODE_MPSSE)

        # read all read_buffer
        size = FTD2xx.FT_GetQueueStatus(self._handle)
        if size > 0:
            ret = FTD2xx.FT_Read(self._handle, size)
            print("read all read_buffer1 ",ret)

        # bogus opcode test
        ret = FTD2xx.FT_Write(self._handle, bytes([0xaa]))
        if ret != 1:
            raise Exception("failed to write test.")
        ret = FTD2xx.FT_Read(self._handle, 2)
        if len(ret) != 2 or ret[0] != 0xfa or ret[1] != 0xaa:
            raise Exception("failed to read test.")
        
        # setup MPSSE
        FTD2xx.FT_Write(self._handle, bytes([0x85])) # disable loopback
        FTD2xx.FT_Write(self._handle, bytes([0x86, 0x02, 0x00])) # set clock divisor (60MHz / 6 = 10MHz)
        FTD2xx.FT_Write(self._handle, bytes([0x8a])) # disable /5 divider
        FTD2xx.FT_Write(self._handle, bytes([0x80, self.pin_ss_high, self.pin_direction])) # set out-pin low byte
        FTD2xx.FT_Write(self._handle, bytes([0x82, 0x00, 0x00])) # set out-pin high byte

        # # out pin test
        # for i in range(10000):
        #     FTD2xx.FT_Write(self._handle, bytes([0x80, 0b0001_1011, self.pin_direction]))
        #     time.sleep(0.3)
        #     FTD2xx.FT_Write(self._handle, bytes([0x80, 0b0000_0000, self.pin_direction]))
        #     time.sleep(0.3)

        self.opend = True
        self.info.id = info.id
        self.info.detail = info.detail

    def _close(self):
        FTD2xx.FT_Close(self._handle)
        FTD2xx.unload_dll()
        self._handle = None
        self.opend = False

    def send_reset_signal(self):
        FTD2xx.FT_Write(self._handle, bytes([0x80, self.pin_rstn_low, self.pin_direction]))
        time.sleep(0.01)
        FTD2xx.FT_Write(self._handle, bytes([0x80, self.pin_rstn_high, self.pin_direction]))

    def write_burst(self, adr, data):
        length = 1 + len(data) - 1
        buf = [0x11, length%256, length//256, adr]
        buf.extend(data)
        buf = bytes(buf)
        FTD2xx.FT_Write(self._handle, self.bytes_ss_low)
        FTD2xx.FT_Write(self._handle, buf)
        FTD2xx.FT_Write(self._handle, self.bytes_ss_high)

    def write_single(self, adr, data):
        buf = bytes([0x11, 0x01, 0x00, adr, data])
        FTD2xx.FT_Write(self._handle, self.bytes_ss_low)
        FTD2xx.FT_Write(self._handle, buf)
        FTD2xx.FT_Write(self._handle, self.bytes_ss_high)

    def write_multi(self, item_list):
        buf_list = []
        for i in range(len(item_list)):
            buf = bytes([0x11, 0x01, 0x00, item_list[i][0], item_list[i][1]])
            buf_list.append(buf)
        for i in range(len(buf_list)):
            FTD2xx.FT_Write(self._handle, self.bytes_ss_low)
            FTD2xx.FT_Write(self._handle, buf_list[i])
            FTD2xx.FT_Write(self._handle, self.bytes_ss_high)

    def read_single(self, adr):
        buf_write = bytes([0x11, 0x00, 0x00, 0x80|adr]) # MOSI only, LowToHighEdge, MSB fast
        buf_read = bytes([0x21, 0x00, 0x00])            # MISO only, LowToHighEdge, MSB fast
        FTD2xx.FT_Write(self._handle, self.bytes_ss_low)
        FTD2xx.FT_Write(self._handle, buf_write)
        FTD2xx.FT_Write(self._handle, buf_read)
        FTD2xx.FT_Write(self._handle, self.bytes_ss_high)
        ret = FTD2xx.FT_Read(self._handle, 1)
        return ret

    def read_multi(self, adr_list):
        buf_write_list = []
        buf_read_list = []
        for i in range(len(adr_list)):
            buf_write = bytes([0x11, 0x00, 0x00, 0x80|adr_list[i]])
            buf_read = bytes([0x21, 0x00, 0x00])
            buf_write_list.append(buf_write)
            buf_read_list.append(buf_read)
        ret_list = []
        for i in range(len(buf_write)):
            FTD2xx.FT_Write(self._handle, self.bytes_ss_low)
            FTD2xx.FT_Write(self._handle, buf_write_list[i])
            FTD2xx.FT_Write(self._handle, buf_read_list[i])
            FTD2xx.FT_Write(self._handle, self.bytes_ss_high)
            ret = FTD2xx.FT_Read(self._handle, 1)
            ret_list.append(ret[0])
        return ret_list

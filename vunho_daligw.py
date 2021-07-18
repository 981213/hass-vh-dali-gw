#!/usr/bin/python3
from pymodbus.client.sync import ModbusTcpClient
import time
UNIT = 0x1

class VunhoDaliGW:
    def __init__(self, host, port) -> None:
        self.client = ModbusTcpClient(host=host, port=port, timeout=1)

    def connect(self) -> bool:
        ret = self.client.connect()
        if not ret:
            return False
        # This annoying device sends a "www.szyuanhao.com,socket=X" string when connected.
        # It should be cleared before any modbus requests.
        time.sleep(0.1)
        self.client._check_read_buffer()
        return True

    def test_or_reconnect(self):
        if self.client.is_socket_open():
            return
        if not self.connect():
            raise RuntimeError("failed to reconnect.")

    def read_regs(self, addr, reg, count):
        mb_reg = addr << 8 | reg
        self.test_or_reconnect()
        rr = self.client.read_holding_registers(mb_reg, count, unit=UNIT)
        assert(not rr.isError())
        return rr.registers

    def write_reg(self, addr, reg, val):
        self.test_or_reconnect()
        mb_reg = addr << 8 | reg
        rr = self.client.write_register(mb_reg, val, unit=UNIT)
        assert(not rr.isError())

    def read_mac_addr(self):
        r = self.read_regs(80, 216, 3)
        return "%02x:%02x:%02x:%02x:%02x:%02x" % (r[0] >> 8, r[0] & 0xff, r[1] >> 8, r[1] & 0xff, r[2] >> 8, r[2] & 0xff)

    def read_dev_list(self):
        ret = []
        r = self.read_regs(80, 238, 1)
        ndevs = r[0]
        self.write_reg(80, 236, 0)
        for _ in range(64):
            r = self.read_regs(80, 240, 1)
            if (r[0] >> 8) < 64:
                ret.append((r[0] >> 8, r[0] & 0xff))
                if len(ret) >= ndevs:
                    break
        return ret

    def set_brightness(self, addr, val):
        if val > 254:
            val = 254
        if val < 0:
            val = 0
        self.write_reg(addr, 44, val)

    def get_brightness(self, addr):
        return self.read_regs(addr, 44, 1)[0]
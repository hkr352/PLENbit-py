# 180927 eeprom motion ,merge
# 180907 mix lib, BLE OK 
from microbit import *

class PLENbit():
    def __init__(self):
        self.SERVO_NUM = 0x08
        self.SERVO_SET_INIT = [1000, 630, 300, 600, 240, 600, 1000, 720]
        self.SERVO_ANGLE =    [1000, 630, 300, 600, 240, 600, 1000, 720]
        self.romADR1 = 0x56
        self._i2c = i2c
        self._i2c.init()
        self.secretIncantation()
        self.setAngle([0, 0, 0, 0, 0, 0, 0, 0], 1000)
    def secretIncantation(self):
        self.write8(0xFE, 0x85)
        self.write8(0xFA, 0x00)
        self.write8(0xFB, 0x00)
        self.write8(0xFC, 0x66)
        self.write8(0xFD, 0x00)
        self.write8(0x00, 0x01)
    def servoWrite(self, num, degrees):
        HighByte = False
        PWMVal = degrees * 100 * 226 / 10000
        PWMVal = round(PWMVal) + 0x66
        if (PWMVal > 0xFF):
            HighByte = True
        self.write8(self.SERVO_NUM + num * 4, PWMVal)
        if (HighByte):
            self.write8(self.SERVO_NUM + num * 4 + 1, 0x01)
        else:
            self.write8(self.SERVO_NUM + num * 4 + 1, 0x00)
    def write8(self, addr, d):
        cmd = bytearray(2)
        cmd[0] = addr
        cmd[1] = d
        self._i2c.write(0x6A, cmd)
        del cmd
    def motion(self, filename):
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        command = ">"
        list_len = 43
        _read_adr = 0x32+860*filename
        error = 0
        while 1:
            if error == 1:
                break
            _ls_n = 0   # list_num
            mf = self.reep(_read_adr, list_len)
            # print(mf)
            _read_adr += list_len
            _bytedata = bytearray(1)
            _bytedata[0] = mf[0]
            if _bytedata == b'\xff':
                break
            mf = str(mf, 'utf-8')
            #print(mf)
            while list_len > _ls_n:
                #print(mf[_ls_n])
                if command != mf[_ls_n]:
                    _ls_n += 1
                    continue
                _ls_n += 1
                if "MF" != (mf[_ls_n] + mf[_ls_n+1]):
                    _ls_n += 2
                    continue
                _ls_n += 2
                
                if filename != int((mf[_ls_n] + mf[_ls_n+1]), 16):
                    error = 1
                    break
                _ls_n += 4
                times = (mf[_ls_n] + mf[_ls_n+1] + mf[_ls_n+2] + mf[_ls_n+3])
                time = int(times, 16)
                _ls_n += 4
                val = 0
                while 1:
                    if (list_len < (_ls_n+4)) or (command == mf[_ls_n]) or (24 < val):
                        self.setAngle(data, time)
                        #print(data)
                        break
                    num = (mf[_ls_n] + mf[_ls_n+1] + mf[_ls_n+2] + mf[_ls_n+3])
                    num_h = int(num, 16)
                    if num_h >= 0x7fff:
                        num_h = ~(~num_h & 0xffff)
                    else:
                        num_h = num_h & 0xffff
                    data[val] = num_h
                    val = val+1
                    _ls_n += 4
        del mf
        del data
    def setAngle(self, angle, msec):
        _step = [0, 0, 0, 0, 0, 0, 0, 0]
        _msec = msec/30
        for _val in range(0, 8):
            _target = (self.SERVO_SET_INIT[_val] - angle[_val])
            if (_target != self.SERVO_ANGLE[_val]):  # Target != Present
                _step[_val] = (_target - self.SERVO_ANGLE[_val])/(_msec)
        for _neko in range(0, _msec):
            for _val in range(0, 8):
                self.SERVO_ANGLE[_val] += _step[_val]
                self.servoWrite(_val, (self.SERVO_ANGLE[_val]/10))
        del _step
        del _msec
    
    def reep(self, eepAdr, num):
        _data = bytearray(2)
        _data[0] = eepAdr >> 8 
        _data[1] = eepAdr & 0xFF
        # need adr change code
        self._i2c.write(self.romADR1, _data)
        value = (self._i2c.read(self.romADR1, num, repeat=False))
        return value[:]

plenbit = PLENbit()
display.show("P")

pin16.write_digital(1) #EYE LED ON
Lsensor = pin0
Rsensor = pin2

def L_chika():
    
    for _val in range(0, 4):
        pin16.write_digital(0)
        sleep(100)
        pin16.write_digital(1)
        sleep(100)

while 1:
    
    if button_a.is_pressed():
        L_chika()
        plenbit.motion(int( b"46",16)) # Walk
    elif button_b.is_pressed():
        display.show(Image.HAPPY)
        plenbit.motion(int( b"29",16)) # Arm patapata
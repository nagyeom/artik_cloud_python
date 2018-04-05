#-*- coding: utf-8 -*-
#for ARTIK530 RGB LED sensor
import sys
import time
import json
from datetime import datetime


class BlinkLED():
    """
    LED센서 동작을 위한 함수를 모아놓은 클래스
    """
    def __init__(self, color):
        self.color = color
        if color == 'red':
            self.gpioNum = 128
        elif color == 'green':
            self.gpioNum = 129
        elif color == 'blue':
            self.gpioNum = 130

    def exportGPIO(self):
        """
        artik에서 sensor 사용하기 위해서는 export 작업이 우선되어야한다.
        #export GPIO pin by opening file and writing the pin number to it
        """
        pinctl = open("/sys/class/gpio/export", "wb", 0)
        try:
            pinctl.write( str(self.gpioNum))
            print "Exported pin", str(self.gpioNum) , self.color
        except:
            print "Pin ", str(self.gpioNum) , self.color , " has been exported"
        pinctl.close()

    def directionGPIO(self):
        """
        export후 direction을 out하는 작업이 필요하다.
        #set GPIO pin to be digital output
        """
        filename = '/sys/class/gpio/gpio%d/direction' % self.gpioNum
        pinctldir = open(filename, "wb", 0)
        try:
            pinctldir.write("out")
            print "Set pin ", str(self.gpioNum), " as digital output"
        except:
            print "Failed to set pin direction"
        pinctldir.close()    

    def turn_on(self):
        """
        sensor turn on : value값이 바뀌기만 하면 상태 변경된다.
        """
        self.exportGPIO()
        self.directionGPIO()
        filename = '/sys/class/gpio/gpio%d/value' % self.gpioNum
        with open(filename,'wb') as pin:
            pin.write(str(0))

    def turn_off(self):
        """
        sensor turn off
        """
        self.exportGPIO()
        self.directionGPIO()
        filename = '/sys/class/gpio/gpio%d/value' % self.gpioNum
        with open(filename,'wb') as pin:
            pin.write(str(1))

    def exitGPIO(self):
        """
        사용하지 않는 sensor에 대한 정보는 unexport 시켜서 완벽하게 제거
        """
        pinctl = open("/sys/class/gpio/unexport", "wb", 0)
        try:
            pinctl.write( str(self.gpioNum))
            print "Unexported pin", str(self.gpioNum)
        except:
            print "Pin ", str(self.gpioNum), " has been unexported"
        pinctl.close()

    def offLED(self, value):
        filename = '/sys/class/gpio/gpio%d/value' % self.gpioNum
        if value == 1: 
            with open(filename,'wb') as pin:
                pin.write( str(0) )
        else :
            with open(filename,'wb') as pin:
                pin.write( str(1) )

def printNowTime():
    now = datetime.now()
    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
    print '\n%s\n' % nowTime
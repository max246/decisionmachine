import time
import threading
import serial

class Arduino:

        def __init__(self,port):
          self.port = port
	def init(self):
	  self.ser = serial.Serial(port=self.port, baudrate=9600)
	  self.ser.close()
	  self.ser.open()

	def reconnect(self):
	  self.ser.close()
	  self.ser.open()

	def send(self,message):

	  if self.ser.isOpen():
	     self.ser.write(message+"\n")
	  else:
	     self.reconnect()
	     self.send(message)


	def read(self):
	  self.ser.timeout = 1
	  return self.ser.readline()


	def close(self):
	  self.ser.timeout = 0
	  self.ser.cloes()



class ThreadArduino(threading.Thread):
	
      
	def __init__(self):
		threading.Thread.__init__(self)
                self.isYesReady = False
                self.isNoReady = False
	
        def setup(self, arduinoYes,arduinoNo):
                self.arduinoYes = arduinoYes
                self.arduinoNo  = arduinoNo

        def update(self,numberYes,numberNo):
                if self.isYesReady:
                    self.arduinoYes.send("U"+str(numberYes)+"\n");
                #if self.isNoReady:
                  #  self.arduinoNo.send("U"+str(numberNo)+"\n");

	def run(self):
		while not self.isYesReady and not self.isNoReady:
			output = self.arduinoYes.read()
                        if output != None and len(output) > 0:
                            if output.find("Segment") >= 0:
                                self.isYesReady = True
                            print "yes",output
                        #output = self.arduinoNo.read()
                        #if output != None and len(output) > 0:
                        #    if output.find("Segment") >= 0:
                        #        self.isNoReady = True
                        #    print "no",output
                            #self.parser(output)
                        time.sleep(1)

#arduino = Arduino()
#arduino.init()

#print arduino.read()
#print arduino.read()
#arduino.send("LIGHT2OFF")

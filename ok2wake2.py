#!/usr/bin/env python
import RPi.GPIO as GPIO, time, datetime
#for checking break file
import os.path
# for importing the ini file
import ConfigParser #chgange to configparser in Python3
settings = ConfigParser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()


# Permanent Settings
my_breakfile = "/break.zzz"
RED_LED = 17
YELLOW_LED = 21


# Setup 
def setup():
 GPIO.setmode(GPIO.BCM)       		# Set the board mode to numbers pins by physical location
 GPIO.setup(RED_LED, GPIO.OUT)   	# Set pin mode as output
 GPIO.setup(YELLOW_LED, GPIO.OUT)  	# Set pin mode as output
		
def loop():
 while True:
  currentHour = datetime.datetime.now().hour
  currentMinute =  datetime.datetime.now().minute
  day_date = datetime.date(year, month, day) # Found this as an example - test to see if it works.
  currentDay = day_date.isoweekday() 	#Monday is 1 and Sunday is 7
  print currentDay
# Import the correct config file 
  if (currentDay >= 1 and currentDay <= 4):
   settings.read('weekday.ini')
  elif (currentDay == 7):
   settings.read('weekday.ini')
  else:
   settings.read('weekend.ini')
# Set variables
# Dynamic settings that will be put into ini files
#hourToSleep = 20
#hourOKtoWake = 06
#minuteOKtoWake = 15
#hourOKtoLeaveRoom = 7
#minuteOKtoLeaveRoom = 00

  hourToSleep = settings.get('time2Sleep', 'hourToSleep')
  miniuteToSleep = settings.get('time2Sleep', 'miniuteToSleep')
  hourOKtoWake = settings.get('timeOK2Wake', 'hourOKtoWake')
  minuteOKtoWake = settings.get('timeOK2Wake', 'minuteOKtoWake')
  hourOKtoLeaveRoom = settings.get('timeOK2LeaveRoom', 'hourOKtoLeaveRoom')
  minuteOKtoLeaveRoom = settings.get('timeOK2LeaveRoom', 'minuteOKtoLeaveRoom')

   
# Looping - run according to the current time
  if os.path.exists(my_breakfile):
   print 'break break break!'
   destroy()
   break

  elif (currentHour == hourToSleep-1):
   print currentHour
   print 'Almost time to go to sleep'
   countA = 0
   while countA < 10:
    GPIO.output(YELLOW_LED, GPIO.HIGH)  # led on
    time.sleep(1)
    GPIO.output(YELLOW_LED, GPIO.LOW)  # led off
    time.sleep(1)
    countA += 1
    time.sleep(1)
#  Sleep before next loop (short)
   time.sleep(45)

  elif (currentHour >= hourToSleep or currentHour < hourOKtoWake-2):
   print currentHour
   print 'Go to sleep!'
   GPIO.output(RED_LED, GPIO.HIGH)   # led on
#  Sleep before next loop (long)
   time.sleep(3600)

  elif (currentHour >= hourOKtoWake-2 and currentHour < hourOKtoWake):
   print currentHour
   print 'almost time to wake'
   GPIO.output(RED_LED, GPIO.HIGH)   # led on
#  Sleep before next loop (short)
   time.sleep(60)
   
  elif (currentHour >= hourOKtoWake and currentMinute >= minuteOKtoWake and currentHour < hourOKtoLeaveRoom):
   print currentHour
   print 'OK to wake up, but stay in your room!'
   GPIO.output(RED_LED, GPIO.LOW)  # led off
   GPIO.output(YELLOW_LED, GPIO.HIGH)  # led on
#  Sleep before next loop (short)
   time.sleep(60)
    
  elif (currentHour == hourOKtoLeaveRoom and currentMinute >= minuteOKtoLeaveRoom):
   print currentHour
   print 'OK to leave room!'
   GPIO.output(RED_LED, GPIO.LOW)  # led off
   GPIO.output(YELLOW_LED, GPIO.LOW)  # led off
#  Sleep before next loop (long)
   time.sleep(3600)

  elif (currentHour >= hourToSleep):
   print currentHour
   print 'Go to sleep!'
   GPIO.output(RED_LED, GPIO.HIGH)   # led on
#  Sleep before next loop (long)
   time.sleep(3600)

  else:
   print currentHour
   GPIO.output(RED_LED, GPIO.LOW)  # led off
   GPIO.output(YELLOW_LED, GPIO.LOW)  # led off
#  Sleep before next loop (long)
   time.sleep(5)
 
def destroy():
 GPIO.output(RED_LED, GPIO.LOW)      # RED led off
 GPIO.output(YELLOW_LED, GPIO.LOW)      # Yellow led off  
 GPIO.cleanup()         # Release resource
 

if __name__ == '__main__':     # Program start from here
 setup()
 
 try:
  loop()
 except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the destroy() will be  executed.
  destroy()
  
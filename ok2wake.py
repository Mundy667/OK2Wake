#!/usr/bin/env python
import RPi.GPIO as GPIO, time, datetime
#for checking break file
import os.path
# for importing the ini file
import ConfigParser #chgange to configparser in Python3
settings = ConfigParser.ConfigParser()
#settings._interpolation = ConfigParser.ExtendedInterpolation()
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.basicConfig(filename='/mnt/OK2Wake_logs/ok2wake.log',level=logging.INFO)

# Permanent Settings
my_breakfile = "/break.zzz"
RED_LED = 17
YELLOW_LED = 21


# Setup 
def setup():
 GPIO.setwarnings(False)
 GPIO.setmode(GPIO.BCM)       		# Set the board mode to numbers pins by physical location
 GPIO.setup(RED_LED, GPIO.OUT)   	# Set pin mode as output
 GPIO.setup(YELLOW_LED, GPIO.OUT)  	# Set pin mode as output
		
def loop():
 while True:
  currentYear = datetime.datetime.now().year
  currentMonth = datetime.datetime.now().month
  currentDay = datetime.datetime.now().day
  currentHour = datetime.datetime.now().hour
  currentMinute =  datetime.datetime.now().minute
  day_date = datetime.date(currentYear, currentMonth, currentDay) 
  currentDay = day_date.isoweekday() 	#Monday is 1 and Sunday is 7
  
# Import the correct config file 
  if (currentDay >= 1 and currentDay <= 4):
   settings.read('weekday.ini')
   print 'import weekday ini'
  elif (currentDay == 6 or currentDay == 7):
   settings.read('weekday.ini')
   print 'import weekend ini'
  else:
   settings.read('weekday.ini')
   print 'something went wrong, importing weekday ini'
# Set variables
  hourToSleep = int(settings.get('time2Sleep', 'hourToSleep'))
  miniuteToSleep = int (settings.get('time2Sleep', 'miniuteToSleep'))
  hourOKtoWake = int (settings.get('timeOK2Wake', 'hourOKtoWake'))
  minuteOKtoWake = int(settings.get('timeOK2Wake', 'minuteOKtoWake'))
  hourOKtoLeaveRoom = int(settings.get('timeOK2LeaveRoom', 'hourOKtoLeaveRoom'))
  minuteOKtoLeaveRoom = int(settings.get('timeOK2LeaveRoom', 'minuteOKtoLeaveRoom'))

# Looping - run according to the current time
  if os.path.exists(my_breakfile):
   logging.warning('break!')
   destroy()
   break

  elif (currentHour == hourToSleep-1):
   logging.info('Almost time to go to sleep!')
   print 'Almost time to go to sleep, its currentHour:currentMinute'
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
   logging.info('Go to sleep!')
   GPIO.output(RED_LED, GPIO.HIGH)   # led on
#  Sleep before next loop (long)
   time.sleep(3600)

  elif (currentHour >= hourOKtoWake-2 and currentHour < hourOKtoWake):
   logging.info('Almost time to wake up')
   print currentHour
   print 'almost time to wake'
   GPIO.output(RED_LED, GPIO.HIGH)   # led on
#  Sleep before next loop (short)
   time.sleep(60)
   
  elif (currentHour >= hourOKtoWake and currentMinute >= minuteOKtoWake and currentHour < hourOKtoLeaveRoom):
   print currentHour
   logging.info('OK to wake, but stay in your room!')
   print 'OK to wake up, but stay in your room!'
   GPIO.output(RED_LED, GPIO.LOW)  # led off
   GPIO.output(YELLOW_LED, GPIO.HIGH)  # led on
#  Sleep before next loop (short)
   time.sleep(60)
    
  elif (currentHour == hourOKtoLeaveRoom and currentMinute >= minuteOKtoLeaveRoom):
   logging.info('Good morning! Its OK to leave your room!')
   print currentHour
   print 'OK to leave room!'
   GPIO.output(RED_LED, GPIO.LOW)  # led off
   GPIO.output(YELLOW_LED, GPIO.LOW)  # led off
#  Sleep before next loop (long)
   time.sleep(3600)

  elif (currentHour >= hourToSleep):
   logging.info('Go to sleep!')
   print currentHour
   print 'Go to sleep!'
   GPIO.output(RED_LED, GPIO.HIGH)   # led on
#  Sleep before next loop (long)
   time.sleep(3600)

  else:
   logging.info('Currently not active')
   print currentHour
   GPIO.output(RED_LED, GPIO.LOW)  # led off
   GPIO.output(YELLOW_LED, GPIO.LOW)  # led off
#  Sleep before next loop (long)
   time.sleep(3600)
 
def destroy():
 logging.warning('Script ending')
 GPIO.output(RED_LED, GPIO.LOW)      # RED led off
 GPIO.output(YELLOW_LED, GPIO.LOW)      # Yellow led off  
 GPIO.cleanup()         # Release resource
 

if __name__ == '__main__':     # Program start from here
 setup()
 
 try:
  loop()
 except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the destroy() will be  executed.
  destroy()
  

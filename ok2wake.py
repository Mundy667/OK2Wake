#!/usr/bin/env python
import RPi.GPIO as GPIO, time, datetime
#for checking break file
import os.path
# for importing the ini file
import ConfigParser #chgange to configparser in Python3
settings = ConfigParser.ConfigParser()
#settings._interpolation = ConfigParser.ExtendedInterpolation()


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
  logFile = "/mnt/OK2Wake_logs/currentYear_currentMonth_currentDay.log"
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
   echo 'break! day_date' >> logFile
   destroy()
   break

  elif (currentHour == hourToSleep-1):
   echo 'Almost time to go to sleep, its currentHour:currentMinute' >> logFile
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
   echo 'Go to sleep! its currentHour:currentMinute' >> logFile
   GPIO.output(RED_LED, GPIO.HIGH)   # led on
#  Sleep before next loop (long)
   time.sleep(3600)

  elif (currentHour >= hourOKtoWake-2 and currentHour < hourOKtoWake):
   echo 'Almost time to wake up, its currentHour:currentMinute' >> logFile
   print currentHour
   print 'almost time to wake'
   GPIO.output(RED_LED, GPIO.HIGH)   # led on
#  Sleep before next loop (short)
   time.sleep(60)
   
  elif (currentHour >= hourOKtoWake and currentMinute >= minuteOKtoWake and currentHour < hourOKtoLeaveRoom):
   print currentHour
   echo 'OK to wake up, but stay in room, its currentHour:currentMinute' >> logFile
   print 'OK to wake up, but stay in your room!'
   GPIO.output(RED_LED, GPIO.LOW)  # led off
   GPIO.output(YELLOW_LED, GPIO.HIGH)  # led on
#  Sleep before next loop (short)
   time.sleep(60)
    
  elif (currentHour == hourOKtoLeaveRoom and currentMinute >= minuteOKtoLeaveRoom):
   echo 'OK to leave room, its currentHour:currentMinute' >> logFile
   print currentHour
   print 'OK to leave room!'
   GPIO.output(RED_LED, GPIO.LOW)  # led off
   GPIO.output(YELLOW_LED, GPIO.LOW)  # led off
#  Sleep before next loop (long)
   time.sleep(3600)

  elif (currentHour >= hourToSleep):
   echo 'Go to sleep, its currentHour:currentMinute' >> logFile
   print currentHour
   print 'Go to sleep!'
   GPIO.output(RED_LED, GPIO.HIGH)   # led on
#  Sleep before next loop (long)
   time.sleep(3600)

  else:
   echo 'Not active - currentHour:currentMinute' >> logFile
   print currentHour
   GPIO.output(RED_LED, GPIO.LOW)  # led off
   GPIO.output(YELLOW_LED, GPIO.LOW)  # led off
#  Sleep before next loop (long)
   time.sleep(3600)
 
def destroy():
 echo 'Script Ending - currentHour:currentMinute' >> logFile
 GPIO.output(RED_LED, GPIO.LOW)      # RED led off
 GPIO.output(YELLOW_LED, GPIO.LOW)      # Yellow led off  
 GPIO.cleanup()         # Release resource
 

if __name__ == '__main__':     # Program start from here
 setup()
 
 try:
  loop()
 except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the destroy() will be  executed.
  destroy()
  

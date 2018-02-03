#!/usr/bin/env python
		
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
# Set variables
  hourToSleep = 20
  miniuteToSleep = 15
  hourOKtoWake = 6
  minuteOKtoWake = 30
  hourOKtoLeaveRoom = 7
  minuteOKtoLeaveRoom = 30

# Looping - run according to the current time
  if (currentHour == hourToSleep-1):
   countA = 0
   while countA < 10:
    countA += 1
#  Sleep before next loop (short)
   time.sleep(45)

  elif (currentHour == hourToSleep):
   if (currentMinute < miniuteToSleep):
    timetowait = 60 * (miniuteToSleep - currentMinute -1)
    time.sleep(timetowait)
   elif (currentMinute => miniuteToSleep):
#   Sleep before next loop (long)
    time.sleep(14400)

  elif (currentHour >= hourToSleep or currentHour < hourOKtoWake-2):
   print currentHour
#  Sleep before next loop (long)
   time.sleep(3600)

  elif (currentHour >= hourOKtoWake-2 and currentHour < hourOKtoWake):
   print currentHour
   print 'almost time to wake'
#  Sleep before next loop (short)
   time.sleep(60)
   
  elif (currentHour >= hourOKtoWake and currentMinute >= minuteOKtoWake and currentHour < hourOKtoLeaveRoom):
   print currentHour
   print 'OK to wake up, but stay in your room!'
#  Sleep before next loop (short)
   time.sleep(60)
    
  elif (currentHour == hourOKtoLeaveRoom and currentMinute >= minuteOKtoLeaveRoom):
   print currentHour
   print 'OK to leave room!'
#  Sleep before next loop (long)
   time.sleep(3600)

  elif (currentHour >= hourToSleep):
   print currentHour
   print 'Go to sleep!'
#  Sleep before next loop (long)
   time.sleep(3600)

  else:
   print currentHour
#  Sleep before next loop (long)
   time.sleep(3600)
 
def destroy():
 

if __name__ == '__main__':     # Program start from here

 try:
  loop()
 except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the destroy() will be  executed.
  destroy()
  

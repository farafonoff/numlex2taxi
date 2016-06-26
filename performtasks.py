import fdb
from configuration import ConfigurationService
import time
import logging
import sys
import signal
import threading
import traceback

cfg = ConfigurationService()

## TASKNAME                              LASTTIME  INTERVALSEC     STARTTIME STARTWEEKDAY ISACTIVE      ERRCODE LASTEXECMSEC
query="""select TASKNAME from TASK
    where (((dateadd(second, INTERVALSEC, LASTTIME) < current_timestamp)
          or (STARTWEEKDAY is null and STARTTIME < current_time and current_date + STARTTIME > coalesce(LASTTIME, '01.01.01'))
	        or (extract(weekday from current_date) = STARTWEEKDAY and STARTTIME < current_time and current_date + STARTTIME > coalesce(LASTTIME, '01.01.01'))))
		    and coalesce(ISACTIVE, '1') = 2
		        order by LASTTIME"""

def performtask(con, taskname):
	try:
		startt = time.time()
		cur=con.cursor()
		cur.execute("execute procedure performtask(?)",[taskname])
		con.commit()
		print(taskname+" executed at "+str(time.time()-startt)+" sec")
	except:
		print(taskname+" failed")
		traceback.print_exc()
		con.rollback()

needexit=False

def safeexit(signal, frame):
#	print("=== exiting === "+str(signal))
	needexit=True

def cleanup():
	print("=== cleanup started ===")
	con = cfg.taxi_connection()
	cur = con.cursor()
	cur.execute("update task set isactive=1 where isactive=2");
	con.commit()
	con.close()
	print("=== cleanup done === ")


con = cfg.taxi_connection()
cur = con.cursor()

#cur.execute("update task set isactive=2 where isactive=1");
def mainloop():
	while not needexit:
		startt = time.time()
		cur.execute(query)
		tasks = cur.fetchall()
		for task in tasks:
			taskname = task[0]
			performtask(con, taskname);
		con.commit()
		if len(tasks)>0:
			print("=== TOTAL TIME: "+str(time.time()-startt)+" sec")
		time.sleep(5)

worker=threading.Thread(target=mainloop)
worker.start()


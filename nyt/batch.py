import win32api

import os
import subprocess
import time
import shutil


yearsNumeral = [2000,2001,2002]
years = [str(y) for y in yearsNumeral]


for year in years:
	log = './"%s"' % year + '.log'
	cmd = ['scrapy ', 'crawl ', 'nyts ', '-a', 'year=', year, ' --logfile ', log]
	p = subprocess.Popen([cmd], shell=False, stdout=subprocess.PIPE)  # Asynchronous
	while p.poll() != 0:
		pass
	pr.terminate()  # Terminated the process Which allows next crawl process to be started
	time.sleep(3600)  #wait one hour until next crawl


	shutil.move("./"+year+".log", "D:\\data\\nyt\\"+year+".log")
	shutil.move("./"+year+".csv", "D:\\data\\nyt\\" + year + ".csv")



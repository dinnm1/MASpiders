import win32api

import os
import subprocess
import time
import shutil


waitingTimeBetweenYears = 15000
yearsNumeral = [1976, 1975,]


years = [str(y) for y in yearsNumeral]


for year in years:
	print("Starting scraping for year: " + year)
	log = './"%s"' % year + '.log'
	cmd = ['scrapy ', 'crawl ', 'nyts19801970 ', '-a', 'year=', year, ' --logfile ', log]
	p = subprocess.Popen([cmd], shell=False, stdout=subprocess.PIPE)  # Asynchronous
	while p.poll() != 0:
		pass
	p.terminate()  # Terminated the process Which allows next crawl process to be started

	shutil.move("./"+year+".log", "D:\\data\\nyt\\test\\"+year+".log")
	shutil.move("./"+year+".csv", "D:\\data\\nyt\\test\\" + year + ".csv")

	print("Finished year: " + year)
	if year != years[-1]:
		print("Entering waiting time between crawls for different years")
		time.sleep(waitingTimeBetweenYears)  #wait until next crawl
		print("Exited waiting time between crawls for different years")




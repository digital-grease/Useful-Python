#HIGHLY RECOMMEND CHANGING VARIABLE NAMES
#Variable names have been scrubbed in an incredibly lazy manner (by me), to the easiest possible replacements.
#I highly recommend replacing them with something more descriptive of the files you're handling,
#for the sake of readability/your own sanity.


import csv, subprocess, time, os
import pandas as pd
from tqdm import tqdm #,trange

print ("Please ensure this script is running in the same directory as your CSV files!!!\n")
print ("Filenames must be: '[filename1].csv' and '[filename2].csv'!!! \n")
time.sleep(3)
csvfile1 = open("""name of first csv file""", 'r+')
csvfile2 = open("""name of second csv file""", 'r+')

def fqdnlookup():
	print ("Checking for FQDN's!!!")
	fqdn1 = open("fqdn1.csv", 'a', newline='')
	fqdn2 = open("fqdn2.csv", 'a', newline='')
	results1 = csv.writer(fqdn1, delimiter=',')
	results2 = csv.writer(fqdn2, delimiter=',')
	CREATE_NO_WINDOW = 0x08000000
	csv1 = pd.read_csv(csvfile1, index_col=False, header=None) [0]
	csv2 = pd.read_csv(csvfile2, index_col=False, header=None) [28]
	list1 = []
	list2 = []

	for thing in csv1:
		list1.append(thing)
	print ('\nfile 1...')
	for i in tqdm(list1):
		fqdn = subprocess.Popen(["nslookup", str(i)], stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
		for line in fqdn.stdout:
			if "Name" in line.decode('utf8'):
				output1 = [str(line)[11:-5]]
				results1.writerow(output1)
	fqdn1.close()

	for thing in csv2:
		list2.append(thing)
	print('\nfile 2...')
	for i in tqdm(list2):
		fqdn = subprocess.Popen(["nslookup", str(i)], stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
		for line in fqdn.stdout:
			if "Name" in line.decode('utf8'):
				output2 = [str(line)[11:-5]]
				results2.writerow(output2)
	fqdn2.close()

#csvdiff function takes in csv's, returns values present in one, but not the other
def csvdiff():
	with open('results1.csv', 'a') as outfile1:	#files that will be written
		fqdn1 = open('fqdn1.csv', 'r+', newline='')
		fqdn2 = open('fqdn2.csv', 'r+', newline='')
		results = csv.writer(outfile1, delimiter=',')
		csv1 = set(pd.read_csv(fqdn1, index_col=False, header=None) [0])
		csv2 = set(pd.read_csv(fqdn2, index_col=False, header=None) [0])
		final = csv1-csv2
		print ("\nDiffing files...")
		for i in tqdm(final, leave=False):
			results.writerow([i])
		fqdn1.close()
		fqdn2.close()


#separatebydomain does exactly that.
def separatebydomain():
	print ("\nSeparating by domain...")
	with open('domain1.csv', 'a', newline='') as domain1, \
	open('domain2.csv', 'a', newline='') as domain2, \
	open('domain3.csv', 'a', newline='') as domain3, \
	open('results1.csv', 'r+') as infile:
		target = pd.read_csv(infile, index_col=False, header=None) [0]
		d1results = csv.writer(domain1, delimiter=',')										#csv writer to csv file
		d2results = csv.writer(domain2, delimiter=',')										#csv writer to csv file
		d3results = csv.writer(domain3, delimiter=',')										#csv writer to csv file

		for line in tqdm(target, leave=False):									#tqdm is progress bar module
			if ".[DOMAIN2]" not in line and ".[DOMAIN3]" not in line:
				d1results.writerow([line])
			elif ".[DOMAIN2]" in line:
				d2results.writerow([line])
			elif ".[DOMAIN3]" in line:
				d3results.writerow([line])
			else:
				print ("I've encountered an error, closing now.")
				break

#fetchlocation takes file of fqdn's and separates by location based on ip range
#only useful really if your network is segmented at least partially by physical location
def fetchlocation():
	with open('domain1.csv', 'r+', newline='') as domain1open, \
	open('domain2.csv', 'r+', newline='') as domain2open, \
	open('domain3.csv', 'r+', newline='') as domain3open:
		CREATE_NO_WINDOW = 0x08000000 #creation flag to keep cmd windows from popping up

		def domain1check():
			print ("\nChecking domain1...\n")
			for i in tqdm(domain1target, leave=False):									#tqdm is progress bar module
				fqdn = subprocess.Popen(["nslookup", i], stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)	#open shell and call nslookup
				for line in fqdn.stdout:
					if "[FIRST_2/3_IP_OCTETS]" in line.decode('utf8'):
						with open('loc1_dom1.csv', 'a', newline='') as loc1dom1:	#the with statements are made inside the if statements
							loc1results = csv.writer(loc1dom1, delimiter=',')		#to prevent creation of empty files
							loc1results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('loc2_dom1.csv', 'a', newline='') as loc2dom1:
							loc2results = csv.writer(loc2dom1, delimiter=',')
							loc2results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('loc3_dom1.csv', 'a', newline='') as loc3dom1:
							loc3results = csv.writer(loc3dom1, delimiter=',')
							loc3results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('loc4_dom1.csv', 'a', newline='') as loc4dom1:
							loc4results = csv.writer(loc4dom1, delimiter=',')
							loc4results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('loc5_dom1.csv', 'a', newline='') as loc5dom1:
							loc5results = csv.writer(loc5dom1, delimiter=',')
							loc5results.writerow([i])
					else:
						with open('random_dom1.csv', 'a', newline='') as randomdom1:
							randomresults = csv.writer(randomdom1, delimiter=',')
							randomresults.writerow([i])
			print ('Finished!!!\n')

		def domain2check():
			print ("Checking domain2...\n")
			for i in tqdm(domain2target, leave=False):									#tqdm is progress bar module
				fqdn = subprocess.Popen(["nslookup", i], stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)	#open shell and call nslookup
				for line in fqdn.stdout:
					if "[FIRST_2/3_IP_OCTETS]" in line.decode('utf8'):
						with open('loc1_dom2.csv', 'a', newline='') as loc1dom2:
							loc1results = csv.writer(loc1dom2, delimiter=',')
							loc1results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('loc2_dom2.csv', 'a', newline='') as loc2dom2:
							loc2results = csv.writer(loc2dom2, delimiter=',')
							loc2results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('loc3_dom2.csv', 'a', newline='') as loc3dom2:
							loc3results = csv.writer(loc3dom2, delimiter=',')
							loc3results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('loc4_dom2.csv', 'a', newline='') as loc4dom2:
							loc4results = csv.writer(loc4dom2, delimiter=',')
							loc4results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('loc5_dom2.csv', 'a', newline='') as loc5dom2:
							loc5results = csv.writer(loc5dom2, delimiter=',')
							loc5results.writerow([i])
					else:
						with open('random_dom2.csv', 'a', newline='') as randomdom2:
							randomresults = csv.writer(randomdom2, delimiter=',')
							randomresults.writerow([i])
			print ('Finished!!!\n')

		def domain3check():
			print ("Checking domain3...\n")
			for i in tqdm(domain3target, leave=False):									#tqdm is progress bar module
				fqdn = subprocess.Popen(["nslookup", i], stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)	#open shell and call nslookup
				for line in fqdn.stdout:
					if "[FIRST_2/3_IP_OCTETS]" in line.decode('utf8'):
						with open('chs_dmz.csv', 'a', newline='') as chsdmz:
							loc1results = csv.writer(chsdmz, delimiter=',')
							loc1results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('clt_dmz.csv', 'a', newline='') as cltdmz:
							loc2results = csv.writer(cltdmz, delimiter=',')
							loc2results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('rdu_dmz.csv', 'a', newline='') as rdudmz:
							loc3results = csv.writer(rdudmz, delimiter=',')
							loc3results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('gvl_dmz.csv', 'a', newline='') as gvldmz:
							loc4results = csv.writer(gvldmz, delimiter=',')
							loc4results.writerow([i])
					elif "[FIRST_2/3_IP_OCTETS]" in line.decode('utf-8'):
						with open('tul_dmz.csv', 'a', newline='') as tuldmz:
							loc5results = csv.writer(tuldmz, delimiter=',')
							loc5results.writerow([i])
					else:
						with open('random_dmz.csv', 'a', newline='') as randomdmz:
							randomresults = csv.writer(randomdmz, delimiter=',')
							randomresults.writerow([i])
			print ('Finished!!!\n')
		if os.path.getsize('domain1.csv') > 0:
			domain1target = pd.read_csv(domain1open, index_col=False, header=None) [0]
			domain1check()
		if os.path.getsize('domain2.csv') > 0:
			domain2target = pd.read_csv(domain2open, index_col=False, header=None) [0]
			domain2check()
		if os.path.getsize('domain3.csv') > 0:
			domain3target = pd.read_csv(domain3open, index_col=False, header=None) [0]
			domain3check()

#cleans up file writes from previous functions
def cleanup():
	print ("Picking up my trash...")
	filelist = ['results1.csv', 'domain1.csv', 'domain2.csv','domain3.csv', 'fqdn1.csv', 'fqdn2.csv']
	for i in filelist:
		os.remove(i)
	print ("All done!!!")
	time.sleep(1)



def main():
	option = input("Would you like to begin? Enter y/n: ")
	print ("\n")
	if option.lower() == 'y':
		try:
			fqdnlookup()
		except:
			print("Fqdnlookup function failed!!! Closing now!!!")
		try:
			csvdiff()
		except:
			print("Csvdiff function failed!!! Closing now!!!")
			time.sleep(3)
		try:
			separatebydomain()
		except:
			print ("Fetchfqdn function failed!!! Closing now!!!")
			time.sleep(3)
		try:
			fetchlocation()
		except:
			print ("Fetchlocation function failed!!! Closing now!!!")
			time.sleep(3)
		try:
			cleanup()
		except:
			print ("Cleanup function failed!!! Closing Now!!!")
			time.sleep(3)
	elif option.lower() == 'n':
		print ('OK, Exiting!!!')
		time.sleep(3)
		exit()
	else:
		print ("\nYou've entered an invalid option, closing now. ")
		time.sleep(2)

	#try functions, except fail

keepgoing = 0
while keepgoing == 0:
	main()
	restart = input('\nDo you want to try again? "y/n": ')
	if restart.lower() == 'y':
		keepgoing = 0
	elif restart.lower() == 'n':
		keepgoing += 1
		break
	else:
		print ("Invalid input")
		keepgoing = 0
print ("\n\nThanks for using my crappy script!!! Goodbye!!!")
time.sleep(3)
exit()
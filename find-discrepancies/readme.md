#Find discrepancies, process and sort

This script does several things, and provides progress bars for each step:

1. Take in two csv files of hostnames/fqdn's, find elements in one but not the other
  * outputs single results file

2. Perform nslookup to acquire fqdn for any that are missing
  * outputs results file

3. Uses nslookup results to sort by specified domains
  * outputs separate results files for each domain

4. Separates further by ip based location
  * *This is only really useful if your internal network is segmented according to location, i.e. 10.100 belongs to one location, while 10.200 belongs to another*
  * outputs files for each domain/location combination, as well as 'random' files for ip's not included in the ranges defined

5. Cleans up all except the final set of files

6. Calls each function in a try/except that will notify if a specific function fails

7. Provides continuation loop in case you want to run it again for some reason

import sys
import getopt
import random
import time

# Global Variables
PROXY_STATUS = 1 				# Put PROXY_STATUS TO 0, for using your real IP
PROXY_GENERATION_STATUS = 0
NAME_LIST = []
ADDRESS_LIST = []
PROXY_LIST = []
COUNT = 5
PROXY_TYPE = 'PROXY_CHAINS'
URL_LIST = []
DELAY = 5
# paths of input and output files
NAME_LIST_PATH = './input_files/name_list.txt'
ADDRESS_LIST_PATH = './input_files/address_list.txt'
PROXY_LIST_PATH = './input_files/proxy_list.txt'
URL_SCRAPPED_PATH = './output_files/url_scrapped.txt'
QUERY_NAME_PATH = './output_files/name_scrapped.txt'
USER_DETAILS = './output_files/user_details.csv'

try:
	from selenium import webdriver
	from selenium.webdriver.support import expected_conditions as EC
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support.select import Select 
	from selenium.webdriver.common.by import By 
	from selenium.webdriver.common.keys import Keys
except:
	print('''
		\033[91m 
		[   ERROR  ] Selenium API not installed in system...\033[97m
		[ SOLUTION ] Install selenium using pip tool...
		''')
	sys.exit()

def banner():
	print('---------------------------------------------------------')
	print('TruePeopleSearch.com Scrapper')
	print('\t\t\tversion: 1.0.1\n\t\t\tauthor: Prashant Varshney')
	print('---------------------------------------------------------')

def usage():
	print('''
	usage :
		python3 optimus.py [ options ]
		
		-n : path of names lists / if not specifies default is used
		-a : path of address lists / if not specifies default is used
		-c : count
		-p : selects proxy type / path of proxy lists 
		-g : generate proxy list
		''')

def parsing_args():
	options = 'n:a:c:p:g'
	optlist,args = getopt.getopt(sys.argv[1:],options)
	if len(optlist) < 1:
		print('''
		\033[91m 
	[   ERROR  ] Invalid / Incomplete system arguments...\033[97m
		''')
		usage()
		sys.exit()
	return (optlist,args)

def generate_proxy_list():
	global PROXY_LIST_PATH
	global PROXY_GENERATION_STATUS
	# will create it latter

def update_global_variables(optlist,args):
	global NAME_LIST
	global ADDRESS_LIST
	global COUNT
	global PROXY_STATUS
	global PROXY_GENERATION_STATUS
	global NAME_LIST_PATH
	global ADDRESS_LIST_PATH
	global PROXY_LIST_PATH
	global PROXY_TYPE
	global PROXY_LIST
	# parsing command line argumemts
	for i in range(len(optlist)):		
		if optlist[i][0] == '-n':
			NAME_LIST_PATH = optlist[i][1]
		if optlist[i][0] == '-a':
			ADDRESS_LIST_PATH = optlist[i][1]
		if optlist[i][0] == '-c':
			COUNT = int(optlist[i][1])
		if optlist[i][0] == '-p':
			PROXY_STATUS = 1
			if optlist[i][1] == 'tor':
				PROXY_TYPE = 'TOR'
			else:
				PROXY_LIST_PATH = optlist[i][1]
		if optlist[i][0] == '-g':
			PROXY_GENERATION_STATUS = 1
	# parsing of command line arguments completed
	# fetching name_list
	with open(NAME_LIST_PATH,'r') as fd:
		string = fd.readline()
		while string:
			NAME_LIST.append(string.replace('\n',''))
			string  = fd.readline()
	#fetching address_list
	with open(ADDRESS_LIST_PATH,'r') as fd:
		string = fd.readline()
		while string:
			ADDRESS_LIST.append(string.replace('\n',''))
			string  = fd.readline()
	#Generating proxy_list
	if PROXY_GENERATION_STATUS :
		generate_proxy_list()
	if PROXY_TYPE == 'PROXY_CHAINS':
		# fetching proxy_list]
		with open(PROXY_LIST_PATH,'r') as fd:
			string = fd.readline()
			while string:
				PROXY_LIST.append(string.replace('\n',''))
				string  = fd.readline()
	if PROXY_TYPE == 'TOR':
		PROXY_LIST.append('127.0.0.1:9050')
	


def initialising_browser():
	print('[ + ] Initialising Firefox')
	firefox_options = webdriver.FirefoxOptions()
	firefox_options.add_argument('--start-maximized')
	profile = webdriver.FirefoxProfile()
	driver = webdriver.Firefox(options=firefox_options,firefox_profile=profile)
	input('[ + ] Press return after installing Proxy Extensions')
	print('[ + ] Initialisation Completed')
	return driver

def detect_reCaptcha(driver):
    captcha_field1 = False
    captcha_field2 = False
    print('[ + ] Checking presence of reCaptcha')
    try:
        captcha_field1 = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/h2').text == 'Human Test'
    except:
        pass
    try:
        captcha_field2 = driver.find_element_by_xpath('/html/body/p').text == 'Human test, sorry for the inconvenience.\nPlease check the box below.'
    except:
        pass
    if captcha_field1 or captcha_field2:
        return True
    else:
        return False

def get_request(driver,url):
	print('[ + ] Requesting URL : '+url)
	loading_status = True
	url_reload_status = True
	reload_count = 0
	while loading_status :
		while url_reload_status:		
			try:
				driver.get(url)
				url_reload_status = False
			except Exception as e:
				print('[ + ] '+str(e))
				input('[ + ] Press return to continue, fetching same URL')
				reload_count += 1
				if reload_count >= 5 :
					print('[ + ] Cannot able to fetch '+url)
					return False
		print('[ + ] Webpage loaded successfully')

		#Detecting the presence of reCaptcha
		if detect_reCaptcha(driver) :
			input('[ + ] Captcha Found, press return after solving reCaptcha ')
			try:
				driver.delete_all_cookies() 
				print('[ + ] Deleting driver Cookies ')
			except:
				print('[ + ] Unable to delete driver Cookies')
			url_reload_status = True
		else:
			loading_status = False
	# inserting delay time so that server doesn't gets overloaded
	print('[ + ] Sleeping for '+str(DELAY)+' seconds')
	time.sleep(5)
	return True

def true_people_search(driver,name, address):
	global URL_LIST
	global QUERY_NAME_PATH
	print('[ + ] Starting Query on Name : '+name+' , Address : '+address)
	#query_url = 'https://www.truepeoplesearch.com/results?name=TEMP_NAME&citystatezip=TEMP_CITY&page=TEMP_NUM'
	query_url = 'https://www.truepeoplesearch.com/results?name=TEMP_NAME&citystatezip=TEMP_CITY&agerange=60-120&page=TEMP_NUM'
	# querying name and address
	search_url = query_url.replace('TEMP_NAME',name).replace('TEMP_CITY',address).replace('TEMP_NUM','1')
	res_status = get_request(driver,search_url)	
	
	# collecting number of results found
	if res_status:
		number_of_results = int(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[1]').text.split(' ')[0])
		print('[ + ] Number of Search Results : ' + str(number_of_results))
		number_of_pages = 1 if (number_of_results < 10) else number_of_results // 10
		print('[ + ] Number of Pages to Query : ' + str(number_of_pages))
		
		# querying on each page
		print('[ + ] Starting querying on each page')
		for num in range(1,number_of_pages+1):
			search_url = query_url.replace('TEMP_NAME',name).replace('TEMP_CITY',address).replace('TEMP_NUM',str(num))
			get_request(driver,search_url)	
			print('[ + ] Bundling list of users found')
			bundled_list = driver.find_elements_by_tag_name('a')
			users_list = []
			for i in range(len(bundled_list)):
			    if bundled_list[i].get_attribute('aria-label') == 'View All Details':
			        users_list.append(bundled_list[i].get_attribute('href'))
			# Removing Duplicate Enteries
			users_list = list(set(users_list))
			with open(URL_SCRAPPED_PATH,'a') as fd:
				for i in range(len(users_list)):
					print(users_list[i])
					fd.write(users_list[i]+'\n')
					fd.flush()
			URL_LIST.extend(users_list)
			if len(URL_LIST) >= COUNT:
				break
	print('[ + ] Finishing Query on Name : '+name+' , Address : '+address)
	with open(QUERY_NAME_PATH,'a') as fd:
		fd.write(name+':'+address+'\n')
		fd.flush()

def generate_list_of_urls():
	global ADDRESS_LIST
	global NAME_LIST
	global URL_LIST
	for name in NAME_LIST:
		for address in ADDRESS_LIST:
		#address = ADDRESS_LIST[random.randint(0,len(ADDRESS_LIST))]		# point of duplicacy of data
			true_people_search(driver,name,address)
			if len(URL_LIST) >= COUNT:
				return

if __name__ == '__main__':
	banner()
	optlist,args = parsing_args()
	update_global_variables(optlist,args)
	driver = initialising_browser()

	# generating list of urls of input name and address
	generate_list_of_urls()
	print('\n[ + ] Total Users Found : '+str(len(URL_LIST)))
	
	# query about the each user in URL_LIST
	for i in range(len(URL_LIST)):
		user_name = ""
		user_age = 'NaN'
		user_contact = ""
		user_address = ""
		print('\n[ + ] Serial : '+str(i+1))
		get_request(driver,URL_LIST[i])
		# Name
		try:
			user_name = driver.find_element_by_xpath('//*[@id="personDetails"]/div[1]/div/span[1]').text.replace('\t',' ').replace(',',' ')
		except:
			pass
		# age
		try:
			user_age = str(int(driver.find_element_by_xpath('//*[@id="personDetails"]/div[1]/div/span[2]').text.split(' ')[1]))
		except:
			pass
		#contact
		try:
			user_contact = driver.find_element_by_xpath('//*[@id="personDetails"]/div[6]/div[2]').text[14:].replace(' - Wireless',',').replace(' - Landline',',').replace('View All Phone Numbers','').replace('\n','').replace('\t',' ')[:-1]
		except:
			pass
		#address 
		try:
			user_address = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[4]/div[2]/div[2]/div[1]/div/a').text.replace('\n',',').replace('\t',' ').replace(',',' ')
		except:
			pass
		user_contact = user_contact
		print('\nName : '+user_name)
		print('Age : '+user_age)
		print('Contact : '+user_contact)
		print('Address : '+user_address)
		
		# writing in CSV file
		with open(USER_DETAILS,'a') as fd:
			fd.write(user_name+','+user_age+','+user_address+',')
			user_contact = user_contact.split(',')
			for num in user_contact:
				fd.write(num+',')
			fd.write('\n')
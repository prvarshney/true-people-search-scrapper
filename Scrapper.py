from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.select import Select 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import xlwt
import sys
import os
import time
from datetime import datetime

## GLOBAL VARIABLES THEIR VALUES DIRECTLY EXTRACTED FROM CONFIG FILES
HTTP_PROXY_1 = None
PORT_1 = None
HTTP_PROXY_2 = None
PORT_2 = None
USER_NAME = None
PASSWORD = None
FIRST_NAMES = None
LAST_NAMES = None
STATES = None
ZIP_CODES = None
AGE_GROUP = None
COUNT = None
TIMEOUT = None
DELAY = None
## GLOBAL VARIABLE THEIR VALUE IS DERIVED FROM ABOVE VARIABLES
PROXY_SERVER_USED = 1
CITY_STATE_ZIP = None
TARGET_URLS = []
DRIVER = None
USER_DETAILS = None

def detect_reCaptcha():
    global DRIVER
    captcha_field1 = False
    captcha_field2 = False
    print('[  INFO  ] Checking Presence Of reCaptcha')
    try:
        ## CHECKING PRESENCE OF TEXT LIKE HUMAN TEST ON PRESENT WEB PAGE
        captcha_field1 = DRIVER.find_element_by_xpath('/html/body/div[2]/div/div[2]/h2').text == 'Human Test'
    except:
        ## THIS BLOCK RUNS WHEN THEIRS NO TEXT LIKE ABOVE AVAILABLE ON WEB PAGE
        pass
    try:
        ## CHECKING PRESENCE OF TEXT LIKE HUMAN TEST, SORRY FOR INCONVENIENCE ON PRESENT WEB PAGE
        captcha_field2 = DRIVER.find_element_by_xpath('/html/body/p').text == 'Human test, sorry for the inconvenience.\nPlease check the box below.'
    except:
        ## THIS BLOCK RUNS WHEN THEIRS NO TEXT LIKE ABOVE AVAILABLE ON WEB PAGE
        pass
    if captcha_field1 or captcha_field2:
        return True
    else:
        return False

def print_banner():
    ## CLEARING CONSOLE
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    ## PRINTING BANNER
    print("""
----------------------------------------------------------------------------------------------
                                    Optimus - True People Scrapper                    v1.0
----------------------------------------------------------------------------------------------
                                                                    -<c> Prashant Varshney""")


## READING CONFIGURATION FILES
def initialisation():
    global HTTP_PROXY_1
    global PORT_1
    global HTTP_PROXY_2
    global PORT_2
    global USER_NAME
    global PASSWORD
    global FIRST_NAMES
    global LAST_NAMES
    global AGE_GROUP
    global ZIP_CODES
    global STATES 
    global COUNT
    global TIMEOUT
    global DELAY
    global CITY_STATE_ZIP
    ############################## READING CONFIGURATION FILES ###############################
    config = ConfigParser(allow_no_value=True)
    if "Config.cfg" in os.listdir():
        print("[  INFO  ] Reading Configuration File - Config.cfg")
        config.read('Config.cfg')
    else:
        print("[  ERROR ] Configuration File - Config.cfg Is Missing")
        print("[  INFO  ] Exiting...")
        sys.exit(0)
    if "TargetingAge.cfg" in os.listdir(os.path.join(os.getcwd(),"InputData")):
        print('[  INFO  ] Reading Configuration File - TargetingAge.cfg ')
        config.read('InputData/TargetingAge.cfg')
    else:
        print("[  ERROR ] Configuration File - TargetingAge.cfg Is Missing")
        print("[  INFO  ] Exiting...")
        sys.exit(0)
    if "TargetingCities.cfg" in os.listdir(os.path.join(os.getcwd(),"InputData")):
        print('[  INFO  ] Reading Configuration File - TargetingCities.cfg ')
        config.read('InputData/TargetingCities.cfg')
    else:
        print("[  ERROR ] Configuration File - TargetingCities.cfg Is Missing")
        print("[  INFO  ] Exiting...")
        sys.exit(0)
    if "TargetingNames.cfg" in os.listdir(os.path.join(os.getcwd(),"InputData")):
        print('[  INFO  ] Reading Configuration File - TargetingNames.cfg ')
        config.read('InputData/TargetingNames.cfg')
    else:
        print("[  ERROR ] Configuration File - TargetingNames.cfg Is Missing")
        print("[  INFO  ] Exiting...")
        sys.exit(0)
    ############################## UPDATING GLOBAL VARIABLES ##################################
    print('[  INFO  ] Updating Global Variables')
    HTTP_PROXY_1 = config["PROXY_SERVER_1"]["HTTP_PROXY"]
    PORT_1 = config["PROXY_SERVER_1"]["PORT"]
    HTTP_PROXY_2 = config["PROXY_SERVER_2"]["HTTP_PROXY"]
    PORT_2 = config["PROXY_SERVER_2"]["PORT"]
    FIRST_NAMES = list(config["FIRST-NAME-COL"])
    LAST_NAMES = list(config["LAST-NAME-COL"])
    AGE_GROUP = list(config["AGE-COL"])
    ## SPLITING AGE GROUPS IN LOWER AND UPPER LIMITS
    for i in range(len(AGE_GROUP)):
        AGE_GROUP[i] = tuple(AGE_GROUP[i].split("-"))
    ZIP_CODES = list(config["ZIP-COL"])
    STATES = list(config["CITY-STATE-COL"])
    COUNT = int(config["SCRAPPER_CONFIG"]["COUNT"])
    DELAY = int(config["SCRAPPER_CONFIG"]["DELAY"])
    TIMEOUT = int(config["SCRAPPER_CONFIG"]["TIMEOUT"])
    CITY_STATE_ZIP = ZIP_CODES + STATES

def initialising_browser():
    global HTTP_PROXY_1
    global PORT_1
    global HTTP_PROXY_2
    global PORT_2
    global PROXY_SERVER_USED
    global DRIVER
    ##
    print('[  INFO  ] Initialising Chrome With Config.cfg Configurations')
    ## SETTING CHROME TO START WITH FULL SCREEN GUI
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--start-maximized')
    ## SETTING UP PROXY SERVER
    if PROXY_SERVER_USED == 1:
        proxy_server = f'{HTTP_PROXY_2}:{PORT_2}'
        PROXY_SERVER_USED = 2
    elif PROXY_SERVER_USED == 2:
        proxy_server = f'{HTTP_PROXY_1}:{PORT_1}'
        PROXY_SERVER_USED = 1
    print(f'[  INFO  ] Using Proxy - {proxy_server}')
    chrome_options.add_argument(f'--proxy-server={proxy_server}')
    ## BLOCKING IMAGE LOADING
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    ## SETTING ALL THESE CONFIGURATIONS
    DRIVER = webdriver.Chrome(
        executable_path=os.path.join(os.getcwd(),"Resources","chromedriver.exe"),
        options=chrome_options
        )
    print('[  INFO  ] Chrome Initialisation Completed')
    return DRIVER

def get_request(url):
    global DELAY
    global DRIVER
    global TIMEOUT
    print('[  INFO  ] Requesting URL : '+url)
    loading_status = True
    url_reload_status = True
    reload_count = 0
    while loading_status :
        while url_reload_status:		
            try:
                DRIVER.set_page_load_timeout(TIMEOUT)
                DRIVER.get(url)
                url_reload_status = False
            except Exception as e:
                print('[  ERROR ] '+str(e))
                print('[  INFO  ] Deleting Browser Cookies')
                DRIVER.delete_all_cookies() 
                print('[  INFO  ] Trying To Fetch Same URL')
                reload_count += 1
                if reload_count >= 5 :
                    print('[  ERROR ] Cannot Able To Fetch : '+url)
                    return False
        print('[  INFO  ] Webpage Loaded Successfully')
        ## DETECTING THE PRESENCE OF RECAPTCHA
        if detect_reCaptcha() :
            print('[  INFO  ] Captcha Found, Rotating IP Address ')
            try:
                DRIVER.delete_all_cookies() 
                DRIVER.quit()           ## CLOSING OLD INSTANCE OF BROWSER
                print('[  INFO  ] Deleting Browser Cookies And Re-Initialising Browser')
                DRIVER = initialising_browser()
            except:
                print('[  INFO  ] Unable To Delete Browser Cookies And Re-Initialise Browser')
            url_reload_status = True
        else:
            loading_status = False
    ## INSERTING DELAY TIME SO THAT SERVER DOESN'T GETS OVERLOADED
    if DELAY > 0:
        print(f'[  INFO  ] Sleeping For {DELAY} Seconds')
        time.sleep(DELAY)
    return True

def true_people_search(f_name,l_name,address,lower_age_limit,upper_age_limit):
    global TARGET_URLS
    global DRIVER
    print(f'\n[  INFO  ] Starting Query on Name : {f_name} {l_name}, Address : {address}, Age Group : {lower_age_limit}-{upper_age_limit}')
    query_url = f'https://www.truepeoplesearch.com/results?name={f_name} {l_name}&citystatezip={address}&agerange={lower_age_limit}-{upper_age_limit}&page=TEMP_NUM'
    search_url = query_url.replace('TEMP_NUM','1')
    res_status = get_request(search_url)	
    ## COLLECTING NUMBER OF RESULTS FOUND
    if res_status:
        ## CHECKING WHETHER THIS COMBINATION PRESENTS ON WEBSITE OR NOT
        try:
            number_of_results = int(DRIVER.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[1]').text.split(' ')[0])
        except:
            number_of_results = 0            
        print('[  INFO  ] Number Of Search Results : ' + str(number_of_results))
        number_of_pages = 1 if (number_of_results < 10) else number_of_results // 10
        print('[  INFO  ] Number Of Pages To Query : ' + str(number_of_pages))
        ## QUERYING ON EACH PAGE
        print('[  INFO  ] Starting Querying On Each Page')
        for num in range(1,number_of_pages+1):
            search_url = query_url.replace('TEMP_NUM',str(num))
            get_request(search_url)	
            print('[  INFO  ] Bundling List Of Users Found\n')
            bundled_list = DRIVER.find_elements_by_tag_name('a')
            users_list = []
            for i in range(len(bundled_list)):
                if bundled_list[i].get_attribute('aria-label') == 'View All Details':
                    users_list.append(bundled_list[i].get_attribute('href'))
            ## Removing Duplicate Enteries
            users_list = list(set(users_list))
            TARGET_URLS.extend(users_list)
            if len(TARGET_URLS) >= COUNT:
                break
        print(f'[  INFO  ] Finishing Query On Name : {f_name} {l_name}, Address : {address}, Age Group : {lower_age_limit}-{upper_age_limit}')


def generate_list_of_urls():
    global FIRST_NAMES
    global LAST_NAMES
    global AGE_GROUP
    global CITY_STATE_ZIP
    global TARGET_URLS
    global COUNT
    ## CREATING COMBINATIONS OF FIRST_NAMES, LAST_NAMES, ETC.
    for (lower_age_limit,upper_age_limit) in AGE_GROUP:
        for f_name in FIRST_NAMES:
            for l_name in LAST_NAMES:
                for address in CITY_STATE_ZIP:
                    true_people_search(f_name,l_name,address,lower_age_limit,upper_age_limit)
                    if len(TARGET_URLS) >= COUNT:
                        return
    print('[  INFO  ] All The Possible Combinations Of Names And CityStateZip Created')


if __name__ == "__main__":
    print_banner()
    initialisation()
    DRIVER = initialising_browser()
    generate_list_of_urls()
    print(f'\n[  INFO  ] Total Users Found : {len(TARGET_URLS)}')
    ## QUERY ABOUT THE EACH USER IN TARGET_URLS
    ## CREATING FILE FOR STORING HARVESTED DATA, HERE I AM GOING TO ADD HEADERS IN FILE
    USER_DETAILS = f'./HarvestedOutput/ScrappedDetails_{datetime.now().strftime("(%d-%m-%Y)_(%H-%M-%S)")}.csv'
    print(f'[  INFO  ] Storing Harvested Data in {USER_DETAILS}')
    with open(USER_DETAILS,'w') as fd:
        fd.write(f'Name,Age,Address,Wireless-1,Wireless-2,Wireless-3,Wireless-4,Wireless-5,Wireless-6,Landline-1,Landline-2,Landline-3,Landline-4,Landline-5,Landline-6\n')
        fd.flush()
    for i in range(len(TARGET_URLS)):
        user_name = ""
        user_age = 'NaN'
        user_contact = ""
        user_address = ""
        print(f'\n[  INFO  ] Serial : {i+1}')
        get_request(TARGET_URLS[i])
        ## NAME
        try:
            user_name = DRIVER.find_element_by_xpath('//*[@id="personDetails"]/div[1]/div/span[1]').text.replace('\t',' ').replace(',',' ')
        except:
            pass
        ## AGE
        try:
            user_age = str(int(DRIVER.find_element_by_xpath('//*[@id="personDetails"]/div[1]/div/span[2]').text.split(' ')[1]))
        except:
            pass
        ## CONTACT
        try:
            user_contact = DRIVER.find_element_by_xpath('//*[@id="personDetails"]/div[6]/div[2]').text[14:].replace('View All Phone Numbers','').replace(' - Landline','&Landline;').replace(' - Wireless','&Wireless;').replace('\n','').replace('\t',' ')
        except:
            pass
        ## ADDRESS 
        try:
            user_address = DRIVER.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[4]/div[2]/div[2]/div[1]/div/a').text.replace('\n',',').replace('\t',' ').replace(',',' ')
        except:
            pass
        if user_age == 'NaN':
            continue
        ## SPLITING INTO DIFFERENT CATEGORIES LIKE LANDLINE AND WIRELESS
        user_contact = user_contact.split(';')[:-1]      ## -1 TO REMOVE BLANK ELEMENT OF LIST
        ## SPLITING FURTHER INTO NUMERIC VALUES AND STRINGS
        wireless = []
        landline = []
        for i in range(len(user_contact)):
            user_contact[i] = user_contact[i].split('&')
            if user_contact[i][1] == 'Landline':
                landline.append(user_contact[i][0])
            if user_contact[i][1] == 'Wireless':
                wireless.append(user_contact[i][0])
        print('\nName : '+user_name)
        print('Age : '+user_age)
        print(f'Wireless Contact : {wireless}')
        print(f'Landline Contact : {landline}')
        print('Address : '+user_address)
        ## WRITING IN CSV FILE
        with open(USER_DETAILS,'a') as fd:
            fd.write(user_name+','+user_age+','+user_address+',')
            ## ENTERING WIRELESS CONTACT NUMBERS
            blank_space = 6-len(wireless) if(len(wireless) <= 6) else 0
            for i in range(len(wireless)):
                fd.write(wireless[i]+',')
                if i == 6:
                    break
            for i in range(blank_space):
                fd.write(',')
            ## ENTERING LANDLINE CONTACT NUMBERS
            blank_space = 6-len(landline) if(len(landline) <= 6) else 0
            for i in range(len(landline)):
                fd.write(landline[i]+',')
                if i == 6:
                    break
            for i in range(blank_space):
                fd.write(',')
            fd.write('\n')
    print('\n\n[  INFO  ] Extraction Completed')
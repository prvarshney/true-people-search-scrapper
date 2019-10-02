from configparser import ConfigParser
import xlwt
import sys
import os

## GLOBAL VARIABLES
HTTP_PROXY = None
PORT = None
USER_NAME = None
PASSWORD = None
FIRST_NAMES = None
LAST_NAMES = None
STATES = None
ZIP_CODES = None
AGE_GROUP = None

def print_banner():
    ## CLEARING CONSOLE
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    ## PRINTING BANNER
    print("""
--------------------------------------------------------------------------------------------------------
                                    Optimus - True People Scrapper                    v1.0
--------------------------------------------------------------------------------------------------------
                                                                    -<c> Prashant Varshney""")

## READING CONFIGURATION FILES
def initialisation():
    global HTTP_PROXY
    global PORT
    global USER_NAME
    global PASSWORD
    global FIRST_NAMES
    global LAST_NAMES
    global AGE_GROUP
    global ZIP_CODES
    global STATES 
    ############################## READING CONFIGURATION FILES ###############################
    config = ConfigParser(allow_no_value=True)
    if "Proxy.cfg" in os.listdir():
        print("[  INFO  ] Reading Configuration File - Proxy.cfg")
        config.read('Proxy.cfg')
    else:
        print("[  ERROR ] Configuration File - Proxy.cfg Is Missing")
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
    ##
    ############################## UPDATING GLOBAL VARIABLES ##################################
    print('[  INFO  ] Updating Global Variables')
    HTTP_PROXY = config["PROXY_SERVER"]["HTTP_PROXY"]
    PORT = config["PROXY_SERVER"]["PORT"]
    USER_NAME = config["PROXY_SERVER"]["USER_NAME"]
    PASSWORD = config["PROXY_SERVER"]["PASSWORD"]
    FIRST_NAMES = list(config["FIRST-NAME-COL"])
    LAST_NAMES = list(config["LAST-NAME-COL"])
    AGE_GROUP = list(config["AGE-COL"])
    ZIP_CODES = list(config["ZIP-COL"])
    STATES = list(config["CITY-STATE-COL"])
    

if __name__ == "__main__":
    print_banner()
    initialisation()
    print(HTTP_PROXY,PORT,USER_NAME,PASSWORD,FIRST_NAMES,LAST_NAMES,AGE_GROUP,ZIP_CODES,STATES,sep="\n")
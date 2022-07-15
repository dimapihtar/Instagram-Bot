# Import needed libraries

#Import selenium features
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

# Import other usefull libraries
import time, random
import os
from urllib import request as urlrequest
import pandas as pd
from datetime import datetime
import zipfile


# Some proxy settings
PROXY_HOST = '127.1.2.3' # ip
PROXY_PORT = 1234 # port
PROXY_USER = 'user' # username
PROXY_PASS = 'qwerty' # password

# Instagram login data
INSTAGRAM_USERNAME = 'username'
INSTAGRAM_PASSWORD = 'qwerty'

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

# Function that connects chrome to proxy
def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        chrome_options=chrome_options)
    return driver

# Authorization function
# Input - Instagram account username & password
# Output - Authorized instagram session

# time.sleep - uses for freezing code execution for a while to avoid  web page loading delay
def auth(username, password, browser):
	try:
                # open instagram web site
		browser.get('https://instagram.com')
		time.sleep(random.randrange(3,4))
		
                # find fields to input username and password
		input_username = browser.find_element_by_name('username')
		input_password = browser.find_element_by_name('password')

                # input given username and password
		input_username.send_keys(username)
		time.sleep(random.randrange(1,2))
		input_password.send_keys(password)
		time.sleep(random.randrange(1,2))
		input_password.send_keys(Keys.ENTER)
		time.sleep(random.randrange(5,6))

		# click on button "don`t save info for login"
		browser.find_elements_by_class_name("y3zKF")[1].click()
		time.sleep(random.randrange(3,4))

		# click on button "don`t send notifications"
		browser.find_element_by_class_name("HoLwm").click()

		print("=======================")
		print("@"+username+": signed in account")
		print("=======================")
		
	# catch any exceptions
	except Exception as err:
		print(err)
		
		# quit if exception was caught
		browser.quit()

# Function that sends messages
# Input - list of usernames to send ms, message text, csv file to save ms history, browser, name of sender account
# Output - sends the messages, saves sent messages story via csv
def send_message(usernames, message, data, browser, account):
        counter = 1
        for username in usernames:
                try:
                        #browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
                        #time.sleep(random.randrange(2,3))

                        # open reciever instagram page
                        url = "https://instagram.com/" + username
                        browser.get(url)
                        time.sleep(random.randrange(3,4))

                        # follow reciever
                        browser.find_elements_by_class_name("_5f5mN")[0].click()
                        print("=======================")
                        print("@"+account+": Following #"+str(counter)+", on "+str(username))
                        print("=======================")
                        time.sleep(random.randrange(30,60))
                        browser.find_element_by_xpath(("//button[contains(text(),'Follow')]")).click()
                        time.sleep(random.randrange(3,4))
                        
                        # click on button "send message"
                        browser.find_element_by_class_name("_8A5w5").click()
                        time.sleep(random.randrange(3,4))

                        # input message
                        # the loop to avoid symbol '\n' as ENTER in order to don`t send message by separate parts
                        for part in message.split('\n'):
                                # send part of message to input field
                                browser.find_elements_by_tag_name("textarea")[0].send_keys(part)
                                # substitute ENTER to SHIFT+ENTER
                                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
                        time.sleep(random.randrange(1,2))

                        # click on button "send message"
                        button = browser.find_elements_by_class_name("y3zKF")[2]
                        ActionChains(browser).move_to_element(button).click(button).perform()

                        # save just sent data to csv file
                        save([account, username, message,datetime.today().strftime('%Y-%m-%d')], data)
                        print("=======================")
                        print("@"+account+": Sent message #"+str(counter)+", to "+str(username))
                        print("=======================")
                        counter +=1
                    
                        time.sleep(random.randrange(100,150))
                    	
                except Exception as err:        
                        print(err)
                        browser.quit()
        browser.quit()

# Function that realizes messages history saving via csv
# Input - list of information (sender account, username that recieved message, message text, date), name of the csv file
# Output - updated csv file
def save(lst, data):
    df = pd.read_csv(data)
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', 1)
    df.loc[len(df)] = lst
    df.to_csv(data)

if __name__ == '__main__':
    # list of users you want to save message
    usernames = ["cristiano", "leomessi"]
    # message text
    message = "Hi how are you?"
    # open browser with proxy login
    browser = get_chromedriver(use_proxy=True)
    # auth into instagram account
    auth(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, browser)
    time.sleep(random.randrange(3,4))
    # send message
    send_message(usernames, message, "info.csv", browser, INSTAGRAM_USERNAME)

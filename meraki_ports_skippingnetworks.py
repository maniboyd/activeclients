from selenium import webdriver
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

#LOGIN = ""
#PASSWORD = ""
LINK = "https://account.meraki.com/secure/login/dashboard_login"
# PLEASE, PUT YOUR PATH TO CHROMEDRIVER
PATH_TO_CHROMEDRIVER = "C:\\Users\\Manish Sharma\\Desktop\\Python Program\\CiscoMinotor\\venv\\Lib\\site-packages\\selenium\\chromedriver.exe"
# PLEASE, WRITE HERE FILE'S NAME
FILE = 'Network.csv'
# PLEASE, WRITE HERE PATH TO CSV FILE
PATH_TO_CSV_FILE = ""
COLUMN_NAME = 'Network Name' #Name of head column, to drop it
ORGANIZATION = '.' 
# THIS DICT MADE TO FOLLOW WHICH NETWORKS ALREADY DONE
CHECK = {}

LANS = []

output = {}
output1 = []

browser = webdriver.Chrome(executable_path=PATH_TO_CHROMEDRIVER)

with open(PATH_TO_CSV_FILE + FILE) as f: 
    #HERE PROGRAM TAKES ALL NETWORK NAMES AND TAKE THEM TO DICTIONARY
    reader = csv.reader(f)
    for row in reader:
        #print('IT CHECKS ALL: ' + row[0])
        #output.append([row[0]]) # output
        #with open('output.csv', "w", newline="") as file:
        #    writer = csv.writer(file)
        #    writer.writerows(output)
        if row[0] != COLUMN_NAME:
            CHECK[row[0]] = ''
    print(CHECK)

def open_link(): 
    # THIS IS MAIN FUNCTION
    global LINK 
    global LOGIN
    global PASSWORD
    global browser
    global output
    global output1
    global LANS
    time.sleep(2)
    browser.get(LINK)

    time.sleep(3)

    #LOG IN
    email = browser.find_element_by_id('email')
    email.send_keys(LOGIN) 
    submit_button = browser.find_element_by_id('next-btn') 
    submit_button.click()

    time.sleep(5)

    password = browser.find_element_by_id('password')
    password.send_keys(PASSWORD)

    log_in_button = browser.find_element_by_id('login-btn')
    log_in_button.click()

    time.sleep(10) # you can change here time for your needs
    
    for i in CHECK:
        if CHECK[i] != 'Done':
            network_name = i
            try:
                # CHOOSE NEEDED ORGANISATION
                organization = browser.find_element_by_link_text('E la Carte, Inc.')
                organization.click()

            #WAITING FOR PAGE LOADING
                time.sleep(3)

            # FIND AND CHOOSE NEEDED NETWORK
                select_arrow_zone = browser.find_element_by_class_name('Select-arrow-zone') 
                select_arrow_zone.click()

                time.sleep(5)

                input_network = browser.find_element_by_xpath('//*[@id="react-select-2--value"]/div[2]/input')
                input_network.send_keys(network_name)
                input_network.send_keys(Keys.ENTER) 

                time.sleep(5)

            #GOING TO Firewall & traffic shaping
                tables = browser.find_elements_by_class_name('menu-item-container') 
                for x in tables:
                    if x.text == 'Teleworker gateway':
                        needed_table = x
                needed_table.click()
                time.sleep(3)
                organization = browser.find_elements_by_tag_name('a') 
                for z in organization:
                    if z.text == 'Addressing & VLANs' or z.text == 'Addressing & VLANs':
                        firewall = z
                firewall.click()

                time.sleep(5)
                ports = browser.find_elements_by_xpath('//*[@class="ReactFlexTable__row ReactFlexTable__bodyRow PerPortVlanSettingsFlexTable__row  clickable"]')
                lans_1 = []
                for port in ports:
                    if '- - -' in port.text:
                        lans_1.append('Disabled')
                    else:
                        lans_1.append('Enabled')
            ###########################################################
            # CLIENTS
            ###########################################################
                tables = browser.find_elements_by_class_name('menu-item-container') 
                for table in tables:
                    if table.text == 'Network-wide':
                        needed_table = table
                needed_table.click()
                time.sleep(3)
                organization = browser.find_elements_by_tag_name('a') 
                for org in organization:
                    if org.text == 'Clients' or org.text == 'Clients':
                        cli = org
                cli.click()
                time.sleep(3)
                clients = browser.find_elements_by_xpath('//*[@class="ft notranslate undefined nodrag"]')
                if len(clients) == 0: 
                    clients = browser.find_elements_by_xpath('//*[@class="no_items_html"]')
            # no_items_html
                clients_to_csv = []
                for foo in clients:
                    clients_to_csv.append(foo.text)
                done_connections = '|'.join(clients_to_csv)
            ###########################################################
            # CLIENTS
            ###########################################################
                LANS.append([i,lans_1[0], lans_1[1], lans_1[2], lans_1[3],done_connections])
                lans_1 = []
                time.sleep(2)
                with open('output_lan.csv', "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(['Network Name', 'LAN Port 1', 'LAN Port 2', 'LAN Port 3', 'LAN Port 4','Clients'])
                    writer.writerows(LANS)
                time.sleep(2)
                CHECK[network_name] = 'Done'
                browser.get('https://account.meraki.com/login/org_list') 
            except:
                print('Unable to find the network {}, skipping it to find the new one'.format(i))
                browser.get('https://account.meraki.com/login/org_list') 
                continue  
        else:
            continue


if __name__ == '__main__':
    LOGIN = input('Enter your login, please: ')
    PASSWORD = input('Enter your password, please: ')
    while True:
        try:
            open_link()
            break
        except Exception as e:
            print(str(e))
            if str(e) == 'list index out of range':
                browser.quit() 
                break   
            else:
                browser.quit()
                open_link()
    #with open('output_lan.csv', "w", newline="") as file:
    #    writer = csv.writer(file)
    #    writer.writerows(LANS)
    print('DONE')
    #with open('output.csv', "w", newline="") as file:
    #    writer = csv.writer(file)
    #    writer.writerows(output1)

# Dormant
# Good

from selenium import webdriver
import time
import functions
import csv

def klik(driver, xpath, s):
    try:
        driver.find_element_by_xpath(xpath).click()
        time.sleep(s)
    except Exception as e:
        print(e)

def get_element(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath)
    except Exception as e:
        print('elementgetter-', xpath, e)

class mail_obj():
    def __init__(self, Email, Password):
       self.Email = Email
       self.Password = Password

webdriver_location = 'C:\gekodriver\geckodriver.exe'

with open('emails.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        i = mail_obj(row[0], row[1])
        with  webdriver.Firefox(executable_path=webdriver_location) as driver:
            driver.maximize_window()
            try:
                functions.login_yahoo(i, driver)
            except Exception as e:
                print('---> login error', e)
            time.sleep(5)
            current_email = row[0]
            functions.email_check(current_email, driver)
            functions.spam_check(current_email, driver)
            try:
                functions.read_email(current_email, driver)
            except Exception as n:
                print(n)





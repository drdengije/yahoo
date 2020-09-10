import time
from selenium.webdriver.common.keys import Keys
import csv
import random


def login_yahoo(i,driver):
    driver.get('https://mail.yahoo.com/')
    mail = i.Email
    password = i.Password
    time.sleep(5)
    driver.find_element_by_xpath("//a[@class='fuji-button-link fuji-button-text fuji-button-inverted']").click()
    time.sleep(5)
    driver.find_element_by_xpath("//input[@id='login-username']").send_keys(mail)
    time.sleep(5)
    driver.find_element_by_xpath("//input[@id='login-signin']").click()
    time.sleep(5)
    driver.find_element_by_xpath("//input[@id='login-passwd']").send_keys(password)
    time.sleep(5)
    driver.find_element_by_xpath("//button[@id='login-signin']").click()
    time.sleep(5)
    driver.get('https://mail.yahoo.com/')  # if doesnt go to yahoo mail
    time.sleep(5)
    driver.find_element_by_xpath("//div[@class='p_a T_6Fd5 R_6Fd5']//span[@class='D_F ab_C gl_C W_6D6F']").click() #if it's a newly created email

def email_check(current_email, driver):
    try:
        inbox_button = driver.find_element_by_xpath("//span[@class='D_F W_6D6F ab_C i_6FIA p_R o_h G_e J_x Q_689y']")
        inbox_button.click()
        time.sleep(5)
        scroll_down(driver)
        time.sleep(10)
        boxes = driver.find_elements_by_xpath('//ul[@class="M_0 P_0 "]//li')
        print(len(boxes))
        print('--------', len(boxes))
        for box in boxes:
            try:
                time.sleep(2)
                email = box.find_element_by_xpath('.//span[@class="o_h J_x em_N G_e"]')
                print(email.get_attribute('title'))
                with open('blacklist.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        if (email.get_attribute('title') == row[0]):
                            a = box.find_element_by_xpath('.//button[@data-test-id="icon-btn-checkbox"]')
                            a.click()
                            time.sleep(2)
                            driver.find_element_by_xpath("//span[@class='D_X em_N o_h X_eo6 G_e t_l i_N']//span[contains(text(),'Spam')]").click() # spam button
                            time.sleep(2)
                            transfer_write(current_email, row[0], 'sent to spam')

            except:
                print('err')
    except Exception as e:
        print(e)
def spam_check(current_email, driver):
    try:
        spam_button = driver.find_element_by_xpath('//span[@aria-label="Spam, "]')
        spam_button.click()
        time.sleep(5)
        scroll_down(driver)
        time.sleep(10)
        boxes = driver.find_elements_by_xpath('//ul[@class="M_0 P_0 "]//li')
        print(len(boxes))
        print('--------', len(boxes))
        for box in boxes:
            try:
                time.sleep(2)
                email = box.find_element_by_xpath('.//span[@class="o_h J_x em_N G_e"]')
                print(email.get_attribute('title'))
                with open('whitelist.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        if (email.get_attribute('title') == row[0]):
                            a = box.find_element_by_xpath('.//button[@data-test-id="icon-btn-checkbox"]')
                            a.click()
                            time.sleep(2)
                            driver.find_element_by_xpath('//button[@aria-label="Mark as not spam"]').click() # spam button
                            time.sleep(2)
                            transfer_write(current_email, row[0], 'sent from spam to inbox')

            except Exception as z:
                print('err', z)
    except Exception as e:
        print(e)

def read_email(current_email, driver):
    time.sleep(2)
    inbox_button = driver.find_element_by_xpath('//span[@aria-label="Inbox, "]')
    inbox_button.click()
    scroll_down(driver)
    time.sleep(10)
    boxes = driver.find_elements_by_xpath('//ul[@class="M_0 P_0 "]//li')
    print(len(boxes))
    print('--------', len(boxes))
    broj = 0
    while(broj<len(boxes)-1):
        boxes = driver.find_elements_by_xpath('//ul[@class="M_0 P_0 "]//li')
        for e,box in enumerate(boxes):
            go_back = 1
            if(e>broj):
                broj = e
                print(e)
                time.sleep(2)
                do_continue = 0
                try:
                    time.sleep(2)
                    email = box.find_element_by_xpath('.//span[@class="o_h J_x em_N G_e"]')
                    print(email.get_attribute('title'))
                    with open('whitelist.csv', 'r') as csv_file:
                        csv_reader = csv.reader(csv_file)
                        for row in csv_reader:
                            if (email.get_attribute('title') == row[0]):
                                try:
                                    button = driver.find_element_by_xpath('//button[@title="Mark as read"]')
                                    button.click()
                                except Exception as g:
                                    print(g)
                                    do_continue = 1
                                if(do_continue == 0):
                                    try:
                                        box.click()
                                        go_back= 0
                                        reply_to_mail(driver)
                                    except Exception as y:
                                        print(y)
                                    try:
                                        link_click(driver)
                                        transfer_write(current_email, row[0], 'link clicked')
                                    except Exception as t:
                                        print(t)

                                    try:
                                        transfer_write(current_email, row[0], 'replied')
                                    except Exception as k:
                                        print(k)
                                    if(go_back == 0):
                                        driver.back()
                                        time.sleep(2)

                except Exception as h:
                    print(h)


            if (go_back == 0):
                break
            print('----',broj)
            print('----',e)
            print('----',len(boxes))

def scroll_down(driver):
    exit_scroll = 0
    while(exit_scroll == 0):
        first_boxes = driver.find_elements_by_xpath('//ul[@class="M_0 P_0 "]//li')
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
        second_boxes = driver.find_elements_by_xpath('//ul[@class="M_0 P_0 "]//li')
        time.sleep(3)
        if(len(first_boxes) == len(second_boxes)):
            exit_scroll = 1


    #html = driver.find_element_by_tag_name('html')
    #html.send_keys(Keys.PAGE_DOWN)

def transfer_write(active_mail, mail, description):
    with open('transfers.csv', 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([active_mail ,mail, description])

def reply_to_mail(driver):

    responses_list = ["thanks", "appreciate it", "hey great thank you!", "awesome"]

    time.sleep(3)
    driver.find_element_by_xpath('//div[@data-test-id="quick-reply"]').click()  # reply
    time.sleep(2)
    message_box = driver.find_element_by_xpath('//div[@aria-label="Message body"]')
    message_box.send_keys(responses_list[random.randint(0,2)])
    time.sleep(5)
    send_button = driver.find_element_by_xpath('//button[@title="Send this email"]').click()
    send_button.click()
    time.sleep(2)

def link_click(driver):
    link = driver.find_element_by_xpath('(//table[@role="presentation"])[4]')
    time.sleep(2)
    link.click()
    time.sleep(5)
    allTabs = driver.window_handles
    driver.switch_to.window(allTabs[1])
    time.sleep(5)
    driver.close()
    time.sleep(5)
    driver.switch_to.window(allTabs[0])
    time.sleep(2)



import os
# webdriver is frame work which allows us to execute test on browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# bs4 for parsing webpages
from bs4 import BeautifulSoup as soup
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# selenium browser setup
def setup_browser():
    chrome_options = webdriver.ChromeOptions()
    # this is a flag which prevents selenium driven webdriver from being detected
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # returns the current working directory
    prefs = {"download.default_directory" : os.getcwd()}
    chrome_options.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome('/Users/hemant/Downloads/chromedriver', options=chrome_options)
    browser.maximize_window()
    return browser

def get_stock_data(stock_symbol):
    # broswer setup and opening url
    browser = setup_browser()
    url = 'https://www.nseindia.com/'
    browser.get(url)
    # waiting for page load
    time.sleep(10)
    # searching stock by its symbol
    search = browser.find_element_by_xpath('//*[@id="header-search-input"]')
    search.send_keys(stock_symbol)
    search.send_keys(Keys.ENTER)
    time.sleep(5)
    search_result = browser.find_element_by_xpath('//*[@id="searchListing"]/div[1]/div/a')
    search_result.click()
    time.sleep(5)
    # switching to next tab as search result will open in seperate tab
    browser.switch_to.window(browser.window_handles[1])
    time.sleep(5)
    ###### NOT WORKING WITHOUT SCROLL
    ###### Page scroll down such that content will be on screen
    #browser.execute_script("window.scrollBy(0,800)","")
    ###### SOMETHING I DONT KNOW
    # getting historical data by clicking on historical data button
    historical_data_page = browser.find_elements_by_link_text('Historical Data')
    historical_data_page[0].click()
    time.sleep(2)
    # setting range to 1 week
    select_range = browser.find_element_by_xpath('//*[@id="historical-trade"]/section/div/div[1]/div/div[1]/ul/li[6]/a')
    select_range.click()
    # applying filter by clicking onto filter button after setting range
    filter_button = browser.find_element_by_xpath('//*[@id="equity-historical-Date-filter"]/div[3]/button')
    filter_button.click()
    time.sleep(10)
    # table content from historical data
    # table columns
    table_content = browser.find_element_by_xpath('//*[@id="equityHistoricalTable"]/thead')
    table_columns_html = soup(table_content.get_attribute('innerHTML'),'html.parser')
    column_names = []
    for column_name in table_columns_html.findAll('th'):
        column_names.append(column_name.text) 
    # table data
    table_stock_data = browser.find_element_by_xpath('//*[@id="equityHistoricalTable"]/tbody')
    table_stock_data = soup(table_stock_data.get_attribute('innerHTML'),'html.parser')
    stock_data = []
    for column_data in table_stock_data.findAll('td'):
        stock_data.append(column_data.text)
    browser.quit()
    # return column names from table and content of table 
    return column_names, stock_data

# setting up skip list for storing data
class Node(object):
    '''
    Class to implement node
    '''

    def __init__(self, key, level):
        self.key = key

        # list to hold references to node of different level
        self.forward = [None] * (level + 1)


class SkipList(object):
    '''
    Class for Skip list
    '''

    def __init__(self, max_lvl, P):
        # Maximum level for this skip list
        self.MAXLVL = max_lvl

        # P is the fraction of the nodes with level
        # i references also having level i+1 references
        self.P = P

        # create header node and initialize key to -1
        self.header = self.createNode(self.MAXLVL, -1)

        # current level of skip list
        self.level = 0

    # create  new node
    def createNode(self, lvl, key):
        n = Node(key, lvl)
        return n

    # create random level for node
    def randomLevel(self):
        lvl = 0
        while random.random() < self.P and                 lvl < self.MAXLVL: lvl += 1
        return lvl

    # insert given key in skip list
    def insertElement(self, key):
        # create update array and initialize it
        update = [None] * (self.MAXLVL + 1)
        current = self.header

        '''
        start from highest level of skip list
        move the current reference forward while key 
        is greater than key of node next to current
        Otherwise inserted current in update and 
        move one level down and continue search
        '''
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        ''' 
        reached level 0 and forward reference to 
        right, which is desired position to 
        insert key.
        '''
        current = current.forward[0]

        '''
        if current is NULL that means we have reached
           to end of the level or current's key is not equal
           to key to insert that means we have to insert
           node between update[0] and current node
       '''
        if current == None or current.key != key:
            # Generate a random level for node
            rlevel = self.randomLevel()

            '''
            If random level is greater than list's current
            level (node with highest level inserted in 
            list so far), initialize update value with reference
            to header for further use
            '''
            if rlevel > self.level:
                for i in range(self.level + 1, rlevel + 1):
                    update[i] = self.header
                self.level = rlevel

            # create new node with random level generated
            n = self.createNode(rlevel, key)

            # insert node by rearranging references
            for i in range(rlevel + 1):
                n.forward[i] = update[i].forward[i]
                update[i].forward[i] = n

            print("Successfully inserted key {}".format(key))

    def deleteElement(self, search_key):

        # create update array and initialize it
        update = [None] * (self.MAXLVL + 1)
        current = self.header

        '''
        start from highest level of skip list
        move the current reference forward while key 
        is greater than key of node next to current
        Otherwise inserted current in update and 
        move one level down and continue search
        '''
        for i in range(self.level, -1, -1):
            while (current.forward[i] and current.forward[i].key < search_key):
                current = current.forward[i]
            update[i] = current

        ''' 
        reached level 0 and advance reference to 
        right, which is possibly our desired node
        '''
        current = current.forward[0]

        # If current node is target node
        if current != None and current.key == search_key:

            '''
            start from lowest level and rearrange references 
            just like we do in singly linked list
            to remove target node
            '''
            for i in range(self.level + 1):

                '''
                If at level i, next node is not target 
                node, break the loop, no need to move 
                further level
                '''
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Remove levels having no elements
            while (self.level > 0 and self.header.forward[self.level] == None):
                self.level -= 1
            print("Successfully deleted {}".format(search_key))

    def searchElement(self, key):
        current = self.header

        for i in range(self.level, -1, -1):
            while (current.forward[i] and current.forward[i].key < key):
                current = current.forward[i]

        # reached level 0 and advance reference to
        # right, which is prssibly our desired node
        current = current.forward[0]

        # If current node have key equal to
        # search key, we have found our target node
        if current and current.key == key:
            print("Found key ", key)
        else:
            print('Not Found')

    # Display skip list level wise
    def displayList(self):
        print("\n*****Skip List******")
        head = self.header
        for lvl in range(self.level + 1):
            print("Level {}: ".format(lvl), end=" ")
            node = head.forward[lvl]
            while (node != None):
                print(node.key, end=" ")
                node = node.forward[lvl]
            print("")
            
    def find(self, key):
        current = self.header

        for i in range(self.level, -1, -1):
            while (current.forward[i] and current.forward[i].key < key):
                current = current.forward[i]
        current = current.forward[0]

        if current and current.key == key:
            print("Found key ", key)
            return True
        else:
            return False

stock_symbol1 = input('Enter First Stock Symbol : ')
stock_symbol2 = input('Enter Second Stock Symbol : ')
col1, stock1 = get_stock_data(stock_symbol1)
col2, stock2 = get_stock_data(stock_symbol2)

stock1


# SkipList Class Takes Max_Levels And Probability As Input
skip_list_stock1 = SkipList(5, 0.5)
for i in range(5,len(stock1),14):
    skip_list_stock1.insertElement(float(stock1[i]))

skip_list_stock1.displayList()

skip_list_stock2 = SkipList(5, 0.5)
for i in range(5,len(stock2),14):
    skip_list_stock2.insertElement(float(stock2[i]))

skip_list_stock2.displayList()

def intersection(list1,list2):
    lst = []
    head  = list1.header
    temp = head.forward[0]
    while temp!=None:
        if(list2.find(temp.key)):
            lst.append(temp.key)
        temp = temp.forward[0]
    return lst

# PLOT VISUALIZATION
stock1_array = np.array(stock1)
stock1_df = pd.DataFrame(stock1_array.reshape(int(stock1_array.shape[0]/14), 14),columns=col1)
stock1_df['Date'] = pd.to_datetime(stock1_df['Date'])
stock1_df['PREV. CLOSE'] = stock1_df['PREV. CLOSE'].apply(lambda x : float(x))stock2_array = np.array(stock2)
stock2_df = pd.DataFrame(stock2_array.reshape(int(stock2_array.shape[0]/14), 14),columns=col2)
stock2_df['Date'] = pd.to_datetime(stock2_df['Date'])
stock2_df['PREV. CLOSE'] = stock2_df['PREV. CLOSE'].apply(lambda x : float(x))plt.style.use('ggplot')
plt.figure(figsize=(12,10))
ax1 = plt.subplot2grid((12,1), (0,0), rowspan=4, colspan=1)
ax1.plot(stock1_df['Date'], stock1_df['PREV. CLOSE'], label=stock_symbol1)
ax1.set_xlabel('Date')
ax1.set_ylabel('Closing Points')
ax1.legend(bbox_to_anchor=[0.9, 0.7],loc='right')

ax2 = plt.subplot2grid((12,1), (6,0), rowspan=4, colspan=1)
ax2.plot(stock2_df['Date'], stock2_df['PREV. CLOSE'], label=stock_symbol2)
ax2.legend(bbox_to_anchor=[0.9, 0.7],loc='right')
ax2.set_xlabel('Date')
ax2.set_ylabel('Closing Points')

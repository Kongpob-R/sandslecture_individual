from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys
class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):  
         
        # He goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention 
        self.assertIn('S&SLecture', self.browser.title)  
        
        # เขาลงชื่อเข้าใช้งานบัญชี โดยการกรอก username กับ password
        login_button=self.browser.find_element_by_id('login')
        login_button.send_keys(Keys.ENTER) 

        username = self.browser.find_element_by_id('username')  
        username.send_keys('Smart')

        password = self.browser.find_element_by_id('password')  
        password.send_keys('123456')     

        logins_button=self.browser.find_element_by_id('logins')
        login_button.send_keys(Keys.ENTER) 

        # เขาพิมชื่อวิชา "Ubiquitous Computing" ลงไปในกล่องข้อความ
        # เมื่อเขาทำการ enter 
        searchbox = self.browser.find_element_by_id('search')  
        searchbox.send_keys('Ubiquitous Computing')  
        searchbox.send_keys(Keys.ENTER)  


        
         
        time.sleep(10)
        self.fail('Finish the test!')  

        # She is invited to enter a to-do item straight away
        

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
class NewVisitorTest(LiveServerTestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    def test_home(self):  
         
        # He goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention 
        self.assertIn('S&SLecture', self.browser.title)  
        
        #เขาลงชื่อเข้าใช้งานบัญชี โดยการกรอก username กับ password
        login_button=self.browser.find_element_by_id('login')
        login_button.send_keys(Keys.ENTER) 

        username = self.browser.find_element_by_id('username')
        username.send_keys('Smart')

        password = self.browser.find_element_by_id('password')  
        password.send_keys('123456')     


        # เขาพิมชื่อวิชา "Ubiquitous Computing" ลงไปในกล่องข้อความ
        # เมื่อเขาทำการ enter 
        searchbox = self.browser.find_element_by_id('search')  
        searchbox.send_keys('Ubiquitous Computing')  
        searchbox.send_keys(Keys.ENTER)  


        
         
        time.sleep(10)
        self.fail('Finish the test!')  

        # She is invited to enter a to-do item straight away

    def test_login(self):  
         
        self.browser.get('http://localhost:8000'+'/accounts/login/')
        # เขาลงชื่อเข้าใช้งานบัญชี โดยการกรอก username กับ password


        username = self.browser.find_element_by_id('id_username')  
        username.send_keys('Andrew')

        password = self.browser.find_element_by_id('id_password')  
        password.send_keys('123456')  
        
        login = self.browser.find_element_by_id('logins')   

        login.send_keys(Keys.ENTER)
        time.sleep(1)


        self.fail('Finish the test!')  
    def upload(self):  
        self.browser.get(self.test_home+'/upload/')
        self.fail('Finish the test!')  

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  
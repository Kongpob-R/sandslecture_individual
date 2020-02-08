from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
class NewVisitorTest(LiveServerTestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    def test_Steve_uploading_a_lecture(self):
        # Steve's friends invite Steve visit their new lecture sharing site named Save&Share lecture
        # Steve's friends register an account for him and give him username and password of the site


        # Steve have found an amazing seminar about computer networking
        # He was take note of all the lecture and dicide to share it online
        # He is visiting his friend's lecture sharing site
        # He entering the site URL in his browser
        self.browser.get(self.live_server_url)

        # He notices the homepage has pop up
        self.assertIn('S&SLecture Home', self.browser.title)  
        
        # He's looking for a login button and click it
        login_button=self.browser.find_element_by_id('login')
        login_button.send_keys(Keys.ENTER) 

        # He notice page have redirect to a login form

        # He's entering a username and password that given by his friend and click login
        username = self.browser.find_element_by_id('username')
        username.send_keys('Steve')

        password = self.browser.find_element_by_id('password')  
        password.send_keys('123456')     

        # the page have redirect back to homepage
        # He found himself login to the site in a navigation bar 
        # He also notice a login button has replace by a logout button
        # He click on a Share lecture button he saw on a navigation bar
        # the page redirect to upload page
        # He start adding photo of the lecture to the given form
        # He filling some of the form and click upload
        # the page is not allow him upload because some field are still empty
        # He fillup the rest of the form and click upload again
        # the page redirect to homepage
        # He found his lecture showing up
        # He click logout

        self.fail('Finish the test!')  

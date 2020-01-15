from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Near has stress about exam midterm coming soon
        #he has heard about a cool new online Share lecture app. he goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        #he look around homepage
        #he see that logo
        self.assertIn('', self.browser.find_element_by_tag_name('img').text  )
        #that Search bar
        self.assertIn( "", self.browser.find_element_by_tag_name('input').text  )
        
        Search_button = self.browser.find_element_by_id('button_Search')
        #element_tag_name_125= Search_button.find_elements_by_tag_name('button')
        self.assertIn('Search', Search_button.text )
        #that login
        Login_button = self.browser.find_element_by_id('button_Login')
        #element_tag_name = Login_button.find_elements_by_tag_name('button')
        
        self.assertIn('Login', Login_button.text )
        #that Popolar post
        self.assertIn('Popular', self.browser.find_element_by_id('Popular').text  )
        self.assertIn('', self.browser.find_element_by_tag_name('div').text  )
        #that Lastest post
        self.assertIn('Lastest', self.browser.find_element_by_id('Lastest').text  )
        self.assertIn('', self.browser.find_element_by_tag_name('div').text  )

        #self.fail('Finish the test!')


if __name__ == '__main__':  
    unittest.main(warnings='ignore')  
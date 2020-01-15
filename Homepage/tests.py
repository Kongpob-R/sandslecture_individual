
from django.shortcuts import render
from django.test import TestCase

class HomePageTest(TestCase):



    def test_home_page_returns_correct_title(self):
        response=self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>S&SLecture</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    
    def test_home_page_returns_correct_divBox(self):
        response=self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<style>', html)
        self.assertIn('div{width: 300px;  padding: 50px;  margin: 20px;}', html)

        self.assertIn('</style>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        
    def test_home_page_returns_correct_logoinbox(self):
        response=self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<div>', html)
        self.assertIn('<img src="">', html)
        self.assertIn('</div>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_home_page_returns_correct_login_inBox(self):
        response=self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<div>', html)
        self.assertIn('<button type="button">Login</button>', html)
        self.assertIn('</div>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_home_page_returns_correct_search_inBox(self):
        response=self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<div>', html)
        self.assertIn('<form>', html)
        self.assertIn('<input type="text" placeholder="Search.." name="search">', html)
        self.assertIn('<<button type="submit"><i class="fa fa-search"></i></button>>', html)
        self.assertIn('</form>', html)
        self.assertIn('</div>', html)
        self.assertTrue(html.strip().endswith('</html>'))
    
    def test_home_page_returns_correct_Popolar_head1(self):
        response=self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<h1>Popular</h1>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_home_page_returns_correct_Box_Popolar(self):
        response=self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<div>', html)
        self.assertIn('</div>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_home_page_returns_correct_Last_head2(self):
        response=self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<h1>Lastest</h1>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_home_page_returns_correct_Box_Last(self):
        response=self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<div>', html)
        self.assertIn('</div>', html)
        self.assertTrue(html.strip().endswith('</html>'))
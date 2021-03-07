from django.test import TestCase
from django.shortcuts import reverse

class LandingPageTest(TestCase):
#Every function will be executed as a different test, It has to have the test in the beginning 
#of the name. For every function you need to make a request and pass it in the checking  


#In this example the 2 tests should be combined in one function because they have the same request
#and they should be named test_get(self) because they are checking the get method 
    def test_status_code(self):
        response= self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response= self.client.get(reverse("landing-page"))
        self.assertTemplateUsed(response, "landing.html")

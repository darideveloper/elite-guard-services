from django.test import TestCase


class RedirectsTestCase(TestCase):
    def test_home_redirect_admin(self):
        """ Test redirect to admin when accessing the home page """
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/')

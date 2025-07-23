from django.test import TestCase
from django.utils import timezone
from utils import dates
import os
from django.conf import settings


class RedirectsTest(TestCase):
    def test_home_redirect_admin(self):
        """ Test redirect to admin when accessing the home page """
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/')
        
        
class UtilsDatesGetCurrentWeekTest(TestCase):
    """ Test function "get_current_week" from utils.dates """
    
    def test_week_52_before_thursday(self):
        """ Try to get 52 week if the date is before Thursday
            Expected result: 51
        """
        
        time_zone = timezone.get_current_timezone()
        date = timezone.datetime(2024, 12, 24, 0, 0, 0, 0, time_zone)
        week = dates.get_current_week(date)
        
        self.assertEqual(week, 51)

    def test_week_52_thursday(self):
        """ Try to get 52 week if the date is Thursday
            Expected result: 52
        """
        
        time_zone = timezone.get_current_timezone()
        date = timezone.datetime(2024, 12, 26, 0, 0, 0, 0, time_zone)
        week = dates.get_current_week(date)
        
        self.assertEqual(week, 52)
        
    def test_week_52_after_thursday(self):
        """ Try to get 52 week if the date is after Thursday
            Expected result: 52
        """
        
        time_zone = timezone.get_current_timezone()
        date = timezone.datetime(2024, 12, 28, 0, 0, 0, 0, time_zone)
        week = dates.get_current_week(date)
        
        self.assertEqual(week, 52)
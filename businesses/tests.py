import unittest
from django.shortcuts import render
from .views import BusinessAccountDashboard


class TestDashboard(unittest.TestCase):

    def setUp(self):
        self.view = BusinessAccountDashboard

    def test_sum(self):
        self.assertEqual(self.view, BusinessAccountDashboard)
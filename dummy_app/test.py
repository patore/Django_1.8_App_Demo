from django.test import TestCase
from .views import dummy_appbusiness


class TestHome(TestCase):
    def test_dummy_appbusiness_page_rendered(self, request):
        value = dummy_appbusiness(request)
        self.assertEqual(value, (request, "dummy_appbusiness.html"))



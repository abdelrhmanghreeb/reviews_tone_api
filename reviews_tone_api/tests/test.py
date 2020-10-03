import unittest
import json
from reviews_tone_api.api import app


class TestHotelsAPI(unittest.TestCase):
    test_hotel_name = "Hotel Russo Palace"
    avg_tone_link = "/avg_tone"
    index_hotel_link = "/index_hotel"

    @classmethod
    def setUpClass(self):
        self.app = app.test_client()

    # API tests
    def test_avg_tone(self):
        """
        Implement a test for /avg_tone - post method
        """
        response = self.app.post(self.avg_tone_link+"/"+ self.test_hotel_name)
        print(response.json)
        self.assertEqual(response.status_code, 200)

    def test_avg_tone_get(self):
        """
        Implement a test for /avg_tone - get method
        """
        response = self.app.get(self.avg_tone_link+"/"+ self.test_hotel_name)
        self.assertEqual(response.status_code, 200)


    def test_index_hotel(self):
        """
        Implement a test for /index_hotel - post method
        """
        response = self.app.post(self.index_hotel_link+"/"+ self.test_hotel_name)
        self.assertEqual(response.status_code, 200)

    def test_index_hotel(self):
        """
        Implement a test for /index_hotel - get method
        """
        response = self.app.get(self.index_hotel_link+"/"+ self.test_hotel_name)
        self.assertEqual(response.status_code, 200)

    def _test_index_hotels(self):
        """
        Implement a test for /index_hotel - post method with no parameter
        """
        response = self.app.post(self.index_hotel_link)
        self.assertEqual(response.status_code, 200)

    def test_bad_request(self):
        """
        Implements a test for a bad request case; missing fields
        """
        response = self.app.post(self.avg_tone_link)
        self.assertEqual(response.status_code, 404)

    def test_not_found_url(self):
        """
        Implements a test for a not-found-url request case
        """
        response = self.app.post(self.avg_tone_link + "x" +"/"+ self.test_hotel_name)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
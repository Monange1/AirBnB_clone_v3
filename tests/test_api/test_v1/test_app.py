from unittest import TestCase
from api.v1.app import app


class TestIntegrations(TestCase):
    def setUp(self):
        """set up app for testing"""
        from models import storage
        self.app = app.test_client()

    # Index view
    def test_statusroute(self):
        """tests the status route returns JSON-formatted
        response correctly"""
        response = self.app.get('/api/v1/status')
        assert b'{\n  "status": "OK"\n}\n' in response.data
        self.assertEqual(response.status_code, 200)

    def test_404error(self):
        """tests the handing of 404 error returns JSON-formatted
        status code response"""
        response = self.app.get('/api/v1/nop')
        self.assertEqual(b'{\n  "error": "Not found"\n}\n', response.data)
        self.assertEqual(response.status_code, 404)

    # States view
    def test_get_states(self):
        """tests that all state objects are returned in JSON"""
        response = self.app.get('api/v1/states')
        self.assertEqual(response.status_code, 200)
        print(response.data)
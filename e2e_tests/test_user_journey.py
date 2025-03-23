import pytest
import requests
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestAPIEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Create token for authentication
        self.token = Token.objects.create(user=self.user)
        self.headers = {'Authorization': f'Token {self.token.key}'}

    def test_login_and_view_events(self, live_server):
        login_url = f"{live_server.url}/api/users/login"

        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        print(f"Trying login at: {login_url}")
        login_response = requests.post(login_url, json=login_data)

        # Print information for debugging
        print(f"Login response status: {login_response.status_code}")
        print(f"Login response content: {login_response.content}")

        # Change this assertion to match the actual API response
        assert login_response.status_code == 200

        # Extract token from response
        token = login_response.json().get('token')
        assert token is not None

        # Use token to access events endpoint
        events_url = f"{live_server.url}/api/events/"
        headers = {'Authorization': f'Token {token}'}
        events_response = requests.get(events_url, headers=headers)
        assert events_response.status_code == 200

        # Verify events data structure
        events_data = events_response.json()
        assert isinstance(events_data, list)

        # Print for debugging
        print(f"Events data: {events_data}")
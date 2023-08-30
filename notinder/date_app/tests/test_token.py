import pytest
from django.urls import reverse
from date_app.models import ZodiacSign

@pytest.mark.django_db
def test_token(api_client):
    ZodiacSign.objects.create(name="Cancer")

    user_data = {
        "username": "new_boy5",
        "password": "1234",
        "gender": "male",
        "email": "new_boy5@example.com",
        "zodiac_sign": "Cancer",
        "description": "I'm a user",
        "photo": ""
    }
    api_client.post(reverse('register'), user_data)

    url = reverse('token')
    data = {
        "username": "new_boy5",
        "password": "1234"
    }
    response = api_client.post(url, data)

    assert response.status_code == 200
    assert "refresh" in response.data
    assert "access" in response.data

    refresh_response = api_client.post(reverse('token_refresh'), {"refresh": response.data["refresh"]})

    assert response.status_code == 200
    assert "access" in refresh_response.data

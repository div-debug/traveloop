import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
os.environ.setdefault('DATABASE_URL', 'sqlite:///d:/New folder (2)/traveloop/db.sqlite3')

django.setup()

from django.test import Client


def main():
    client = Client()

    # Public endpoints
    print('maps-config', client.get('/api/maps/config/').status_code)
    print('city-search', client.get('/api/maps/cities/?query=Lisbon').status_code)

    # Auth + write verification
    username = 'verifyuser1'
    password = 'VerifyPass123!'

    # Signup (ignore if already exists)
    signup_payload = {
        'username': username,
        'full_name': 'Verify User',
        'email': 'verifyuser1@example.com',
        'password': password,
        'confirm_password': password,
    }
    signup_resp = client.post('/api/auth/signup/', signup_payload, content_type='application/json')
    print('auth-signup', signup_resp.status_code)

    # Login
    login_payload = {'username': username, 'password': password}
    login_resp = client.post('/api/auth/login/', login_payload, content_type='application/json')
    print('auth-login', login_resp.status_code)

    access = None
    try:
        access = login_resp.json().get('access')
    except Exception:
        access = None

    if not access:
        print('auth-login-access-token-missing', access)
        return

    headers = {'HTTP_AUTHORIZATION': f'Bearer {access}'}

    # Create trip (write)
    trip_payload = {
        'title': 'Verify Trip',
        'destination': 'Lisbon',
        'description': 'Endpoint verification trip',
        'start_date': '2026-06-01',
        'end_date': '2026-06-05',
        'privacy_status': 'private',
        'estimated_budget': '1000',
    }
    trips_resp = client.post('/api/trips/', trip_payload, content_type='application/json', **headers)
    print('trips-create', trips_resp.status_code)
    if trips_resp.status_code < 200 or trips_resp.status_code >= 300:
        print('trips-create-body', getattr(trips_resp, 'content', b'').decode('utf-8', errors='ignore'))
        return

    trip_id = trips_resp.json().get('id')
    print('trip-id', trip_id)

    # Itinerary stop create
    itinerary_payload = {
        'trip': trip_id,
        'day': 1,
        'title': 'Arrival',
        'description': 'Arrival stop',
        'location': 'Lisbon, Portugal',
        'latitude': None,
        'longitude': None,
        'start_time': None,
        'end_time': None,
        'cost': 100,
        'order': 1,
    }
    it_resp = client.post('/api/itineraries/', itinerary_payload, content_type='application/json', **headers)
    print('itineraries-create', it_resp.status_code)
    if it_resp.status_code < 200 or it_resp.status_code >= 300:
        print('itineraries-create-body', getattr(it_resp, 'content', b'').decode('utf-8', errors='ignore'))
    else:
        # list
        it_list = client.get(f'/api/itineraries/?trip={trip_id}', **headers)
        print('itineraries-list', it_list.status_code)

    # Activity create
    activity_payload = {
        'trip': trip_id,
        'title': 'Sunset Walk',
        'category': 'culture',
        'location': 'Lisbon, Portugal',
        'start_time': None,
        'end_time': None,
        'duration_minutes': 180,
        'notes': 'Test activity',
        'cost': 80,
        'rating': 4.7,
        'image_url': '',
    }
    act_resp = client.post('/api/activities/', activity_payload, content_type='application/json', **headers)
    print('activities-create', act_resp.status_code)
    if act_resp.status_code < 200 or act_resp.status_code >= 300:
        print('activities-create-body', getattr(act_resp, 'content', b'').decode('utf-8', errors='ignore'))
    else:
        act_list = client.get(f'/api/activities/?trip={trip_id}', **headers)
        print('activities-list', act_list.status_code)

    # Budget entry create (seed)
    budget_payload = {
        'trip': trip_id,
        'category': 'Lodging',
        'planned_amount': 400,
        'spent_amount': 0,
        'notes': '',
    }
    b_resp = client.post('/api/budget/', budget_payload, content_type='application/json', **headers)
    print('budget-create', b_resp.status_code)
    if b_resp.status_code < 200 or b_resp.status_code >= 300:
        print('budget-create-body', getattr(b_resp, 'content', b'').decode('utf-8', errors='ignore'))
    else:
        b_sum = client.get(f'/api/budget/summary/?trip={trip_id}', **headers)
        print('budget-summary', b_sum.status_code)

    # Notes create
    notes_payload = {
        'trip': trip_id,
        'title': 'Test note',
        'content': 'Hello from verify_endpoints',
    }
    n_resp = client.post('/api/notes/', notes_payload, content_type='application/json', **headers)
    print('notes-create', n_resp.status_code)
    if n_resp.status_code < 200 or n_resp.status_code >= 300:
        print('notes-create-body', getattr(n_resp, 'content', b'').decode('utf-8', errors='ignore'))
    else:
        n_list = client.get(f'/api/notes/?trip={trip_id}', **headers)
        print('notes-list', n_list.status_code)

    # Trips list (auth)
    trips_list_resp = client.get('/api/trips/', **headers)
    print('trips-list', trips_list_resp.status_code)


if __name__ == '__main__':
    main()

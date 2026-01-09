import requests
import json

BASE_URL = "http://localhost:8000"

def test_get_devices():
    print("Testing GET /devices/...")
    try:
        response = requests.get(f"{BASE_URL}/devices/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_device(relay_id, state):
    print(f"Testing PATCH /devices/{relay_id} with state={state}...")
    try:
        response = requests.patch(
            f"{BASE_URL}/devices/{relay_id}",
            json={"state": state}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Note: Backend must be running for this to work
    print("🚀 Starting Device Control API tests...")
    if test_get_devices():
        test_update_device("relay1", True)
        test_get_devices()
        test_update_device("relay1", False)
        test_get_devices()
    else:
        print("❌ GET /devices/ failed. Is the backend running?")

import requests
import pytest

BASE_URL = "https://qa-internship.avito.com/api/1"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Ручка 1
@pytest.mark.parametrize("seller_id, expected_status", [
    ({"sellerID": 345826, "name": "Test", "price": 100}, 200),                  # Test case 1 - Positive
    ({"sellerID": 345826, "price": 100}, 400),                                  # Test case 2 - Negative (Missing name)
    ({"sellerID": 1, "name": "Test", "price": 100}, 400),                       # Test case 3 - Negative (seller_id below range)
    ({"sellerID": 9999999999999999, "name": "Test", "price": 100}, 400),        # Test case 4 - Negative (seller_id above range)
    ({"name": "Test", "price": 100}, 400)                                       # Test case 5 - Negative (missing seller_id)
])
def test_create_ad(seller_id, expected_status):
    response = requests.post(f"{BASE_URL}/item", json={"sellerID": seller_id, "name": "Ad Test", "price": 100}, headers=HEADERS)
    assert response.status_code == expected_status

# Ручка 2
@pytest.mark.parametrize("item_id, expected_status", [
    ("0cd4183f-a699-4486-83f8-b513dfde477a", 200),      # Test case 1 - Positive
    ("invalid_id", 400)                                 # Test case 2 - Negative (non-existing item id)
])
def test_get_ad_by_id(item_id, expected_status):
    response = requests.get(f"{BASE_URL}/item/{item_id}", headers=HEADERS)
    assert response.status_code == expected_status

# Ручка 3
@pytest.mark.parametrize("seller_id, expected_status", [
    (345826, 200),              # Test case 1 - Positive
    (1, 400),                   # Test case 3 - Negative (seller_id below range)
    (9999999999999999, 400)     # Test case 3 - Negative (seller_id above range)
])
def test_get_ads_by_seller_id(seller_id, expected_status):
    response = requests.get(f"{BASE_URL}/{seller_id}/item", headers=HEADERS)
    assert response.status_code == expected_status

# Ручка 4
@pytest.mark.parametrize("item_id, expected_status, expected_statistics", [
    ("0cd4183f-a699-4486-83f8-b513dfde477a", 200, {"likes": 123, "viewCount": 12, "contacts": 3}),      # Test case 1 - Positive
    ("non_existing_id", 400, None)                                                                      # Test case 2 - Negative (non-existing item id)
])
def test_get_stats_by_item_id(item_id, expected_status, expected_statistics):
    response = requests.get(f"{BASE_URL}/statistic/{item_id}", headers=HEADERS)
    assert response.status_code == expected_status
    if expected_status == 200 and expected_statistics:
        statistics = response.json()[0]
        assert statistics == expected_statistics

if __name__ == "__main__":
    pytest.main(["-v", "--tb=short"])

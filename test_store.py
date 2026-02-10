from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
3) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
4) Validate the response codes and values
5) Validate the response message "Order and pet status updated successfully"
'''

# This test was completed by applicant Andrea Altenkirch, GitHub user: Testadora on 2/9/26 as part of required tasks 
@pytest.fixture
def order_with_available_pet():
    pets_response = api_helpers.get_api_data("/pets/findByStatus", {"status": "available"})
    assert pets_response.status_code == 200

    pets = pets_response.json()
    if not pets:
        pytest.skip("No available pets to place an order.")

    pet_id = pets[0]["id"]
    order_payload = {
        "pet_id": pet_id
    }

    order_response = api_helpers.post_api_data("/store/order", order_payload)
    assert order_response.status_code == 201
    # added order schema validation as optional task #3 in the TODO list
    validate(instance=order_response.json(), schema=schemas.order)

    order = order_response.json()
    return {
        "order_id": order["id"],
        "pet_id": pet_id
    }

def test_patch_order_by_id(order_with_available_pet):
    order_id = order_with_available_pet["order_id"]
    pet_id = order_with_available_pet["pet_id"]

    update_payload = {
        "status": "sold"
    }

    order_update_response = api_helpers.patch_api_data(f"/store/order/{order_id}", update_payload)

    assert order_update_response.status_code == 200    

    order_update = order_update_response.json()
    assert_that(order_update.get("message", ""), is_("Order and pet status updated successfully"))


    pet_response = api_helpers.get_api_data(f"/pets/{pet_id}")
    assert pet_response.status_code == 200

    pet = pet_response.json()
    assert_that(pet.get("status"), is_("sold"))
    validate(instance=pet, schema=schemas.pet)

    # clean up - set pet back to available for future test runs
    api_helpers.patch_api_data(f"/store/order/{order_id}", {"status": "available"})


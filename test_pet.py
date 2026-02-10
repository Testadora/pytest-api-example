from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
# This test was debugged by applicant Andrea Altenkirch, GitHub user: Testadora on 2/9/26
# The source of error was that the schema was incorrectly defined for the name property in schemas.py
# The name property was defined as an integer instead of a string, which caused the validation to fail. After correcting the schema definition, the test now passes successfully.
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''

# This test was completed by applicant Andrea Altenkirch, GitHub user: Testadora on 2/9/26
# The 4 tasks in the TODO list have been implemented.
@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    # Validate the appropriate response code
    assert response.status_code == 200

    pets = response.json()
    for pet in pets:        
        #Validate the 'status' property in the response is equal to the expected status for each object in the response
        assert_that(pet.get("status"), is_(status))
        #Validate the schema for each object in the response
        validate(instance=pet, schema=schemas.pet)

'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
# TODO...
# This test was completed by applicant Andrea Altenkirch, GitHub user: Testadora on 2/9/26
# The 2 tasks in the TODO list have been implemented.
# This is an edge case test for invalid pet IDs. We can use a configurable upper bounded value as examples of invalid IDs.
upperBound = 999999
@pytest.mark.parametrize("pet_id", [upperBound])
def test_get_by_id_404(pet_id):
    test_endpoint = f"/pets/{pet_id}"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 404

    error = response.json()
    assert_that(error.get("message", ""), contains_string(f"Pet with ID {pet_id} not found"))


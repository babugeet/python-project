from unittest.mock import patch
import passlib.hash
import unittest
# Your function to be tested
def verify_password(password, hashed_password):
    flag = passlib.hash.bcrypt.using(rounds=13).verify(password, bytes(hashed_password, 'utf-8'))
    if flag:
        return True
    else:
        return False

# Your test case
@patch('passlib.hash.bcrypt.using')
def test_verify_password(mock_bcrypt_using):
    # Mock the bcrypt.using function to always return True
    mock_bcrypt_using.return_value.verify.return_value = False

    # Call the function with any password and hashed_password values
    result = verify_password("any_password", "any_hashed_password")
    
    # Assertion: The result should be True regardless of the input values
    assert result is False


test_verify_password()
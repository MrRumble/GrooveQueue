import pytest
from api.utils.validators import validate_password, validate_email

def test_valid_password():
    assert validate_password("Password123!") == True
    assert validate_password("Valid1Pass!") == True
    assert validate_password("StrongP@ssw0rd") == True

def test_invalid_passwords():
    assert validate_password("short") == False
    assert validate_password("NoSpecialChar1") == False
    assert validate_password("NoNumber!") == False
    assert validate_password("Alllowercase!") == False
    assert validate_password("ALLUPPERCASE1") == False
    assert validate_password("12345678") == False
    assert validate_password("Special$Char") == False
    assert validate_password("Pass123") == False

def test_validate_email():
    assert validate_email("test@example.com") == True
    assert validate_email("user.name@domain.com") == True
    assert validate_email("user@domain.com") == True
    assert validate_email("user@domain.co") == True
    assert validate_email("user@domain.c") == False
    assert validate_email("user@domain..com") == False
    assert validate_email("user@.com") == False
    assert validate_email("plainaddress") == False
    assert validate_email("user@domain") == False
    assert validate_email("user@domain@domain.com") == False


# To run the tests, save this file and use the command `pytest` in the terminal


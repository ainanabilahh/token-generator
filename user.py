"""
User Model Module

This module defines the User class, representing a user with a username and password.
It is designed to be used in conjunction with authentication processes such as token generation.
"""
from pydantic import BaseModel


class User(BaseModel):
    """
    User Model

    Represents a user with a username and password, suitable for authentication purposes.

    Attributes:
        username (str): The username associated with the user.
        password (str): The password for the user.
    """
    username: str
    password: str

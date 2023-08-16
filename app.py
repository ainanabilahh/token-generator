"""
Token Generation API

This module provides an endpoint for user authentication, including functions to create JWT tokens
and secure secret keys.
"""

import datetime
import random
import secrets
import shutil
from pathlib import Path

import jwt
from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile

from user import User

app = FastAPI()

SECRET_KEY = "yoursecretkey"
ALGORITHM = "HS256"


def create_secret_key(length=32) -> str:
    """Generate a URL-safe secret key.

    Args:
        length (int): Length of the secret key. Default is 32 characters.

    Returns:
        str: The generated secret key.
    """
    return secrets.token_urlsafe(length)


def create_token(user: User) -> str:
    """Create a JWT token for the given user.

    The token will include the username and an expiration time of 1 hour.

    Args:
        user (User): The user for whom to create the token.

    Returns:
        str: The encoded JWT token.
    """
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        "exp": expiration,
        "sub": user.username,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> bool:
    """
    Verify the given JWT token.

    Args:
        token (str): The token to verify.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    try:
        # Decode the token using the same secret key and algorithm used to encode it
        jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM])

        # Optional: You can add additional checks, such as verifying the 'sub' (subject) field
        # if decoded_token['sub'] != expected_username:
        #     return False

        return True

    except jwt.ExpiredSignatureError:
        print("Token is expired.")
        return False

    except jwt.InvalidTokenError:
        print("Token is invalid.")
        return False


@app.post("/token/")
def generate_token(username: str = Form(...), password: str = Form(...)):
    """Generate an access token for the provided user.

    This endpoint expects a JSON object with the user's username and password.
    It returns a JWT token that can be used for authenticated requests.

    Args:
        user (User): A Pydantic model containing the user's username and password.

    Returns:
        dict: A dictionary containing the access token and token type.
    """

    user = User(username=username, password=password)

    token = create_token(user)
    return {"ticket": token, "token_type": "bearer"}


@app.post("/random/")
def generate_random_id() -> str:
    """
    Generate a Random Numeric ID

    Creates a random numeric ID with the specified length, only if the provided token is valid.

    Args:
        token (str): The authentication token to validate.
        length (int, optional): The length of the ID to generate. Default is 8.

    Returns:
        str: The generated random numeric ID, or an error message if the token is invalid.

    Raises:
        HTTPException: If the token is invalid.
    """

    # Extract the token from the header value (assuming the format is "Bearer <token>")
    return ''.join(random.choice('0123456789') for _ in range(8))


@app.post("/upload/")
async def upload_file(authorization: str = Header(...), file: UploadFile = File(...)):
    """
    Upload a File and Generate a Random ID

    Accept a file upload and an authorization token. It verifies the token, saves the file
    to the "data" folder, and returns a randomly generated ID.

    Args:
        authorization (str): The authorization token provided in the request header.
        file (UploadFile): The file to be uploaded, provided as multipart data.

    Returns:
        dict: A dictionary containing the random ID and the path where the file was saved.

    Raises:
        HTTPException: If the token is invalid or if there is an error in processing the file.
    """
    # Extract the token from the header and verify it
    # Extract the token from the header value (assuming the format is "Bearer <token>")
    token = authorization.split(
        " ")[1] if " " in authorization else authorization

    print(token)

    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if the filename is provided
    if file.filename is None:
        raise HTTPException(status_code=400, detail="Filename is missing")


    # Define the path to the "data" folder
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    # Define the path to save the uploaded file
    file_path = data_folder / file.filename

    # Save the uploaded file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate a random ID
    random_id = generate_random_id()

    # Return the random ID and the path where the file was saved
    return {"id": random_id}

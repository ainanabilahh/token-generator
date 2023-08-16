# Dummy Token Generation API (FastAPI)

## Overview

This project provides a dummy API for token generation, verification, and random ID creation, implemented using the FastAPI framework. FastAPI's speed and ease of use make it an ideal choice for this project, offering automatic interactive documentation, data validation, and asynchronous capabilities.

### Why FastAPI?

- **Performance:** FastAPI is one of the fastest frameworks for building APIs, only slower than Node.js and Starlette (which is the basis of FastAPI).
- **Ease of Use:** Write standard Python types, and FastAPI takes care of the rest. It generates API documentation automatically using Swagger UI and ReDoc.
- **Asynchronous Support:** FastAPI supports asynchronous request handling, allowing for high performance while handling a large number of simultaneous connections.

### Purpose of This Dummy API

- **Testing and Development:** Ideal for rapid prototyping and integration testing.
- **Demonstration:** Serves as an educational resource or for product demos.
- **Built with FastAPI:** Leverages FastAPI's features for a quick and powerful implementation.

## Features

- **Token Generation:** Securely create JSON Web Tokens (JWT) for user authentication.
- **Token Verification:** Verify the authenticity and validity of tokens.
- **Random ID Creation:** Generate random numeric IDs based on valid tokens.

## Installation

You'll need to install FastAPI and other dependencies to get started:

\`\`\`bash
pip install fastapi jwt pydantic uvicorn
\`\`\`

Then you can run the server using Uvicorn:

\`\`\`bash
uvicorn app:app --reload
\`\`\`

## Usage

TBA

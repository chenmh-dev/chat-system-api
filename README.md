# Chat System API

A backend chat system API built with Flask, supporting user authentication, direct conversations, and messaging.

This project is designed to practice backend engineering skills, including API design, layered architecture, and modular system design.

---

## Tech Stack

- Python
- Flask
- SQLite
- Werkzeug (password hashing)
- itsdangerous (token-based authentication)

---

## Project Structure


app/
  core/          # config, db, logging
  common/        # auth, decorators, errors, response
  modules/
    auth/
    users/
    conversations/
    messages/
  validators/
  utils/


---

## Features

### Authentication
- User registration
- User login
- Token-based authentication

### User
- Get current user (`/me`)

### Conversations
- Create or get direct conversation
- List user conversations (pagination, sorting, filtering)
- Get conversation detail

### Messages
- Send message
- List messages (pagination, sorting, filtering)

---

## Example API

```
http
@baseURL = http://127.0.0.1:5000

### Register
POST {{baseURL}}/register
Content-Type: application/json

{
    "username": "cmh8",
    "password": "123"
}

### Login
# @name login
POST {{baseURL}}/login
Content-Type: application/json

{
    "username": "cmh",
    "password": "123"
}

###
@token = {{login.response.body.data.token}}

GET {{baseURL}}/me
Authorization: Bearer {{token}}

### Create or get direct conversation
POST {{baseURL}}/conversations/direct
Authorization: Bearer {{token}}
Content-Type: application/json 

{
    "target_user_id": 2
}

### List conversations
GET {{baseURL}}/conversations?page=1&page_size=10&sort=id&order=asc
Authorization: Bearer {{token}}

### Get conversation detail
GET {{baseURL}}/conversations/2
Authorization: Bearer {{token}}

### Send message
POST {{baseURL}}/conversations/1/messages
Authorization: Bearer {{token}}
Content-Type: application/json 

{
    "content": "hello"
}

### List messages
GET {{baseURL}}/conversations/1/messages?page=1&page_size=10
Authorization: Bearer {{token}}
```

---

## How to Run
pip install -r requirements.txt
python run.py

---

## Current Version

Only supports direct conversations (1-to-1)

Group conversations are not implemented yet

---

## Design Highlights

Layered architecture (route / service / repository separation)

Modular design by domain (auth, users, conversations, messages)

Resource-level authorization for conversations and messages

Pagination, sorting, and filtering support

Centralized error handling system

Request logging with request_id for traceability

---

## Design Notes

Conversations and users are linked through a conversation_members table to support future group chat.

Direct and group conversations share the same conversations table for extensibility.

Business logic is handled in the service layer, while database access is isolated in the repository layer.
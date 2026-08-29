# FastAPI — SQL, Schemas, and Authentication Schemes

## 1. `cursor.execute()` — Get User ID

```python
cursor.execute(
    "SELECT id FROM users WHERE email=%s",
    (user.email,)
)
```

### Meaning

> Find the `id` of the user whose email matches the supplied email.

### Breakdown

```sql
SELECT id
```

→ Ask the database for only the `id`.

```sql
FROM users
```

→ Look in the `users` table.

```sql
WHERE email=%s
```

→ Find the user whose email matches the supplied value.

```python
(user.email,)
```

→ Provides the actual value for `%s`.

For example:

```python
user.email = "abc@gmail.com"
```

Conceptually:

```sql
SELECT id FROM users WHERE email='abc@gmail.com'
```

The database might return:

```text
101
```

---

## 2. Why the Comma?

```python
(user.email,)
```

is a **1-element tuple**.

The comma is important:

```python
(user.email,)   # tuple ✅
(user.email)    # just the value ❌
```

`psycopg2` expects query parameters to be supplied as a sequence such as a tuple.

---

## 3. Why `SELECT id` Instead of `SELECT *`?

If you only need the user's ID for creating a JWT:

```python
access_token = oauth2.create_access_token(
    data={"user_id": user["id"]}
)
```

there is no need to retrieve the entire user row.

```text
SELECT *   → get all columns

SELECT id  → get only the ID
```

Using `SELECT id` is cleaner when only the ID is needed.

---

# 4. What Does `schemas` Mean?

In a FastAPI project, `schemas` usually refers to the Python module/file:

```text
schemas.py
```

For example:

```text
app/
├── main.py
├── schemas.py
└── routers/
```

Import it:

```python
from .. import schemas
```

This means:

> Import the `schemas.py` module.

---

## 5. Pydantic Models in `schemas.py`

Example:

```python
from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
```

These are **Pydantic models** that define the expected structure of data.

You can then use:

```python
user_credentials: schemas.UserLogin
```

and:

```python
response_model=schemas.Token
```

---

# 6. What Is a Schema?

A **schema describes the expected structure of data**.

Example:

```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

This says that a `Token` should contain:

```text
access_token → string
token_type   → string
```

Therefore:

```python
return {
    "access_token": access_token,
    "token_type": "bearer"
}
```

matches the `Token` schema.

---

# 7. `schemas.Token`

When you see:

```python
schemas.Token
```

read it as:

> The `Token` Pydantic model defined inside `schemas.py`.

```text
schemas.py
    ↓
Python module
    ↓
Token
    ↓
Pydantic model
    ↓
Defines the structure of token response
```

---

# 8. Schema vs Scheme

These are different words.

## Schema

**Schema → structure of data**

Example:

```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

It defines what the data should look like.

---

## Scheme

**Scheme → method/protocol used for something.**

In authentication:

```text
Authorization: Bearer <token>
```

`Bearer` is the **authentication scheme**.

---

# 9. Authentication Scheme — Bearer

When you send an access token to a protected API:

```text
Authorization: Bearer <token>
```

The important parts are:

```text
Authorization → HTTP header

Bearer → authentication scheme

<token> → actual access token
```

So:

```text
schema → structure of data

scheme → method/protocol used for authentication
```

---

# 10. OAuth2PasswordBearer

In FastAPI:

```python
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

`OAuth2PasswordBearer` uses the **Bearer authentication scheme**.

The client sends:

```text
Authorization: Bearer <access_token>
```

And:

```python
tokenUrl="login"
```

means:

> The endpoint used to obtain the access token is `/login`.

It does **not** itself create the JWT.

---

# 11. Complete Mental Model

```text
                 DATABASE
                    │
                    │
             SELECT id ...
                    │
                    ▼
              user["id"]
                    │
                    ▼
          create_access_token()
                    │
                    ▼
               JWT token
                    │
                    ▼
       Authorization: Bearer <token>
                    │
                    ▼
             Protected API
```

And separately:

```text
schemas.py
    ↓
Pydantic models
    ↓
Define structure of request/response data
```

### Quick Reference

```text
schemas.py
→ Python file containing Pydantic models

Schema
→ Structure/shape of data

Scheme
→ Method/protocol

Bearer
→ Authentication scheme

Token
→ Credential used for authentication/authorization

JWT
→ A token format that can be used as an access token

SELECT id
→ Retrieve only the user's ID

user["id"]
→ Access the ID from a dictionary-like database row

(user.email,)
→ One-element tuple used as SQL query parameters
```

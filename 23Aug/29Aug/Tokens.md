# FastAPI Authentication — Quick Summary

## 1. `utils.py` / Utility

`utils.py` is commonly used to store **reusable helper functions**.

```python
# utils.py

def verify(plain_password, hashed_password):
    ...
```

Use it elsewhere:

```python
import utils

utils.verify(user_credentials.password, user["password"])
```

**Remember:**

```text
utils.py → reusable helper functions
```

`utils.py` is just a naming convention; Python/FastAPI does not give it special meaning.

---

# 2. `RealDictCursor` vs Normal Cursor

## With `RealDictCursor`

The database row behaves like a dictionary:

```python
user = {
    "id": 101,
    "email": "abc@gmail.com",
    "password": "hashed123"
}
```

Access values using:

```python
user["password"]
```

## Without `RealDictCursor`

The database row is generally returned as a tuple:

```python
user = (
    101,
    "abc@gmail.com",
    "hashed123"
)
```

Access values using their position:

```python
user[0]   # id
user[1]   # email
user[2]   # password
```

### Rule

```text
Dictionary → user["password"]

Tuple/list → user[2]

Object → user.password
```

`.password` is used when `user` is an object that has a `password` attribute.

---

# 3. Password During Login

Suppose the user sends:

```json
{
    "email": "abc@gmail.com",
    "password": "hello123"
}
```

FastAPI creates:

```python
user_credentials
```

So:

```python
user_credentials.password
```

means:

```text
Password entered by the user
```

---

## Password Stored in Database

The database should store a **password hash**, not the plain password.

Example:

```text
email: abc@gmail.com
password: $2b$12$........
```

After querying:

```python
user = cursor.fetchone()
```

with `RealDictCursor`:

```python
user["password"]
```

means:

```text
Hashed password retrieved from the database
```

---

# 4. Password Verification

Typical code:

```python
if not utils.verify(
    user_credentials.password,
    user["password"]
):
    raise HTTPException(
        status_code=403,
        detail="Invalid credentials"
    )
```

The two values are different:

```text
user_credentials.password
        ↓
Plain password entered by user
        ↓
"hello123"


user["password"]
        ↓
Hashed password from database
        ↓
"$2b$12$...."
```

The verification function checks whether the entered password matches the stored hash.

You **do not normally compare them directly**:

```python
user_credentials.password == user["password"]   # ❌
```

Instead:

```python
utils.verify(plain_password, hashed_password)   # ✅
```

---

# 5. What Is a Token?

A **token** is a value used by the client to prove that it has authenticated successfully.

After successful login:

```text
User
 ↓
Email + Password
 ↓
Backend verifies password
 ↓
Backend creates access token
 ↓
Token returned to client
```

The client then sends the token with later requests.

Example:

```text
Authorization: Bearer <access_token>
```

---

# 6. Who Creates the Token?

The **backend/server creates the access token**.

Example:

```python
@app.post("/login")
def login(...):

    # Verify user and password

    token = create_access_token(user_id)

    return {
        "access_token": token
    }
```

The client does not normally create the authentication token itself.

---

# 7. Access Token vs JWT

These are not exactly the same thing.

### Access Token

Describes the **purpose** of the value:

```text
Access Token
= token used to access protected resources
```

### JWT

Describes the **format/structure** of the token:

```text
JWT
= JSON Web Token
= a particular token format
```

Therefore:

```text
Access Token = PURPOSE

JWT = FORMAT
```

A JWT can be used as an access token.

---

# 8. Different Types of Access Tokens

An access token does not have to be a JWT.

## Option 1 — Random/opaque token

Example:

```text
8f72a91bc82d....
```

The server can keep track of which user/session that token belongs to.

## Option 2 — JWT access token

Example:

```text
xxxxx.yyyyy.zzzzz
```

A JWT has a structured format and is cryptographically signed.

So:

```text
                 ACCESS TOKEN
                      │
             ┌────────┴────────┐
             │                 │
        Random token          JWT
         (opaque)        (structured)
```

---

# 9. What Is JWT?

JWT stands for:

```text
JSON Web Token
```

A JWT is a **structured, signed token format** commonly used for authentication.

It typically has three parts:

```text
HEADER.PAYLOAD.SIGNATURE
```

Example shape:

```text
xxxxx.yyyyy.zzzzz
```

The payload can contain claims such as:

```text
user_id
expiration time
issuer
etc.
```

The JWT is signed so the server can verify that it was issued by a trusted party and has not been modified.

---

# 10. `OAuth2PasswordBearer`

In FastAPI you may see:

```python
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

This does **not create the JWT**.

It tells FastAPI/OAuth2-related tooling that:

```text
The endpoint used to obtain the token is /login
```

The flow is:

```text
POST /login
     ↓
Email + Password
     ↓
Verify password
     ↓
Create access token
     ↓
Return token
```

Then:

```text
Protected API
     ↑
Authorization: Bearer <token>
```

---

# 11. Why `OAuth2PasswordBearer` Has These Words

```python
OAuth2PasswordBearer(...)
```

### OAuth2

Refers to the OAuth 2.0 authorization framework.

### Password

The login/token flow involves the user providing credentials such as a username/password to obtain a token.

### Bearer

The token is sent as a **Bearer token**:

```text
Authorization: Bearer <token>
```

So:

```text
OAuth2PasswordBearer
        ↓
OAuth2 authentication concept
        +
Password-based token obtaining flow
        +
Bearer token sent with requests
```

---

# 12. Important: Bearer ≠ JWT

`Bearer` does **not** mean JWT.

Bearer describes **how the token is presented**:

```text
Authorization: Bearer <token>
```

The token itself could be:

```text
Random opaque token
```

or:

```text
JWT
```

So:

```text
Bearer → how the token is sent

JWT → token format
```

---

# 13. Complete Login Flow

Putting everything together:

```text
                 USER
                  │
                  │ email + password
                  ▼
                /login
                  │
                  ▼
          Find user in database
                  │
                  ▼
       Get stored password hash
                  │
                  ▼
          Verify entered password
                  │
            ┌─────┴─────┐
            │           │
          Wrong        Correct
            │           │
            ▼           ▼
          403       Create access
                      token
                        │
                  ┌─────┴─────┐
                  │           │
                Random       JWT
                token        token
                  │           │
                  └─────┬─────┘
                        ▼
                 Return token
                        │
                        ▼
             Protected API request
                        │
                        ▼
          Authorization: Bearer <token>
```

---

# 14. One-Line Definitions

```text
utils.py
→ File for reusable helper functions.

user_credentials.password
→ Plain password supplied by the user.

user["password"]
→ Password hash retrieved from the database when using a dict-like DB row.

Access Token
→ Credential used to access protected resources.

JWT
→ A structured, signed token format.

Bearer
→ Method of sending an access token in the Authorization header.

OAuth2PasswordBearer
→ FastAPI helper for extracting a Bearer token and declaring the token endpoint.

tokenUrl="login"
→ Tells the OAuth2 configuration that /login is the endpoint where a token is obtained.
```

# 15. The Most Important Mental Model

```text
PASSWORD
   ↓
User enters password
   ↓
Backend verifies it against stored HASH
   ↓
Backend creates ACCESS TOKEN
   ↓
ACCESS TOKEN may be a JWT
   ↓
Client sends:
Authorization: Bearer <JWT>
   ↓
Protected API
```

**The simplest distinction to remember:**

```text
Token = general concept

Access Token = token used to access protected APIs

JWT = one format that an access token can use

Bearer = how the access token is sent

OAuth2PasswordBearer = FastAPI helper for reading that Bearer token
```

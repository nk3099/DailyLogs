# FastAPI + PostgreSQL + JWT Authentication — Complete Notes for Protecting Routes

## Table of Contents

1. FastAPI Application and Routes
2. Router vs App
3. Request Body and Pydantic Models
4. PostgreSQL + `get_db()`
5. Creating Users
6. Password Hashing with Bcrypt
7. Bcrypt / Passlib Version Error
8. `500 Internal Server Error`
9. `422 Unprocessable Entity`
10. Response Models
11. `created_at` and Database Defaults
12. Handling `404 Not Found`
13. Login Flow
14. Why Login Does Not Require a Token
15. `403 Forbidden`
16. JWT
17. Access Token
18. HS256
19. JWT Structure
20. Secret Key
21. Encoding a JWT
22. Decoding a JWT
23. `algorithm` vs `algorithms`
24. JWT Payload
25. `user_id` and Other Payload Fields
26. `verify_access_token()`
27. OAuth2PasswordBearer
28. `Depends()`
29. Protected Endpoints
30. `401 Unauthorized`
31. RealDictCursor
32. Tuple vs Dictionary
33. Circular Imports
34. Correct Router Structure
35. Login Endpoint
36. Complete Authentication Flow
37. Common Errors and Fixes
38. Useful Commands
39. Complete Project Structure
40. Complete Example Code
41. Quick Revision Summary

---

# 1. FastAPI Application and Routes

A basic FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()
```

Here:

```python
app = FastAPI()
```

creates an instance/object of the `FastAPI` class.

Think of:

```text
FastAPI
   ↓
class

FastAPI()
   ↓
object / instance

app
   ↓
reference to that object
```

Then:

```python
@app.get("/")
def root():
    return {"message": "Hello World"}
```

`@app.get("/")` is a decorator.

It tells FastAPI:

> When an HTTP GET request comes to `/`, execute this function.

Flow:

```text
Client
   |
   | GET /
   ↓
FastAPI
   |
   | finds registered route
   ↓
root()
   |
   ↓
{"message": "Hello World"}
```

---

# 2. Router vs App

## `app`

The main FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()
```

It represents the entire API application.

Example:

```python
@app.get("/")
def root():
    ...

@app.post("/users")
def create_user():
    ...

@app.post("/login")
def login():
    ...
```

Everything is registered directly on `app`.

---

# Router

A router is used to organize endpoints into separate files.

Example:

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
```

Then:

```python
@router.post("/")
def create_user():
    ...
```

Because the router has:

```python
prefix="/users"
```

the actual endpoint becomes:

```text
POST /users/
```

Then the router is connected to the main application:

```python
app.include_router(user_router)
```

---

## Why use routers?

Instead of putting everything into:

```text
main.py
```

you can organize:

```text
main.py
users.py
auth.py
posts.py
```

Example:

```text
main.py
   |
   +---- users router
   |
   +---- auth router
   |
   +---- posts router
```

This is much cleaner as the application grows.

---

# 3. Request Body and Pydantic Models

Suppose:

```python
class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

And:

```python
@app.post("/login")
async def login(user_creds: schemas.UserLogin):
    ...
```

FastAPI understands that:

```python
user_creds: schemas.UserLogin
```

is a request body.

So the client sends:

```json
{
    "email": "abc@gmail.com",
    "password": "abc123"
}
```

FastAPI converts it into a Pydantic object:

```text
JSON
 ↓
FastAPI
 ↓
Pydantic validation
 ↓
UserLogin object
 ↓
user_creds
```

Then:

```python
user_creds.email
```

gets:

```text
abc@gmail.com
```

and:

```python
user_creds.password
```

gets:

```text
abc123
```

---

# 4. PostgreSQL + `get_db()`

A typical database dependency:

```python
def get_db():
    conn = psycopg2.connect(
        host="localhost",
        database="fastapiAug",
        user="postgres",
        password="admin",
        port=5432,
        cursor_factory=RealDictCursor
    )

    try:
        yield conn
    finally:
        conn.close()
```

Then:

```python
@app.get("/users")
def get_users(db=Depends(database.get_db)):
    cursor = db.cursor()
```

`Depends()` tells FastAPI:

> Before executing this endpoint, run this dependency and give me its result.

Flow:

```text
GET /users
     |
     ↓
FastAPI
     |
     ↓
Depends(get_db)
     |
     ↓
PostgreSQL connection
     |
     ↓
db
     |
     ↓
db.cursor()
     |
     ↓
SQL query
```

---

# 5. Creating Users

Example:

```python
@app.post("/users")
async def create_user(
    data: schemas.UserRequest,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    hashed_password = utils.hash(data.password)

    data.password = hashed_password

    cursor.execute(
        """
        INSERT INTO users(email, password)
        VALUES (%s, %s)
        RETURNING *
        """,
        (data.email, data.password)
    )

    user = cursor.fetchone()

    db.commit()

    return user
```

Important:

```python
data.password
```

initially contains the plain password.

Example:

```text
password = "abc123"
```

Then:

```python
hashed_password = utils.hash(data.password)
```

produces something like:

```text
$2b$12$...
```

The database should store the hash, not the original password.

Flow:

```text
User
 |
 | email + password
 ↓
FastAPI
 |
 ↓
Pydantic validation
 |
 ↓
hash password
 |
 ↓
bcrypt hash
 |
 ↓
INSERT into PostgreSQL
 |
 ↓
Database
```

---

# 6. Password Hashing with Bcrypt

Typical `utils.py`:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password: str, hash_password: str):
    return pwd_context.verify(
        plain_password,
        hash_password
    )
```

## Hashing

```python
utils.hash("abc123")
```

returns something like:

```text
$2b$12$...
```

The same password does not necessarily produce exactly the same hash every time because bcrypt uses a salt.

Therefore:

```text
abc123
   ↓
bcrypt
   ↓
hash
```

---

# 7. Bcrypt / Passlib Version Error

You encountered:

```text
(trapped) error reading bcrypt version

AttributeError:
module 'bcrypt' has no attribute '__about__'
```

and eventually:

```text
ValueError:
password cannot be longer than 72 bytes
```

The important issue was a compatibility problem between the installed versions of:

```text
passlib
bcrypt
```

Your older Passlib setup was interacting badly with the newer bcrypt package.

A commonly used fix for that setup was to install a compatible bcrypt version:

```bash
pip install bcrypt==4.0.1
```

Then verify:

```bash
pip show bcrypt
```

or:

```bash
pip freeze | grep bcrypt
```

---

# How to know which version is installed?

Use:

```bash
pip show bcrypt
```

Example:

```text
Name: bcrypt
Version: 4.0.1
```

Or:

```bash
pip freeze
```

This shows installed packages and versions.

Example:

```text
bcrypt==4.0.1
fastapi==...
passlib==...
```

---

# How to check the latest version?

Use:

```bash
pip index versions bcrypt
```

This shows available versions.

You can also use:

```bash
pip install --upgrade bcrypt
```

But:

> Latest does not always mean compatible with every other package.

This is why production projects normally pin compatible versions in:

```text
requirements.txt
```

Example:

```text
fastapi==0.x.x
passlib==1.7.4
bcrypt==4.0.1
psycopg2-binary==...
python-jose==...
```

---

# 8. What does `500 Internal Server Error` mean?

A `500` generally means:

> Something went wrong inside your server/application.

For example:

```text
POST /users
      |
      ↓
FastAPI
      |
      ↓
utils.hash()
      |
      ↓
Passlib
      |
      ↓
Exception
      |
      ↓
500 Internal Server Error
```

A `500` is different from validation errors.

For example:

```text
422
```

usually means the request doesn't match the expected input schema.

---

# 9. `422 Unprocessable Entity`

You encountered:

```text
422 Unprocessable Entity
```

with:

```text
{
    "type": "missing",
    "loc": ["body", "emai"],
    "msg": "Field required"
}
```

The important part was:

```text
"emai"
```

Your Pydantic model expected:

```python
emai: ...
```

while your JSON contained:

```json
{
    "email": "abc2@gmail.com",
    "password": "abc1"
}
```

So FastAPI said:

> I need a field called `emai`, but you sent `email`.

Correct schema:

```python
class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

Correct request:

```json
{
    "email": "abc2@gmail.com",
    "password": "abc1"
}
```

---

# 422 vs 500

## 422

Request doesn't satisfy validation.

Example:

```text
Missing email
Invalid email
Wrong data type
Wrong field name
```

## 500

Server-side exception.

Example:

```text
Python exception
Database exception
Hashing exception
Incorrect code
```

---

# 10. Response Models

Suppose:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
```

and:

```python
@app.get(
    "/users/{id}",
    response_model=schemas.UserResponse
)
def get_user(id: int):
    ...
```

FastAPI expects the returned value to contain:

```text
id
email
name
```

If you return something that doesn't match:

```python
return something_wrong
```

FastAPI can raise:

```text
ResponseValidationError
```

---

# Important

A `response_model` validates the **response**.

A Pydantic parameter validates the **request**.

Example:

```python
def create_user(data: UserRequest):
```

means:

```text
Request validation
```

while:

```python
response_model=UserResponse
```

means:

```text
Response validation
```

---

# 11. `created_at` and Database Defaults

Suppose:

```python
class postResponse(validate_postBase):
    id: int
    created_at: datetime
```

Where does `created_at` come from?

It doesn't automatically come from Pydantic just because you declared:

```python
created_at: datetime
```

Usually the database creates it.

For example PostgreSQL:

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    published BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

When inserting:

```sql
INSERT INTO posts(title, content)
VALUES ('Hello', 'My post');
```

PostgreSQL automatically generates:

```text
created_at
```

because of:

```sql
DEFAULT NOW()
```

Flow:

```text
INSERT
  |
  ↓
PostgreSQL
  |
  +---- id → generated
  |
  +---- created_at → NOW()
  |
  ↓
RETURNING *
  |
  ↓
FastAPI response
```

---

# 12. Handling `404 Not Found`

You had an issue where an endpoint returned an `HTTPException` object instead of actually raising it.

Wrong:

```python
return HTTPException(
    status_code=404,
    detail=f"the {id} not found"
)
```

Correct:

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"the {id} not found"
)
```

The keyword is:

```python
raise
```

not:

```python
return
```

---

# Why?

`HTTPException` is an exception.

You tell Python/FastAPI:

```python
raise HTTPException(...)
```

meaning:

> Stop executing this endpoint and return this HTTP error.

Example:

```python
user = cursor.fetchone()

if not user:
    raise HTTPException(
        status_code=404,
        detail=f"User with id {id} not found"
    )

return user
```

Flow:

```text
SELECT user
    |
    ↓
Found?
 /     \
YES     NO
 |       |
 ↓       ↓
return  raise 404
user
```

---

# 13. Login Flow

Login does approximately this:

```text
User
 |
 | email + password
 ↓
POST /login
 |
 ↓
Find user by email
 |
 ↓
User exists?
 /       \
NO       YES
 |         |
403       verify password
           |
           ↓
       Password correct?
        /          \
      NO            YES
      |              |
     403             ↓
                 create JWT
                     |
                     ↓
                 return token
```

---

# 14. Why Login Does NOT Require a Token

This is a very important rule.

You cannot normally require an access token to obtain the first access token.

Correct:

```text
Signup
  ↓
NO TOKEN

Login
  ↓
NO TOKEN

Protected endpoint
  ↓
TOKEN REQUIRED
```

If `/login` required a token:

```text
Need token
   ↓
to login
   ↓
but need login
   ↓
to get token
   ↓
infinite loop
```

Therefore:

```python
@app.post("/login")
async def login(...):
```

does NOT use:

```python
Depends(oauth2.get_current_user)
```

---

# 15. `403 Forbidden`

For incorrect login credentials, your code can return:

```python
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Invalid credentials"
)
```

Example:

```python
if not user:
    raise HTTPException(
        status_code=403,
        detail="Invalid credentials"
    )
```

and:

```python
if not utils.verify(
    user_creds.password,
    user["password"]
):
    raise HTTPException(
        status_code=403,
        detail="Invalid credentials"
    )
```

---

# Note

You wrote:

```python
details="invalid creds"
```

The correct argument is:

```python
detail="invalid creds"
```

not:

```python
details
```

---

# 16. JWT

JWT means:

> JSON Web Token

JWT is commonly used to represent authentication information between a client and server.

A JWT has three parts:

```text
HEADER.PAYLOAD.SIGNATURE
```

Example conceptually:

```text
xxxxx.yyyyy.zzzzz
```

---

# 17. Access Token

An access token is a credential that the client sends to a protected endpoint.

Example:

```http
Authorization: Bearer <access_token>
```

JWT can be the format used for that access token.

Therefore:

> JWT and access token are related, but they are not exactly the same concept.

Think:

```text
Access token
   |
   +---- can be represented as JWT
   |
   +---- can use another format too
```

---

# 18. HS256

HS256 means:

> HMAC using SHA-256

More specifically:

```text
HS256
 ↓
HMAC-SHA256
```

It is a JWT signing algorithm.

HS256 uses the same secret key for:

```text
Signing
and
Verification
```

Conceptually:

```text
Payload
   +
Secret Key
   +
HS256
   ↓
Signature
```

---

# 19. JWT Structure

JWT consists of:

```text
HEADER
   .
PAYLOAD
   .
SIGNATURE
```

---

## Header

The header contains metadata such as:

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

Meaning:

```text
alg = algorithm
typ = token type
```

So:

```text
alg: HS256
```

means:

> The JWT is signed using HS256.

---

# 20. Secret Key

Example:

```python
SECRET_KEY = "some-long-secret-key"
```

The secret key is used for signing and verifying the JWT.

Conceptually:

```text
Payload
   |
   + Secret Key
   |
   + HS256
   ↓
Signature
```

The secret key should be kept secret.

It should not be exposed to clients.

---

# 21. Encoding a JWT

Example:

```python
access_token = jwt.encode(
    to_encode,
    SECRET_KEY,
    algorithm=ALGORITHM
)
```

Suppose:

```python
ALGORITHM = "HS256"
```

Then:

```python
jwt.encode(
    payload,
    SECRET_KEY,
    algorithm="HS256"
)
```

creates a signed JWT.

---

# 22. Decoding a JWT

Example:

```python
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
```

This verifies the token and extracts the payload.

Flow:

```text
JWT token
   |
   ↓
jwt.decode()
   |
   +---- SECRET_KEY
   |
   +---- allowed algorithms
   |
   ↓
Signature verified?
   |
   +---- NO → error
   |
   +---- YES
          ↓
       payload
```

---

# 23. `algorithm` vs `algorithms`

This was one of your important questions.

## Encoding

You are creating one token using one algorithm:

```python
jwt.encode(
    data,
    SECRET_KEY,
    algorithm=ALGORITHM
)
```

So:

```python
algorithm="HS256"
```

is a **single value**.

---

## Decoding

You are telling the decoder which algorithms it is allowed to accept:

```python
jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
```

Notice:

```python
algorithms=[ALGORITHM]
```

is a list.

Example:

```python
ALGORITHM = "HS256"
```

Then:

```python
algorithms=[ALGORITHM]
```

becomes:

```python
algorithms=["HS256"]
```

---

# Why a list?

The JWT library's decode API accepts a collection of allowed algorithms.

It means:

> Only accept tokens whose algorithm is one of these allowed algorithms.

For your application:

```python
algorithms=["HS256"]
```

means:

> Only accept HS256.

It is NOT mixing algorithms.

It is NOT trying to decode the token using all algorithms.

It is an allow-list.

---

# Example

```python
algorithms=["HS256"]
```

means:

```text
Token says:
alg = HS256

Allowed:
HS256

Result:
YES
```

If token says:

```text
alg = RS256
```

but you only allow:

```python
["HS256"]
```

then it should not be accepted.

---

# 24. JWT Payload

The payload is the data stored inside the JWT.

Example:

```python
data = {
    "user_id": 101
}
```

Then:

```python
to_encode = data.copy()
```

creates a copy.

Then:

```python
to_encode.update({
    "exp": expire
})
```

adds expiration.

The resulting payload could conceptually be:

```json
{
    "user_id": 101,
    "exp": 1780000000
}
```

---

# Important

The JWT payload is **not encrypted by default**.

It is encoded and signed.

Therefore:

> Don't put sensitive secrets/passwords inside the payload.

---

# 25. `user_id` and Other Payload Fields

You wrote:

```python
access_token = oauth2.create_access_token(
    data={
        "user_id": user["id"]
    }
)
```

Then later:

```python
user_id = payload.get("user_id")
```

These two strings:

```text
"user_id"
```

are related because you chose the same payload key.

You could technically use another key.

For example:

```python
data={
    "user": user["id"]
}
```

Then decoding:

```python
user_id = payload.get("user")
```

would work.

The important rule is:

```text
Key used when creating token
        =
Key used when reading token
```

---

# Example

Create:

```python
data={
    "user_id": 101
}
```

Read:

```python
payload.get("user_id")
```

Correct.

But:

```python
payload.get("user")
```

would return:

```python
None
```

because there is no `"user"` key.

---

# You can store multiple fields

For example:

```python
data = {
    "user_id": user["id"],
    "role": "admin"
}
```

Then:

```python
payload.get("user_id")
payload.get("role")
```

can retrieve them.

---

# 26. `verify_access_token()`

Typical implementation:

```python
def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        return user_id

    except JWTError:
        raise credentials_exception
```

This function checks whether the JWT is valid and extracts the user ID.

---

# What happens?

Suppose:

```text
Authorization:
Bearer eyJ...
```

FastAPI gets the token.

Then:

```python
jwt.decode(...)
```

checks:

```text
Is token structurally valid?
        ↓
Is signature valid?
        ↓
Was it signed using an allowed algorithm?
        ↓
Has it expired?
        ↓
Return payload
```

Then:

```python
payload.get("user_id")
```

gets the user ID.

---

# 27. OAuth2PasswordBearer

Example:

```python
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

This tells FastAPI's OAuth2 security machinery:

> The endpoint used to obtain a token is `/login`.

It also provides a dependency that extracts the Bearer token from the request.

For example:

```python
token: str = Depends(oauth2_scheme)
```

If the request is:

```http
Authorization: Bearer abc123
```

then:

```python
token
```

becomes:

```text
abc123
```

---

# Important

`OAuth2PasswordBearer` does NOT itself create the JWT.

It mainly helps:

```text
Extract Bearer token
+
Describe OAuth2 security to FastAPI/OpenAPI
```

Your login endpoint creates the token.

---

# 28. `Depends()`

Example:

```python
user_id: int = Depends(oauth2.get_current_user)
```

means:

> Before running this endpoint, execute `get_current_user()` and inject its return value into `user_id`.

For example:

```python
@app.get("/users")
def get_all_users(
    db=Depends(database.get_db),
    user_id: int = Depends(oauth2.get_current_user)
):
    ...
```

There are two dependencies:

```text
database.get_db
       ↓
      db

oauth2.get_current_user
       ↓
    user_id
```

---

# 29. Protected Endpoints

Suppose:

```python
@app.get("/users")
def get_all_users(
    db=Depends(database.get_db),
    user_id: int=Depends(oauth2.get_current_user)
):
    ...
```

This endpoint requires authentication.

Flow:

```text
GET /users
     |
     ↓
Authorization header?
     |
     +---- NO
     |      ↓
     |     401
     |
     +---- YES
            |
            ↓
       Extract token
            |
            ↓
       Decode JWT
            |
            ↓
       Verify signature
            |
            ↓
       Get user_id
            |
            ↓
       Execute endpoint
```

---

# Signup vs Login vs Protected Endpoint

```text
POST /users
   |
   └── Create account
       Token required? NO


POST /login
   |
   └── Verify credentials
       Token required? NO
       Returns token


GET /users
   |
   └── Protected resource
       Token required? YES
```

---

# 30. `401 Unauthorized`

You encountered:

```text
401 Not authenticated
```

This commonly happens when a protected endpoint does not receive a valid authentication credential.

Example:

```text
GET /users
```

without:

```http
Authorization: Bearer <token>
```

can result in:

```text
401 Unauthorized
```

---

# 401 vs 403

A useful mental model:

## 401

Authentication is missing or invalid.

Example:

```text
No token
Invalid token
Expired token
```

## 403

The server understood who you are / the request, but access is forbidden.

In your login code, you used:

```python
403
```

for invalid credentials.

The exact status-code conventions can vary by API design, but the important thing is to use them consistently.

---

# 31. RealDictCursor

You used:

```python
from psycopg2.extras import RealDictCursor
```

This makes returned rows behave like dictionaries.

Example:

```python
user = cursor.fetchone()
```

could look like:

```python
{
    "id": 101,
    "email": "abc@gmail.com",
    "password": "hashed..."
}
```

Then:

```python
user["password"]
```

works.

And:

```python
user["id"]
```

works.

---

# Without RealDictCursor

A normal cursor may return:

```python
(
    101,
    "abc@gmail.com",
    "hashed..."
)
```

Then:

```python
user[0]
```

is the ID.

```python
user[1]
```

is the email.

```python
user[2]
```

is the password.

---

# Important

You cannot know whether:

```python
user["password"]
```

works merely from:

```python
cursor.fetchone()
```

You need to know what cursor class is being used.

You used:

```python
RealDictCursor
```

so dictionary-style access works.

---

# 32. ResponseValidationError with List Instead of Object

You encountered:

```text
ResponseValidationError

Input should be a valid dictionary or object

input:
[
    RealDictRow(...)
]
```

This happened because your response model expected one object:

```python
response_model=schemas.UserResponse
```

but your endpoint returned a list:

```python
users = cursor.fetchall()

return users
```

`fetchall()` returns multiple rows:

```python
[
    {...},
    {...},
    {...}
]
```

while `UserResponse` represents one user:

```python
{
    "id": 1,
    "email": "...",
    "name": "..."
}
```

---

# Correct solution

For multiple users:

```python
@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)
def get_all_users(...):
    ...
```

Now FastAPI expects:

```text
list of UserResponse
```

Flow:

```text
fetchall()
   ↓
[
  user1,
  user2,
  user3
]
   ↓
list[UserResponse]
   ↓
valid response
```

---

# 33. Circular Imports

You encountered:

```text
ImportError:
cannot import name 'app' from partially initialized module 'main'
```

because you had something like:

## `main.py`

```python
import auth

app = FastAPI()
```

and:

## `auth.py`

```python
from main import app
```

This creates:

```text
main.py
  |
  ↓
imports auth.py
  |
  ↓
auth.py imports main.py
  |
  ↓
main.py is still loading
  |
  ↓
circular import
```

Hence:

```text
partially initialized module
```

---

# Why importing `auth` before `app` doesn't solve it

Suppose:

```python
import auth

app = FastAPI()
```

`auth.py` still executes:

```python
from main import app
```

But `main.py` hasn't yet created `app`.

So:

```python
app = FastAPI()
```

has not executed yet.

Therefore it still fails.

---

# 34. Correct Router Structure

Instead of making `auth.py` import:

```python
from main import app
```

create a router.

## `auth.py`

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    ...
```

Then in:

## `main.py`

```python
from fastapi import FastAPI
from auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)
```

Now:

```text
main.py
   |
   ↓
creates app
   |
   ↓
includes auth router
   |
   ↓
/login registered
```

No circular dependency.

---

# 35. Login Endpoint

A clean login endpoint:

```python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/login")
async def login(
    user_creds: schemas.UserLogin,
    conn=Depends(get_db)
):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email=%s
        """,
        (user_creds.email,)
    )

    user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    if not utils.verify(
        user_creds.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    access_token = oauth2.create_access_token(
        data={
            "user_id": user["id"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

---

# Login only searches by email first

This query:

```python
cursor.execute(
    """
    SELECT * FROM users
    WHERE email=%s
    """,
    (user_creds.email,)
)
```

means:

> Find the database user whose email matches the email supplied during login.

It does NOT check the password in SQL.

The password is checked separately:

```python
utils.verify(
    user_creds.password,
    user["password"]
)
```

---

# Login flow in detail

Suppose request:

```json
{
    "email": "test1@gmail.com",
    "password": "test1"
}
```

### Step 1

FastAPI validates:

```python
UserLogin
```

### Step 2

SQL:

```sql
SELECT *
FROM users
WHERE email=%s
```

### Step 3

Database returns:

```python
{
    "id": 766,
    "email": "test1@gmail.com",
    "password": "$2b$12$..."
}
```

### Step 4

Verify:

```python
utils.verify(
    "test1",
    "$2b$12$..."
)
```

### Step 5

If correct:

```python
oauth2.create_access_token(
    data={"user_id": 766}
)
```

### Step 6

Return:

```json
{
    "access_token": "eyJ...",
    "token_type": "bearer"
}
```

---

# 36. Complete JWT Creation Function

Example:

```python
from datetime import datetime, timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 10

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
```

---

# What is `data.copy()`?

Suppose:

```python
data = {
    "user_id": 101
}
```

Then:

```python
to_encode = data.copy()
```

creates another dictionary:

```text
data
 ↓
{"user_id": 101}

to_encode
 ↓
{"user_id": 101}
```

This allows you to add:

```python
"exp"
```

without modifying the original dictionary.

---

# What is `timedelta(minutes=10)`?

```python
timedelta(minutes=10)
```

represents a duration of 10 minutes.

So:

```python
datetime.utcnow() + timedelta(minutes=10)
```

means:

> Current UTC time + 10 minutes.

---

# `exp`

JWT has a standard claim:

```text
exp
```

which means:

> expiration time

Example:

```python
{
    "user_id": 101,
    "exp": ...
}
```

When the token expires, it should no longer be accepted.

---

# 37. Complete Authentication Flow

The entire system can be visualized as:

```text
                 ┌─────────────────┐
                 │     CLIENT      │
                 └────────┬────────┘
                          │
                          │ POST /users
                          ↓
                 ┌─────────────────┐
                 │    FastAPI      │
                 └────────┬────────┘
                          │
                          ↓
                 Validate request
                          │
                          ↓
                 Hash password
                          │
                          ↓
                 ┌─────────────────┐
                 │   PostgreSQL    │
                 └─────────────────┘
```

Then login:

```text
CLIENT
  |
  | POST /login
  | email + password
  ↓
FastAPI
  |
  ↓
Find user by email
  |
  ↓
PostgreSQL
  |
  ↓
Stored password hash
  |
  ↓
bcrypt.verify()
  |
  ↓
Correct?
 /       \
NO       YES
 |         |
403       create JWT
           |
           ↓
       return token
```

Then accessing a protected endpoint:

```text
CLIENT
  |
  | GET /users
  |
  | Authorization:
  | Bearer eyJ...
  ↓
FastAPI
  |
  ↓
OAuth2PasswordBearer
  |
  ↓
Extract token
  |
  ↓
jwt.decode()
  |
  ↓
Verify signature
  |
  ↓
Read user_id
  |
  ↓
get_current_user()
  |
  ↓
Protected endpoint
  |
  ↓
Database
  |
  ↓
Response
```

---

# 38. JWT Flow

```text
                 LOGIN
                   |
                   ↓
          email + password
                   |
                   ↓
             Find user
                   |
                   ↓
          Verify password
                   |
                   ↓
             user_id
                   |
                   ↓
          Create JWT payload
                   |
                   ↓
          +----------------+
          | user_id: 101   |
          | exp: ...       |
          +----------------+
                   |
                   ↓
                 HS256
                   +
              SECRET_KEY
                   |
                   ↓
               SIGNATURE
                   |
                   ↓
                 JWT
                   |
                   ↓
               CLIENT
```

---

# 39. What exactly does HS256 do?

Conceptually:

```text
HEADER
   +
PAYLOAD
   +
SECRET KEY
   |
   ↓
 HMAC-SHA256
   |
   ↓
SIGNATURE
```

The JWT becomes:

```text
base64url(header)
.
base64url(payload)
.
signature
```

The server later recomputes/verifies the signature using:

```text
same SECRET_KEY
+
HS256
```

If the token was modified:

```text
original payload
      ↓
modified payload
      ↓
signature no longer matches
      ↓
token rejected
```

---

# 40. JWT Is Signed, Not Normally Encrypted

This distinction is important.

HS256 provides:

```text
Integrity
+
Authenticity
```

It does not make the payload secret.

Therefore don't put:

```text
password
credit card information
secret data
```

inside a JWT payload.

For example:

```python
{
    "user_id": 101
}
```

is fine.

---

# 41. `user_id` Is Your Choice

This:

```python
data={
    "user_id": user["id"]
}
```

is an application-level design choice.

JWT itself does not force you to use:

```text
user_id
```

You could use:

```python
{
    "sub": "101"
}
```

`sub` is actually a standard JWT claim meaning:

> subject

Many authentication systems use:

```python
"sub"
```

for the user identifier.

But if your code uses:

```python
"user_id"
```

that's completely understandable for learning and simple applications.

---

# 42. OpenID Connect

JWT and OpenID Connect are related to authentication, but they are not the same thing.

```text
OAuth 2.0
   |
   +---- Authorization framework
   |
   ↓
OpenID Connect
   |
   +---- Authentication layer built on OAuth 2.0
```

JWT is a token format that can be used by authentication/authorization systems.

So:

```text
JWT ≠ OpenID Connect
```

and:

```text
OAuth2PasswordBearer ≠ OpenID Connect
```

Your FastAPI application is using OAuth2-style Bearer authentication with JWT.

---

# 43. Common Mistakes

## Mistake 1 — Wrong SQL syntax

Wrong:

```python
SELCT * FROM users
```

Correct:

```python
SELECT * FROM users
```

---

# Mistake 2 — Missing comma in SQL parameter tuple

Correct:

```python
(user_creds.email,)
```

Why comma?

Because:

```python
("abc@gmail.com")
```

is just a string.

While:

```python
("abc@gmail.com",)
```

is a tuple containing one element.

---

# Mistake 3 — `details` instead of `detail`

Wrong:

```python
HTTPException(
    status_code=403,
    details="invalid creds"
)
```

Correct:

```python
HTTPException(
    status_code=403,
    detail="invalid creds"
)
```

---

# Mistake 4 — `return HTTPException`

Wrong:

```python
return HTTPException(...)
```

Correct:

```python
raise HTTPException(...)
```

---

# Mistake 5 — Using `user_id` inconsistently

Create:

```python
{
    "user_ids": user["id"]
}
```

but decode:

```python
payload.get("user_id")
```

These are different keys.

You must use the same key:

```python
{
    "user_id": user["id"]
}
```

and:

```python
payload.get("user_id")
```

---

# Mistake 6 — Response model expects one object

If:

```python
response_model=UserResponse
```

but:

```python
fetchall()
```

returns a list:

```python
[...]
```

you need:

```python
response_model=list[UserResponse]
```

---

# Mistake 7 — Circular imports

Avoid:

```text
main.py → auth.py → main.py
```

Use routers:

```text
main.py
   |
   ↓
auth router
```

---

# Mistake 8 — Protected signup/login

Don't do:

```python
@app.post("/login")
def login(
    ...,
    user_id=Depends(get_current_user)
):
```

Login should not normally require the token it is supposed to issue.

---

# 44. Duplicate User ID

If your table uses:

```sql
id INT PRIMARY KEY
```

and you manually generate:

```python
random_id = random.randint(1, 1000)
```

you can eventually generate an ID that already exists.

Example:

```text
Existing:
id = 500

New random ID:
500

INSERT
 ↓
PRIMARY KEY violation
 ↓
500 Internal Server Error
```

A better database design is usually:

```sql
id SERIAL PRIMARY KEY
```

or modern PostgreSQL identity columns:

```sql
id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
```

Then don't manually generate the ID in Python.

Example:

```sql
INSERT INTO users(email, password)
VALUES (%s, %s)
RETURNING *
```

PostgreSQL generates the ID.

---

# 45. Recommended User Table

Example:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

Important:

```text
id
 ↓
Database generated

email
 ↓
UNIQUE

password
 ↓
bcrypt hash

created_at
 ↓
Database generated
```

---

# 46. Better Duplicate Email Handling

Before inserting:

```python
cursor.execute(
    "SELECT id FROM users WHERE email=%s",
    (user.email,)
)

if cursor.fetchone():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Email already registered"
    )
```

Then insert.

`409 Conflict` is useful for:

> The request conflicts with existing server state.

---

# 47. Complete Recommended Project Structure

```text
fastapiAug/
│
├── main.py
├── database.py
├── schemas.py
├── utils.py
├── oauth2.py
├── auth.py
├── users.py
│
└── .venv/
```

---

# 48. `main.py`

```python
from fastapi import FastAPI

from users import router as users_router
from auth import router as auth_router

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }
```

---

# 49. `schemas.py`

```python
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
```

---

# 50. `utils.py`

```python
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash(password: str):
    return pwd_context.hash(password)


def verify(
    plain_password: str,
    hash_password: str
):
    return pwd_context.verify(
        plain_password,
        hash_password
    )
```

---

# 51. `database.py`

Example:

```python
import psycopg2

from psycopg2.extras import RealDictCursor


def get_db():

    conn = psycopg2.connect(
        host="localhost",
        database="fastapiAug",
        user="postgres",
        password="admin",
        port=5432,
        cursor_factory=RealDictCursor
    )

    try:
        yield conn
    finally:
        conn.close()
```

---

# 52. `oauth2.py`

```python
from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_access_token(
    token: str,
    credentials_exception
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id: int = payload.get(
            "user_id"
        )

        if user_id is None:
            raise credentials_exception

        return user_id

    except JWTError:
        raise credentials_exception


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    return verify_access_token(
        token,
        credentials_exception
    )
```

---

# 53. `auth.py`

```python
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

import schemas
import utils
import oauth2

from database import get_db


router = APIRouter()


@router.post("/login")
async def login(
    user_creds: schemas.UserLogin,
    conn=Depends(get_db)
):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email=%s
        """,
        (user_creds.email,)
    )

    user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    if not utils.verify(
        user_creds.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    access_token = oauth2.create_access_token(
        data={
            "user_id": user["id"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

---

# 54. `users.py`

```python
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

import schemas
import utils
import oauth2

from database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut
)
def create_user(
    user: schemas.UserCreate,
    conn=Depends(get_db)
):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email=%s
        """,
        (user.email,)
    )

    if cursor.fetchone():

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    hashed_password = utils.hash(
        user.password
    )

    cursor.execute(
        """
        INSERT INTO users(email, password)
        VALUES(%s, %s)
        RETURNING *
        """,
        (
            user.email,
            hashed_password
        )
    )

    new_user = cursor.fetchone()

    conn.commit()

    return new_user


@router.get(
    "/",
    response_model=list[schemas.UserOut]
)
def get_all_users(
    conn=Depends(get_db),
    user_id: int=Depends(
        oauth2.get_current_user
    )
):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, email
        FROM users
        """
    )

    users = cursor.fetchall()

    return users


@router.get(
    "/{id}",
    response_model=schemas.UserOut
)
def get_user(
    id: int,
    conn=Depends(get_db)
):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, email
        FROM users
        WHERE id=%s
        """,
        (id,)
    )

    user = cursor.fetchone()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    return user
```

---

# 55. Important Route Ordering

Suppose you have:

```python
@app.get("/users")
```

and:

```python
@app.get("/users/{id}")
```

The static route:

```text
/users
```

is different from:

```text
/users/{id}
```

Examples:

```text
GET /users
```

means all users.

```text
GET /users/101
```

means user 101.

---

# 56. Testing the API

Start the server:

```bash
uvicorn main:app --reload
```

If you get:

```text
ERROR: [Errno 48] Address already in use
```

it means something is already using port `8000`.

Usually another Uvicorn process is running.

Stop the existing server with:

```text
CTRL + C
```

or find the process:

```bash
lsof -i :8000
```

Then terminate it if necessary.

---

# 57. `-y`

You asked about:

```bash
-y
```

For many package managers/commands:

```bash
-y
```

means:

> Automatically answer yes to confirmation prompts.

For example, depending on the command:

```bash
brew uninstall something -y
```

or:

```bash
apt install something -y
```

The exact support for `-y` depends on the command.

It is not a universal shell option.

---

# 58. `-e` in `pip install -e`

You also asked about:

```bash
-e
```

In pip:

```bash
pip install -e .
```

means:

> Install the current project in editable mode.

Editable mode is useful when developing a Python package.

Instead of copying the package into the environment, pip links it to your source directory.

So changes to your source code are immediately reflected.

---

# 59. `pip freeze`

You asked what `freeze` means.

```bash
pip freeze
```

prints the installed Python packages and their exact versions.

Example:

```text
fastapi==0.x.x
bcrypt==4.0.1
passlib==1.7.4
psycopg2-binary==...
python-jose==...
```

You can save it:

```bash
pip freeze > requirements.txt
```

Then another environment can install the same versions:

```bash
pip install -r requirements.txt
```

Flow:

```text
Current environment
       |
       ↓
pip freeze
       |
       ↓
requirements.txt
       |
       ↓
another environment
       |
       ↓
pip install -r requirements.txt
```

---

# 60. Installing `python-jose`

If your code says:

```python
from jose import jwt, JWTError
```

the commonly used package is:

```bash
pip install "python-jose[cryptography]"
```

Important:

```text
jose
```

is the module name you import:

```python
from jose import jwt
```

while:

```text
python-jose
```

is the package you install.

---

# 61. Why `from jose import jwt`

You install:

```bash
pip install python-jose
```

Then Python provides the module:

```python
jose
```

So:

```python
from jose import jwt
```

means:

> Import the `jwt` functionality from the `jose` package.

---

# 62. Complete Authentication Architecture

```text
                         FASTAPI
                            |
            +---------------+---------------+
            |               |               |
            ↓               ↓               ↓
          USERS            LOGIN          POSTS
            |               |               |
            |               ↓               |
            |          Verify password      |
            |               |               |
            |               ↓               |
            |          Create JWT           |
            |               |               |
            |               ↓               |
            |          Return token         |
            |                               |
            +---------------+---------------+
                            |
                            ↓
                    Protected endpoints
                            |
                            ↓
                    Bearer token
                            |
                            ↓
                    OAuth2PasswordBearer
                            |
                            ↓
                       jwt.decode
                            |
                            ↓
                      verify signature
                            |
                            ↓
                        user_id
                            |
                            ↓
                       allow access
```

---

# 63. End-to-End Example

## Step 1 — Register

Request:

```http
POST /users/
```

Body:

```json
{
    "email": "test1@gmail.com",
    "password": "test1"
}
```

FastAPI:

```text
Validate
 ↓
Hash password
 ↓
Insert into DB
```

Database:

```text
id = 766
email = test1@gmail.com
password = $2b$12$...
```

---

# Step 2 — Login

Request:

```http
POST /login
```

Body:

```json
{
    "email": "test1@gmail.com",
    "password": "test1"
}
```

Server:

```text
Find email
 ↓
Get hash
 ↓
bcrypt.verify()
 ↓
Correct
 ↓
Create JWT
```

Response:

```json
{
    "access_token": "eyJ...",
    "token_type": "bearer"
}
```

---

# Step 3 — Call protected endpoint

Request:

```http
GET /users/
```

Header:

```http
Authorization: Bearer eyJ...
```

FastAPI:

```text
Extract token
 ↓
Decode token
 ↓
Verify signature
 ↓
Read user_id
 ↓
Allow endpoint
```

---

# Step 4 — Invalid token

```text
GET /users/
      |
      ↓
Invalid/missing token
      |
      ↓
401 Unauthorized
```

---

# Step 5 — Wrong login password

```text
POST /login
      |
      ↓
Find user
      |
      ↓
Password verification
      |
      ↓
Wrong password
      |
      ↓
403 Forbidden
```

---

# 64. Most Important Concepts to Remember

## FastAPI

```python
app = FastAPI()
```

creates the main FastAPI application object.

---

## Decorator

```python
@app.get("/users")
```

registers a route.

---

## Router

```python
router = APIRouter()
```

organizes related endpoints.

---

## `include_router`

```python
app.include_router(router)
```

connects the router to the main FastAPI application.

---

## `Depends`

```python
db=Depends(get_db)
```

asks FastAPI to execute a dependency and inject its result.

---

## Pydantic request model

```python
user: UserCreate
```

validates incoming request data.

---

## Response model

```python
response_model=UserOut
```

validates/serializes outgoing response data.

---

## Password hashing

```python
utils.hash(password)
```

turns a plain password into a bcrypt hash.

---

## Password verification

```python
utils.verify(
    plain_password,
    stored_hash
)
```

checks whether the supplied password matches the stored hash.

---

## JWT

```text
HEADER.PAYLOAD.SIGNATURE
```

is the token structure.

---

## HS256

```text
HMAC + SHA-256
```

is a JWT signing algorithm.

---

## Secret key

Used by HS256 to create and verify the signature.

---

## `algorithm`

Used during encoding:

```python
algorithm="HS256"
```

One algorithm.

---

## `algorithms`

Used during decoding:

```python
algorithms=["HS256"]
```

An allow-list of acceptable algorithms.

It does **not** mix them.

---

## Payload

Contains claims/data such as:

```python
{
    "user_id": 101,
    "exp": ...
}
```

---

## `user_id`

Not magic.

It's simply the key you chose:

```python
"user_id"
```

You must use the same key when reading:

```python
payload.get("user_id")
```

---

## `exp`

Standard JWT expiration claim.

```python
"exp": expire
```

tells the JWT when it expires.

---

## OAuth2PasswordBearer

Extracts the Bearer token from the request and integrates OAuth2 security with FastAPI/OpenAPI.

It does not itself create your JWT.

---

## Protected endpoint

Uses:

```python
Depends(oauth2.get_current_user)
```

to require authentication.

---

## `401`

Usually authentication missing/invalid.

---

## `403`

Access/credentials rejected according to the API's chosen semantics.

---

## `404`

Resource not found.

---

## `409`

Conflict, such as duplicate email.

---

## `422`

Request validation failed.

---

## `500`

Unexpected server-side exception.

---

# 65. One Final Mental Model

The entire authentication system can be remembered as:

```text
                SIGNUP
                  |
                  ↓
          email + password
                  |
                  ↓
            hash password
                  |
                  ↓
             PostgreSQL
                  |
                  |
                  ↓
                LOGIN
                  |
                  ↓
          email + password
                  |
                  ↓
         find user by email
                  |
                  ↓
         verify password hash
                  |
                  ↓
          create JWT payload
                  |
                  ↓
        +-------------------+
        | user_id: 101      |
        | exp: future time  |
        +-------------------+
                  |
                  ↓
          HS256 + SECRET_KEY
                  |
                  ↓
                JWT
                  |
                  ↓
               CLIENT
                  |
                  |
       Authorization: Bearer JWT
                  |
                  ↓
          PROTECTED ENDPOINT
                  |
                  ↓
       OAuth2PasswordBearer
                  |
                  ↓
          extract JWT
                  |
                  ↓
            jwt.decode()
                  |
                  ↓
       verify signature + expiry
                  |
                  ↓
        payload["user_id"]
                  |
                  ↓
          authenticated user
                  |
                  ↓
          execute endpoint
```

---

# 66. Quick Interview Revision

### What is JWT?

A compact token format consisting of:

```text
Header.Payload.Signature
```

used to carry claims between parties.

### What is HS256?

```text
HMAC-SHA256
```

a symmetric JWT signing algorithm.

### What is the secret key?

The secret used to generate and verify the HS256 signature.

### What is the payload?

The data/claims inside the JWT.

Example:

```json
{
    "user_id": 101,
    "exp": 123456789
}
```

### Why `algorithm` during encode?

Because you're specifying the algorithm used to create the token:

```python
algorithm="HS256"
```

### Why `algorithms` during decode?

Because the decoder receives a list of algorithms it is allowed to accept:

```python
algorithms=["HS256"]
```

### Is it mixing algorithms?

No.

It is an allow-list.

### Why is `user_id` used?

It identifies which user the token represents.

It's an application-chosen payload key.

### Does JWT require `user_id`?

No.

You could use:

```python
"sub"
```

or another claim.

### Why does login not require a token?

Because login is what gives the client the token in the first place.

### What does `OAuth2PasswordBearer` do?

It extracts the Bearer token from the request and integrates with FastAPI's OAuth2 security scheme.

### What does `Depends()` do?

It tells FastAPI to resolve and inject a dependency.

### Why did `ResponseValidationError` happen?

Your response model expected one user, but `fetchall()` returned a list.

Use:

```python
response_model=list[UserResponse]
```

for a list.

### Why did `ImportError: partially initialized module` happen?

Circular import:

```text
main.py → auth.py → main.py
```

Use `APIRouter` and `include_router()`.

### Why did `422` happen?

The request didn't match the Pydantic model.

For example:

```text
Expected: emai
Received: email
```

### Why did `500` happen?

An unhandled exception occurred inside the application.

### Why use `raise HTTPException`?

Because `HTTPException` is an exception that FastAPI should handle.

Use:

```python
raise HTTPException(...)
```

not:

```python
return HTTPException(...)
```

---

# 67. The Core 10-Line Concept

If you remember only one piece of the entire topic, remember this:

```text
1. User registers
       ↓
2. Password is hashed
       ↓
3. Hash stored in DB
       ↓
4. User logs in
       ↓
5. Find user by email
       ↓
6. Verify password against hash
       ↓
7. Create JWT
       ↓
8. JWT contains user_id + exp
       ↓
9. Client sends Bearer JWT
       ↓
10. Server decodes/verifies JWT before protected endpoints
```

And the JWT itself:

```text
HEADER
  |
  | alg = HS256
  ↓
PAYLOAD
  |
  | user_id
  | exp
  ↓
SIGNATURE
  |
  | HMAC-SHA256
  | +
  | SECRET_KEY
  ↓
VALID JWT
```

This covers the main concepts and the specific errors you worked through, including **HS256, JWT encoding/decoding, `algorithm` vs `algorithms`, payload/user IDs, `exp`, OAuth2 Bearer tokens, `Depends`, routers, circular imports, Pydantic validation, PostgreSQL, bcrypt, 401/403/404/409/422/500, and the complete login → JWT → protected endpoint flow**.

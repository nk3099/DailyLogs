````md
# FastAPI + Pydantic + BaseModel + Request/Response Schemas — Complete Summary

## 1. Pydantic

**Pydantic** is a Python library used to:

- Define the structure of data
- Validate data
- Convert/parse data into the expected types
- Serialize data
- Create schemas/models that FastAPI can use

Example:

```python
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
````

Here:

* `BaseModel` comes from Pydantic
* `UserResponse` is our custom Pydantic model
* `id: int` means `id` should be an integer
* `email: EmailStr` means `email` should be a valid email
* `name: str` means `name` should be a string

---

# 2. `BaseModel`

`BaseModel` is a class provided by Pydantic.

When we write:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
```

we are using **class inheritance**.

```text
UserResponse
      |
      | inherits from
      ↓
BaseModel
```

Therefore:

> `UserResponse` is a subclass/child class of Pydantic's `BaseModel`.

`BaseModel` provides Pydantic functionality such as:

* Validation
* Parsing
* Serialization
* Model creation
* `model_dump()`
* Integration with FastAPI

Without `BaseModel`:

```python
class UserResponse:
    id: int
    email: str
```

this is just a normal Python class with type annotations.

With:

```python
class UserResponse(BaseModel):
```

it becomes a Pydantic model.

---

# 3. Class Inheritance

General Python inheritance looks like:

```python
class Animal:
    pass

class Dog(Animal):
    pass
```

Here:

```text
Dog
 ↓
inherits from
 ↓
Animal
```

The same concept applies to Pydantic:

```python
class UserResponse(BaseModel):
    id: int
    email: str
```

```text
UserResponse
      ↓
inherits from
      ↓
BaseModel
```

So when you see:

```python
class Something(BaseModel):
```

you should recognize:

> This is class inheritance.

---

# 4. Pydantic Model / Schema

A class that inherits from `BaseModel` is commonly used as a **Pydantic model/schema**.

Example:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
```

This defines the expected structure:

```text
UserResponse
├── id       → int
├── email    → EmailStr
└── name     → str
```

It does NOT query the database.

It defines the **shape and rules of the data**.

---

# 5. Defining Fields — No Commas

Inside a Pydantic model, fields are written on separate lines:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
```

You do NOT normally write:

```python
class UserResponse(BaseModel):
    id: int,
    email: EmailStr,
    name: str,
```

The colon means:

```text
field_name : field_type
```

For example:

```python
id: int
```

means:

> `id` is a field whose expected type is `int`.

---

# 6. Creating an Object — Commas Are Used

When creating an instance of the Pydantic model, commas separate arguments:

```python
user = UserResponse(
    id=102,
    email="neeraj@gmail.com",
    name="neeraj"
)
```

So:

### Defining fields

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
```

No commas.

### Creating an object

```python
UserResponse(
    id=102,
    email="neeraj@gmail.com"
)
```

Commas are used.

---

# 7. `response_model`

FastAPI allows us to specify an expected response model:

```python
@app.get(
    "/users/{id}",
    response_model=UserResponse
)
```

This means:

> Use `UserResponse` as the expected schema/format for the response of this endpoint.

Important:

```python
response_model=UserResponse
```

is NOT class inheritance.

The inheritance happened here:

```python
class UserResponse(BaseModel):
```

`response_model=UserResponse` simply tells FastAPI to use that Pydantic model for the endpoint's response.

---

# 8. Response Model Flow

Suppose PostgreSQL returns:

```python
user = {
    "id": 102,
    "email": "neeraj@gmail.com",
    "name": "neeraj"
}
```

And your endpoint is:

```python
@app.get(
    "/users/{id}",
    response_model=UserResponse
)
async def get_user(id: int):
    return user
```

The flow is approximately:

```text
PostgreSQL
     ↓
Python dictionary
     ↓
return user
     ↓
FastAPI
     ↓
UserResponse
     ↓
Pydantic validation/serialization
     ↓
JSON response
```

The client receives JSON:

```json
{
    "id": 102,
    "email": "neeraj@gmail.com",
    "name": "neeraj"
}
```

So don't think:

> "The client receives a Python Pydantic object."

Instead:

> FastAPI uses the Pydantic model to validate/serialize/document the response, and the client receives JSON.

---

# 9. Response Model Controls the Response Structure

Suppose your database contains:

```python
{
    "id": 102,
    "email": "neeraj@gmail.com",
    "name": "neeraj",
    "password": "hashed_password",
    "created_at": "2026-08-25"
}
```

But your response model is:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
```

The response schema defines what your API is expected to expose.

This is one reason response models are useful.

## Important

Do NOT normally include a user's password in a response model.

Bad:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    password: str
```

Better:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
```

Passwords should generally be stored hashed and should not be returned to API clients.

---

# 10. Path Parameters

Example:

```python
@app.get("/posts/{id}")
def get_post(id: int):
    ...
```

Here:

```text
/posts/{id}
```

means `id` is a **path parameter**.

Request:

```text
GET /posts/10
```

The `10` comes from the URL.

URLs are text, so the path value is initially represented as URL text.

Conceptually:

```text
URL
 ↓
/posts/10
 ↓
"10"
 ↓
FastAPI sees:
id: int
 ↓
validates/converts
 ↓
10
```

Therefore:

```python
def get_post(id: int):
```

means:

> FastAPI should validate the path parameter as an integer and provide it to the function as an `int`.

You generally do NOT need:

```python
find_post(int(id))
```

because:

```python
id: int
```

already tells FastAPI to handle the conversion/validation.

---

# 11. Invalid Path Parameter

If the endpoint is:

```python
@app.get("/posts/{id}")
def get_post(id: int):
    ...
```

and the client sends:

```text
GET /posts/abc
```

FastAPI sees:

```text
"abc"
```

and tries to validate it as:

```python
int
```

It cannot do that.

Therefore FastAPI rejects the request before your function executes.

Conceptually:

```text
GET /posts/abc
       ↓
"abc"
       ↓
id: int ?
       ↓
Validation fails
       ↓
422 validation error
```

---

# 12. Request/Input Schema

For input, we can create another Pydantic model.

Example:

```python
from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    email: EmailStr
    password: str
```

Then:

```python
@app.post("/users")
async def create_user(user: CreateUser):
    print(user)
    print(user.email)
    print(user.password)
```

Here:

```python
user: CreateUser
```

is the **input/request schema**.

FastAPI understands:

> The request body should be validated using `CreateUser`.

---

# 13. Where Does the Input Data Come From?

The client sends JSON.

For example:

```http
POST /users
```

Request body:

```json
{
    "email": "neeraj@gmail.com",
    "password": "neeraj123"
}
```

FastAPI receives this JSON and uses:

```python
class CreateUser(BaseModel):
    email: EmailStr
    password: str
```

to validate it.

Flow:

```text
Client
  ↓
POST /users
  ↓
JSON request body
  ↓
FastAPI
  ↓
CreateUser Pydantic model
  ↓
Validation
  ↓
user
  ↓
your function
```

Inside the function:

```python
user.email
```

gives:

```text
neeraj@gmail.com
```

and:

```python
user.password
```

gives:

```text
neeraj123
```

---

# 14. Input vs Output Schemas

This is an important FastAPI concept.

You can have:

```python
class CreateUser(BaseModel):
    email: EmailStr
    password: str
```

for input.

And:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
```

for output.

Then:

```python
@app.post(
    "/users",
    response_model=UserResponse
)
async def create_user(user: CreateUser):
    ...
```

Now:

```text
                    POST /users
                         ↓
               ┌─────────────────┐
               │ Request JSON    │
               │                 │
               │ email           │
               │ password        │
               └────────┬────────┘
                        ↓
                 CreateUser
                 (input schema)
                        ↓
                  Your function
                        ↓
                    Database
                        ↓
                     return
                        ↓
                UserResponse
                (output schema)
                        ↓
                   JSON response
```

---

# 15. Why Separate CreateUser and UserResponse?

Because the fields you accept don't necessarily equal the fields you return.

For example, when creating a user:

```json
{
    "email": "neeraj@gmail.com",
    "password": "neeraj123"
}
```

You need the password as input.

But you should not return:

```json
{
    "id": 102,
    "email": "neeraj@gmail.com",
    "password": "neeraj123"
}
```

Instead:

```json
{
    "id": 102,
    "email": "neeraj@gmail.com",
    "name": "neeraj"
}
```

Therefore:

```text
CreateUser
    ↓
INPUT

UserResponse
    ↓
OUTPUT
```

---

# 16. `HTTPException`

Suppose you query the database:

```python
cursor.execute(
    "SELECT * FROM users WHERE id=%s",
    (id,)
)

user = cursor.fetchone()
```

If the user doesn't exist:

```python
user = None
```

If you simply do:

```python
return user
```

FastAPI can return:

```json
null
```

with a successful response.

For a GET `/users/{id}`, it is usually better to explicitly return a 404.

```python
from fastapi import HTTPException

if user is None:
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
```

Response:

```text
404 Not Found
```

```json
{
    "detail": "User not found"
}
```

---

# 17. `status_code` in the Decorator

You can specify a normal/success status code in the route decorator:

```python
@app.get(
    "/users/{id}",
    response_model=UserResponse,
    status_code=200
)
```

This means:

> When the endpoint successfully returns, use HTTP status code 200.

But for GET:

```python
status_code=200
```

is normally unnecessary because `200` is already the default successful response.

You could simply write:

```python
@app.get(
    "/users/{id}",
    response_model=UserResponse
)
```

---

# 18. `status_code` vs `HTTPException`

They serve different purposes.

| `status_code` in decorator          | `HTTPException`                           |
| ----------------------------------- | ----------------------------------------- |
| Configures normal endpoint response | Handles an error condition                |
| Endpoint configuration              | Runtime decision                          |
| Commonly `200`, `201`               | Commonly `400`, `401`, `403`, `404`, etc. |
| Doesn't stop the function           | `raise` stops the function                |

Example:

```python
@app.post("/users", status_code=201)
```

means:

> Successful user creation returns `201 Created`.

While:

```python
raise HTTPException(
    status_code=404,
    detail="User not found"
)
```

means:

> Something happened during execution and the requested resource was not found.

---

# 19. `Response` vs `HTTPException`

Another way to set a status code is to receive FastAPI's `Response` object:

```python
from fastapi import Response, status

@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)

    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND

        return {
            "message": f"Post with id {id} not found"
        }

    return {
        "post_detail": post
    }
```

Here:

```python
response.status_code = 404
```

means:

> Modify the HTTP response that FastAPI is going to send.

You still return a normal dictionary.

---

# 20. `Response` vs `HTTPException`

### Using `Response`

```python
if not post:
    response.status_code = 404

    return {
        "message": "Post not found"
    }
```

Flow:

```text
No post
   ↓
modify Response status
   ↓
return dictionary
   ↓
404 response
```

### Using `HTTPException`

```python
if not post:
    raise HTTPException(
        status_code=404,
        detail="Post not found"
    )
```

Flow:

```text
No post
   ↓
raise exception
   ↓
function stops
   ↓
FastAPI creates error response
   ↓
404
```

For normal API errors, `HTTPException` is generally cleaner.

---

# 21. `@app.get()` vs Function Parameters

Consider:

```python
@app.get(
    "/users/{id}",
    response_model=UserResponse
)
async def get_user(
    id: int,
    db=Depends(database.get_db)
):
    ...
```

The decorator configures the endpoint:

```text
@app.get()
    ↓
URL
response_model
status_code
etc.
```

The function parameters represent inputs/dependencies:

```text
async def get_user()
        ↓
id
db
```

So:

```python
response_model=UserResponse
```

belongs in the decorator.

While:

```python
id: int
db=Depends(...)
```

belongs in the function.

---

# 22. `response_model` Is Not Inheritance

This:

```python
@app.get(
    "/users/{id}",
    response_model=UserResponse
)
```

is NOT inheritance.

Inheritance happens here:

```python
class UserResponse(BaseModel):
```

The relationship is:

```text
UserResponse
     ↓
inherits from
     ↓
BaseModel
```

Then:

```python
response_model=UserResponse
```

means:

> FastAPI should use that Pydantic model as the expected response schema.

---

# 23. Model Validator

Suppose you want:

```text
email = "neeraj@gmail.com"
name  = "neeraj"
```

and you want to create `name` automatically from `email`.

You can use a Pydantic model validator:

```python
from pydantic import BaseModel, EmailStr, model_validator

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    password: str
    name: str

    @model_validator(mode="before")
    @classmethod
    def set_name(cls, data):

        if isinstance(data, dict) and "email" in data:
            data["name"] = str(data["email"]).split("@")[0]

        return data
```

---

# 24. `@model_validator(mode="before")`

This means:

> Run this validator before Pydantic performs the normal model validation.

Flow:

```text
Input data
    ↓
model_validator(mode="before")
    ↓
modify data
    ↓
Pydantic validation
    ↓
UserResponse
```

---

# 25. Where Does `data` Come From?

Suppose PostgreSQL returns:

```python
{
    "id": 102,
    "email": "neeraj@gmail.com",
    "password": "abc123"
}
```

That data goes through the response model.

Conceptually:

```text
PostgreSQL
    ↓
user dictionary
    ↓
Pydantic
    ↓
model_validator
```

The validator receives:

```python
data = {
    "id": 102,
    "email": "neeraj@gmail.com",
    "password": "abc123"
}
```

---

# 26. `isinstance(data, dict)`

This:

```python
isinstance(data, dict)
```

checks:

> Is `data` a Python dictionary?

Example:

```python
data = {
    "id": 102,
    "email": "neeraj@gmail.com"
}
```

Then:

```python
isinstance(data, dict)
```

returns:

```text
True
```

---

# 27. `"email" in data`

This:

```python
"email" in data
```

checks whether the dictionary contains an `email` key.

For:

```python
data = {
    "id": 102,
    "email": "neeraj@gmail.com"
}
```

the result is:

```text
True
```

Therefore:

```python
if isinstance(data, dict) and "email" in data:
```

means:

> If the input is a dictionary AND it contains an email field, execute the following code.

---

# 28. `data["email"]`

This gets the value of the email key:

```python
data["email"]
```

Given:

```python
data = {
    "email": "neeraj@gmail.com"
}
```

we get:

```text
neeraj@gmail.com
```

---

# 29. `.split("@")[0]`

This:

```python
str(data["email"]).split("@")[0]
```

works like this:

```text
"neeraj@gmail.com"
        ↓
split("@")
        ↓
["neeraj", "gmail.com"]
        ↓
[0]
        ↓
"neeraj"
```

Then:

```python
data["name"] = "neeraj"
```

So the original data:

```python
{
    "id": 102,
    "email": "neeraj@gmail.com",
    "password": "abc123"
}
```

becomes:

```python
{
    "id": 102,
    "email": "neeraj@gmail.com",
    "password": "abc123",
    "name": "neeraj"
}
```

---

# 30. Why `name: email.split("@")[0]` Does NOT Work

This is wrong:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: email.split("@")[0]
```

Because in a class:

```python
name: something
```

means:

```text
name → field
something → expected type
```

So Python tries to interpret:

```python
email.split("@")[0]
```

as a type.

But `email` isn't a variable available there.

Therefore you get:

```text
NameError: name 'email' is not defined
```

Correct:

```python
name: str
```

and then calculate the value separately using a validator or another mechanism.

---

# 31. PostgreSQL GET by ID

Instead of an in-memory list:

```python
userList = [
    {"id": 1, "email": "neeraj@gmail.com"},
    {"id": 2, "email": "nitin@gmail.com"}
]
```

you can query PostgreSQL:

```python
@app.get(
    "/users/{id}",
    response_model=schemas.UserResponse
)
async def get_user(
    id: int,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (id,)
    )

    user = cursor.fetchone()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
```

Flow:

```text
GET /users/102
       ↓
id = 102
       ↓
database.get_db()
       ↓
PostgreSQL
       ↓
SELECT * FROM users WHERE id = 102
       ↓
fetchone()
       ↓
User found?
   ↓          ↓
 YES          NO
 ↓             ↓
return       HTTPException
user            ↓
 ↓            404
UserResponse
 ↓
JSON
```

---

# 32. Why `fetchone()` Can Return `None`

This:

```python
user = cursor.fetchone()
```

returns:

### User exists

```python
{
    "id": 102,
    "email": "neeraj@gmail.com"
}
```

### User doesn't exist

```python
None
```

If you simply do:

```python
return user
```

then:

```python
None
```

becomes:

```json
null
```

Therefore, for a specific resource:

```python
if user is None:
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
```

is usually better.

---

# 33. PostgreSQL POST — Old vs New

## Old in-memory version

```python
@app.post("/users")
async def create_user(email: EmailStr, password: str):

    random_id = random.randint(1, 1000)

    userList.append({
        "id": random_id,
        "email": email,
        "password": password
    })

    return {
        "User": email.split("@")[0],
        "has been created with": email,
        "and id": random_id
    }
```

Here:

```text
random_id
    ↓
Python userList
    ↓
data exists only in application memory
```

---

# 34. PostgreSQL POST

If PostgreSQL generates the ID:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

then you do NOT need:

```python
random_id = random.randint(1, 1000)
```

PostgreSQL generates the ID.

Python:

```python
@app.post("/users")
async def create_user(
    email: EmailStr,
    password: str,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO users (email, password)
        VALUES (%s, %s)
        RETURNING id, email
        """,
        (email, password)
    )

    user = cursor.fetchone()

    db.commit()

    return {
        "User": str(user["email"]).split("@")[0],
        "has been created with": user["email"],
        "and id": user["id"]
    }
```

---

# 35. Where Does the ID Come From?

There is no random ID in this PostgreSQL version.

You send:

```text
email
password
```

to PostgreSQL.

PostgreSQL generates:

```text
id = 103
```

because the column is configured to generate IDs.

Then:

```sql
RETURNING id, email
```

asks PostgreSQL to return the generated ID.

Flow:

```text
POST /users
     ↓
email + password
     ↓
INSERT INTO users
     ↓
PostgreSQL generates ID
     ↓
id = 103
     ↓
RETURNING id, email
     ↓
Python receives:
{
    "id": 103,
    "email": "..."
}
```

This is preferable to:

```python
random.randint(1, 1000)
```

because random IDs can collide with existing IDs.

---

# 36. Complete Input + Output Example

A clean FastAPI structure can look like:

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()


# INPUT SCHEMA
class CreateUser(BaseModel):
    email: EmailStr
    password: str


# OUTPUT SCHEMA
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
async def create_user(
    user: CreateUser,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO users (email, password)
        VALUES (%s, %s)
        RETURNING id, email
        """,
        (user.email, user.password)
    )

    created_user = cursor.fetchone()

    db.commit()

    return {
        "id": created_user["id"],
        "email": created_user["email"],
        "name": str(created_user["email"]).split("@")[0]
    }


@app.get(
    "/users/{id}",
    response_model=UserResponse
)
async def get_user(
    id: int,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        "SELECT id, email FROM users WHERE id=%s",
        (id,)
    )

    user = cursor.fetchone()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user["id"],
        "email": user["email"],
        "name": str(user["email"]).split("@")[0]
    }
```

---

# 37. The Big Picture

The main concepts can be remembered like this:

```text
                    PYDANTIC
                       │
                       ↓
                  BaseModel
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        CreateUser          UserResponse
             │                   │
             ↓                   ↓
       INPUT SCHEMA        OUTPUT SCHEMA
             │                   │
             ↓                   ↑
        Request JSON        Return data
             │                   │
             ↓                   │
          FastAPI                │
             │                   │
             ↓                   │
          Function ──────────────┘
             │
             ↓
         PostgreSQL
```

## The most important rules

```text
1. Pydantic
   → Python library for data validation/models.

2. BaseModel
   → Pydantic base class.

3. class UserResponse(BaseModel)
   → Class inheritance.

4. response_model=UserResponse
   → Use UserResponse as the expected API response schema.

5. user: CreateUser
   → Use CreateUser as the request/input schema.

6. Path parameter:
   /users/{id}
   → value comes from URL.

7. id: int
   → FastAPI validates/converts the path value to int.

8. status_code=200
   → Normal/success response configuration.

9. HTTPException(404)
   → Runtime error response.

10. fetchone()
    → Returns a row if found, otherwise None.

11. return None
    → Can become JSON null.

12. raise HTTPException(404)
    → Explicit "resource not found" response.

13. PostgreSQL SERIAL/identity ID
    → Database generates the ID.

14. response schema
    → Should generally NOT expose passwords.

15. Input and output models
    → Should often be separate.
```

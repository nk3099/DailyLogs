````md
# FastAPI — Complete Notes: Decorators, Routes, Pydantic, Dependency Injection & Database

---

# 1. Creating a FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI()
````

`FastAPI()` creates an instance/object of the `FastAPI` class.

Conceptually:

```text
FastAPI class
      ↓
  FastAPI()
      ↓
   app object
```

The `app` object manages:

* Routes
* HTTP methods
* Requests
* Responses
* Dependencies
* API documentation

So:

```python
app = FastAPI()
```

means:

> Create a FastAPI application object and store it in `app`.

---

# 2. What Is a Route?

A route maps an HTTP request to a Python function.

Example:

```python
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

This creates the relationship:

```text
GET /
 ↓
root()
```

So when the client sends:

```http
GET /
```

FastAPI knows that it should execute:

```python
root()
```

---

# 3. What Is `app.get()`?

```python
app.get("/")
```

`get()` is a method of the FastAPI application object.

It is used to register a GET route.

Example:

```python
@app.get("/users")
async def get_users():
    return {"message": "Users"}
```

This tells FastAPI:

```text
GET /users
     ↓
get_users()
```

---

# 4. FastAPI Does Something Similar Internally

To understand how:

```python
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

works, imagine FastAPI's `app.get()` as something conceptually similar to:

```python
def get(path):

    def decorator(func):

        # Register the route
        # GET path → func

        return func

    return decorator
```

This is a **simplified model** to understand the concept.

FastAPI's actual implementation is much more complex, but the important idea is similar.

---

# 5. What Does `app.get("/")` Return?

When we write:

```python
app.get("/")
```

it does not directly receive `root`.

Instead, conceptually:

```python
app.get("/")
```

returns a **decorator function**.

Think:

```text
app.get("/")
     ↓
returns decorator
```

Then that decorator receives the function.

---

# 6. What Is a Decorator?

A decorator is a function that receives another function and modifies, registers, or wraps it.

Example:

```python
def my_decorator(func):

    print("Function received:", func)

    return func
```

Then:

```python
@my_decorator
def hello():
    print("Hello")
```

is conceptually equivalent to:

```python
def hello():
    print("Hello")

hello = my_decorator(hello)
```

So:

```text
my_decorator
      ↓
receives hello
      ↓
returns hello
```

---

# 7. How `@app.get("/")` Works

This:

```python
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

is conceptually similar to:

```python
def root():
    return {"message": "Hello World"}

decorator = app.get("/")

root = decorator(root)
```

Or more compactly:

```python
root = app.get("/")(root)
```

The flow is:

```text
app.get("/")
     ↓
returns decorator
     ↓
decorator(root)
     ↓
FastAPI registers:
GET / → root
     ↓
returns root
```

---

# 8. Why Does the Decorator Return the Function?

Our simplified decorator:

```python
def decorator(func):

    # Register route

    return func
```

receives the function:

```python
func = root
```

It registers the route:

```text
GET / → root
```

and returns the function:

```python
return func
```

So the function remains available.

---

# 9. General Decorator Rule

Whenever you see:

```python
@something
def function():
    ...
```

remember:

```python
function = something(function)
```

For FastAPI:

```python
@app.get("/")
def root():
    ...
```

conceptually becomes:

```python
root = app.get("/")(root)
```

because:

```python
app.get("/")
```

first returns a decorator.

Then:

```python
decorator(root)
```

receives the function.

---

# 10. Route Registration vs Request Handling

These are two different things.

## Step 1 — Route Registration

When the application starts:

```python
@app.get("/")
async def root():
    ...
```

FastAPI registers:

```text
GET / → root
```

## Step 2 — Request Handling

Later, the client sends:

```http
GET /
```

FastAPI finds:

```text
GET / → root
```

and executes:

```python
root()
```

Complete flow:

```text
Application starts
      ↓
@app.get("/")
      ↓
Register GET / → root
      ↓
Application is ready
      ↓
Client sends GET /
      ↓
FastAPI finds root
      ↓
root()
      ↓
Response
```

---

# 11. Path Parameters

Example:

```python
@app.get("/users/{id}")
async def get_user(id: int):
    return {"id": id}
```

`{id}` is a path parameter.

Request:

```text
GET /users/10
```

FastAPI extracts:

```python
id = 10
```

and conceptually calls:

```python
get_user(id=10)
```

Flow:

```text
GET /users/10
      ↓
Match /users/{id}
      ↓
Extract id = 10
      ↓
get_user(10)
```

---

# 12. Query Parameters

Example:

```python
@app.get("/users")
async def get_user(email: str):
    return {"email": email}
```

Request:

```text
GET /users?email=neeraj@gmail.com
```

FastAPI extracts:

```python
email = "neeraj@gmail.com"
```

and calls:

```python
get_user(email="neeraj@gmail.com")
```

Difference:

```text
Path parameter:

/users/10


Query parameter:

/users?email=abc@gmail.com
```

---

# 13. POST Request

Example:

```python
@app.post("/users")
async def create_user(email: str, password: str):
    return {
        "email": email
    }
```

If `email` and `password` are normal function parameters, FastAPI treats them as query parameters by default.

So Swagger may show:

```text
email     (query)
password  (query)
```

and the request may look like:

```text
POST /users?email=abc@gmail.com&password=abc123
```

---

# 14. Pydantic `BaseModel`

Instead of sending fields as query parameters, we can define a request body.

```python
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    email: EmailStr
    password: str
```

Here:

```python
class UserCreate(BaseModel):
```

means:

> `UserCreate` inherits from `BaseModel`.

Conceptually:

```text
BaseModel
    ↑
    |
UserCreate
```

`UserCreate` gets functionality from Pydantic's `BaseModel`.

It provides things such as:

* Data validation
* Data parsing
* Type checking
* Serialization

---

# 15. Creating a Pydantic Object

Normally in Python:

```python
user = UserCreate(
    email="neeraj@gmail.com",
    password="abc123"
)
```

Now:

```python
user
```

is an object/instance of `UserCreate`.

Therefore:

```python
user.email
```

works.

And:

```python
user.password
```

works.

---

# 16. Why Does `user.email` Work in FastAPI?

Suppose:

```python
@app.post("/users")
async def create_user(user: UserCreate):

    return {
        "email": user.email
    }
```

You might wonder:

> Where did `user = UserCreate(...)` happen?

You did not explicitly create it.

FastAPI + Pydantic handle this for you.

Suppose the client sends:

```json
{
    "email": "neeraj@gmail.com",
    "password": "abc123"
}
```

Conceptually, FastAPI/Pydantic does something similar to:

```python
user = UserCreate(
    email="neeraj@gmail.com",
    password="abc123"
)
```

Then:

```python
create_user(user)
```

So:

```text
JSON request
     ↓
Pydantic validation
     ↓
UserCreate object
     ↓
user
     ↓
user.email
```

---

# 17. Type Annotation vs Object Creation

This:

```python
def create_user(user: UserCreate):
```

does NOT itself manually create an object.

`user: UserCreate` means:

> The `user` parameter is expected to contain a `UserCreate` object.

FastAPI creates/populates that object from the incoming request body.

Conceptually:

```python
user = UserCreate(...)
```

is created as part of FastAPI's request processing.

Then your function receives it.

---

# 18. Dependency Injection

Dependency Injection means:

> A function receives something it needs from an external provider instead of creating that thing itself.

Example without Dependency Injection:

```python
def create_user():

    conn = create_database_connection()

    ...
```

Here `create_user()` creates its own database connection.

The database connection is a dependency.

---

# 19. Dependency Injection in Simple Python

Without FastAPI:

```python
def get_database():

    return "database connection"


def create_user(conn):

    print(conn)


conn = get_database()

create_user(conn)
```

Flow:

```text
get_database()
      ↓
connection
      ↓
create_user(conn)
```

`create_user()` did not create the connection.

Someone else provided it.

That is the basic idea of Dependency Injection.

---

# 20. FastAPI `Depends()`

FastAPI provides:

```python
from fastapi import Depends
```

Example:

```python
def get_db():
    ...


@app.get("/users")
def get_users(conn=Depends(get_db)):
    ...
```

This tells FastAPI:

> `conn` depends on `get_db`. Resolve `get_db` and provide its result to `conn`.

---

# 21. What Is `Depends()`?

```python
conn = Depends(get_db)
```

means:

```text
conn
 ↓
depends on
 ↓
get_db
```

FastAPI sees the dependency and manages it.

---

# 22. Why `Depends(get_db)` Instead of `get_db()`?

We write:

```python
Depends(get_db)
```

not:

```python
Depends(get_db())
```

because we are passing the function itself.

Compare:

```python
get_db
```

means:

> The function itself.

Whereas:

```python
get_db()
```

means:

> Call the function now.

So:

```python
Depends(get_db)
```

means:

> FastAPI, here is the dependency function. You manage when it should be called.

---

# 23. What Is `get_db()`?

Example:

```python
import psycopg2


def get_db():

    conn = psycopg2.connect(
        host="localhost",
        dbname="fastapiAug",
        user="postgres",
        password="YOUR_PASSWORD",
        port=5432
    )

    try:
        yield conn

    finally:
        conn.close()
```

`get_db()` is a dependency provider.

Its job is:

```text
Create DB connection
       ↓
Provide connection
       ↓
Endpoint uses connection
       ↓
Close connection
```

---

# 24. Why Create `get_db()`?

Without `get_db()`:

```python
@app.get("/users")
def get_users():

    conn = psycopg2.connect(...)
    ...
```

Another endpoint:

```python
@app.post("/users")
def create_user():

    conn = psycopg2.connect(...)
    ...
```

Another:

```python
@app.delete("/users/{id}")
def delete_user(id: int):

    conn = psycopg2.connect(...)
    ...
```

We repeat the database connection code.

Instead, centralize it:

```python
def get_db():
    ...
```

Then reuse it:

```python
conn=Depends(get_db)
```

---

# 25. Why Is Dependency Injection Better?

Without Dependency Injection:

```text
GET users
   ↓
Create DB connection


POST users
   ↓
Create DB connection


DELETE users
   ↓
Create DB connection
```

With Dependency Injection:

```text
                 get_db()
                    ↑
          ┌─────────┼─────────┐
          │         │         │
          ↓         ↓         ↓
       GET users POST users DELETE user
```

The connection logic is centralized.

---

# 26. `yield` in `get_db()`

Example:

```python
def get_db():

    conn = psycopg2.connect(...)

    try:
        yield conn

    finally:
        conn.close()
```

`yield` allows the dependency to:

1. Create a resource
2. Give it to the endpoint
3. Allow the endpoint to use it
4. Perform cleanup afterward

Flow:

```text
get_db()
   ↓
Create connection
   ↓
yield connection
   ↓
Endpoint uses connection
   ↓
Endpoint finishes
   ↓
finally executes
   ↓
conn.close()
```

---

# 27. `return` vs `yield`

With:

```python
def get_db():

    conn = create_connection()

    return conn
```

the function simply returns the connection.

With:

```python
def get_db():

    conn = create_connection()

    try:
        yield conn

    finally:
        conn.close()
```

there is a cleanup phase.

Think:

```text
return:

create
  ↓
give
  ↓
DONE
```

Whereas:

```text
yield:

create
  ↓
give
  ↓
endpoint uses it
  ↓
come back
  ↓
cleanup
```

This is why `yield` is useful for database dependencies.

---

# 28. Complete Dependency Injection Flow

Suppose:

```python
@app.get("/users")
def get_users(conn=Depends(get_db)):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users"
    )

    return cursor.fetchall()
```

Client sends:

```text
GET /users
```

FastAPI conceptually does:

```text
1. Match GET /users
        ↓
2. Find get_users()
        ↓
3. See Depends(get_db)
        ↓
4. Execute get_db()
        ↓
5. Create DB connection
        ↓
6. Provide connection
        ↓
7. Call get_users(conn)
        ↓
8. Execute SQL
        ↓
9. Return response
        ↓
10. Cleanup dependency
        ↓
11. conn.close()
```

---

# 29. Does `get_db()` Run for Every Endpoint?

Not every endpoint automatically.

It runs when an endpoint uses it as a dependency.

Example:

```python
@app.get("/")
def root():
    return {"message": "Hello"}
```

This endpoint does NOT use:

```python
Depends(get_db)
```

Therefore, `get_db()` does not need to run for this endpoint.

But:

```python
@app.get("/users")
def get_users(conn=Depends(get_db)):
    ...
```

does use the dependency.

---

# 30. Does `get_db()` Run for Every Request?

For an endpoint that declares:

```python
conn=Depends(get_db)
```

FastAPI resolves that dependency for the request.

For example:

```text
Request 1
   ↓
get_db()
   ↓
connection
   ↓
get_users()
   ↓
cleanup


Request 2
   ↓
get_db()
   ↓
connection
   ↓
get_users()
   ↓
cleanup
```

This does NOT mean `get_db()` is a Singleton.

---

# 31. Dependency Injection vs Singleton

These are different concepts.

## Dependency Injection

Question:

> Who provides the dependency?

```python
conn=Depends(get_db)
```

Answer:

> FastAPI's dependency system gets it from `get_db`.

Purpose:

```text
Provide required resources to functions.
```

---

## Singleton

Question:

> How many instances of this class should exist?

Answer:

```text
One instance.
```

Purpose:

```text
Ensure one shared object exists.
```

---

# 32. Singleton Pattern

Example:

```python
class Database:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance
```

Now:

```python
db1 = Database()
db2 = Database()
```

Check:

```python
print(db1 is db2)
```

Output:

```text
True
```

Both variables refer to the same object.

---

# 33. Understanding `__new__`

Normally:

```python
db = Database()
```

creates an object.

`__new__()` controls object creation.

Our Singleton checks:

```python
if cls._instance is None:
```

If there is no object:

```text
None
 ↓
Create object
 ↓
Store object
```

If an object already exists:

```text
Existing object
 ↓
Return same object
```

---

# 34. Singleton Flow

First call:

```python
db1 = Database()
```

Flow:

```text
Database()
    ↓
_instance is None?
    ↓
YES
    ↓
Create object
    ↓
Store object
    ↓
Return object
```

Second call:

```python
db2 = Database()
```

Flow:

```text
Database()
    ↓
_instance is None?
    ↓
NO
    ↓
Return existing object
```

Therefore:

```python
db1 is db2
```

is:

```text
True
```

---

# 35. Singleton Does NOT Mean Function/Constructor Is Called Only Once

This is important.

You can write:

```python
Database()
Database()
Database()
Database()
```

many times.

The calls happen every time.

But the Singleton implementation ensures the same object is returned.

Therefore:

```text
Number of calls ≠ Number of objects
```

Example:

```text
Database() → Object #1
Database() → Object #1
Database() → Object #1
Database() → Object #1
```

---

# 36. `get_db()` Is Not a Singleton

This:

```python
def get_db():

    conn = psycopg2.connect(...)

    try:
        yield conn

    finally:
        conn.close()
```

is a dependency provider.

It is NOT automatically a Singleton.

Its purpose is:

```text
Create connection
      ↓
Provide connection
      ↓
Use connection
      ↓
Close connection
```

Singleton's purpose is:

```text
Database()
      ↓
Ensure one object
```

---

# 37. Singleton + Database Example

You could technically create a Singleton database object:

```python
import psycopg2


class Database:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.conn = psycopg2.connect(
                host="localhost",
                dbname="fastapiAug",
                user="postgres",
                password="YOUR_PASSWORD",
                port=5432
            )

        return cls._instance
```

Then:

```python
db1 = Database()
db2 = Database()
```

Both refer to the same `Database` object:

```python
print(db1 is db2)
```

Output:

```text
True
```

However, using a single shared database connection for an entire web application is generally not the same thing as using a proper connection pool.

---

# 38. Connection Pool

A connection pool manages multiple reusable database connections.

Conceptually:

```text
Connection Pool

┌─────────────────┐
│ Connection 1    │
│ Connection 2    │
│ Connection 3    │
│ Connection 4    │
└─────────────────┘
```

A request can:

```text
Request
   ↓
Borrow connection
   ↓
Execute SQL
   ↓
Return connection
   ↓
Pool
```

---

# 39. Singleton vs Connection Pool

## Singleton

```text
ONE shared object
```

```text
Request A ──┐
Request B ──┼──→ One object
Request C ──┘
```

## Connection Pool

```text
MULTIPLE reusable connections
```

```text
Request A → Connection 1
Request B → Connection 2
Request C → Connection 3
Request D → Connection 4
```

A connection pool is designed to efficiently handle multiple database requests.

---

# 40. PostgreSQL Connection With `psycopg2`

Install:

```bash
python3 -m pip install psycopg2-binary
```

Then:

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="fastapiAug",
    user="postgres",
    password="YOUR_PASSWORD",
    port=5432
)
```

`psycopg2` is a PostgreSQL adapter/driver for Python.

It allows Python to:

* Connect to PostgreSQL
* Execute SQL
* Commit transactions
* Roll back transactions
* Fetch results

---

# 41. Cursor

After connecting:

```python
cursor = conn.cursor()
```

A cursor is used to execute SQL statements.

Example:

```python
cursor.execute(
    "SELECT * FROM users"
)
```

Then:

```python
users = cursor.fetchall()
```

gets the results.

Flow:

```text
Python
  ↓
psycopg2
  ↓
Connection
  ↓
Cursor
  ↓
SQL
  ↓
PostgreSQL
```

---

# 42. `RealDictCursor`

Normally:

```python
cursor = conn.cursor()
```

results may look like:

```python
[
    (1, "neeraj@gmail.com", "abc123"),
    (2, "nitin@gmail.com", "xyz123")
]
```

These are tuples.

If using:

```python
from psycopg2.extras import RealDictCursor

cursor = conn.cursor(
    cursor_factory=RealDictCursor
)
```

results can look like:

```python
[
    {
        "id": 1,
        "email": "neeraj@gmail.com",
        "password": "abc123"
    },
    {
        "id": 2,
        "email": "nitin@gmail.com",
        "password": "xyz123"
    }
]
```

Then you can use:

```python
user["email"]
```

instead of:

```python
user[1]
```

---

# 43. Database Dependency Example

## `database.py`

```python
import psycopg2


def get_db():

    conn = psycopg2.connect(
        host="localhost",
        dbname="fastapiAug",
        user="postgres",
        password="YOUR_PASSWORD",
        port=5432
    )

    try:

        yield conn

    finally:

        conn.close()
```

---

# 44. Pydantic Schema

## `schemas.py`

```python
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    email: EmailStr
    password: str
```

---

# 45. FastAPI Endpoint

## `main.py`

```python
from fastapi import FastAPI, Depends

from database import get_db
from schemas import UserCreate


app = FastAPI()


@app.get("/")
async def root():

    return {
        "message": "Hello World"
    }


@app.get("/users")
async def get_users(
    conn=Depends(get_db)
):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users"
    )

    users = cursor.fetchall()

    return users


@app.post("/users")
async def create_user(
    user: UserCreate,
    conn=Depends(get_db)
):

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (email, password)
        VALUES (%s, %s)
        """,
        (
            user.email,
            user.password
        )
    )

    conn.commit()

    return {
        "message": "User created",
        "email": user.email
    }
```

---

# 46. Complete Architecture

```text
                         CLIENT
                           │
                           ↓
                     HTTP REQUEST
                           │
                           ↓
                        FASTAPI
                           │
                           ↓
                     ROUTE MATCHING
                           │
                           ↓
                ┌──────────────────────┐
                │ Endpoint Function    │
                │                      │
                │ get_users(...)       │
                └──────────┬───────────┘
                           │
                   Depends(get_db)
                           │
                           ↓
                        get_db()
                           │
                           ↓
                  Create DB connection
                           │
                           ↓
                       yield conn
                           │
                           ↓
                  Inject into endpoint
                           │
                           ↓
                    get_users(conn)
                           │
                           ↓
                      Execute SQL
                           │
                           ↓
                      PostgreSQL
                           │
                           ↓
                       Response
                           │
                           ↓
                  Dependency cleanup
                           │
                           ↓
                      conn.close()
```

---

# 47. Complete Mental Model

## `FastAPI()`

```python
app = FastAPI()
```

Means:

> Create the FastAPI application object.

---

## `app.get("/")`

```python
app.get("/")
```

Conceptually:

```text
app.get("/")
    ↓
returns decorator
```

---

## Decorator

```python
@app.get("/")
def root():
    ...
```

Conceptually:

```python
root = app.get("/")(root)
```

The decorator:

```text
receives root
     ↓
registers GET / → root
     ↓
returns root
```

---

## Route

```python
@app.get("/users")
```

Registers:

```text
GET /users → function
```

---

## Pydantic Model

```python
class UserCreate(BaseModel):

    email: str
    password: str
```

Defines and validates the expected request data.

---

## Pydantic Object

```python
user = UserCreate(...)
```

Creates an object.

Therefore:

```python
user.email
```

works.

In FastAPI, FastAPI/Pydantic create/populate this object from the request body.

---

## Dependency Injection

```python
conn = Depends(get_db)
```

Means:

> This endpoint needs `conn`, and FastAPI should obtain it from `get_db`.

---

## `get_db()`

```python
def get_db():
    ...
    yield conn
    ...
```

Means:

```text
Create connection
      ↓
Provide connection
      ↓
Endpoint uses connection
      ↓
Cleanup
```

---

## Singleton

```text
One object/instance
```

Purpose:

> Ensure that a class has only one instance.

---

## Connection Pool

```text
Multiple reusable DB connections
```

Purpose:

> Efficiently manage database connections for multiple requests.

---

# 48. Most Important Flows

## Route Decorator Flow

```text
@app.get("/")
      ↓
app.get("/")
      ↓
returns decorator
      ↓
decorator(root)
      ↓
register GET / → root
      ↓
return root
```

---

## Request Flow

```text
Client
  ↓
GET /
  ↓
FastAPI route matching
  ↓
root()
  ↓
Response
```

---

## Pydantic Flow

```text
JSON request
      ↓
Pydantic validation
      ↓
UserCreate object
      ↓
user.email
      ↓
Endpoint
```

---

## Dependency Injection Flow

```text
Endpoint
   ↓
Depends(get_db)
   ↓
FastAPI resolves dependency
   ↓
get_db()
   ↓
Create connection
   ↓
yield connection
   ↓
Inject into endpoint
   ↓
Endpoint uses connection
   ↓
Endpoint finishes
   ↓
finally
   ↓
conn.close()
```

---

## Singleton Flow

```text
Database()
     ↓
Does instance exist?
     ↓
   ┌───────┐
   │       │
  NO      YES
   │       │
   ↓       ↓
Create   Return
object   existing
   │       │
   └───┬───┘
       ↓
   Same object
```

---

# 49. Final Comparison

| Concept          | Main Question                               | Purpose                          |
| ---------------- | ------------------------------------------- | -------------------------------- |
| `FastAPI()`      | What is my application?                     | Creates FastAPI app              |
| `app.get()`      | What happens with GET?                      | Registers GET route              |
| `@app.get("/")`  | Which function handles `/`?                 | Connects route to function       |
| Decorator        | What function should be registered/wrapped? | Receives a function              |
| Route            | Which request goes where?                   | Maps HTTP request → function     |
| Path parameter   | What value is in the URL path?              | Extracts values like `/users/10` |
| Query parameter  | What values are in the query string?        | Extracts values like `?email=x`  |
| `BaseModel`      | What should request data look like?         | Defines/validates data           |
| `UserCreate`     | What object represents request data?        | Pydantic model                   |
| `Depends()`      | Who provides this dependency?               | Dependency Injection             |
| `get_db()`       | How do I provide the DB connection?         | DB dependency provider           |
| `yield`          | How do I provide + clean up?                | Resource lifecycle               |
| Singleton        | How many instances?                         | Ensures one instance             |
| Connection Pool  | How do I manage many connections?           | Reuses multiple DB connections   |
| `psycopg2`       | How does Python talk to PostgreSQL?         | PostgreSQL Python driver         |
| Cursor           | How do I execute SQL?                       | Executes SQL and fetches results |
| `RealDictCursor` | How do I get rows as dictionaries?          | Returns dictionary-like rows     |

---

# 50. One-Line Memory Trick

```text
FastAPI()
   ↓
creates APP

@app.get()
   ↓
registers ROUTE

Decorator
   ↓
receives FUNCTION

BaseModel
   ↓
validates REQUEST DATA

Pydantic
   ↓
creates MODEL OBJECT

Depends()
   ↓
asks FastAPI to PROVIDE DEPENDENCY

get_db()
   ↓
PROVIDES DATABASE CONNECTION

yield
   ↓
PROVIDE → USE → CLEANUP

Singleton
   ↓
ONE OBJECT

Connection Pool
   ↓
MULTIPLE REUSABLE CONNECTIONS

psycopg2
   ↓
PYTHON ↔ POSTGRESQL
```

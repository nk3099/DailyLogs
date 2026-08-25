
````md
# Python Class → Object → Method for Conn and Cursor in SQL

## 1. Class vs Object

A **class** is a blueprint/type used to create objects.

```python
class Connection:

    def cursor(self):
        print("Creating cursor")
````

Create an object:

```python
conn = Connection()
```

Here:

```text
Connection
    ↓
class/type

Connection()
    ↓
creates object

conn
    ↓
object/instance of Connection
```

So:

```python
conn = Connection()
```

means `conn` is an **object of the `Connection` class**.

---

# 2. Calling a Method on an Object

If the class has:

```python
class Connection:

    def cursor(self):
        print("Creating cursor")
```

we normally call the method through the object:

```python
conn = Connection()

conn.cursor()
```

Here:

```text
conn
 ↓
object
 ↓
.cursor()
 ↓
method executes
```

Python automatically passes `conn` as `self`.

Conceptually:

```python
conn.cursor()
```

is equivalent to:

```python
Connection.cursor(conn)
```

---

# 3. Why `self`?

Consider:

```python
class Connection:

    def cursor(self):
        print(self)
```

When we do:

```python
conn = Connection()

conn.cursor()
```

Python conceptually does:

```python
Connection.cursor(conn)
```

Therefore:

```text
self = conn
```

So:

```python
conn.cursor()
```

means:

> Call the `cursor()` method belonging to this particular `conn` object.

---

# 4. Class Method Call vs Object Method Call

These are different ways of calling the same instance method.

### Normal way

```python
conn.cursor()
```

Python automatically supplies `self`.

### Through the class

```python
Connection.cursor(conn)
```

Here we explicitly provide the object.

So:

```text
conn.cursor()
        ↓
Connection.cursor(conn)
```

The first form is the normal/recommended way.

---

# 5. Creating an Object vs Calling a Method

Do not confuse these:

```python
Connection()
```

and:

```python
Connection.cursor(conn)
```

### `Connection()`

Creates an object:

```text
Connection()
    ↓
object
    ↓
conn
```

### `Connection.cursor(conn)`

Calls a method on an existing object:

```text
Connection.cursor(conn)
        ↓
cursor() method executes
        ↓
self = conn
```

---

# 6. PostgreSQL / psycopg2 Example

With `psycopg2`:

```python
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host="localhost",
    database="fastapiAug",
    user="postgres",
    password="admin",
    port=5432,
    cursor_factory=RealDictCursor
)

cursor = conn.cursor()
```

The important part:

```python
cursor = conn.cursor()
```

means:

> Call the `cursor()` method of the `conn` object and store whatever that method returns in `cursor`.

Conceptually:

```text
psycopg2.connect(...)
        ↓
Connection object
        ↓
conn
        ↓
conn.cursor()
        ↓
Cursor object
        ↓
cursor
```

Therefore:

```text
conn
 ↓
Connection object

cursor
 ↓
Cursor object
```

---

# 7. `conn` Is an Object, Not the Class

This:

```python
conn = psycopg2.connect(...)
```

creates/returns a connection object.

So conceptually:

```text
Connection
    ↓
class/type

psycopg2.connect(...)
    ↓
Connection object

conn
    ↓
reference to that object
```

Therefore:

```python
conn.cursor()
```

is calling a method on the connection object.

You should NOT think:

```python
conn = Connection
```

because that would mean `conn` refers to the class itself.

Instead:

```python
conn = Connection()
```

means `conn` is an object.

---

# 8. Cursor Is Also an Object

This:

```python
cursor = conn.cursor()
```

returns a cursor object.

Therefore we can call methods on `cursor`:

```python
cursor.execute("SELECT * FROM users")

user = cursor.fetchone()

users = cursor.fetchall()
```

Conceptually:

```text
Connection object
       │
       │ .cursor()
       ↓
Cursor object
       │
       ├── .execute()
       ├── .fetchone()
       └── .fetchall()
```

---

# 9. Database Connection vs Cursor

### `conn`

Represents the connection/session with PostgreSQL.

```python
conn = psycopg2.connect(...)
```

### `cursor`

Used to execute SQL and retrieve query results.

```python
cursor = conn.cursor()
```

Then:

```python
cursor.execute(
    "SELECT * FROM users"
)
```

and:

```python
user = cursor.fetchone()
```

---

# 10. FastAPI Example

Now combine this with FastAPI and Pydantic.

```python
from fastapi import FastAPI, Depends
import psycopg2

app = FastAPI()


@app.post("/users")
async def create_user(
    data: schemas.UserRequest,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO users (email, password)
        VALUES (%s, %s)
        """,
        (data.email, data.password)
    )

    return {
        "message": "User created"
    }
```

Notice:

```python
data: schemas.UserRequest
```

and:

```python
db=Depends(database.get_db)
```

are two different things.

---

# 11. `data: schemas.UserRequest`

Suppose:

```python
class UserRequest(BaseModel):
    email: EmailStr
    password: str
```

Client sends:

```json
{
    "email": "neeraj@gmail.com",
    "password": "neeraj123"
}
```

FastAPI conceptually does:

```python
data = schemas.UserRequest(
    email="neeraj@gmail.com",
    password="neeraj123"
)
```

Pydantic validates it.

Then FastAPI calls your function with that object:

```python
create_user(data, db)
```

So:

```text
JSON request
     ↓
UserRequest
     ↓
Pydantic validation
     ↓
UserRequest object
     ↓
data
     ↓
create_user(data, db)
```

You can then use:

```python
data.email
data.password
```

because `data` is a Pydantic object.

---

# 12. `db=Depends(database.get_db)`

This is different.

FastAPI calls the dependency:

```python
database.get_db
```

and provides its result to:

```python
db
```

For example, your dependency may be:

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

    print("Database connection successful")

    return conn
```

Then:

```python
db=Depends(database.get_db)
```

conceptually results in:

```text
database.get_db()
       ↓
connection object
       ↓
db
```

Then:

```python
cursor = db.cursor()
```

creates a cursor from that connection.

---

# 13. Important Correction in the Example

Do NOT write:

```python
@app.post("/users")
async def create_user(
    data: schemas.UserRequest,
    db=Depends(database.get_db)
):

    conn.cursor()
```

if `conn` has not been defined inside that function.

Instead, if `get_db()` returns the connection:

```python
@app.post("/users")
async def create_user(
    data: schemas.UserRequest,
    db=Depends(database.get_db)
):

    cursor = db.cursor()
```

Because:

```text
database.get_db()
       ↓
connection object
       ↓
db
       ↓
db.cursor()
       ↓
cursor object
```

---

# 14. Full Dependency Example

### `database.py`

```python
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db():

    try:

        conn = psycopg2.connect(
            host="localhost",
            database="fastapiAug",
            user="postgres",
            password="admin",
            port=5432,
            cursor_factory=RealDictCursor
        )

        print("Database connection successful")

        return conn

    except Exception as e:

        print(
            "Database failed to connect with error as",
            e
        )
```

### `main.py`

```python
from fastapi import FastAPI, Depends

app = FastAPI()


@app.post("/users")
async def create_user(
    data: schemas.UserRequest,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO users (email, password)
        VALUES (%s, %s)
        """,
        (data.email, data.password)
    )

    return {
        "message": "User created"
    }
```

---

# 15. Complete Flow

When the client sends:

```json
{
    "email": "neeraj@gmail.com",
    "password": "neeraj123"
}
```

FastAPI does conceptually:

```text
                         HTTP REQUEST
                              │
                              ↓
                         FastAPI
                              │
              ┌───────────────┴───────────────┐
              ↓                               ↓
       data: UserRequest              Depends(get_db)
              ↓                               ↓
      Pydantic validation              get_db() executes
              ↓                               ↓
       UserRequest object              Connection object
              ↓                               ↓
            data                              db
              │                               │
              └───────────────┬───────────────┘
                              ↓
                       create_user()
                              ↓
                        db.cursor()
                              ↓
                        Cursor object
                              ↓
                     cursor.execute(...)
                              ↓
                         PostgreSQL
```

---

# 16. The Core Python Concept

The whole thing is based on normal Python:

```python
class Connection:

    def cursor(self):
        return "Cursor object"


conn = Connection()

cursor = conn.cursor()
```

Meaning:

```text
class
 ↓
object
 ↓
object.method()
 ↓
method returns something
 ↓
store returned value
```

In PostgreSQL:

```python
conn = psycopg2.connect(...)
cursor = conn.cursor()
```

is the same general concept:

```text
psycopg2
   ↓
connect()
   ↓
Connection object
   ↓
conn
   ↓
conn.cursor()
   ↓
Cursor object
   ↓
cursor
```

---

# 17. Final Cheat Sheet

```python
class Connection:
```

→ Defines a class/type.

```python
conn = Connection()
```

→ Creates an object/instance.

```python
conn.cursor()
```

→ Calls `cursor()` on that object.

Conceptually equivalent to:

```python
Connection.cursor(conn)
```

because Python automatically passes the object as `self`.

```python
cursor = conn.cursor()
```

→ Calls the method and stores its returned value in `cursor`.

```python
cursor.execute(...)
```

→ Calls a method on the cursor object.

---

# 18. FastAPI Mental Model

```python
@app.post("/users")
async def create_user(
    data: schemas.UserRequest,
    db=Depends(database.get_db)
):
```

Think:

```text
data
 ↓
Pydantic UserRequest object

db
 ↓
database connection object
```

Then:

```python
cursor = db.cursor()
```

means:

```text
db
 ↓
connection object
 ↓
.cursor()
 ↓
cursor object
```

And:

```python
cursor.execute(...)
```

means:

```text
cursor object
 ↓
execute()
 ↓
SQL sent to PostgreSQL
```

## One-line summary

```text
Pydantic:
JSON → UserRequest object → data

Database:
get_db() → Connection object → db
                         ↓
                      db.cursor()
                         ↓
                    Cursor object
                         ↓
                    cursor.execute()
                         ↓
                    PostgreSQL
```

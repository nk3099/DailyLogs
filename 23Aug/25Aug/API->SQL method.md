# FastAPI + PostgreSQL + psycopg2 — Complete Summary

## 1. Overall Architecture

### Earlier — Without SQL

Users were stored directly in a Python list:

```text
FastAPI
   ↓
Python userList
   ↓
Dictionaries
```

Example:

```python
userList = [
    {
        "id": 1,
        "name": "neeraj@gmail.com",
        "password": "neeraj123"
    },
    {
        "id": 2,
        "name": "nitin@gmail.com",
        "password": "nitin123"
    }
]
```

### Now — With PostgreSQL

Users are stored in a PostgreSQL database:

```text
FastAPI
   ↓
psycopg2
   ↓
PostgreSQL
   ↓
users table
```

---

# 2. PostgreSQL Tools

PostgreSQL has different components:

```text
PostgreSQL
│
├── PostgreSQL Server
│      └── Stores databases and tables
│
├── psql
│      └── Terminal tool for manually running SQL
│
└── psycopg2
       └── Python library/driver
           for Python → PostgreSQL
```

### Install PostgreSQL using Homebrew

```bash
brew install postgresql
```

Check `psql`:

```bash
psql --version
```

Start PostgreSQL:

```bash
brew services start postgresql
```

Connect to a database:

```bash
psql -U postgres -d fastapiAug
```

You should see:

```text
fastapiAug=#
```

Now you are inside the PostgreSQL terminal.

Run SQL:

```sql
SELECT * FROM users;
```

---

# 3. PostgreSQL Commands vs Shell Commands

When you see:

```text
fastapiAug=#
```

you are inside PostgreSQL (`psql`).

SQL commands can be executed here:

```sql
SELECT * FROM users;
```

To list databases:

```text
\l
```

or:

```text
\list
```

To list tables:

```text
\dt
```

To describe a table:

```text
\d users
```

To quit PostgreSQL:

```text
\q
```

### Important

This:

```sql
SELECT * FROM users;
```

must be executed **inside `psql`**, not directly in the normal zsh terminal.

If you type:

```bash
select * from users;
```

in zsh, you may get:

```text
zsh: parse error near `*'
```

because zsh is not PostgreSQL.

---

# 4. `psql` vs `psycopg2`

They both interact with PostgreSQL, but in different ways.

### `psql`

Used manually from the terminal:

```bash
psql -U postgres -d fastapiAug
```

Then:

```sql
SELECT * FROM users;
```

Flow:

```text
Terminal
   ↓
psql
   ↓
PostgreSQL
```

### `psycopg2`

Used by Python:

```python
import psycopg2
```

Flow:

```text
Python / FastAPI
       ↓
    psycopg2
       ↓
   PostgreSQL
```

---

# 5. Database Connection — `database.py`

```python
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db():

    conn = None

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

        yield conn

    except Exception as e:

        print("Database failed to connect with error:", e)

        raise

    finally:

        if conn:
            conn.close()
```

---

# 6. Why `conn = None`?

This is important when using `finally`.

Suppose the connection fails:

```python
conn = psycopg2.connect(...)
```

If the connection fails, `conn` may never get created.

Then this would cause another error:

```python
finally:
    conn.close()
```

because `conn` doesn't exist.

Therefore:

```python
conn = None
```

is initialized first.

Then:

```python
finally:
    if conn:
        conn.close()
```

means:

> Only close the connection if a connection was actually created.

---

# 7. `try / except / finally`

General structure:

```python
try:
    # Code that may fail

except Exception as e:
    # Handle the error

finally:
    # Code that should run afterward
```

Example:

```python
try:
    conn = psycopg2.connect(...)
except Exception as e:
    print("Error:", e)
finally:
    if conn:
        conn.close()
```

### `Exception as e`

```python
except Exception as e:
```

means:

- `Exception` → catch an exception
- `as e` → store the exception object in variable `e`

Then:

```python
print(e)
```

prints the actual error.

---

# 8. Why `yield conn`?

In:

```python
def get_db():

    conn = psycopg2.connect(...)

    yield conn

    conn.close()
```

`yield conn` gives the database connection to FastAPI.

For example:

```python
@app.get("/users")
async def get_all_users(
    db=Depends(database.get_db)
):
```

FastAPI gets the yielded connection as:

```python
db
```

Flow:

```text
Request
   ↓
get_db()
   ↓
psycopg2.connect()
   ↓
conn
   ↓
yield conn
   ↓
db in endpoint
   ↓
endpoint executes SQL
   ↓
request finishes
   ↓
finally
   ↓
conn.close()
```

---

# 9. Why `Depends(database.get_db)`?

```python
@app.get("/users")
async def get_all_users(
    db=Depends(database.get_db)
):
```

means:

> FastAPI should call `database.get_db()` and provide its yielded connection as `db`.

You can also import the function directly:

```python
from database import get_db
```

Then:

```python
db = Depends(get_db)
```

Both approaches work.

---

# 10. Cursor

After getting a database connection:

```python
db
```

create a cursor:

```python
cursor = db.cursor()
```

The cursor is used to execute SQL:

```python
cursor.execute("SELECT * FROM users")
```

Think:

```text
db
 ↓
Database connection

cursor
 ↓
Used to execute SQL
```

---

# 11. GET All Users — Old Version

Previously:

```python
userList = [
    {
        "id": 1,
        "name": "neeraj@gmail.com",
        "password": "neeraj123"
    },
    {
        "id": 2,
        "name": "nitin@gmail.com",
        "password": "nitin123"
    }
]
```

The endpoint was:

```python
@app.get("/users")
async def get_all_users():

    return userList
```

Flow:

```text
GET /users
    ↓
get_all_users()
    ↓
Python userList
    ↓
return userList
    ↓
JSON response
```

No database was involved.

---

# 12. GET All Users — PostgreSQL Version

Now:

```python
@app.get("/users")
async def get_all_users(
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    return users
```

Flow:

```text
GET /users
    ↓
get_all_users()
    ↓
Depends(database.get_db)
    ↓
PostgreSQL connection
    ↓
cursor = db.cursor()
    ↓
SELECT * FROM users
    ↓
fetchall()
    ↓
return users
    ↓
JSON response
```

---

# 13. Old vs New — GET All Users

| Earlier — Python List | PostgreSQL |
|---|---|
| Data stored in `userList` | Data stored in PostgreSQL |
| Python memory | Database storage |
| `return userList` | `SELECT * FROM users` |
| No cursor | Cursor required |
| No SQL | SQL query |
| No database connection | `Depends(database.get_db)` |
| `userList` contains dictionaries | PostgreSQL contains rows |

### Old

```python
@app.get("/users")
async def get_all_users():
    return userList
```

### New

```python
@app.get("/users")
async def get_all_users(
    db=Depends(database.get_db)
):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    return users
```

---

# 14. `fetchone()` vs `fetchall()`

## `fetchone()`

Used when expecting one row:

```python
user = cursor.fetchone()
```

Example:

```sql
SELECT * FROM users WHERE id = 1;
```

Flow:

```text
SQL
 ↓
One matching row
 ↓
fetchone()
 ↓
one user
```

## `fetchall()`

Used when expecting multiple rows:

```python
users = cursor.fetchall()
```

Example:

```sql
SELECT * FROM users;
```

Flow:

```text
SQL
 ↓
Multiple rows
 ↓
fetchall()
 ↓
all users
```

---

# 15. RealDictCursor

We use:

```python
from psycopg2.extras import RealDictCursor
```

and:

```python
cursor_factory=RealDictCursor
```

This makes returned rows behave like dictionaries.

For example:

```python
user = cursor.fetchone()
```

can behave like:

```python
{
    "id": 1,
    "email": "neeraj@gmail.com",
    "password": "..."
}
```

instead of accessing values by numeric positions.

---

# 16. GET One User — Old Version

Previously:

```python
@app.get("/users/{id}")
async def get_user(id: int):

    for user in userList:

        if user["id"] == id:
            return user
```

Flow:

```text
/users/2
    ↓
Loop through userList
    ↓
Check user["id"]
    ↓
Find matching user
    ↓
return user
```

---

# 17. GET One User — PostgreSQL Version

```python
@app.get("/users/{id}")
async def get_user(
    id: int,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = %s",
        (id,)
    )

    user = cursor.fetchone()

    return user
```

Flow:

```text
/users/2
    ↓
get_db()
    ↓
PostgreSQL connection
    ↓
cursor
    ↓
SELECT * FROM users WHERE id = %s
    ↓
(id,)
    ↓
fetchone()
    ↓
return user
```

---

# 18. What is `%s`?

In `psycopg2`, `%s` is a **parameter placeholder**.

Example:

```python
cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    (id,)
)
```

There are two parts:

```text
SQL:
SELECT * FROM users WHERE id = %s

Parameters:
(id,)
```

If:

```python
id = 101
```

then:

```text
%s → 101
```

The tuple is passed separately to `psycopg2`.

---

# 19. Why `(id,)`?

The comma creates a one-item tuple.

```python
(id)      # just id
(id,)     # tuple containing id
```

Example:

```python
id = 101

print((id))
# 101

print((id,))
# (101,)
```

### Multiple values

```python
(id, email)
```

```python
(id, email, age)
```

### Easy rule

```text
One value:
(a,)

Multiple values:
(a, b, c)
```

---

# 20. Is the Tuple Required by SQL?

No.

The tuple is not a PostgreSQL storage format.

It is a Python-side parameter container used by the `psycopg2` API.

```text
Python
   ↓
(id,)
   ↓
psycopg2
   ↓
%s
   ↓
PostgreSQL
```

PostgreSQL does NOT store:

```text
(101,)
```

If the column is:

```sql
id INTEGER
```

PostgreSQL stores:

```text
101
```

---

# 21. Other Parameter Formats

### Tuple

```python
cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    (id,)
)
```

### List

```python
cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    [id]
)
```

### Multiple parameters

```python
cursor.execute(
    "SELECT * FROM users WHERE id = %s AND email = %s",
    (id, email)
)
```

### Dictionary with named placeholders

```python
cursor.execute(
    """
    SELECT * FROM users
    WHERE id = %(user_id)s
    """,
    {
        "user_id": id
    }
)
```

For normal positional `%s` parameters, the tuple form is the most common.

---

# 22. Why Not Directly Put Values in SQL?

Avoid:

```python
# ❌ Avoid
cursor.execute(
    f"SELECT * FROM users WHERE id = {id}"
)
```

Use:

```python
# ✅ Parameterized query
cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    (id,)
)
```

The parameterized form lets `psycopg2` handle the parameter separately and safely.

---

# 23. Create User — Old Version

Previously:

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

Flow:

```text
POST /users
    ↓
Create Python dictionary
    ↓
userList.append()
    ↓
Stored in Python memory
```

---

# 24. Create User — PostgreSQL Version

Now PostgreSQL stores the user:

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
        RETURNING *
        """,
        (email, password)
    )

    user = cursor.fetchone()

    db.commit()

    return user
```

Mapping:

```text
%s → email
%s → password
```

Parameters:

```python
(email, password)
```

---

# 25. Why `commit()`?

`SELECT` only reads:

```sql
SELECT * FROM users;
```

For `INSERT`, `UPDATE`, or `DELETE`, the database is changed.

Therefore:

```python
db.commit()
```

saves the transaction.

Flow:

```text
INSERT
  ↓
cursor.execute()
  ↓
Transaction
  ↓
db.commit()
  ↓
Changes saved
```

---

# 26. Complete SQL-Based FastAPI API

```python
import database

from fastapi import FastAPI, Depends
from pydantic import EmailStr


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# GET one user
@app.get("/users/{id}")
async def get_user(
    id: int,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = %s",
        (id,)
    )

    user = cursor.fetchone()

    return user


# GET all users
@app.get("/users")
async def get_all_users(
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users"
    )

    users = cursor.fetchall()

    return users


# CREATE user
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
        RETURNING *
        """,
        (email, password)
    )

    user = cursor.fetchone()

    db.commit()

    return user
```

---

# 27. Old API vs SQL API

## GET all

### Old

```python
@app.get("/users")
async def get_all_users():
    return userList
```

### SQL

```python
@app.get("/users")
async def get_all_users(
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    return users
```

---

## GET one

### Old

```python
@app.get("/users/{id}")
async def get_user(id: int):

    for user in userList:
        if user["id"] == id:
            return user
```

### SQL

```python
@app.get("/users/{id}")
async def get_user(
    id: int,
    db=Depends(database.get_db)
):

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = %s",
        (id,)
    )

    return cursor.fetchone()
```

---

## POST

### Old

```python
userList.append({
    "id": random_id,
    "email": email,
    "password": password
})
```

### SQL

```python
cursor.execute(
    """
    INSERT INTO users (email, password)
    VALUES (%s, %s)
    RETURNING *
    """,
    (email, password)
)

db.commit()
```

---

# 28. Final Architecture

```text
                         FastAPI
                            │
                            ↓
                     API Endpoint
                            │
                            ↓
                Depends(database.get_db)
                            │
                            ↓
                        get_db()
                            │
                            ↓
                   psycopg2.connect()
                            │
                            ↓
                    PostgreSQL Connection
                            │
                            ↓
                         Cursor
                            │
                ┌───────────┼────────────┐
                ↓           ↓            ↓
             SELECT       INSERT       UPDATE/DELETE
                │           │            │
                ↓           ↓            ↓
           fetchone()    commit()     commit()
           fetchall()
                │
                ↓
           FastAPI Response
                            │
                            ↓
                       conn.close()
```

# 29. Key Things to Remember

```text
psql
→ Terminal tool for manually running SQL

psycopg2
→ Python driver for connecting to PostgreSQL

psycopg2.connect()
→ Creates database connection

db
→ Database connection received by FastAPI

db.cursor()
→ Creates cursor for executing SQL

cursor.execute()
→ Executes SQL

%s
→ Parameter placeholder used by psycopg2

(id,)
→ One-value tuple containing the parameter

(id, email)
→ Tuple containing two parameters

fetchone()
→ Get one row

fetchall()
→ Get all rows

db.commit()
→ Save INSERT/UPDATE/DELETE changes

yield conn
→ Give connection to FastAPI dependency

finally
→ Cleanup code that runs afterward

conn.close()
→ Close database connection

Depends(database.get_db)
→ FastAPI dependency that provides the database connection
```

# 30. Most Important Concept

### Before

```text
FastAPI
   ↓
Python List
   ↓
Dictionary
```

### After

```text
FastAPI
   ↓
Depends(get_db)
   ↓
psycopg2
   ↓
SQL
   ↓
PostgreSQL
   ↓
Table
```

The API endpoints remain similar, but the **source of the data changes**:

```text
OLD:
return userList

NEW:
cursor.execute("SELECT ...")
        ↓
fetchone()/fetchall()
        ↓
return result
```

> **Python list = application-memory storage**
>
> **PostgreSQL = persistent database storage**
>
> **psycopg2 = bridge between Python and PostgreSQL**
>
> **`cursor.execute()` = send SQL to PostgreSQL**
>
> **`fetchone()` / `fetchall()` = retrieve query results**

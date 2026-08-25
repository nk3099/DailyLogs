````md
# `psycopg2` Connection → Cursor — Mental Model

## 1. Start Here

```python
conn = psycopg2.connect(...)

cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
````

Understand this in **three steps**:

```text
psycopg2.connect()
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
        ↓
cursor.execute()
        ↓
SQL query
```

---

# 2. What Is `psycopg2.connect()`?

```python
conn = psycopg2.connect(...)
```

`connect()` is a function provided by the `psycopg2` library.

Its job is to establish a connection with PostgreSQL and return a **Connection object**.

```text
psycopg2.connect()
        ↓
Connection object
        ↓
conn
```

So:

```python
conn
```

is an **object**.

It is NOT the `Connection` class itself.

---

# 3. What Does the Connection Object Do?

The Connection object has methods.

For example:

```python
conn.cursor()
conn.commit()
conn.rollback()
conn.close()
```

The most important one here is:

```python
conn.cursor()
```

It asks the connection:

> "Give me a cursor that I can use to execute SQL."

---

# 4. What Happens With `conn.cursor()`?

When we write:

```python
cursor = conn.cursor()
```

the method `cursor()` returns a **Cursor object**.

So:

```text
conn
 ↓
Connection object
 ↓
.cursor()
 ↓
returns Cursor object
 ↓
cursor
```

Then:

```python
cursor.execute("SELECT * FROM users")
```

works because the returned Cursor object has an `execute()` method.

---

# 5. Very Important: `cursor` Is Just a Variable Name

This:

```python
cursor = conn.cursor()
```

does NOT mean `cursor` is a special Python keyword.

You could use any valid variable name.

### Example 1

```python
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
```

### Example 2

```python
my_cursor = conn.cursor()

my_cursor.execute("SELECT * FROM users")
```

### Example 3

```python
abc = conn.cursor()

abc.execute("SELECT * FROM users")
```

All three work.

Why?

Because in all three cases:

```text
conn.cursor()
      ↓
returns the same type of object
      ↓
Cursor object
```

Only the variable name changes.

---

# 6. Compare the Three

### Code:

```python
cursor = conn.cursor()
```

Mental model:

```text
conn
 ↓
Connection object
 ↓
cursor()
 ↓
Cursor object
 ↓
stored in variable named `cursor`
```

### Code:

```python
my_cursor = conn.cursor()
```

Mental model:

```text
conn
 ↓
Connection object
 ↓
cursor()
 ↓
Cursor object
 ↓
stored in variable named `my_cursor`
```

### Code:

```python
abc = conn.cursor()
```

Mental model:

```text
conn
 ↓
Connection object
 ↓
cursor()
 ↓
Cursor object
 ↓
stored in variable named `abc`
```

Therefore:

```python
my_cursor.execute(...)
```

works just like:

```python
cursor.execute(...)
```

because both variables refer to a Cursor object.

---

# 7. Why Does `.execute()` Exist?

Think about the class/type of the returned object.

Conceptually, `psycopg2` has something similar to:

```python
class Connection:

    def cursor(self):
        return Cursor()


class Cursor:

    def execute(self, sql):
        # Execute SQL against PostgreSQL
        pass

    def fetchone(self):
        pass

    def fetchall(self):
        pass
```

This is a **simplified mental model** of what the library provides.

So:

```python
conn = psycopg2.connect(...)
```

gives you a Connection object.

Then:

```python
cursor = conn.cursor()
```

gives you a Cursor object.

And because the Cursor type has:

```python
execute()
fetchone()
fetchall()
```

you can do:

```python
cursor.execute(...)
cursor.fetchone()
cursor.fetchall()
```

---

# 8. Complete Mental Model

```text
                psycopg2 library
                       │
                       ↓
               connect() function
                       │
                       ↓
              Connection object
                       │
                       ↓
                      conn
                       │
                       │
                       │ .cursor()
                       ↓
                Cursor object
                       │
                       ↓
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       execute()    fetchone()   fetchall()
          │
          ↓
      PostgreSQL
```

---

# 9. The Most Important Python Concept

Remember this general Python pattern:

```python
result = object.method()
```

The method can **return another object**.

For example:

```python
class A:

    def create(self):
        return B()


class B:

    def hello(self):
        print("Hello")


a = A()

result = a.create()

result.hello()
```

Flow:

```text
a
 ↓
A object
 ↓
create()
 ↓
B object
 ↓
result
 ↓
result.hello()
```

This is exactly the same idea as:

```python
conn = psycopg2.connect(...)

cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
```

Flow:

```text
psycopg2.connect()
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
        ↓
cursor.execute()
```

---

# 10. Your PostgreSQL Code

```python
conn = psycopg2.connect(
    host="localhost",
    database="fastapiAug",
    user="postgres",
    password="admin",
    port=5432,
    cursor_factory=RealDictCursor
)

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    (102,)
)

user = cursor.fetchone()
```

Mental model:

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
        ↓
cursor.execute(...)
        ↓
SQL sent/executed through the database connection
        ↓
cursor.fetchone()
        ↓
result
        ↓
user
```

---

# 11. One-Line Rule to Remember

```text
VARIABLE NAME ≠ OBJECT TYPE
```

For example:

```python
abc = conn.cursor()
```

`abc` is just the variable name.

The object stored inside `abc` is a **Cursor object**.

Therefore:

```python
abc.execute(...)
```

works because **the object is a Cursor**, not because the variable is called `abc` or `cursor`.

## Final Mental Model

```text
connect()
   ↓
Connection object
   ↓
conn
   ↓
cursor()
   ↓
Cursor object
   ↓
stored in ANY variable name
   ↓
cursor / my_cursor / abc
   ↓
Cursor methods
   ↓
execute() / fetchone() / fetchall()
```

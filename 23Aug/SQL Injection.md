````md
# SQL Injection

## 1. What is SQL Injection?

**SQL Injection (SQLi)** is a vulnerability that occurs when an application directly combines **user-controlled input with SQL code**.

The core problem is:

```text
User Input
    ↓
Application directly inserts input into SQL
    ↓
SQL + User Data become ONE string
    ↓
Database interprets the resulting SQL
````

The application should keep:

```text
SQL structure ≠ User data
```

---

# 2. General Example

Suppose we have this table:

```sql
users
--------------------------------
id | username | password
--------------------------------
1  | neeraj   | abc123
2  | rahul    | xyz456
3  | amit     | hello789
```

The application wants to find a user by username.

### ❌ Vulnerable Code

```python
username = input("Username: ")

query = f"""
SELECT *
FROM users
WHERE username = '{username}'
"""

cursor.execute(query)
```

If the user enters:

```text
neeraj
```

the application creates:

```sql
SELECT *
FROM users
WHERE username = 'neeraj';
```

This is the intended query.

---

# 3. How SQL Injection Happens

The vulnerability is here:

```python
f"WHERE username = '{username}'"
```

The developer has written:

```text
WHERE username = '       '
                         ↑
                    user input
```

The application expects the user input to be **only data**.

For example:

```text
username = neeraj
```

But the user can provide characters that have meaning in SQL.

A classic illustrative input is:

```text
' OR '1'='1
```

Python receives this as a normal string:

```python
username = "' OR '1'='1"
```

The application then substitutes it into:

```python
f"WHERE username = '{username}'"
```

Conceptually:

```text
WHERE username = '
        +
' OR '1'='1
        +
'
```

So the resulting SQL resembles:

```sql
SELECT *
FROM users
WHERE username = '' OR '1'='1';
```

---

# 4. What Actually Went Wrong?

Originally, the developer wanted:

```sql
WHERE username = 'USER_VALUE'
```

For example:

```sql
WHERE username = 'neeraj'
```

The application assumes:

```text
USER_VALUE = DATA
```

But because the application directly constructs the SQL string, the user can provide characters that SQL interprets as syntax.

The input:

```text
' OR '1'='1
```

contains:

```text
'       → SQL string delimiter
OR      → SQL operator
'1'='1' → SQL condition
```

So instead of remaining:

```text
DATA
```

the input becomes part of:

```text
SQL STRUCTURE
```

That is the fundamental SQL Injection problem.

---

# 5. SQL Injection in One Diagram

### ❌ Vulnerable

```text
             User
              |
              | username
              ↓
        Application
              |
              | f-string
              ↓
       SQL + User Input
              |
              ↓
        ONE SQL STRING
              |
              ↓
          Database
```

The user input can influence the SQL structure.

---

# 6. Solution — Parameterized Queries

Instead of creating SQL using an f-string:

```python
# ❌ Bad

query = f"""
SELECT *
FROM users
WHERE username = '{username}'
"""

cursor.execute(query)
```

use a parameterized query:

```python
# ✅ Good

query = """
SELECT *
FROM users
WHERE username = %s
"""

cursor.execute(query, (username,))
```

Now there are two separate things:

```text
SQL:

SELECT *
FROM users
WHERE username = %s
```

and:

```text
Data:

username
```

The database driver handles the parameter separately.

Conceptually:

```text
SQL structure
      +
User data
      ↓
Database Driver
      ↓
Database
```

The user's value is treated as **data**, not as SQL syntax.

---

# 7. What Happens to the Same Input with Parameterization?

Suppose the user enters:

```text
' OR '1'='1
```

The application executes:

```python
query = """
SELECT *
FROM users
WHERE username = %s
"""

cursor.execute(query, (username,))
```

The important difference is:

```text
SQL structure:

SELECT *
FROM users
WHERE username = %s
```

The user's input is supplied separately:

```text
username = "' OR '1'='1"
```

The database driver treats the entire value as a **username value**.

It does NOT interpret:

```text
OR
```

as a SQL `OR` operator.

---

# 8. Why Parameterization Prevents SQL Injection

### ❌ String construction

```python
query = f"SELECT ... WHERE username = '{username}'"
```

Results conceptually in:

```text
SQL code + user data
        ↓
ONE STRING
        ↓
Database parses everything as SQL
```

### ✅ Parameterization

```python
query = "SELECT ... WHERE username = %s"

cursor.execute(query, (username,))
```

Results in:

```text
SQL structure
      +
Parameter value
      ↓
Database driver
      ↓
Database
```

The database knows that the parameter is a **value**, not additional SQL code.

---

# 9. What About ORM?

ORMs such as **SQLAlchemy** and **Django ORM** can help prevent SQL Injection because their normal query APIs generally generate parameterized SQL.

Example:

```python
user = (
    session.query(User)
    .filter(User.username == username)
    .first()
)
```

Conceptually:

```text
Python ORM
    ↓
Parameterized SQL
    ↓
Database
```

So:

```text
ORM + normal query API
        ↓
Generally safe
```

However:

```text
ORM ≠ automatic immunity
```

You can still introduce SQL Injection by constructing unsafe raw SQL:

```python
# ❌ Still vulnerable

query = f"""
SELECT *
FROM users
WHERE username = '{username}'
"""

session.execute(text(query))
```

So the rule remains:

> **Whether you use raw SQL or an ORM, never directly concatenate untrusted input into SQL.**

---

# 10. Other Important Defenses

### 1. Parameterized queries

Primary defense:

```python
cursor.execute(
    "SELECT * FROM users WHERE username = %s",
    (username,)
)
```

### 2. Input validation

Validate expected types and formats.

For example, if an ID must be an integer:

```python
user_id = int(user_id)
```

### 3. Allowlisting

For dynamic SQL elements such as column names, allow only known values.

```python
allowed_columns = {
    "name": User.name,
    "email": User.email,
    "age": User.age
}
```

### 4. Least privilege

The application's database account should have only the permissions it actually needs.

### 5. Safe error handling

Don't expose detailed database errors to users.

---

# 11. Bad vs Safe — Common SQL Operations

| Operation         | ❌ Bad / Vulnerable                                           | ✅ Safe                                                                          |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| **SELECT**        | `f"SELECT * FROM users WHERE username = '{username}'"`       | `cursor.execute("SELECT * FROM users WHERE username = %s", (username,))`        |
| **INSERT**        | `f"INSERT INTO users(name) VALUES ('{name}')"`               | `cursor.execute("INSERT INTO users(name) VALUES (%s)", (name,))`                |
| **UPDATE**        | `f"UPDATE users SET email = '{email}' WHERE id = {user_id}"` | `cursor.execute("UPDATE users SET email = %s WHERE id = %s", (email, user_id))` |
| **DELETE**        | `f"DELETE FROM users WHERE id = {user_id}"`                  | `cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))`                 |
| **Search / LIKE** | `f"SELECT * FROM products WHERE name LIKE '%{search}%'"`     | `cursor.execute("SELECT * FROM products WHERE name LIKE %s", (f"%{search}%",))` |
| **ORDER BY**      | `f"SELECT * FROM users ORDER BY {column}"`                   | Use an **allowlist** of permitted columns                                       |

---

# 12. Final Mental Model

```text
                 SQL INJECTION

                    User Input
                        |
                        ↓
              Direct SQL Construction
                        |
                        ↓
               SQL + User Data
                        |
                        ↓
                  ONE STRING
                        |
                        ↓
                    Database
                        |
                        ↓
             SQL meaning can change
```

### Prevention:

```text
                 USER INPUT
                     |
                     ↓
               Application
                     |
          ┌──────────┴──────────┐
          ↓                     ↓
    SQL Structure           User Data
          |                     |
          └──────────┬──────────┘
                     ↓
             Parameterized Query
                     ↓
                  Database
```

## Key Rule

> **Never allow untrusted user input to become SQL syntax. Use parameterized queries/prepared statements, or safe ORM APIs, to keep SQL structure and user data separate.**

```
```

# cls in OOPs and Python Singleton Pattern — Detailed Explanation, Code Flow, and Practical Uses

## 1. What Is a Singleton?

A **Singleton** is a design pattern where a class is intended to have **only one shared instance** throughout an application.

Normally:

```python
sql1 = SQL(config)
sql2 = SQL(config)
sql3 = SQL(config)
```

creates three separate objects:

```text
SQL(config)
    ↓
Object A

SQL(config)
    ↓
Object B

SQL(config)
    ↓
Object C
```

With a Singleton-style implementation:

```python
sql1 = SQL.get_instance(config)
sql2 = SQL.get_instance(config)
sql3 = SQL.get_instance(config)
```

all three variables can refer to the same object:

```text
              ┌── sql1
              │
Object A ─────┼── sql2
              │
              └── sql3
```

Therefore:

```python
sql1 is sql2
```

returns:

```text
True
```

---

# 2. Why Would We Want Only One Object?

Some objects represent something that should be **shared** rather than recreated repeatedly.

For example, imagine an application has:

```text
100 functions
       ↓
all need SQL access
```

You could create:

```text
function A → SQL()
function B → SQL()
function C → SQL()
...
```

This may result in many SQL-related objects or resources.

Instead, you can have:

```text
function A ──┐
function B ──┤
function C ──┼──→ one shared SQL object
function D ──┤
function E ──┘
```

This can be useful when initialization is expensive or when the application wants one shared piece of state.

---

# 3. Important: Singleton Is a Design Pattern

Singleton is **not a special Python keyword**.

Python does not have:

```python
singleton SQL
```

Instead, Singleton is a **design pattern**.

A design pattern is a commonly used approach for solving a recurring software-design problem.

The Singleton idea is:

```text
Create one instance
       ↓
store it somewhere shared
       ↓
return that same instance
       ↓
don't repeatedly create new instances
```

---

# 4. Basic Singleton Example

```python
class SQL:

    _instance = None

    def __init__(self, config):
        self.config = config

    @classmethod
    def get_instance(cls, config):

        if cls._instance is None:
            cls._instance = cls(config)

        return cls._instance
```

Let's understand **every line**.

---

# 5. `_instance = None`

```python
class SQL:

    _instance = None
```

`_instance` is a **class variable**.

Initially, there is no SQL object.

Therefore:

```text
SQL._instance
       ↓
     None
```

Why store it on the class?

Because the class method needs a shared place where it can remember:

> "Have I already created the object?"

---

# 6. The Constructor

```python
def __init__(self, config):
    self.config = config
```

This is the normal constructor.

Whenever you do:

```python
SQL(config)
```

Python creates a new SQL instance and runs:

```python
SQL.__init__(self, config)
```

For example:

```python
sql = SQL(config)
```

Flow:

```text
SQL(config)
    ↓
new SQL object created
    ↓
SQL.__init__(self, config)
    ↓
self.config = config
    ↓
object ready
```

---

# 7. The Class Method

```python
@classmethod
def get_instance(cls, config):
```

The important part is:

```python
@classmethod
```

This means the method receives the **class** as its first argument.

When you call:

```python
SQL.get_instance(config)
```

Python effectively gives:

```text
cls = SQL
```

So inside the method:

```python
cls
```

refers to the `SQL` class.

---

# 8. `self` vs `cls`

This distinction is extremely important.

## Normal instance method

```python
class SQL:

    def connect(self):
        print(self)
```

Call:

```python
sql = SQL(config)
sql.connect()
```

Conceptually:

```text
sql.connect()
     ↓
self = sql
```

Therefore:

```text
self → current object / instance
```

---

## Class method

```python
class SQL:

    @classmethod
    def get_instance(cls):
        print(cls)
```

Call:

```python
SQL.get_instance()
```

Conceptually:

```text
SQL.get_instance()
        ↓
cls = SQL
```

Therefore:

```text
cls → current class
```

---

# 9. What Does "Python Passes the Class into `cls`" Mean?

You write:

```python
SQL.get_instance(config)
```

You don't write:

```python
get_instance(SQL, config)
```

Python automatically supplies the class because the method is a `@classmethod`.

Conceptually:

```text
SQL.get_instance(config)
        ↓
get_instance(cls=SQL, config=config)
```

So:

```python
cls
```

contains the class:

```text
cls
 ↓
SQL
```

---

# 10. The Important Line

Inside our method:

```python
cls._instance = cls(config)
```

At first this looks confusing.

But remember:

```text
cls = SQL
```

Therefore:

```python
cls._instance
```

means:

```python
SQL._instance
```

And:

```python
cls(config)
```

means:

```python
SQL(config)
```

So conceptually:

```python
cls._instance = cls(config)
```

becomes:

```python
SQL._instance = SQL(config)
```

---

# 11. What Does `SQL(config)` Do?

This is a normal object creation operation.

```python
SQL(config)
```

means:

> Create a new object of the `SQL` class using `config`.

Python then invokes the constructor:

```python
SQL.__init__(self, config)
```

So the flow is:

```text
SQL(config)
    ↓
creates SQL object
    ↓
SQL.__init__(self, config)
    ↓
self.config = config
    ↓
object is initialized
    ↓
object returned
```

---

# 12. The Complete First-Call Flow

Suppose:

```python
sql1 = SQL.get_instance(config)
```

### Step 1

Call:

```python
SQL.get_instance(config)
```

Because it is a class method:

```text
cls = SQL
```

---

### Step 2

Check:

```python
if cls._instance is None:
```

This means:

```python
if SQL._instance is None:
```

Initially:

```text
SQL._instance
      ↓
    None
```

So the condition is true.

---

### Step 3

Run:

```python
cls._instance = cls(config)
```

Replace `cls` with `SQL`:

```python
SQL._instance = SQL(config)
```

---

### Step 4

Run:

```python
SQL(config)
```

This creates an object.

```text
SQL(config)
    ↓
creates SQL object
    ↓
SQL.__init__(self, config)
    ↓
self.config = config
    ↓
object returned
```

---

### Step 5

The returned object is stored:

```text
SQL._instance
      ↓
   Object A
```

---

### Step 6

Finally:

```python
return cls._instance
```

means:

```python
return SQL._instance
```

So `sql1` receives Object A.

Complete flow:

```text
SQL.get_instance(config)
        ↓
cls = SQL
        ↓
SQL._instance is None?
        ↓
       YES
        ↓
SQL(config)
        ↓
creates SQL object
        ↓
SQL.__init__(self, config)
        ↓
self.config = config
        ↓
object returned
        ↓
SQL._instance = Object A
        ↓
return Object A
        ↓
sql1 → Object A
```

---

# 13. What Happens on the Second Call?

Now:

```python
sql2 = SQL.get_instance(config)
```

Again:

```text
cls = SQL
```

Then:

```python
if cls._instance is None:
```

means:

```python
if SQL._instance is None:
```

But now:

```text
SQL._instance
      ↓
   Object A
```

It is **not `None`**.

Therefore:

```python
cls(config)
```

doesn't run.

Instead:

```python
return cls._instance
```

returns Object A.

Flow:

```text
SQL.get_instance(config)
        ↓
cls = SQL
        ↓
SQL._instance is None?
        ↓
        NO
        ↓
don't create SQL(config)
        ↓
return SQL._instance
        ↓
Object A
        ↓
sql2 → Object A
```

---

# 14. First Call vs Second Call

## First call

```python
sql1 = SQL.get_instance(config)
```

```text
_instance = None
      ↓
create object
      ↓
Object A
      ↓
store Object A
      ↓
return Object A
```

## Second call

```python
sql2 = SQL.get_instance(config)
```

```text
_instance = Object A
      ↓
object already exists
      ↓
don't create another object
      ↓
return Object A
```

Therefore:

```python
print(sql1 is sql2)
```

Output:

```text
True
```

---

# 15. Why Is `_instance` a Class Variable?

Because we want one shared storage location.

```python
class SQL:
    _instance = None
```

Conceptually:

```text
              SQL CLASS
                  │
                  │
             _instance
                  │
                  ↓
              Object A
```

If `_instance` were only an instance variable:

```python
self._instance
```

you would already need an object before you could access it.

But the whole purpose of `get_instance()` is to **get/create the object in the first place**.

Therefore a class-level variable is convenient for storing the shared instance.

---

# 16. Why Is `get_instance()` a Class Method?

Because we want to call:

```python
SQL.get_instance(config)
```

before we have a SQL object.

A normal instance method would require:

```python
sql = SQL(config)
sql.get_instance()
```

But that already creates the object.

That defeats the purpose.

With:

```python
@classmethod
def get_instance(cls, config):
```

we can do:

```python
SQL.get_instance(config)
```

without first creating a SQL instance.

---

# 17. Why Use `cls(config)` Instead of `SQL(config)`?

You might ask:

> Why not simply write `SQL(config)`?

We could:

```python
SQL._instance = SQL(config)
```

But:

```python
cls._instance = cls(config)
```

is more flexible.

Suppose we have:

```python
class MySQL(SQL):
    pass
```

Now:

```python
MySQL.get_instance(config)
```

Because it is a class method:

```text
cls = MySQL
```

Therefore:

```python
cls(config)
```

becomes:

```python
MySQL(config)
```

instead of always:

```python
SQL(config)
```

This allows the method to respect the class that called it.

---

# 18. Practical Example — Database Manager

Imagine an application has many services:

```text
UserService
OrderService
PaymentService
ReportService
```

All of them need database access.

Instead of repeatedly creating the same database manager:

```python
db1 = SQL(config)
db2 = SQL(config)
db3 = SQL(config)
```

the application can have:

```python
db = SQL.get_instance(config)
```

and reuse it.

Conceptually:

```text
UserService ───┐
OrderService ──┤
PaymentService ┼──→ SQL Object
ReportService ─┘
```

This can be useful when the SQL object manages shared resources or expensive initialization.

---

# 19. Practical Example — Configuration Manager

Suppose an application loads configuration:

```python
class Config:
    _instance = None

    def __init__(self):
        self.database_url = "..."
        self.api_key = "..."

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
```

Different parts of the application can do:

```python
config1 = Config.get_instance()
config2 = Config.get_instance()
```

Both refer to the same configuration object:

```text
config1 ──┐
          ├──→ Config Object
config2 ──┘
```

This can be useful when you want a single shared configuration state.

---

# 20. Practical Example — Application Logger

Logging configuration is another common example of shared application-wide state.

Conceptually:

```text
Application
    │
    ├── Module A
    ├── Module B
    ├── Module C
    └── Module D
             │
             ↓
      shared logging setup
```

Instead of each module independently constructing a completely separate logging manager, an application can centralize logging configuration.

In real Python applications, however, the built-in `logging` module already provides mechanisms for shared/named loggers, so you don't necessarily need to implement your own Singleton.

---

# 21. Practical Example — Cache Manager

Imagine an application has a cache:

```text
Cache
 ├── user:123 → data
 ├── user:456 → data
 └── product:789 → data
```

If every part of the application created a different cache object:

```text
Module A → Cache A
Module B → Cache B
Module C → Cache C
```

they wouldn't necessarily share the same cached state.

A shared cache manager could instead provide:

```text
Module A ──┐
Module B ──┼──→ one Cache Manager
Module C ──┘
```

This is a situation where shared state can be useful.

---

# 22. Practical Example — Expensive Resource

Suppose creating an object involves expensive initialization:

```python
class ExpensiveService:

    def __init__(self):
        print("Performing expensive initialization...")
```

Without a shared instance:

```python
a = ExpensiveService()
b = ExpensiveService()
c = ExpensiveService()
```

Initialization happens three times.

A Singleton-style approach can initialize it once and reuse it.

```text
First request
     ↓
Create service
     ↓
Store it
     ↓
Reuse it

Later requests
     ↓
Return existing service
```

---

# 23. When Singleton Can Be Useful

Singleton can make sense when you genuinely want **one shared instance** of something.

Common examples:

```text
✓ Application configuration
✓ Shared cache manager
✓ Certain service managers
✓ Shared resource managers
✓ Some logging/application infrastructure
✓ Expensive-to-initialize shared services
```

The important requirement is not:

> "Singleton is always better."

The requirement is:

> "Does this resource logically need one shared instance?"

If not, normal object creation is usually simpler.

---

# 24. Singleton Is Not Automatically Required for Database Connections

This is an important practical point.

You may hear:

> "Database connection = Singleton."

That's not always correct.

Modern applications often use **connection pools**.

Instead of:

```text
one connection forever
```

a pool may maintain:

```text
Connection 1
Connection 2
Connection 3
Connection 4
...
```

and reuse them efficiently.

So distinguish:

```text
Singleton
    ↓
one shared object

Connection pool
    ↓
multiple reusable connections
```

They solve different problems.

---

# 25. Why Singleton Can Sometimes Be a Bad Idea

Singleton introduces **global shared state**.

For example:

```text
Module A
   ↓
Singleton
   ↑
Module B
```

Both modules can modify the same object.

That can make code:

* harder to test
* harder to reason about
* more tightly coupled
* harder to manage in concurrent applications

For this reason, modern applications often prefer **dependency injection** when appropriate.

Instead of every module secretly accessing a global Singleton:

```python
SQL.get_instance(config)
```

you can explicitly give a service the dependency it needs:

```python
def process_orders(db):
    ...
```

Then:

```python
db = SQL(...)
process_orders(db)
```

This makes the dependency visible.

---

# 26. Singleton vs Normal Object

### Normal object creation

```python
sql1 = SQL(config)
sql2 = SQL(config)
```

Flow:

```text
SQL(config) → Object A
SQL(config) → Object B
```

Therefore:

```python
sql1 is sql2
```

is:

```text
False
```

---

### Singleton-style access

```python
sql1 = SQL.get_instance(config)
sql2 = SQL.get_instance(config)
```

Flow:

```text
First call
    ↓
create Object A
    ↓
store Object A

Second call
    ↓
return Object A
```

Therefore:

```python
sql1 is sql2
```

is:

```text
True
```

---

# 27. The Most Important Code

```python
class SQL:

    _instance = None

    def __init__(self, config):
        self.config = config

    @classmethod
    def get_instance(cls, config):

        if cls._instance is None:
            cls._instance = cls(config)

        return cls._instance
```

And:

```python
sql1 = SQL.get_instance(config)
sql2 = SQL.get_instance(config)

print(sql1 is sql2)
```

Output:

```text
True
```

---

# 28. Complete Mental Model

Remember this:

```text
                  SQL CLASS
                     │
          ┌──────────┴──────────┐
          │                     │
    _instance             get_instance()
          │                     │
          │                @classmethod
          │                     │
          │                 cls = SQL
          │                     │
          │                 cls(config)
          │                     │
          │                     ↓
          │                SQL(config)
          │                     │
          │                     ↓
          │                SQL OBJECT
          │                     │
          └─────────────────────┘
                     │
                     ↓
              SQL._instance
```

The complete first-call sequence is:

```text
SQL.get_instance(config)
        ↓
@classmethod
        ↓
cls = SQL
        ↓
check SQL._instance
        ↓
None?
        ↓
YES
        ↓
cls(config)
        ↓
SQL(config)
        ↓
creates SQL object
        ↓
SQL.__init__(self, config)
        ↓
object initialized
        ↓
object returned
        ↓
SQL._instance = object
        ↓
return object
```

The second call:

```text
SQL.get_instance(config)
        ↓
cls = SQL
        ↓
check SQL._instance
        ↓
already contains Object A
        ↓
don't call SQL(config)
        ↓
return Object A
```

---

# 29. Final Summary

The entire pattern is built from a few simple Python concepts:

```text
class
  ↓
defines what objects look like

SQL(config)
  ↓
creates an instance

__init__()
  ↓
initializes that instance

class variable
  ↓
stores shared class-level state

@classmethod
  ↓
allows calling a method through the class

cls
  ↓
refers to the class

cls(config)
  ↓
creates an instance of that class

_instance
  ↓
remembers the already-created instance

Singleton
  ↓
ensures/restricts access to one shared instance
```

The key line:

```python
cls._instance = cls(config)
```

can be understood, when `cls == SQL`, as:

```python
SQL._instance = SQL(config)
```

And the flow is:

```text
SQL(config)
    ↓
creates a SQL object
    ↓
SQL.__init__(self, config)
    ↓
object initialized
    ↓
object returned
    ↓
stored in SQL._instance
    ↓
future get_instance() calls return the same object
```

**That's the central idea behind this Singleton implementation.**

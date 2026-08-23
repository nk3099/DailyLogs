# Python OOP, Constructors, Modules, Packages, and Python Path

## 1. OOP — Object-Oriented Programming

**OOP (Object-Oriented Programming)** is a programming approach where we organize code around **objects**.

An object contains:

* **Data** → attributes/properties
* **Functions** → methods that operate on that data

Example:

```python
class Labour:
    def __init__(self, name, age, wage):
        self.name = name
        self.age = age
        self.wage = wage

    def buildhouse(self):
        print(f"{self.name} is building a house.")

    def calculate_daily_wage(self):
        return self.wage * 8
```

Creating objects:

```python
ram = Labour("Ram", 25, 500)
shyam = Labour("Shyam", 30, 600)
```

Now each object has its own data:

```text
ram
 ├── name = Ram
 ├── age = 25
 └── wage = 500

shyam
 ├── name = Shyam
 ├── age = 30
 └── wage = 600
```

---

# 2. Constructor

A **constructor** is used to initialize an object's data when the object is created.

In Python, we commonly use:

```python
__init__()
```

Example:

```python
class Labour:

    def __init__(self, name, age, wage):
        self.name = name
        self.age = age
        self.wage = wage
```

When we write:

```python
ram = Labour("Ram", 25, 500)
```

Python automatically calls:

```python
__init__(ram, "Ram", 25, 500)
```

Therefore:

```text
ram
 ↓
name = "Ram"
age = 25
wage = 500
```

### Important terms

```python
class Labour:
    def __init__(self, name, age, wage):
```

* `self` → current object
* `name`, `age`, `wage` → parameters
* `"Ram"`, `25`, `500` → arguments
* `self.name`, `self.age`, `self.wage` → attributes of the object

---

# 3. Why is the Constructor Useful?

Without OOP, we might repeatedly pass the same information to different functions:

```python
def buildhouse(name, age, wage):
    print(name, "is building a house")


def calculate_wage(name, age, wage):
    print(wage * 8)


def check_worker(name, age, wage):
    print(name, age, wage)
```

Then:

```python
buildhouse("Ram", 25, 500)
calculate_wage("Ram", 25, 500)
check_worker("Ram", 25, 500)
```

The same data is repeatedly passed around.

With OOP:

```python
class Labour:

    def __init__(self, name, age, wage):
        self.name = name
        self.age = age
        self.wage = wage

    def buildhouse(self):
        print(self.name, "is building a house")

    def calculate_wage(self):
        print(self.wage * 8)

    def check_worker(self):
        print(self.name, self.age, self.wage)
```

Create the object once:

```python
ram = Labour("Ram", 25, 500)
```

Then:

```python
ram.buildhouse()
ram.calculate_wage()
ram.check_worker()
```

We don't repeatedly pass:

```text
name
age
wage
```

because they are already stored inside `ram`.

---

# 4. Important OOP Benefit: Multiple Methods Can Share the Same Object Data

This is one of the important things you noticed.

Suppose we have many functions doing different things:

```python
class Labour:

    def __init__(self, name, age, wage):
        self.name = name
        self.age = age
        self.wage = wage

    def buildhouse(self):
        print(self.name, "is building a house")

    def calculate_wage(self):
        return self.wage * 8

    def give_raise(self, percentage):
        self.wage = self.wage + (self.wage * percentage / 100)

    def display_details(self):
        print(self.name)
        print(self.age)
        print(self.wage)

    def work(self):
        self.buildhouse()
        print("Daily wage:", self.calculate_wage())
```

Create the object:

```python
ram = Labour("Ram", 25, 500)
```

Now:

```python
ram.work()
```

Inside `work()`:

```python
self.buildhouse()
self.calculate_wage()
```

Both methods already know which object they are working with.

`self` refers to the same `ram` object.

```text
ram
 │
 ├── name = Ram
 ├── age = 25
 └── wage = 500
       │
       ├── buildhouse()
       ├── calculate_wage()
       ├── give_raise()
       ├── display_details()
       └── work()
```

So you don't need:

```python
work(ram.name, ram.age, ram.wage)
```

and then:

```python
buildhouse(ram.name, ram.age, ram.wage)
calculate_wage(ram.name, ram.age, ram.wage)
```

Instead:

```python
ram.work()
```

and the methods access the object's state using `self`.

---

# 5. Another Important Benefit: State is Maintained

Suppose:

```python
class Labour:

    def __init__(self, name, wage):
        self.name = name
        self.wage = wage

    def give_raise(self, amount):
        self.wage += amount

    def display_wage(self):
        print(self.wage)
```

Create:

```python
ram = Labour("Ram", 500)
```

Initially:

```text
wage = 500
```

Call:

```python
ram.give_raise(100)
```

Now the object has:

```text
wage = 600
```

Then:

```python
ram.display_wage()
```

prints:

```text
600
```

The change made by one method is available to another method because both operate on the **same object**.

```text
ram
 │
 └── wage = 500
        │
        ↓
   give_raise()
        │
        ↓
   wage = 600
        │
        ↓
   display_wage()
        │
        ↓
      600
```

This is the idea of **object state**.

---

# 6. Module

A **module is a `.py` file** containing Python code.

Example:

```text
project/
│
├── main.py
└── calculator.py    ← module
```

`calculator.py`:

```python
def add(a, b):
    return a + b
```

`main.py`:

```python
from calculator import add

print(add(10, 20))
```

So:

```text
calculator.py
      ↓
   MODULE
```

---

# 7. Package

A **package is a directory used to organize related modules**.

Example:

```text
project/
│
├── main.py
│
└── calculator/          ← package
    ├── __init__.py
    ├── addition.py      ← module
    └── subtraction.py   ← module
```

`addition.py`:

```python
def add(a, b):
    return a + b
```

`subtraction.py`:

```python
def subtract(a, b):
    return a - b
```

`main.py`:

```python
from calculator.addition import add
from calculator.subtraction import subtract

print(add(10, 20))
print(subtract(20, 10))
```

The hierarchy is:

```text
calculator/
     ↓
  PACKAGE
     │
     ├── addition.py
     │       ↓
     │    MODULE
     │
     └── subtraction.py
             ↓
          MODULE
```

---

# 8. Easy Way to Remember Module vs Package

```text
.py file       → Module

Folder         → Package

Class          → Blueprint for objects

Object         → Instance of a class

Function       → Reusable block of code

Method         → Function defined inside a class
```

Overall:

```text
Package
   ↓
 Module
   ↓
 Class
   ↓
 Object
   ↓
 Methods
```

---

# 9. What is `__init__.py`?

A package can contain:

```text
calculator/
│
├── __init__.py
├── addition.py
└── subtraction.py
```

`__init__.py` is a special file associated with a Python package.

It can be empty or contain package initialization code.

Modern Python also supports **namespace packages**, so `__init__.py` is not always required.

---

# 10. What is `PYTHONPATH`?

`PYTHONPATH` tells Python **where to look for modules and packages**.

Suppose:

```text
/Users/neeraj/project/
│
├── main.py
└── calculator/
    ├── __init__.py
    └── addition.py
```

If Python cannot find `calculator`, you might get:

```text
ModuleNotFoundError: No module named 'calculator'
```

Python searches locations stored in:

```python
import sys

print(sys.path)
```

You can add your project directory to the Python search path:

```bash
export PYTHONPATH=/Users/neeraj/project
```

Now Python knows:

```text
PYTHONPATH
     ↓
/Users/neeraj/project
     ↓
calculator/
     ↓
addition.py
```

So:

```python
from calculator.addition import add
```

can be resolved.

---

# 11. Very Important: `PYTHONPATH` Does Not Create a Module

`PYTHONPATH` does **not** convert a file into a module.

Instead:

```text
calculator.py
     ↓
already a module

PYTHONPATH
     ↓
tells Python where to find it
```

For a package:

```text
/project
   ↓
PYTHONPATH
   ↓
calculator/
   ↓
addition.py
```

Python can now find the package and its modules.

---

# 12. Complete Picture

All these concepts connect together:

```text
                         PYTHONPATH
                             ↓
                         /project
                             ↓
                    ┌────────────────┐
                    │    package     │
                    │  calculator/   │
                    └────────────────┘
                       ↓           ↓
                  addition.py   labour.py
                       ↓           ↓
                    MODULE       MODULE
                       ↓           ↓
                    function      CLASS
                                   ↓
                                 Object
                                   ↓
                              __init__()
                                   ↓
                              Object state
                                   ↓
                    ┌──────────────┴──────────────┐
                    ↓              ↓               ↓
                 method 1       method 2        method 3
                    ↓              ↓               ↓
                 self.data      self.data        self.data
```

## Core OOP idea

The most important idea to remember is:

> **An object stores its own data (state), and multiple methods can operate on that same data through `self`.**

This is why, when many functions need to work on the **same entity/data**, OOP can make the code easier to organize and avoid repeatedly passing the same data between functions.

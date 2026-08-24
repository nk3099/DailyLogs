# Factory Pattern and `@staticmethod` — Complete Summary

## 1. What Is the Factory Pattern?

The **Factory Pattern** is a design pattern used to **centralize object creation**.

Instead of directly creating different objects everywhere:

```python
carpenter = Carpenter()
electrician = Electrician()
plumber = Plumber()
```

we use a factory:

```python
labour = LabourFactory.create_labour("carpenter")
```

The factory decides **which object should be created**.

### Basic idea

```text
Application
     |
     v
LabourFactory
     |
     +---- "carpenter"   -> Carpenter()
     |
     +---- "electrician" -> Electrician()
     |
     +---- "plumber"     -> Plumber()
```

---

# 2. Why Use a Factory?

Suppose we have different types of labour:

```python
class Labour:
    def work(self):
        print("Labour is working")


class Carpenter(Labour):
    def work(self):
        print("Carpenter is doing carpentry")


class Electrician(Labour):
    def work(self):
        print("Electrician is doing electrical work")


class Plumber(Labour):
    def work(self):
        print("Plumber is doing plumbing")
```

Without a factory:

```python
carpenter = Carpenter()
electrician = Electrician()
plumber = Plumber()
```

The calling code needs to know the concrete classes.

With a factory:

```python
carpenter = LabourFactory.create_labour("carpenter")
electrician = LabourFactory.create_labour("electrician")
plumber = LabourFactory.create_labour("plumber")
```

The object-creation logic is centralized inside `LabourFactory`.

---

# 3. Simple Factory Example

```python
class Labour:
    def work(self):
        print("Labour is working")


class Carpenter(Labour):
    def work(self):
        print("Carpenter is doing carpentry")


class Electrician(Labour):
    def work(self):
        print("Electrician is doing electrical work")


class Plumber(Labour):
    def work(self):
        print("Plumber is doing plumbing")


class LabourFactory:

    @staticmethod
    def create_labour(labour_type):

        if labour_type == "carpenter":
            return Carpenter()

        elif labour_type == "electrician":
            return Electrician()

        elif labour_type == "plumber":
            return Plumber()

        else:
            raise ValueError("Unknown labour type")
```

Usage:

```python
labour = LabourFactory.create_labour("carpenter")

labour.work()
```

Output:

```text
Carpenter is doing carpentry
```

---

# 4. Factory Code Flow

When we write:

```python
labour = LabourFactory.create_labour("carpenter")
```

the flow is:

```text
LabourFactory.create_labour("carpenter")
                |
                v
       labour_type = "carpenter"
                |
                v
     labour_type == "carpenter"?
                |
               YES
                |
                v
          Carpenter()
                |
                v
     Carpenter object created
                |
                v
              return
                |
                v
             labour
```

So the factory is responsible for:

> **Deciding what object to create.**

---

# 5. Factory Can Create Different Objects

The same factory method can create different classes:

```python
carpenter = LabourFactory.create_labour("carpenter")
electrician = LabourFactory.create_labour("electrician")
plumber = LabourFactory.create_labour("plumber")
```

Flow:

```text
"carpenter"
    |
    v
Carpenter()


"electrician"
    |
    v
Electrician()


"plumber"
    |
    v
Plumber()
```

The important idea is:

> **One creation method can decide which concrete object to create based on input.**

---

# 6. Factory + Inheritance

Factory works particularly well with inheritance.

```python
class Labour:
    def work(self):
        print("Labour is working")


class Carpenter(Labour):
    def work(self):
        print("Carpenter is doing carpentry")


class Electrician(Labour):
    def work(self):
        print("Electrician is doing electrical work")
```

Relationship:

```text
             Labour
               |
       +-------+-------+
       |               |
   Carpenter       Electrician
```

The factory creates the appropriate child object.

---

# 7. Factory + Polymorphism

This is a very useful combination.

```python
labour = LabourFactory.create_labour("carpenter")

labour.work()
```

The variable:

```python
labour
```

can refer to different child objects:

```text
labour
   |
   +--> Carpenter object
   |
   +--> Electrician object
   |
   +--> Plumber object
```

But we can use the same method:

```python
labour.work()
```

Python executes the correct overridden method.

### Carpenter example

```python
labour = LabourFactory.create_labour("carpenter")
labour.work()
```

Flow:

```text
Factory
   |
   v
Carpenter object
   |
   v
labour.work()
   |
   v
Carpenter.work()
```

For an electrician:

```text
Factory
   |
   v
Electrician object
   |
   v
labour.work()
   |
   v
Electrician.work()
```

This is **polymorphism**.

---

# 8. Factory With Constructor Arguments

Different labour types can have different properties.

```python
class Labour:

    def __init__(self, name, age):
        self.name = name
        self.age = age


class Carpenter(Labour):

    def __init__(self, name, age, experience):
        super().__init__(name, age)
        self.experience = experience


class Electrician(Labour):

    def __init__(self, name, age, certification):
        super().__init__(name, age)
        self.certification = certification
```

The factory can handle different constructors:

```python
class LabourFactory:

    @staticmethod
    def create_labour(labour_type, **kwargs):

        if labour_type == "carpenter":
            return Carpenter(
                kwargs["name"],
                kwargs["age"],
                kwargs["experience"]
            )

        elif labour_type == "electrician":
            return Electrician(
                kwargs["name"],
                kwargs["age"],
                kwargs["certification"]
            )

        else:
            raise ValueError("Unknown labour type")
```

Usage:

```python
ram = LabourFactory.create_labour(
    "carpenter",
    name="Ram",
    age=25,
    experience=5
)

john = LabourFactory.create_labour(
    "electrician",
    name="John",
    age=30,
    certification="Electrical Level 2"
)
```

Result:

```text
ram
 ↓
Carpenter object

john
 ↓
Electrician object
```

---

# 9. What Is `@staticmethod`?

A static method is a method that **does not automatically receive `self` or `cls`**.

Example:

```python
class Labour:

    @staticmethod
    def calculate_wage(hours, rate):
        return hours * rate
```

Call it:

```python
wage = Labour.calculate_wage(8, 500)

print(wage)
```

Output:

```text
4000
```

Nothing is automatically passed to `calculate_wage()`.

The arguments are simply:

```text
hours = 8
rate = 500
```

---

# 10. Why Use `@staticmethod`?

Suppose:

```python
class Labour:

    @staticmethod
    def calculate_wage(hours, rate):
        return hours * rate
```

This method doesn't need a particular labour object's data.

It doesn't use:

```python
self.name
self.age
self.skill
```

It only needs:

```python
hours
rate
```

Therefore, a static method is appropriate.

---

# 11. Static Method vs Normal Method

## Normal Instance Method

```python
class Labour:

    def calculate_wage(self, hours, rate):
        return hours * rate
```

Create an object:

```python
ram = Labour()

ram.calculate_wage(8, 500)
```

Python automatically passes:

```text
ram.calculate_wage(8, 500)
        |
        v
calculate_wage(self=ram, hours=8, rate=500)
```

Therefore:

```text
self -> current object / instance
```

---

## Static Method

```python
class Labour:

    @staticmethod
    def calculate_wage(hours, rate):
        return hours * rate
```

Call:

```python
Labour.calculate_wage(8, 500)
```

Python does **not** automatically pass:

```text
self
```

or:

```text
cls
```

Conceptually:

```text
calculate_wage(hours=8, rate=500)
```

---

# 12. Static Method vs Class Method

This distinction is very important.

## Instance Method

```python
class Labour:

    def work(self):
        print(self)
```

Call:

```python
ram = Labour()
ram.work()
```

Python automatically passes:

```text
self = ram
```

Therefore:

```text
self -> current object
```

---

## Class Method

```python
class Labour:

    @classmethod
    def create(cls):
        print(cls)
```

Call:

```python
Labour.create()
```

Python automatically passes:

```text
cls = Labour
```

Therefore:

```text
cls -> current class
```

---

## Static Method

```python
class Labour:

    @staticmethod
    def calculate_wage(hours, rate):
        return hours * rate
```

Call:

```python
Labour.calculate_wage(8, 500)
```

Nothing is automatically passed.

Therefore:

```text
self -> object
cls  -> class
static method -> nothing automatically passed
```

---

# 13. Three Methods Side by Side

```python
class Labour:

    # Instance method
    def introduce(self):
        print(self.name)

    # Class method
    @classmethod
    def company_name(cls):
        print("ABC Construction")

    # Static method
    @staticmethod
    def calculate_wage(hours, rate):
        return hours * rate
```

### Instance Method

```python
ram = Labour()
ram.introduce()
```

Flow:

```text
ram.introduce()
      |
      v
self = ram
```

### Class Method

```python
Labour.company_name()
```

Flow:

```text
Labour.company_name()
          |
          v
      cls = Labour
```

### Static Method

```python
Labour.calculate_wage(8, 500)
```

Flow:

```text
Labour.calculate_wage(8, 500)
          |
          v
nothing automatically passed
```

---

# 14. Why Is Factory Often a Static Method?

Look at:

```python
class LabourFactory:

    @staticmethod
    def create_labour(labour_type):

        if labour_type == "carpenter":
            return Carpenter()

        elif labour_type == "electrician":
            return Electrician()

        elif labour_type == "plumber":
            return Plumber()
```

What does `create_labour()` need?

It needs:

```text
labour_type
```

It doesn't need:

```text
self
```

because we don't need a `LabourFactory` object.

It also doesn't need:

```text
cls
```

because we don't need the `LabourFactory` class itself.

Therefore:

```python
@staticmethod
```

is a good choice.

---

# 15. Why Not Make Factory an Instance Method?

You could write:

```python
class LabourFactory:

    def create_labour(self, labour_type):
        ...
```

Then you would need:

```python
factory = LabourFactory()

labour = factory.create_labour("carpenter")
```

You created a `LabourFactory` object even though the factory doesn't need object-specific state.

With a static method:

```python
labour = LabourFactory.create_labour("carpenter")
```

No factory object is required.

---

# 16. Why Not Make It a Class Method?

You could write:

```python
class LabourFactory:

    @classmethod
    def create_labour(cls, labour_type):
        ...
```

This works.

But if you don't need `cls`, a static method is simpler:

```python
@staticmethod
def create_labour(labour_type):
    ...
```

Use `@classmethod` when you actually need the class:

```python
@classmethod
def create(cls, data):
    return cls(...)
```

Use `@staticmethod` when you need neither the object nor the class.

---

# 17. Static Method Can Be Called Through an Object

You can technically do:

```python
factory = LabourFactory()

factory.create_labour("carpenter")
```

But no `factory` object is automatically passed as `self`.

It behaves essentially like:

```python
LabourFactory.create_labour("carpenter")
```

When a method doesn't need an object, this is usually clearer:

```python
LabourFactory.create_labour("carpenter")
```

---

# 18. Real-World Factory Examples

## Payment Factory

```text
"credit_card"
      |
      v
CreditCardPayment

"upi"
      |
      v
UPIPayment

"paypal"
      |
      v
PayPalPayment
```

## Database Factory

```text
"mysql"
   |
   v
MySQLConnection

"postgres"
   |
   v
PostgresConnection

"mongodb"
   |
   v
MongoConnection
```

## File Processor Factory

```text
"csv"
   |
   v
CSVProcessor

"json"
   |
   v
JSONProcessor

"xml"
   |
   v
XMLProcessor
```

## Labour Factory

```text
"carpenter"
     |
     v
Carpenter

"electrician"
     |
     v
Electrician

"plumber"
     |
     v
Plumber
```

---

# 19. Factory vs Singleton

These patterns solve different problems.

## Singleton

Question:

> How can I have/reuse one shared instance?

Example:

```python
sql1 = SQL.get_instance(config)
sql2 = SQL.get_instance(config)
```

Conceptually:

```text
sql1 ──┐
       ├──> same SQL object
sql2 ──┘
```

```text
Singleton → one shared instance
```

---

## Factory

Question:

> Which object should I create?

Example:

```python
labour = LabourFactory.create_labour("carpenter")
```

Flow:

```text
"carpenter"
      |
      v
Carpenter object
```

Another call can create another object:

```python
labour = LabourFactory.create_labour("electrician")
```

Flow:

```text
"electrician"
      |
      v
Electrician object
```

Therefore:

```text
Singleton → controls/reuses instances
Factory   → decides what type of object to create
```

---

# 20. Factory Does NOT Mean One Object

This is important.

```python
a = LabourFactory.create_labour("carpenter")
b = LabourFactory.create_labour("carpenter")
```

Normally:

```text
a → Carpenter Object A
b → Carpenter Object B
```

They can be different objects.

```python
print(a is b)
```

Normally:

```text
False
```

A Singleton instead aims for:

```text
a → Object A
b → Object A
```

So:

```text
Factory   → can create many objects
Singleton → intended to reuse one shared object
```

---

# 21. Factory + Inheritance + Polymorphism

These concepts fit together naturally.

```text
                       Labour
                          |
              +-----------+-----------+
              |           |           |
              v           v           v
         Carpenter    Electrician   Plumber
                          ^
                          |
                    subclasses
                          
                    LabourFactory
                          |
                    create_labour()
```

The factory decides:

```text
Which subclass should be created?
```

Inheritance provides:

```text
Common parent / common interface
```

Polymorphism provides:

```text
Correct subclass-specific behavior
```

Example:

```python
labour = LabourFactory.create_labour("carpenter")

labour.work()
```

The factory creates:

```text
Carpenter object
```

Then:

```python
labour.work()
```

calls:

```text
Carpenter.work()
```

because the actual object is a `Carpenter`.

---

# 22. Complete Labour Factory Example

```python
class Labour:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def work(self):
        print(f"{self.name} is working")


class Carpenter(Labour):

    def work(self):
        print(f"{self.name} is doing carpentry")


class Electrician(Labour):

    def work(self):
        print(f"{self.name} is doing electrical work")


class Plumber(Labour):

    def work(self):
        print(f"{self.name} is doing plumbing")


class LabourFactory:

    @staticmethod
    def create_labour(labour_type, name, age):

        if labour_type == "carpenter":
            return Carpenter(name, age)

        elif labour_type == "electrician":
            return Electrician(name, age)

        elif labour_type == "plumber":
            return Plumber(name, age)

        else:
            raise ValueError("Unknown labour type")


ram = LabourFactory.create_labour(
    "carpenter",
    "Ram",
    25
)

john = LabourFactory.create_labour(
    "electrician",
    "John",
    30
)

sam = LabourFactory.create_labour(
    "plumber",
    "Sam",
    28
)

ram.work()
john.work()
sam.work()
```

Output:

```text
Ram is doing carpentry
John is doing electrical work
Sam is doing plumbing
```

### Complete flow for Ram

```text
LabourFactory.create_labour("carpenter", "Ram", 25)
                         |
                         v
                labour_type == "carpenter"
                         |
                         v
                 Carpenter("Ram", 25)
                         |
                         v
                 Carpenter object
                         |
                         v
                    ram.work()
                         |
                         v
                 Carpenter.work()
```

---

# 23. When Should You Use `@staticmethod`?

Use a static method when:

```text
The method is logically related to the class
        AND
does not need instance data (`self`)
        AND
does not need class data (`cls`)
```

Example:

```python
class Labour:

    @staticmethod
    def calculate_wage(hours, rate):
        return hours * rate
```

It doesn't need:

```python
self.name
self.age
```

or:

```python
cls.some_class_variable
```

Therefore:

```python
@staticmethod
```

is appropriate.

---

# 24. Easy Rule to Remember

```text
Does the method need object data?
            |
           YES
            |
            v
       def method(self)


Does the method need class data?
            |
           YES
            |
            v
       @classmethod
            |
            v
           cls


Does it need neither?
            |
           YES
            |
            v
      @staticmethod
```

Or simply:

```text
self   → object
cls    → class
static → neither automatically
```

---

# 25. Final Cheat Sheet

| Concept         | Meaning                                                       |
| --------------- | ------------------------------------------------------------- |
| Factory Pattern | Centralizes object creation                                   |
| Factory method  | Decides which object/class to instantiate                     |
| `@staticmethod` | Method with no automatic `self` or `cls`                      |
| Instance method | Automatically receives `self`                                 |
| `@classmethod`  | Automatically receives `cls`                                  |
| `self`          | Current object                                                |
| `cls`           | Current class                                                 |
| Inheritance     | Child class gets behavior/structure from parent               |
| Polymorphism    | Same method call can behave differently for different objects |
| Singleton       | Intended to provide/reuse one shared instance                 |

## Most Important Distinction

```text
Factory
   ↓
"What object should I create?"


Singleton
   ↓
"Should I create/reuse one shared object?"


Instance method
   ↓
"I need this object's data."
   ↓
self


Class method
   ↓
"I need the class."
   ↓
cls


Static method
   ↓
"I need neither the object nor the class."
```

## One-Line Memory Trick

```text
Factory   → CREATE
Singleton → ONE
self      → OBJECT
cls       → CLASS
static    → NEITHER
```

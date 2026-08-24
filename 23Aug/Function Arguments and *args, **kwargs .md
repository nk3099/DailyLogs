````md
# Python Function Arguments — Complete Summary

## 1. Types of Function Arguments

Python functions can receive arguments in several ways.

The main types are:

1. Positional arguments
2. Keyword arguments
3. Default arguments
4. Variable-length positional arguments (`*args`)
5. Variable-length keyword arguments (`**kwargs`)
6. Keyword-only arguments

---

# 2. Parameter vs Argument

### Parameter

A **parameter** is the variable defined in the function.

```python
def greet(name):
    print(name)
````

Here:

```text
name → parameter
```

### Argument

An **argument** is the actual value passed when calling the function.

```python
greet("Neeraj")
```

Here:

```text
"Neeraj" → argument
```

---

# 3. Positional Arguments

Arguments are assigned based on their **position/order**.

```python
def introduce(name, age):
    print(name)
    print(age)

introduce("Neeraj", 25)
```

Mapping:

```text
"name" → "Neeraj"
"age"  → 25
```

The order matters.

```python
introduce(25, "Neeraj")
```

would produce:

```text
name = 25
age = "Neeraj"
```

Python does not know that `25` was "supposed" to be the age.

---

# 4. Keyword Arguments

Instead of relying on position, provide the parameter name.

```python
def introduce(name, age):
    print(name)
    print(age)

introduce(name="Neeraj", age=25)
```

You can also change the order:

```python
introduce(age=25, name="Neeraj")
```

This works because Python uses the parameter names.

```text
name="Neeraj" → name
age=25        → age
```

---

# 5. Positional + Keyword Arguments

You can combine them.

```python
def introduce(name, age, city):
    print(name, age, city)

introduce("Neeraj", age=25, city="Delhi")
```

This is valid.

But positional arguments must come **before** keyword arguments.

### Invalid

```python
introduce(name="Neeraj", 25, "Delhi")
```

Why?

Python has already started supplying arguments by keyword, so a positional argument cannot come afterward.

---

# 6. Default Arguments

A parameter can have a default value.

```python
def greet(name, city="Delhi"):
    print(name, city)
```

Now:

```python
greet("Neeraj")
```

uses:

```text
name = "Neeraj"
city = "Delhi"
```

You can override it:

```python
greet("Neeraj", "Bangalore")
```

Result:

```text
name = "Neeraj"
city = "Bangalore"
```

---

# 7. `*args`

`*args` allows a function to accept a **variable number of positional arguments**.

```python
def add_numbers(*args):
    print(args)

add_numbers(10, 20, 30, 40)
```

Output:

```python
(10, 20, 30, 40)
```

`args` is a **tuple**.

```python
args = (10, 20, 30, 40)
```

You can loop through it:

```python
def add_numbers(*args):
    total = 0

    for number in args:
        total += number

    return total

print(add_numbers(10, 20, 30))
```

Output:

```text
60
```

The name `args` is conventional.

This is also valid:

```python
def add_numbers(*numbers):
    return sum(numbers)
```

The important part is `*`.

---

# 8. Why Use `*args`?

Suppose you don't know how many numbers the user will provide.

Without `*args`:

```python
def add(a, b, c):
    return a + b + c
```

This only supports exactly three values.

With `*args`:

```python
def add(*numbers):
    return sum(numbers)
```

You can do:

```python
add(10)
add(10, 20)
add(10, 20, 30)
add(10, 20, 30, 40, 50)
```

All work.

---

# 9. `**kwargs`

`**kwargs` allows a function to accept a **variable number of keyword arguments**.

```python
def student(**kwargs):
    print(kwargs)

student(
    name="Neeraj",
    age=25,
    city="Delhi"
)
```

Output:

```python
{
    "name": "Neeraj",
    "age": 25,
    "city": "Delhi"
}
```

`kwargs` is a **dictionary**.

```text
**kwargs → dictionary
```

Again, `kwargs` is only a conventional name.

This is also valid:

```python
def student(**details):
    print(details)
```

The important part is `**`.

---

# 10. `*args` vs `**kwargs`

| Feature      | `*args`                              | `**kwargs`                       |
| ------------ | ------------------------------------ | -------------------------------- |
| Accepts      | Positional arguments                 | Keyword arguments                |
| Stored as    | Tuple                                | Dictionary                       |
| Example      | `10, 20, 30`                         | `name="Neeraj"`                  |
| Access       | `args[0]`                            | `kwargs["name"]`                 |
| Main purpose | Variable number of positional values | Variable number of named options |

Think:

```text
10, 20, 30
     ↓
   *args
     ↓
(10, 20, 30)
```

and:

```text
name="Neeraj", age=25
          ↓
       **kwargs
          ↓
{"name": "Neeraj", "age": 25}
```

---

# 11. Using `*args` and `**kwargs` Together

You can use both:

```python
def test(*args, **kwargs):
    print(args)
    print(kwargs)
```

Call:

```python
test(
    10,
    20,
    30,
    name="Neeraj",
    age=25
)
```

Python separates them:

```text
10, 20, 30
     ↓
   *args
     ↓
(10, 20, 30)
```

and:

```text
name="Neeraj", age=25
          ↓
       **kwargs
          ↓
{"name": "Neeraj", "age": 25}
```

Output:

```text
(10, 20, 30)
{'name': 'Neeraj', 'age': 25}
```

So:

```python
def test(*args, **kwargs):
```

means:

> Accept any number of positional arguments and any number of keyword arguments.

---

# 12. Why Are Both Useful?

They provide flexibility.

All of these can work:

```python
test()
```

```python
test(10, 20)
```

```python
test(name="Neeraj")
```

```python
test(10, 20, name="Neeraj")
```

```python
test(
    10,
    20,
    30,
    name="Neeraj",
    age=25,
    city="Delhi"
)
```

The function doesn't need to know in advance exactly how many arguments will be supplied.

---

# 13. Keyword-Only Arguments

Consider:

```python
def test(*args, a, b):
    print(args)
    print(a)
    print(b)
```

Parameters after `*args` become **keyword-only**.

Therefore:

```python
test(10, 20, 30, a=100, b=200)
```

is valid.

The mapping is:

```text
10, 20, 30 → *args

a=100       → a

b=200       → b
```

But:

```python
test(10, 20, 30, 100, 200)
```

is invalid.

Why?

Because all extra positional arguments go into `*args`:

```text
args = (10, 20, 30, 100, 200)
```

Python will not automatically put `100` into `a` and `200` into `b`.

Therefore `a` and `b` must be provided by name:

```python
test(10, 20, 30, a=100, b=200)
```

---

# 14. `*args` and `**kwargs` Order

Correct:

```python
def test(*args, **kwargs):
    pass
```

Incorrect:

```python
def test(**kwargs, *args):
    pass
```

`**kwargs` comes at the end.

You can also have keyword-only parameters between them:

```python
def test(*args, a, b, **kwargs):
    pass
```

For example:

```python
test(
    10,
    20,
    a=100,
    b=200,
    c=300
)
```

Mapping:

```text
args   = (10, 20)

a      = 100

b      = 200

kwargs = {
    "c": 300
}
```

---

# 15. Real Application — Shopping Basket

Suppose we want to calculate a shopping bill.

We don't know how many products the customer will buy.

So use `*args` for product prices.

```python
def calculate_bill(*prices):
    total = sum(prices)
    return total
```

Call:

```python
calculate_bill(500, 200, 300)
```

Calculation:

```text
500 + 200 + 300 = 1000
```

Result:

```text
1000
```

Here:

```python
prices = (500, 200, 300)
```

---

# 16. Add Discount, Tax and Shipping

Now we want optional billing settings:

```text
discount
tax
shipping
```

We can use `**kwargs`.

```python
def calculate_bill(*prices, **kwargs):

    total = sum(prices)

    discount = kwargs.get("discount", 0)
    tax = kwargs.get("tax", 0)
    shipping = kwargs.get("shipping", 0)

    total = total - discount
    total = total + tax
    total = total + shipping

    return total
```

Call:

```python
bill = calculate_bill(
    500,
    200,
    300,
    discount=100,
    tax=50,
    shipping=30
)

print(bill)
```

Calculation:

```text
Products:

500 + 200 + 300
= 1000

Discount:

1000 - 100
= 900

Tax:

900 + 50
= 950

Shipping:

950 + 30
= 980
```

Output:

```text
980
```

Internally:

```python
prices = (500, 200, 300)

kwargs = {
    "discount": 100,
    "tax": 50,
    "shipping": 30
}
```

---

# 17. Why This Is Useful in Real Applications

Imagine an e-commerce application.

Different customers may have different billing options:

```python
calculate_bill(500, 200)
```

or:

```python
calculate_bill(
    500,
    200,
    discount=100
)
```

or:

```python
calculate_bill(
    500,
    200,
    discount=100,
    tax=50
)
```

or:

```python
calculate_bill(
    500,
    200,
    discount=100,
    tax=50,
    shipping=30,
    cashback=20
)
```

You don't have to change the function every time a new optional setting is introduced.

---

# 18. Another Real Application — HTTP/API Status Codes

`**kwargs` is commonly useful when a function has many optional configuration values.

For example:

```python
def create_response(data, **kwargs):

    status_code = kwargs.get("status_code", 200)
    headers = kwargs.get("headers", {})
    message = kwargs.get("message", "Success")

    return {
        "data": data,
        "status_code": status_code,
        "headers": headers,
        "message": message
    }
```

Call:

```python
response = create_response(
    {"name": "Neeraj"},
    status_code=201,
    headers={"Content-Type": "application/json"},
    message="User created"
)
```

Result:

```python
{
    "data": {"name": "Neeraj"},
    "status_code": 201,
    "headers": {
        "Content-Type": "application/json"
    },
    "message": "User created"
}
```

Here:

```text
data
 ↓
normal parameter

status_code
headers
message
 ↓
**kwargs
```

This is useful when a function has many optional settings.

---

# 19. HTTP Status Codes Example

For APIs, status codes commonly include:

```text
200 → OK / successful request
201 → Resource created
400 → Bad request
401 → Authentication required/failed
403 → Forbidden
404 → Resource not found
500 → Internal server error
```

You could create a flexible response function:

```python
def api_response(data=None, **kwargs):

    status_code = kwargs.get("status_code", 200)
    message = kwargs.get("message", "Success")

    return {
        "status_code": status_code,
        "message": message,
        "data": data
    }
```

Successful response:

```python
api_response(
    {"id": 101},
    status_code=200,
    message="User found"
)
```

Created response:

```python
api_response(
    {"id": 101},
    status_code=201,
    message="User created"
)
```

Error response:

```python
api_response(
    None,
    status_code=404,
    message="User not found"
)
```

Here `**kwargs` allows the caller to provide different optional response settings.

---

# 20. `*args` and `**kwargs` in Decorators

They are especially important in decorators because the decorator often does not know what arguments the original function will receive.

Example:

```python
def my_decorator(func):

    def wrapper(*args, **kwargs):
        print("Before function")

        result = func(*args, **kwargs)

        print("After function")

        return result

    return wrapper
```

Suppose the original function is:

```python
@my_decorator
def add(a, b):
    return a + b
```

Call:

```python
add(10, 20)
```

The wrapper receives:

```python
args = (10, 20)
kwargs = {}
```

Another function might be:

```python
@my_decorator
def greet(name, city="Delhi"):
    print(name, city)
```

Call:

```python
greet(
    "Neeraj",
    city="Delhi"
)
```

The wrapper receives:

```python
args = ("Neeraj",)

kwargs = {
    "city": "Delhi"
}
```

That's why decorators commonly use:

```python
def wrapper(*args, **kwargs):
```

It makes the wrapper flexible enough to work with functions having different argument signatures.

---

# 21. Unpacking — `*` During Function Calls

There is another use of `*`.

Suppose:

```python
numbers = [10, 20, 30]
```

You can do:

```python
def add(a, b, c):
    return a + b + c

add(*numbers)
```

This is equivalent to:

```python
add(10, 20, 30)
```

Here `*` is **unpacking** the list.

So:

```text
Function definition:

*args
   ↓
collect positional arguments


Function call:

*list
   ↓
unpack positional values
```

---

# 22. Unpacking — `**` During Function Calls

Suppose:

```python
details = {
    "name": "Neeraj",
    "age": 25
}
```

Function:

```python
def introduce(name, age):
    print(name, age)
```

You can do:

```python
introduce(**details)
```

This is equivalent to:

```python
introduce(
    name="Neeraj",
    age=25
)
```

So:

```text
Function definition:

**kwargs
    ↓
collect keyword arguments


Function call:

**dictionary
    ↓
unpack keyword arguments
```

---

# 23. Complete Mental Model

```text
                     FUNCTION ARGUMENTS
                            |
            ┌───────────────┼────────────────┐
            |               |                |
       Positional       Keyword          Default
            |               |                |
            |               |                |
          10, 20        name="Neeraj"     age=25
            |               |
            ↓               ↓
          *args          **kwargs
            |               |
            ↓               ↓
          tuple          dictionary
```

And:

```text
*args
  ↓
Many positional arguments

**kwargs
  ↓
Many keyword arguments
```

---

# 24. Quick Reference

```python
# Positional arguments
def test(a, b):
    pass

test(10, 20)
```

```python
# Keyword arguments
def test(a, b):
    pass

test(a=10, b=20)
```

```python
# Default argument
def test(a, b=100):
    pass

test(10)
```

```python
# Variable positional arguments
def test(*args):
    pass

test(10, 20, 30)
```

```python
# Variable keyword arguments
def test(**kwargs):
    pass

test(name="Neeraj", age=25)
```

```python
# Both
def test(*args, **kwargs):
    pass

test(
    10,
    20,
    name="Neeraj",
    age=25
)
```

```python
# Keyword-only arguments
def test(*args, name, age):
    pass

test(
    10,
    20,
    name="Neeraj",
    age=25
)
```

---

# 25. Final Rules to Remember

### Rule 1

```python
*args
```

means:

> Variable number of **positional arguments**.

Stored as:

```python
tuple
```

---

### Rule 2

```python
**kwargs
```

means:

> Variable number of **keyword arguments**.

Stored as:

```python
dictionary
```

---

### Rule 3

Both together:

```python
def function(*args, **kwargs):
```

means:

> Accept any number of positional and keyword arguments.

---

### Rule 4

After `*args`, normal parameters become keyword-only:

```python
def function(*args, a, b):
    pass
```

Call:

```python
function(10, 20, a=30, b=40)
```

---

### Rule 5

`**kwargs` comes after `*args`:

```python
def function(*args, **kwargs):
    pass
```

Not:

```python
def function(**kwargs, *args):  # ❌
    pass
```

---

### Rule 6

`*` and `**` can also **unpack** values during a function call:

```python
numbers = [10, 20, 30]

add(*numbers)
```

and:

```python
details = {
    "name": "Neeraj",
    "age": 25
}

introduce(**details)
```

---

## One-Line Summary

```text
*args    → collect many positional arguments → tuple

**kwargs → collect many keyword arguments   → dictionary

*args + **kwargs
         → flexible function accepting both types
```

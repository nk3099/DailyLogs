# Decorators in Python 
Decorators are a powerful and elegant way to modify the behavior of functions or classes — without changing their code.

# 🧠 Simple Definition:
A decorator is a function that:

- Takes another function as input

- Adds some functionality

- Returns a new function

# 🛠 Basic Syntax:
```
@decorator_name
def some_function():
    ...
```
This is equivalent to:

```
some_function = decorator_name(some_function)
```

####  ✅ Example: A Simple Decorator

```def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def greet():
    print("Hello!")

greet()
```

#### 📦 Output:

```
Before function call
Hello!
After function call
```

# 🔄 Decorator with Arguments
```
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi!")

say_hi()
```

#### 📦 Output:

```
Hi!
Hi!
Hi!
```

# 🎯 Use Cases
- Logging

- Authentication

- Timing (performance monitoring)

- Caching results

- Validating inputs

# ✅ Real Example: @app.get() in FastAPI

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome!"}
```
Here, @app.get("/") is a decorator that registers the home() function as a route handler for HTTP GET requests to /.

# 📌 Summary
Decorator	 -> A function that wraps another <br>
@decorator	-> Syntactic sugar for applying it <br>
wrapper()	-> Inner function that adds logic


# Python Decorators — Complete Concept Summary

## 1. What is a Decorator?

A **decorator** is a function that takes another function and adds/modifies its behavior **without changing the original function's code**.

Example:

```python
def decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")

    return wrapper
```

Usage:

```python
@decorator
def hello():
    print("Hello")
```

When we call:

```python
hello()
```

the decorator code runs around the original `hello()` function.

---

# 2. The Most Important Rule

When you see:

```python
@decorator
def hello():
    pass
```

Python essentially converts it to:

```python
def hello():
    pass

hello = decorator(hello)
```

This is the key concept.

The original `hello` function is passed to `decorator`.

```text
Original function
      ↓
decorator(function)
      ↓
returns wrapper
      ↓
name now points to wrapper
```

Therefore:

```python
hello()
```

actually calls the returned `wrapper()`.

---

# 3. Basic Decorator Structure

The standard pattern is:

```python
def decorator(func):

    def wrapper(*args, **kwargs):
        # extra behavior

        result = func(*args, **kwargs)

        # extra behavior

        return result

    return wrapper
```

Usage:

```python
@decorator
def hello(name):
    print(f"Hello {name}")
```

---

# 4. What Does `decorator(func)` Receive?

In the standard decorator pattern:

```python
def decorator(func):
```

`func` receives the **original function**.

For:

```python
@decorator
def hello():
    print("Hello")
```

Python does:

```python
hello = decorator(hello)
```

Therefore:

```text
decorator
    ↓
func = original hello function
```

So:

```text
decorator → receives the function
```

### Important

This is **not a universal rule for every function named `decorator`**.

It happens because we wrote:

```python
def decorator(func):
```

A decorator can technically be designed to accept other things.

But a normal decorator has the pattern:

```python
def decorator(func):
    ...
```

---

# 5. What is the Wrapper?

The wrapper is the function that **replaces the original function** after decoration.

Example:

```python
def decorator(func):

    def wrapper():
        print("Before")
        func()
        print("After")

    return wrapper
```

When:

```python
@decorator
def hello():
    print("Hello")
```

Python effectively does:

```python
hello = decorator(hello)
```

And `decorator(hello)` returns `wrapper`.

Therefore:

```text
Before decoration:

hello → original hello function


After decoration:

hello → wrapper
            ↓
       original hello
```

So when we call:

```python
hello()
```

we are actually calling:

```python
wrapper()
```

---

# 6. Why Does the Wrapper Need `*args, **kwargs`?

Because **the wrapper receives the arguments when the decorated function is called**.

Suppose:

```python
@decorator
def add(a, b):
    print(a + b)
```

After decoration:

```text
add → wrapper
```

Therefore:

```python
add(10, 20)
```

actually means:

```python
wrapper(10, 20)
```

So the wrapper must be able to receive those arguments:

```python
def wrapper(*args, **kwargs):
```

Then it forwards them:

```python
func(*args, **kwargs)
```

Flow:

```text
Caller
  ↓
wrapper(*args, **kwargs)
  ↓
original function(*args, **kwargs)
```

---

# 7. `*args`

`*args` captures **positional arguments**.

Example:

```python
def wrapper(*args):
    print(args)
```

Call:

```python
wrapper(10, 20, 30)
```

Then:

```text
args = (10, 20, 30)
```

The `*` allows us to unpack them again:

```python
func(*args)
```

which becomes:

```python
func(10, 20, 30)
```

---

# 8. `**kwargs`

`**kwargs` captures **keyword arguments**.

Example:

```python
def wrapper(**kwargs):
    print(kwargs)
```

Call:

```python
wrapper(a=10, b=20)
```

Then:

```text
kwargs = {
    "a": 10,
    "b": 20
}
```

The `**` allows us to unpack them again:

```python
func(**kwargs)
```

which becomes:

```python
func(a=10, b=20)
```

---

# 9. Why Use Both `*args` and `**kwargs`?

A decorator usually doesn't know how the original function will be called.

It could be:

```python
func(10, 20)
```

or:

```python
func(a=10, b=20)
```

or:

```python
func(10, b=20)
```

Therefore the generic decorator uses:

```python
def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
```

This allows the decorator to work with many different function signatures.

---

# 10. Decorator Without Configuration

The simplest decorator does **not** need an outer function.

Example:

```python
def log_call(func):

    def wrapper(*args, **kwargs):
        print("Function is being called")
        result = func(*args, **kwargs)
        return result

    return wrapper
```

Usage:

```python
@log_call
def add(a, b):
    return a + b
```

Python converts:

```python
add = log_call(add)
```

Flow:

```text
@log_call
    ↓
log_call(original_function)
    ↓
func = original_function
    ↓
returns wrapper
    ↓
add = wrapper
```

Then:

```python
add(10, 20)
```

becomes:

```text
wrapper(10, 20)
      ↓
args = (10, 20)
      ↓
func(*args)
      ↓
original add(10, 20)
```

---

# 11. Decorator With Configuration

Sometimes we want to configure the decorator.

Example:

```python
@repeat(3)
def hello():
    print("Hello")
```

Here `3` is **not the function**.

It is configuration for the decorator.

Therefore we need an additional outer function:

```python
def repeat(n):

    def decorator(func):

        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)

        return wrapper

    return decorator
```

Usage:

```python
@repeat(3)
def hello(name):
    print(name)
```

---

# 12. Why Are There Three Functions?

For a configurable decorator:

```python
def repeat(n):

    def decorator(func):

        def wrapper(*args, **kwargs):
            ...

        return wrapper

    return decorator
```

There are three levels because there are three different things:

```text
repeat
  ↓
configuration

decorator
  ↓
original function

wrapper
  ↓
function-call arguments
```

Specifically:

```text
repeat(3)
    ↓
n = 3

decorator(hello)
    ↓
func = hello

wrapper("Ram")
    ↓
args = ("Ram",)
```

---

# 13. Complete `@repeat(3)` Flow

Given:

```python
def repeat(n):

    def decorator(func):

        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)

        return wrapper

    return decorator
```

And:

```python
@repeat(3)
def hello(name):
    print(name)
```

Python effectively performs:

### Step 1

```python
repeat(3)
```

Therefore:

```text
n = 3
```

`repeat()` returns `decorator`.

---

### Step 2

Python now applies the returned decorator:

```python
hello = decorator(hello)
```

Therefore:

```text
func = original hello
```

`decorator()` returns `wrapper`.

---

### Step 3

Now:

```text
hello → wrapper
```

When we call:

```python
hello("Ram")
```

we are actually calling:

```python
wrapper("Ram")
```

Therefore:

```text
args = ("Ram",)
```

---

### Step 4

Wrapper executes:

```python
for _ in range(n):
```

Since:

```text
n = 3
```

this becomes:

```python
for _ in range(3):
```

Then:

```python
func(*args, **kwargs)
```

calls:

```python
original_hello("Ram")
```

three times.

---

# 14. Three Different Values at Three Different Stages

This is the easiest way to remember the whole thing:

```text
┌──────────────────────────────────────────────┐
│ 1. repeat(3)                                 │
│                                              │
│    n = 3                                     │
│    ↓                                         │
│    configuration                             │
└──────────────────────────────────────────────┘

                    ↓

┌──────────────────────────────────────────────┐
│ 2. decorator(hello)                          │
│                                              │
│    func = hello                              │
│    ↓                                         │
│    original function                         │
└──────────────────────────────────────────────┘

                    ↓

┌──────────────────────────────────────────────┐
│ 3. wrapper("Ram")                            │
│                                              │
│    args = ("Ram",)                            │
│    ↓                                         │
│    function-call arguments                   │
└──────────────────────────────────────────────┘
```

So:

```text
repeat     → configuration
decorator  → function
wrapper    → function arguments
```

---

# 15. Does Wrapper Receive `3`?

**No.**

This is a common misunderstanding.

In:

```python
@repeat(3)
def hello(name):
    print(name)

hello("Ram")
```

the wrapper receives:

```text
"Ram"
```

not `3`.

`3` is stored in:

```text
n
```

The wrapper can still access `n` because of a **closure**.

---

# 16. Closure

A **closure** occurs when an inner function remembers variables from its enclosing scope even after the outer function has finished executing.

Example:

```python
def outer(x):

    def inner():
        print(x)

    return inner
```

Now:

```python
f = outer(10)
f()
```

Output:

```text
10
```

Why does `inner()` still know `x = 10`?

Because `inner` **closed over** `x`.

Conceptually:

```text
outer(10)
   │
   ├── x = 10
   │
   └── inner
         │
         └── remembers x = 10
```

---

# 17. Closure in a Decorator

In:

```python
def repeat(n):

    def decorator(func):

        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)

        return wrapper

    return decorator
```

`wrapper` uses:

```python
n
```

But `n` belongs to `repeat()`.

After `repeat()` returns, why can `wrapper` still use it?

Because `wrapper` has a closure over `n`.

```text
repeat(3)
   │
   ├── n = 3
   │
   └── decorator
         │
         └── wrapper
               │
               └── remembers n = 3
```

Therefore:

```python
for _ in range(n):
```

still works.

---

# 18. Decorator vs Closure

They are related but **not the same concept**.

### Decorator

A decorator is about:

> **Taking a function and modifying/extending its behavior.**

```python
def decorator(func):
    ...
    return wrapper
```

### Closure

A closure is about:

> **An inner function remembering variables from an enclosing scope.**

```python
def outer(x):
    def inner():
        print(x)
    return inner
```

A decorator with configuration often uses a closure.

Example:

```text
Configurable Decorator
        │
        ├── Decorator
        │
        └── Closure
              ↓
        remembers configuration
```

---

# 19. Parameters vs Arguments

This distinction is important when understanding decorators.

### Parameter

A variable defined in a function definition:

```python
def repeat(n):
```

Here:

```text
n = parameter
```

### Argument

The actual value passed during the function call:

```python
repeat(3)
```

Here:

```text
3 = argument
```

Similarly:

```python
def decorator(func):
```

`func` is a parameter.

When:

```python
decorator(hello)
```

runs:

```text
hello = argument
func = parameter receiving hello
```

---

# 20. `@` Syntax Is Just Syntactic Sugar

This:

```python
@decorator
def hello():
    pass
```

is equivalent to:

```python
def hello():
    pass

hello = decorator(hello)
```

And:

```python
@repeat(3)
def hello():
    pass
```

is effectively:

```python
def hello():
    pass

hello = repeat(3)(hello)
```

The second version makes the two stages easier to see:

```text
repeat(3)
    ↓
returns decorator
    ↓
decorator(hello)
    ↓
returns wrapper
    ↓
hello = wrapper
```

---

# 21. Decorator Without Arguments vs With Arguments

## Without decorator configuration

```python
@decorator
def hello():
    pass
```

Conceptually:

```python
hello = decorator(hello)
```

Pattern:

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

---

## With decorator configuration

```python
@decorator(3)
def hello():
    pass
```

Conceptually:

```python
hello = decorator(3)(hello)
```

Pattern:

```python
def decorator(config):

    def actual_decorator(func):

        def wrapper(*args, **kwargs):
            ...
        
        return wrapper

    return actual_decorator
```

The extra function is needed because:

```text
decorator(3)
```

must first process the configuration and return a function that can later receive `hello`.

---

# 22. General Rule for Decorators

### Normal decorator

```python
@decorator
def func(...):
    ...
```

Flow:

```text
decorator(func)
    ↓
returns wrapper
    ↓
func = wrapper
```

### Configurable decorator

```python
@decorator(config)
def func(...):
    ...
```

Flow:

```text
decorator(config)
    ↓
returns actual_decorator
    ↓
actual_decorator(func)
    ↓
returns wrapper
    ↓
func = wrapper
```

### When function is called

```python
func(arguments)
```

Flow:

```text
wrapper(arguments)
    ↓
original_function(arguments)
```

---

# 23. Final Mental Model

## Normal decorator

```text
@decorator
    ↓
decorator(original_function)
    ↓
wrapper
    ↓
function_name = wrapper
    ↓
function_name(arguments)
    ↓
wrapper(arguments)
    ↓
original_function(arguments)
```

## Configurable decorator

```text
@decorator(config)
    ↓
decorator(config)
    ↓
returns actual_decorator
    ↓
actual_decorator(original_function)
    ↓
returns wrapper
    ↓
function_name = wrapper
    ↓
function_name(arguments)
    ↓
wrapper(arguments)
    ↓
original_function(arguments)
```

## Closure

```text
outer(value)
    ↓
inner function remembers value
    ↓
outer finishes
    ↓
inner still has access to value
```

---

# 24. One Final Cheat Sheet

```text
DECORATOR
────────────────────────────────────────

@decorator
def func():
    pass

Equivalent to:

func = decorator(func)


CONFIGURABLE DECORATOR
────────────────────────────────────────

@decorator(3)
def func():
    pass

Equivalent to:

func = decorator(3)(func)


NORMAL DECORATOR
────────────────────────────────────────

def decorator(func):
    def wrapper(*args, **kwargs):
        ...
    return wrapper

decorator → receives original function
wrapper   → receives function-call arguments


CONFIGURABLE DECORATOR
────────────────────────────────────────

def decorator(config):
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            ...
        return wrapper
    return actual_decorator

outer function
    → configuration

actual decorator
    → original function

wrapper
    → function-call arguments


CLOSURE
────────────────────────────────────────

An inner function remembers variables
from its enclosing scope.

outer(x)
    ↓
inner()
    ↓
inner remembers x


ARGS
────────────────────────────────────────

*args
    → positional arguments

**kwargs
    → keyword arguments


PARAMETER vs ARGUMENT
────────────────────────────────────────

def func(x):
          ↑
       parameter

func(10)
     ↑
   argument
```

## The core idea to remember

> **A decorator receives a function, a wrapper receives the arguments used to call that function, and a configurable decorator has an outer layer that receives the configuration. A closure allows the inner wrapper to remember that configuration.**

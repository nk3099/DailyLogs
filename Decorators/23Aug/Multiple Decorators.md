````md
# Python Multiple Decorators — Stacking, Chaining & Execution Flow

## 1. What Are Multiple Decorators?

When **more than one decorator is applied to the same function**, they are called **multiple decorators**.

This is also commonly referred to as:

- **Multiple decorators**
- **Stacked decorators**
- **Decorator stacking**
- **Decorator chaining**
- **Decorator composition**

Example:

```python
@decorator1
@decorator2
def my_function():
    pass
````

The most important thing to understand is:

> The decorator written at the bottom is applied first, but the decorator written at the top executes first when the final function is called.

---

# 2. The Most Important Rule

Consider:

```python
@A
@B
def func():
    pass
```

Python interprets this as:

```python
func = A(B(func))
```

So the decoration happens like this:

```text
Original function
      ↓
B wraps original
      ↓
B.wrapper
      ↓
A wraps B.wrapper
      ↓
A.wrapper
```

Final structure:

```text
A.wrapper
    ↓
B.wrapper
    ↓
Original function
```

---

# 3. Three Different Orders

This is where multiple decorators can become confusing.

For:

```python
@A
@B
def func():
    pass
```

## A. Decoration / Application Order

Decorators are applied:

```text
BOTTOM → TOP

B → A
```

Because:

```python
func = A(B(func))
```

---

## B. Normal Function Execution

When we call:

```python
func()
```

execution happens:

```text
TOP → BOTTOM → ORIGINAL

A → B → Original
```

The outermost wrapper runs first.

---

## C. Exception Propagation

If the original function raises an exception:

```text
Original → B → A
```

The exception travels **from the inside toward the outside** until some decorator catches it.

Therefore, memorize:

```text
DECORATION:
BOTTOM → TOP

NORMAL EXECUTION:
TOP → BOTTOM → ORIGINAL

EXCEPTION:
INNER → OUTER
```

---

# 4. Why Does the Bottom Decorator Apply First?

Consider:

```python
@A
@B
def func():
    pass
```

Python first does:

```python
func = B(func)
```

Then:

```python
func = A(func)
```

But at this point `func` is no longer the original function.

It is already:

```text
B.wrapper
    ↓
Original
```

So `A` wraps that:

```text
A.wrapper
    ↓
B.wrapper
    ↓
Original
```

This is why:

> **The bottom decorator is applied first.**

---

# 5. What Does `func` Mean Inside a Decorator?

Consider:

```python
def decorator(func):

    def wrapper():
        func()

    return wrapper
```

Here `func` means:

> The function that this decorator is currently receiving.

With multiple decorators, that function may be another wrapper.

For:

```python
@A
@B
def original():
    pass
```

inside `B`:

```text
func → original
```

But inside `A`:

```text
func → B.wrapper
```

So:

```text
A.wrapper
    ↓
B.wrapper
    ↓
original
```

This is the key concept behind decorator chaining.

---

# 6. Example 1 — One Decorator

First consider a single decorator:

```python
from datetime import datetime


def etl_logs(func):

    def wrapper():

        print("this is from decorator")

        func()

    return wrapper


@etl_logs
def load_table():

    print("load starting")
    print("start time", datetime.now())
    print("loading data into table")
    print("load done")
    print("end time", datetime.now())


load_table()
```

## Meaning of `@etl_logs`

This:

```python
@etl_logs
def load_table():
```

means:

```python
load_table = etl_logs(load_table)
```

The structure becomes:

```text
load_table
    ↓
etl_logs.wrapper
    ↓
original load_table
```

## Output

```text
this is from decorator
load starting
start time 2026-05-22 07:17:57.207941
loading data into table
load done
end time 2026-05-22 07:17:57.207952
```

## Flow

```text
load_table()
     ↓
etl_logs.wrapper()
     ↓
print("this is from decorator")
     ↓
func()
     ↓
original load_table()
     ↓
load starting
     ↓
start time
     ↓
loading data
     ↓
load done
     ↓
end time
```

---

# 7. Example 2 — `handle_failure` Outside `etl_logs`

Now we have two decorators:

```python
from datetime import datetime


def etl_logs(func):

    def wrapper(*args, **kwargs):

        print("load starting")
        print("start time", datetime.now())

        func(*args, **kwargs)

        print("load done")
        print("end time", datetime.now())

    return wrapper


def handle_failure(func):

    def wrapper(*args, **kwargs):

        try:
            func(*args, **kwargs)

        except Exception as e:

            print("job failed")
            print("error:", e)

    return wrapper


@handle_failure
@etl_logs
def load_table(tablename, schema, databasename):

    print(f"loading data into {databasename}.{schema}.{tablename}")

    a = 1 / 0

    print(a)


load_table("sales", "dbo", "namastesql")
```

---

# 8. Example 2 — Output

The output is:

```text
load starting
start time 2026-05-22 07:43:08.008890
loading data into namastesql.dbo.sales
job failed
error: division by zero
```

Notice:

```text
load done
end time
```

are **NOT printed**.

Why?

We will trace the flow.

---

# 9. Example 2 — First Understand the Decoration

We have:

```python
@handle_failure
@etl_logs
def load_table(...):
```

Python converts this into:

```python
load_table = handle_failure(etl_logs(load_table))
```

The bottom decorator is applied first.

### Step 1

```python
etl_logs(load_table)
```

creates:

```text
etl_logs.wrapper
      ↓
original load_table
```

### Step 2

Then:

```python
handle_failure(etl_logs.wrapper)
```

creates:

```text
handle_failure.wrapper
      ↓
etl_logs.wrapper
      ↓
original load_table
```

Therefore the final structure is:

```text
load_table
    ↓
handle_failure.wrapper
    ↓
etl_logs.wrapper
    ↓
original load_table
```

---

# 10. Example 2 — Normal Execution Flow

We call:

```python
load_table("sales", "dbo", "namastesql")
```

The final `load_table` is actually:

```text
handle_failure.wrapper
```

So execution starts here:

```text
load_table()
    ↓
handle_failure.wrapper
    ↓
etl_logs.wrapper
    ↓
original load_table
```

### Step 1 — `handle_failure`

It executes:

```python
try:
    func(*args, **kwargs)
```

Here:

```text
func → etl_logs.wrapper
```

So it calls `etl_logs.wrapper`.

---

### Step 2 — `etl_logs`

It prints:

```text
load starting
start time ...
```

Then it executes:

```python
func(*args, **kwargs)
```

Here:

```text
func → original load_table
```

So the original function starts.

---

### Step 3 — Original Function

It prints:

```text
loading data into namastesql.dbo.sales
```

Then:

```python
a = 1 / 0
```

causes:

```text
ZeroDivisionError: division by zero
```

---

# 11. Example 2 — Exception Flow

The normal flow was:

```text
handle_failure
      ↓
etl_logs
      ↓
original
```

But when the original function fails, the exception travels outward:

```text
original
    ↑
etl_logs
    ↑
handle_failure
```

`etl_logs` has no `try/except`.

Therefore it cannot handle the error.

The error continues outward to:

```text
handle_failure
```

`handle_failure` has:

```python
try:
    func(*args, **kwargs)

except Exception as e:
    print("job failed")
    print("error:", e)
```

So it catches the error.

---

# 12. Why Does Example 2 NOT Print `load done`?

Inside `etl_logs`:

```python
func(*args, **kwargs)

print("load done")
print("end time", datetime.now())
```

The exception occurs during:

```python
func(*args, **kwargs)
```

Therefore Python immediately leaves that function.

It does NOT continue to:

```python
print("load done")
print("end time", datetime.now())
```

Instead:

```text
original
    ↓
ERROR
    ↑
etl_logs
    ↑
handle_failure catches
```

Therefore output ends with:

```text
job failed
error: division by zero
```

---

# 13. Example 3 — Reverse the Decorators

Now change the order:

```python
@etl_logs
@handle_failure
def load_table(tablename, schema, databasename):

    print(f"loading data into {databasename}.{schema}.{tablename}")

    a = 1 / 0

    print(a)
```

The important change is:

```text
Example 2:
@handle_failure
@etl_logs

Example 3:
@etl_logs
@handle_failure
```

---

# 14. Example 3 — Equivalent Code

This:

```python
@etl_logs
@handle_failure
def load_table():
    pass
```

means:

```python
load_table = etl_logs(handle_failure(load_table))
```

Again, the bottom decorator is applied first.

### Step 1

```python
handle_failure(load_table)
```

creates:

```text
handle_failure.wrapper
      ↓
original load_table
```

### Step 2

```python
etl_logs(handle_failure.wrapper)
```

creates:

```text
etl_logs.wrapper
      ↓
handle_failure.wrapper
      ↓
original load_table
```

Final structure:

```text
load_table
    ↓
etl_logs.wrapper
    ↓
handle_failure.wrapper
    ↓
original load_table
```

---

# 15. Example 3 — Output

The output is:

```text
load starting
start time 2026-05-22 07:40:59.889339
loading data into namastesql.dbo.sales
job failed
error: division by zero
load done
end time 2026-05-22 07:40:59.889354
```

The important difference is:

```text
load done
end time
```

ARE printed.

Why?

Because this time `handle_failure` is **inside** `etl_logs`.

---

# 16. Example 3 — Execution Flow

The structure is:

```text
etl_logs.wrapper
      ↓
handle_failure.wrapper
      ↓
original load_table
```

We call:

```python
load_table(...)
```

Flow:

```text
load_table()
      ↓
etl_logs.wrapper
      ↓
print("load starting")
      ↓
print("start time")
      ↓
handle_failure.wrapper
      ↓
original load_table
      ↓
loading data
      ↓
1 / 0
      ↓
EXCEPTION
```

Now `handle_failure` catches the exception:

```text
original
    ↑
handle_failure catches
```

It prints:

```text
job failed
error: division by zero
```

Then `handle_failure.wrapper` finishes.

Because it handled the exception and did not re-raise it, control returns to `etl_logs`.

Therefore `etl_logs` continues:

```text
etl_logs
    ↓
load done
    ↓
end time
```

---

# 17. Example 2 vs Example 3 — The Key Difference

## Example 2

```python
@handle_failure
@etl_logs
def load_table():
    pass
```

Equivalent:

```python
load_table = handle_failure(etl_logs(load_table))
```

Structure:

```text
handle_failure
      ↓
etl_logs
      ↓
original
```

Exception:

```text
original
    ↑
etl_logs
    ↑
handle_failure catches
```

Therefore:

```text
load done
end time
```

are **NOT printed**.

---

## Example 3

```python
@etl_logs
@handle_failure
def load_table():
    pass
```

Equivalent:

```python
load_table = etl_logs(handle_failure(load_table))
```

Structure:

```text
etl_logs
      ↓
handle_failure
      ↓
original
```

Exception:

```text
original
    ↑
handle_failure catches
    ↓
returns normally
    ↑
etl_logs continues
```

Therefore:

```text
load done
end time
```

**ARE printed.**

---

# 18. Why Does Decorator Order Matter?

The two versions may look almost identical:

```python
@handle_failure
@etl_logs
```

versus:

```python
@etl_logs
@handle_failure
```

But they create different wrapper chains.

### Version 1

```text
handle_failure
      ↓
etl_logs
      ↓
original
```

### Version 2

```text
etl_logs
      ↓
handle_failure
      ↓
original
```

The location of the `try/except` changes.

That changes which code gets interrupted by the exception.

Therefore:

> **Changing the order of multiple decorators can change the behavior and output of the program.**

---

# 19. Important Concept — A Decorator Can Receive Another Wrapper

This is the part that often causes confusion.

Suppose:

```python
@A
@B
def func():
    pass
```

First:

```python
B(func)
```

returns:

```text
B.wrapper
```

Then `A` receives that wrapper:

```python
A(B.wrapper)
```

Therefore, inside `A`:

```text
func → B.wrapper
```

not the original function.

So a decorator does not necessarily receive the original function.

It can receive:

* the original function
* another decorator's wrapper
* another callable

This is why decorator chaining works.

---

# 20. "Bottom to Top" — What Does It Actually Mean?

When we say:

> Decorators are applied bottom-to-top

we mean **decoration/application**, not execution.

Example:

```python
@A
@B
def func():
    pass
```

Application:

```text
B applied first
    ↓
A applied second
```

But once the final function is created:

```text
A.wrapper
    ↓
B.wrapper
    ↓
original
```

calling the function starts at the top:

```text
A
 ↓
B
 ↓
original
```

So:

```text
BOTTOM → TOP
```

is for **creating the decorator chain**.

```text
TOP → BOTTOM
```

is for **normal execution**.

---

# 21. Multiple Decorators With Three Decorators

Consider:

```python
@A
@B
@C
def func():
    pass
```

Python converts this to:

```python
func = A(B(C(func)))
```

Decoration:

```text
C → B → A
```

Final structure:

```text
A.wrapper
    ↓
B.wrapper
    ↓
C.wrapper
    ↓
original
```

Normal execution:

```text
A
 ↓
B
 ↓
C
 ↓
original
```

Exception:

```text
original
    ↑
C
    ↑
B
    ↑
A
```

So the same rule works for any number of decorators.

---

# 22. General Formula

For:

```python
@A
@B
@C
@D
def func():
    pass
```

Python creates:

```python
func = A(B(C(D(func))))
```

Final structure:

```text
A.wrapper
    ↓
B.wrapper
    ↓
C.wrapper
    ↓
D.wrapper
    ↓
original
```

Normal execution:

```text
A → B → C → D → original
```

Exception flow:

```text
original → D → C → B → A
```

---

# 23. Best Mental Model

Whenever you see multiple decorators, imagine **layers around the original function**.

For:

```python
@A
@B
def func():
    pass
```

think:

```text
┌───────────────────────┐
│       A.wrapper       │
│   ┌────────────────┐  │
│   │   B.wrapper    │  │
│   │   ┌──────────┐ │  │
│   │   │ Original │ │  │
│   │   └──────────┘ │  │
│   └────────────────┘  │
└───────────────────────┘
```

The outside layer executes first.

The inside function executes later.

If the inside raises an exception, the exception travels outward through the layers.

---

# 24. Final Cheat Sheet

```text
Multiple decorators
= Stacked decorators
= Decorator chaining
= Decorator composition
```

For:

```python
@A
@B
def func():
    pass
```

remember:

```python
func = A(B(func))
```

### Decoration

```text
BOTTOM → TOP

B → A
```

### Final Structure

```text
A.wrapper
    ↓
B.wrapper
    ↓
original
```

### Normal Execution

```text
TOP → BOTTOM

A → B → original
```

### Exception

```text
INNER → OUTER

original → B → A
```

### Most Important Point

> **The bottom decorator wraps the original function first. The decorator above it wraps the result of that decoration. Therefore, changing the order of decorators changes the wrapper chain and can change the program's behavior.**

---

# 25. Your Two Main Examples — One-Line Summary

### Example 2

```python
@handle_failure
@etl_logs
```

means:

```python
handle_failure(etl_logs(load_table))
```

Flow:

```text
handle_failure
      ↓
etl_logs
      ↓
original
      ↓
ERROR
      ↑
handle_failure catches
```

Result:

```text
load done → NOT printed
end time  → NOT printed
```

---

### Example 3

```python
@etl_logs
@handle_failure
```

means:

```python
etl_logs(handle_failure(load_table))
```

Flow:

```text
etl_logs
      ↓
handle_failure
      ↓
original
      ↓
ERROR
      ↑
handle_failure catches
      ↓
returns normally
      ↑
etl_logs continues
```

Result:

```text
load done → printed
end time  → printed
```

---

# 26. Final Rule to Memorize

```text
                    MULTIPLE DECORATORS

              @A
              @B
              def func():
                  pass


Equivalent to:

              func = A(B(func))


DECORATOR APPLICATION:
              B → A
              Bottom → Top


NORMAL EXECUTION:
              A → B → Original
              Top → Bottom


EXCEPTION:
              Original → B → A
              Inner → Outer
```

**So never confuse "bottom-to-top" with execution order.**

**Bottom-to-top = decorator application.**

**Top-to-bottom = normal execution.**

**Inner-to-outer = exception propagation.**

```
```

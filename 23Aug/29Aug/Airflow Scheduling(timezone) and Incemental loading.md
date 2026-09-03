````md
# Airflow Complete Summary — DAGs, kwargs, XCom, Scheduling & Incremental Loading

## 1. `@dag` decorator

`@dag` converts a Python function into an Airflow DAG definition.

### Valid forms

```python
@dag
def my_dag():
    ...
````

```python
@dag()
def my_dag():
    ...
```

```python
@dag(dag_id="my_dag")
def my_dag():
    ...
```

These are alternative ways to use the decorator.

### Do NOT stack them

```python
@dag(dag_id="my_dag")
@dag
def my_dag():
    ...
```

Do not apply two active `@dag` decorators to the same function.

Use only one:

```python
@dag(...)
def my_dag():
    ...
```

Comments such as:

```python
# @dag
# @dag()
```

do nothing because Python ignores commented lines.

---

# 2. DAG ID vs Python function name

They are separate concepts.

```python
@dag(dag_id="neeraj_abcom_auto_dag")
def neeraj_xcom_auto_dag():
    ...
```

Here:

```text
Python function name
        ↓
neeraj_xcom_auto_dag

Airflow DAG ID
        ↓
neeraj_abcom_auto_dag
```

If `dag_id` is not explicitly supplied, Airflow can derive it from the function name.

---

# 3. `@task` and `@task.python`

Example:

```python
@task
def extract_data():
    ...
```

or:

```python
@task.python
def extract_data():
    ...
```

Calling:

```python
extract = extract_data()
```

creates the task representation used to construct the DAG.

It does **not** mean the Python function immediately executes during DAG parsing.

Example:

```python
extract = extract_data()
transform = transform_data()

extract >> transform
```

means:

```text
extract_data
      ↓
transform_data
```

The actual execution happens later when Airflow runs the DAG.

---

# 4. `**kwargs` in Python

`**kwargs` is normal Python syntax.

Example:

```python
def test(**kwargs):
    print(kwargs)

test(name="Neeraj", age=25)
```

Conceptually:

```python
kwargs = {
    "name": "Neeraj",
    "age": 25
}
```

So `kwargs` is a **dictionary**.

---

# 5. `**kwargs` in Airflow

Airflow can provide runtime execution context to a task.

Conceptually:

```python
kwargs = {
    "ti": <TaskInstance object>,
    "dag": <DAG object>,
    "task": <Task object>,
    "dag_run": <DagRun object>,
    "logical_date": <datetime>,
    "data_interval_start": <datetime>,
    "data_interval_end": <datetime>,
    "params": {...},
    ...
}
```

The exact available context depends on the Airflow version and execution context.

The important point:

```python
kwargs
```

is a dictionary.

Therefore:

```python
ti = kwargs["ti"]
```

means:

> Get the value stored under `"ti"` from the dictionary.

---

# 6. `ti` — TaskInstance

Usually:

```python
ti = kwargs["ti"]
```

`ti` refers to the current Airflow **TaskInstance**.

Conceptually:

```text
kwargs
   ↓
dictionary
   ↓
["ti"]
   ↓
TaskInstance object
```

Because `ti` is an object, you can use its methods and attributes:

```python
ti.task_id
ti.dag_id
ti.run_id
ti.xcom_pull()
ti.xcom_push()
```

---

# 7. Dictionary vs Object

This distinction is important.

### `kwargs`

```python
kwargs
```

is a dictionary.

So:

```python
kwargs["ti"]
```

is dictionary/subscript access.

### `ti`

```python
ti = kwargs["ti"]
```

is a TaskInstance object.

So:

```python
ti.task_id
```

is attribute access.

And:

```python
ti.xcom_pull()
```

is a method call.

### Mental model

```text
kwargs
   ↓
dictionary
   ↓
["ti"]
   ↓
TaskInstance object
   ↓
.xcom_pull()
```

---

# 8. What does "subscriptable" mean?

A subscript operation uses:

```python
[]
```

Examples:

```python
my_list[0]
my_dict["name"]
my_string[2]
```

In your Airflow code:

```python
kwargs["ti"]
```

is a subscript operation.

This is also a subscript:

```python
data["weekend_flag"]
```

For example:

```python
data = {
    "numbers": [1, 2, 3],
    "weekend_flag": "true"
}

data["weekend_flag"]
```

returns:

```text
"true"
```

---

# 9. How to inspect `kwargs` in Airflow

You can print it in a task:

```python
@task
def inspect_context(**kwargs):

    print("kwargs type:", type(kwargs))
    print("kwargs:", kwargs)

    for key, value in kwargs.items():
        print("KEY:", key)
        print("VALUE:", value)
        print("TYPE:", type(value))
```

Then check:

```text
Airflow UI
    ↓
DAG
    ↓
Task
    ↓
Logs
```

The task logs allow you to inspect the runtime context.

---

# 10. XCom

XCom is Airflow's mechanism for sharing relatively small pieces of data between tasks.

Basic flow:

```text
Task A
   |
   | xcom_push()
   v
  XCom
   |
   | xcom_pull()
   v
Task B
```

---

# 11. `xcom_push()`

Example:

```python
@task.python
def extract_data(**kwargs):

    ti = kwargs["ti"]

    api_data = {
        "numbers": [1, 2, 3, 4, 5],
        "weekend_flag": "true"
    }

    ti.xcom_push(
        key="data",
        value=api_data
    )
```

Conceptually, this stores:

```text
Task:
extract_data

Key:
data

Value:
{
    "numbers": [1, 2, 3, 4, 5],
    "weekend_flag": "true"
}
```

---

# 12. `xcom_pull()`

Another task can retrieve it:

```python
data = ti.xcom_pull(
    task_ids="extract_data",
    key="data"
)
```

This means:

> Get the XCom with key `"data"` from task `"extract_data"`.

---

# 13. Why `task_ids` is needed

Multiple tasks can create XComs.

For example:

```text
extract_users
    |
    +-- key="data" → users

extract_orders
    |
    +-- key="data" → orders

extract_products
    |
    +-- key="data" → products
```

All three can use the same key:

```text
data
```

Therefore:

```python
ti.xcom_pull(
    task_ids="extract_users",
    key="data"
)
```

means:

```text
WHO?
  ↓
extract_users

WHICH XCom?
  ↓
data
```

### Memory trick

```text
task_ids = WHO pushed it?
key      = WHICH XCom?
value    = WHAT was stored?
```

---

# 14. Multiple XCom values from one task

A task can push multiple values using different keys:

```python
ti.xcom_push(
    key="numbers",
    value=[1, 2, 3]
)

ti.xcom_push(
    key="name",
    value="Neeraj"
)

ti.xcom_push(
    key="status",
    value="success"
)
```

Conceptually:

```text
extract_data
    |
    +-- numbers → [1,2,3]
    |
    +-- name    → "Neeraj"
    |
    +-- status  → "success"
```

Then another task can pull a specific one:

```python
numbers = ti.xcom_pull(
    task_ids="extract_data",
    key="numbers"
)
```

---

# 15. Multiple `task_ids`

You can request XComs associated with multiple task IDs:

```python
ti.xcom_pull(
    task_ids=["extract_users", "extract_orders"],
    key="data"
)
```

The important distinction is:

```text
task_ids
    ↓
Which task(s)?

key
    ↓
Which XCom key?
```

A DAG can have many tasks, and each task can have multiple XCom entries.

---

# 16. Your `NoneType` XCom error

You had:

```python
weekend_flag = ti.xcom_pull(
    task_ids="extract_data"
)["weekend_flag"]
```

But your upstream task did:

```python
ti.xcom_push(
    key="data",
    value=api_data
)
```

You pushed using:

```text
key = "data"
```

but pulled without:

```python
key="data"
```

The desired XCom therefore wasn't retrieved.

If:

```python
data = ti.xcom_pull(
    task_ids="extract_data"
)
```

returns:

```python
None
```

then this:

```python
None["weekend_flag"]
```

produces:

```text
TypeError: 'NoneType' object is not subscriptable
```

---

# 17. Correct version

Because you pushed:

```python
ti.xcom_push(
    key="data",
    value=api_data
)
```

pull it using the same key:

```python
data = ti.xcom_pull(
    task_ids="extract_data",
    key="data"
)

weekend_flag = data["weekend_flag"]
```

Or directly:

```python
weekend_flag = ti.xcom_pull(
    task_ids="extract_data",
    key="data"
)["weekend_flag"]
```

---

# 18. Your `tasks_id` error

You originally had:

```python
ti.xcom_pull(
    tasks_id="extract_data"
)
```

This is wrong.

The parameter is:

```python
task_ids
```

not:

```python
tasks_id
```

Correct:

```python
ti.xcom_pull(
    task_ids="extract_data",
    key="data"
)
```

Your error:

```text
TypeError:
RuntimeTaskInstance.xcom_pull()
got an unexpected keyword argument 'tasks_id'
```

was caused by that typo.

---

# 19. `return` vs `xcom_push`

## Explicit XCom

```python
ti.xcom_push(
    key="data",
    value=api_data
)
```

Then:

```python
ti.xcom_pull(
    task_ids="extract_data",
    key="data"
)
```

## Return value

```python
@task
def extract_data():

    api_data = {
        "numbers": [1, 2, 3],
        "weekend_flag": "true"
    }

    return api_data
```

Airflow makes the task's return value available through XCom.

Then a traditional pull can retrieve the return value:

```python
ti.xcom_pull(
    task_ids="extract_data"
)
```

### Memory trick

```text
xcom_push(key="data")
        ↓
xcom_pull(key="data")

return value
        ↓
default return-value XCom
```

---

# 20. XCom flow in your DAG

Your flow:

```text
extract_data
      |
      | push key="data"
      v
transform_data
      |
      | push key="data"
      v
decider_node
    /       \
   /         \
  v           v
load_data   no_load_data
```

Notice that both `extract_data` and `transform_data` can use:

```text
key="data"
```

because XComs are associated with the task as well.

Conceptually:

```text
extract_data
    |
    +-- data
         {
           numbers: [...],
           weekend_flag: "true"
         }


transform_data
    |
    +-- data
         {
           transformed_data: [...]
         }
```

To distinguish them:

```python
task_ids="extract_data"
```

or:

```python
task_ids="transform_data"
```

---

# 21. `@task.branch`

Example:

```python
@task.branch
def decider_node(**kwargs):

    ti = kwargs["ti"]

    data = ti.xcom_pull(
        task_ids="extract_data",
        key="data"
    )

    weekend_flag = data["weekend_flag"]

    if weekend_flag == "true":
        return "no_load_data"
    else:
        return "load_data"
```

The returned task ID determines which downstream branch proceeds.

Flow:

```text
                 decider_node
                  /         \
                 /           \
        weekend=true      weekend=false
             |                  |
             v                  v
      no_load_data          load_data
```

---

# 22. Branch dependency

This:

```python
decider_node() >> [load, no_load]
```

means both tasks are downstream of the branch task.

It does **not** mean both execute.

The branch task decides which downstream path proceeds.

---

# 23. Python list multiplication

You had:

```python
transformed_data = [1, 2, 3, 4, 5]

transformed_data *= 2
```

For a Python list, this repeats the list:

```python
[1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
```

It does **not** produce:

```python
[2, 4, 6, 8, 10]
```

For element-by-element multiplication:

```python
transformed_data = [
    number * 2
    for number in transformed_data
]
```

---

# 24. Scheduling: schedule/interval-based vs trigger-based

The key question is:

> What causes the DAG run to be created?

| Type                | What causes the DAG run?              | Example                      |
| ------------------- | ------------------------------------- | ---------------------------- |
| Schedule/time-based | Timetable reaches its scheduled time  | Every day at 4 PM            |
| Interval-based      | A time interval elapses               | Every 3 days                 |
| Trigger-based       | An explicit trigger/event             | UI/API/another DAG           |
| Date-based          | Usually part of scheduling boundaries | Start from a particular date |

"Date-based" is generally not a separate execution mechanism from scheduled/time-based execution.

---

# 25. Cron schedule

Example:

```python
schedule=CronTriggerTimetable(
    "0 16 * * MON-FRI",
    timezone="Asia/Kolkata"
)
```

Cron:

```text
0 16 * * MON-FRI
│ │  │ │ └── day of week
│ │  │ └──── month
│ │  └────── day of month
│ └───────── hour
└─────────── minute
```

Meaning:

```text
Monday    4:00 PM
Tuesday   4:00 PM
Wednesday 4:00 PM
Thursday  4:00 PM
Friday    4:00 PM
```

This is schedule/time-driven.

---

# 26. Delta interval

Example:

```python
schedule=DeltaTriggerTimetable(
    duration(days=3)
)
```

Conceptually:

```text
Day 1
  ↓
Day 4
  ↓
Day 7
  ↓
Day 10
```

This is interval/time-driven.

---

# 27. Trigger-based execution

Examples:

```text
User clicks Trigger DAG
        ↓
DAG Run
```

```text
API request
    ↓
DAG Run
```

```text
Another DAG/system
        ↓
DAG Run
```

The important idea:

> The run is initiated by an explicit trigger/event rather than waiting for the timetable's next scheduled point.

---

# 28. `start_date` vs `schedule`

This is very important.

Example:

```python
start_date=datetime(
    2026,
    8,
    27,
    tz="Asia/Kolkata"
)
```

This does **not** simply mean:

> Run once on August 27.

Instead:

```text
start_date
    ↓
Scheduling boundary

schedule
    ↓
When scheduled runs occur
```

---

# 29. Date/time arguments

With:

```python
from pendulum import datetime, duration

from airflow.timetables.trigger import (
    CronTriggerTimetable,
    DeltaTriggerTimetable
)
```

use:

| What you use              | Imported from | Argument        | Example                                                             |
| ------------------------- | ------------- | --------------- | ------------------------------------------------------------------- |
| `datetime()`              | `pendulum`    | `tz`            | `datetime(2026, 8, 27, tz="Asia/Kolkata")`                          |
| Python `datetime()`       | `datetime`    | `tzinfo`        | `datetime(..., tzinfo=ZoneInfo("Asia/Kolkata"))`                    |
| `CronTriggerTimetable()`  | Airflow       | `timezone`      | `CronTriggerTimetable("0 16 * * MON-FRI", timezone="Asia/Kolkata")` |
| `DeltaTriggerTimetable()` | Airflow       | duration/period | `DeltaTriggerTimetable(duration(days=3))`                           |
| `duration()`              | `pendulum`    | days/hours/etc. | `duration(days=3)`                                                  |
| `ZoneInfo()`              | Python        | timezone name   | `ZoneInfo("Asia/Kolkata")`                                          |

### Memory trick

```text
Pendulum datetime()       → tz
Python datetime()         → tzinfo
CronTriggerTimetable()    → timezone
DeltaTriggerTimetable()   → duration
duration()                → days / hours / minutes
```

---

# 30. `catchup=True`

Example:

```python
@dag(
    dag_id="neeraj_first_dag",

    start_date=datetime(
        year=2026,
        month=8,
        day=27,
        tz="Asia/Kolkata"
    ),

    schedule=CronTriggerTimetable(
        "0 16 * * MON-FRI",
        timezone="Asia/Kolkata"
    ),

    end_date=datetime(
        year=2026,
        month=8,
        day=31,
        tz="Asia/Kolkata"
    ),

    is_paused_upon_creation=False,

    catchup=True
)
```

`catchup=True` tells Airflow to create applicable historical scheduled DAG runs that were missed between the scheduling boundary and the current scheduling point.

It is commonly useful for historical or initial processing.

Important:

> `catchup=True` does not itself load historical data. It creates historical DAG runs. Your tasks decide what data each run processes.

---

# 31. Scheduling vs incremental loading

These are two different concepts.

### Scheduling asks:

> **When should my DAG run?**

### Incremental loading asks:

> **Which data should this particular DAG run process?**

Example:

```text
Schedule:
Every day at 2 AM

Incremental load:
Process the completed data interval
```

---

# 32. Incremental loading

Instead of processing everything every time:

```text
Source:
10 million records

Every run:
process all 10 million
```

incremental loading processes only new or changed data:

```text
Day 1 → load Day 1 records
Day 2 → load Day 2 records
Day 3 → load Day 3 records
```

Flow:

```text
Source
   |
   | only new/changed records
   v
Incremental ETL
   |
   v
Warehouse
```

Benefits:

* Less data to process
* Faster pipelines
* Lower compute cost
* Less unnecessary work
* Easier to scale

---

# 33. The "next day looks back" concept

This is an important Airflow data-interval concept.

Suppose a DAG is scheduled daily.

A common beginner mental model is:

```text
Jan 2 at 2 AM
    ↓
process Jan 2
```

For a daily data pipeline, the run can instead represent the **completed previous interval**.

Conceptually:

```text
Jan 1 00:00 ───────── Jan 2 00:00
                         |
                         v
                  processing point
                         |
                         v
                  process Jan 1
                     interval
```

So the run happens after the relevant interval has completed.

This is why Airflow provides:

```python
data_interval_start
data_interval_end
```

The exact timing/semantics depend on the timetable being used, so think in terms of the **data interval represented by the run**, not simply "today."

---

# 34. Daily incremental-load example

Suppose:

```text
DAG schedule:
Every day at 2 AM
```

The source contains:

```text
Aug 27 data
Aug 28 data
Aug 29 data
Aug 30 data
```

Conceptually:

```text
Aug 27 00:00 ───── Aug 28 00:00
                       ↓
                  next run
                       ↓
              process Aug 27 interval


Aug 28 00:00 ───── Aug 29 00:00
                       ↓
                  next run
                       ↓
              process Aug 28 interval
```

The important idea:

> A scheduled run can process the data interval that has just completed.

---

# 35. Using Airflow's data interval

A task can access:

```python
@task
def extract_data(**context):

    start = context["data_interval_start"]
    end = context["data_interval_end"]

    print("Start:", start)
    print("End:", end)
```

Then a source query can conceptually use:

```sql
SELECT *
FROM source_table
WHERE updated_at >= :start
  AND updated_at < :end;
```

Flow:

```text
Airflow DAG run
       |
       +-- data_interval_start
       |
       +-- data_interval_end
       |
       v
SQL filter
       |
       v
Only records in that interval
       |
       v
Incremental load
```

---

# 36. Why `[start, end)` is useful

A common incremental-load condition is:

```sql
WHERE timestamp >= start
  AND timestamp < end
```

This is called a **half-open interval**:

```text
[start, end)
```

Meaning:

```text
include start
exclude end
```

Example:

```text
Aug 27 00:00 <= timestamp < Aug 28 00:00
```

A record exactly at:

```text
Aug 28 00:00
```

belongs to the next interval.

This helps avoid duplicate processing at interval boundaries.

---

# 37. Catchup + incremental loading

These concepts work together.

Suppose:

```text
Today:
31 Aug

start_date:
27 Aug

catchup:
True
```

Airflow can create applicable historical scheduled runs.

Each run has its own data interval.

Conceptually:

```text
             start_date
                  ↓
               Aug 27
                  |
       +----------+----------+
       |          |          |
       v          v          v
     Run 1      Run 2      Run 3
       |          |          |
       v          v          v
   interval   interval   interval
    Aug 27     Aug 28     Aug 29
       |          |          |
       v          v          v
 incremental incremental incremental
    load        load        load
```

Therefore:

```text
catchup
   ↓
creates historical DAG runs

data interval
   ↓
tells each run which time window it represents

incremental query
   ↓
loads data for that time window
```

---

# 38. Catchup does NOT equal backfill data

Think:

```text
catchup
    =
create missed DAG runs
```

Not:

```text
catchup
    =
automatically load old database records
```

The tasks inside those runs determine what data gets loaded.

---

# 39. Complete mental model

Keep these concepts separate:

```text
1. start_date
   ↓
Where scheduling begins

2. schedule / timetable
   ↓
When scheduled DAG runs occur

3. catchup
   ↓
Whether applicable historical scheduled runs are created

4. data interval
   ↓
Which time window a particular DAG run represents

5. incremental loading
   ↓
Process only new/changed data for the required window
```

Full flow:

```text
                  start_date
                      |
                      v
                DAG timetable
                      |
                      v
               Scheduled runs
                      |
                 catchup=True
                      |
                      v
          Historical runs created
                      |
                      v
               Data interval
            +-------------------+
            | start             |
            | end               |
            +-------------------+
                      |
                      v
              SQL/API filtering
                      |
                      v
             New/changed records
                      |
                      v
             Incremental loading
                      |
                      v
                 Data warehouse
```

---

# 40. Interview answer — Scheduling

> **A timetable or schedule determines when Airflow should create scheduled DAG runs. For example, a cron timetable can schedule a DAG every day at 4 PM, while a delta timetable can schedule it every three days. Trigger-based execution starts a DAG run because of an explicit trigger such as an API call, manual UI trigger, another DAG, or an event. `start_date` defines the scheduling boundary, while `catchup` controls whether applicable historical scheduled runs are created.**

---

# 41. Interview answer — Incremental loading

> **Incremental loading means processing only new or changed data instead of reprocessing the entire source every time. In Airflow, a DAG run can use its data interval, such as `data_interval_start` and `data_interval_end`, to identify the time window represented by that run. The task can then filter source data using that interval and load only the relevant records.**

---

# 42. Final Cheat Sheet

```text
@dag
    → defines a DAG

@task
    → defines a task

**kwargs
    → Python dictionary containing runtime context

kwargs["ti"]
    → TaskInstance object

ti.xcom_push()
    → stores an XCom

ti.xcom_pull()
    → retrieves an XCom

task_ids
    → identifies the task whose XCom you want

key
    → identifies which XCom key you want

[]
    → subscript/access an item in a collection

start_date
    → scheduling boundary

schedule/timetable
    → determines scheduled timing

catchup=True
    → creates applicable historical scheduled runs

schedule/time-based
    → run because timetable says it is time

trigger-based
    → run because something explicitly triggered it

data_interval_start
    → beginning of the run's data interval

data_interval_end
    → end of the run's data interval

incremental loading
    → process only new/changed data

[start, end)
    → include start, exclude end
```

---

# 43. Final Visual

```text
                         AIRFLOW
                            |
              +-------------+-------------+
              |                           |
          SCHEDULE                     TRIGGER
              |                           |
              v                           v
       creates DAG run             creates DAG run
              |                           |
              +-------------+-------------+
                            |
                            v
                         DAG RUN
                            |
                            v
                      DATA INTERVAL
                   +-------------------+
                   | start             |
                   | end               |
                   +-------------------+
                            |
                            v
                     INCREMENTAL QUERY
                            |
                            v
                  Only relevant records
                            |
                            v
                         ETL/LOAD
                            |
                            v
                       WAREHOUSE
```

```
```

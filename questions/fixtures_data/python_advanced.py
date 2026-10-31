# 40 Python Advanced Questions with 4 options and detailed technical explanations

PYTHON_ADVANCED_QUESTIONS = [
    {
        "category": "Python Advanced",
        "topic": "GIL",
        "difficulty": "ADVANCED",
        "content": "What is the Global Interpreter Lock (GIL) in CPython and what fundamental limitation does it impose?",
        "code_snippet": "# In CPython:\n# Thread 1 and Thread 2 running pure CPU math",
        "explanation": "The GIL is a mutex that prevents multiple native threads from executing CPython bytecodes simultaneously. It was introduced to simplify thread-safe memory management (reference counting). As a result, pure CPU-bound Python threads do not achieve multi-core parallelism.",
        "options": [
            ("A mutex ensuring only one native thread executes Python bytecode at a time, limiting CPU-bound multi-core parallelism", True, "Correct. While I/O-bound threads release the GIL during network/disk operations, CPU tasks are serialized."),
            ("An OS-level file lock on the python.exe binary", False, "Incorrect. The GIL is an internal interpreter mutex."),
            ("A compiler flag that prevents memory leaks in third-party C libraries", False, "Incorrect. It protects internal CPython state and reference counts."),
            ("A hardware interrupt lock implemented on x86 processors", False, "Incorrect. It is a software construct in CPython."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Multithreading",
        "difficulty": "ADVANCED",
        "content": "In which scenario does Python's `threading` module provide genuine performance improvements despite the GIL?",
        "code_snippet": "import threading, requests\n# Fetching 50 URLs concurrently",
        "explanation": "During I/O-bound operations (network requests, database queries, file reading, `time.sleep()`), CPython releases the GIL before the system call and reacquires it when the call completes. Multiple threads can wait for I/O concurrently.",
        "options": [
            ("I/O-bound tasks where threads spend significant time waiting on sockets or disk I/O", True, "Correct. CPython releases the GIL during blocking I/O calls, allowing other threads to run."),
            ("Heavy mathematical calculations and matrix multiplications in pure Python", False, "Incorrect. CPU-bound pure Python suffers overhead from thread context switching under the GIL."),
            ("Compiling large regular expressions in tight loops", False, "Incorrect. Regex evaluation in Python locks the GIL."),
            ("Image processing performed using pure Python lists and loops", False, "Incorrect. Pure Python CPU operations are constrained by the GIL."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Multiprocessing",
        "difficulty": "ADVANCED",
        "content": "How does `multiprocessing` achieve true multi-core parallel execution in Python?",
        "code_snippet": "from multiprocessing import Pool\n\nwith Pool() as p:\n    results = p.map(heavy_cpu_task, data)",
        "explanation": "The `multiprocessing` module creates separate OS processes, each with its own independent Python interpreter and private memory space (and thus its own GIL). Because they are separate processes, the OS schedules them across multiple CPU cores in true parallel.",
        "options": [
            ("By spawning separate OS processes, each with its own independent Python interpreter and GIL", True, "Correct. Each process runs on its own core without GIL contention between them."),
            ("By disabling the GIL dynamically via bytecode injection", False, "Incorrect. Standard CPython does not dynamically disable the GIL per thread."),
            ("By converting Python functions into C++ assembly routines at runtime", False, "Incorrect. multiprocessing runs standard Python interpreters."),
            ("By sharing a single global stack across all CPU hardware registers", False, "Incorrect. Processes have separate address spaces."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Asyncio",
        "difficulty": "ADVANCED",
        "content": "How does `asyncio` differ fundamentally from `multithreading`?",
        "code_snippet": "import asyncio\n\nasync def fetch():\n    await asyncio.sleep(1)",
        "explanation": "`asyncio` uses cooperative multitasking on a single thread via an event loop: coroutines explicitly yield control back to the loop using `await`. Multithreading uses preemptive multitasking where the OS kernel interrupts and switches threads at arbitrary times.",
        "options": [
            ("Asyncio uses single-threaded cooperative multitasking with an event loop; threading uses OS preemptive scheduling", True, "Correct. Coroutines yield control cooperatively via await without kernel context-switch overhead."),
            ("Asyncio spawns a new OS kernel thread for every async function call", False, "Incorrect. Asyncio runs on a single thread by default."),
            ("Asyncio bypasses Python bytecode and talks directly to the NIC", False, "Incorrect. It runs standard Python coroutines."),
            ("Asyncio eliminates the need for database connection pooling", False, "Incorrect. Connection pools are essential in async applications."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Coroutines",
        "difficulty": "ADVANCED",
        "content": "What happens if a developer executes a blocking synchronous call (like `time.sleep(5)` or `requests.get()`) inside an `asyncio` coroutine?",
        "code_snippet": "async def bad_handler():\n    time.sleep(5)  # Blocking call\n    return 'done'",
        "explanation": "Because `asyncio` runs cooperatively on a single thread, any blocking call freezes the entire thread, halting the event loop. No other concurrent coroutines, timers, or network events can execute during those 5 seconds.",
        "options": [
            ("It freezes the entire event loop, blocking all other concurrent coroutines from executing", True, "Correct. Use asyncio.to_thread() or async libraries (httpx, aiohttp) to avoid blocking the loop."),
            ("Asyncio automatically detects the block and moves the task to a background thread", False, "Incorrect. Python does not automatically threadify synchronous calls."),
            ("The event loop raises a BlockedEventLoopException immediately", False, "Incorrect. The interpreter simply stalls silently."),
            ("Only that single coroutine is affected; other tasks continue unhindered", False, "Incorrect. The single event loop thread is frozen."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Metaclasses",
        "difficulty": "ADVANCED",
        "content": "What is a metaclass in Python and what is the default metaclass for all standard classes?",
        "code_snippet": "class CustomMeta(type):\n    def __new__(mcs, name, bases, attrs):\n        return super().__new__(mcs, name, bases, attrs)",
        "explanation": "A metaclass is the 'class of a class'—it defines how a class itself is constructed and behaves. Just as an object is an instance of a class, a class in Python is an instance of a metaclass. The default metaclass in Python is `type`.",
        "options": [
            ("A class whose instances are classes; `type` is the default metaclass", True, "Correct. Classes are objects at runtime, and `type` is the metaclass that constructs them."),
            ("A parent class that can only be inherited once", False, "Incorrect. That is a single-inheritance constraint."),
            ("A decorator applied to functions before compilation", False, "Incorrect. Metaclasses govern class creation, not functions."),
            ("A C-extension module that binds Python to native shared libraries", False, "Incorrect. Metaclasses are part of the core Python object system."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Descriptors",
        "difficulty": "ADVANCED",
        "content": "What methods define Python's Descriptor Protocol, and what powers Django ORM fields under the hood?",
        "code_snippet": "class IntegerField:\n    def __get__(self, instance, owner):\n        ...\n    def __set__(self, instance, value):\n        ...\n    def __delete__(self, instance):\n        ...",
        "explanation": "The descriptor protocol consists of `__get__`, `__set__`, and `__delete__` (plus `__set_name__` in Python 3.6+). When an attribute implements any of these methods, attribute lookup behavior on an instance is customized. Django model fields are descriptors.",
        "options": [
            ("`__get__`, `__set__`, and `__delete__`", True, "Correct. Descriptors power properties, classmethods, staticmethods, and Django ORM field tracking."),
            ("`__read__`, `__write__`, and `__close__`", False, "Incorrect. Those are file-like stream method names."),
            ("`__fetch__`, `__store__`, and `__evict__`", False, "Incorrect. Those resemble cache protocols."),
            ("`__enter__`, `__exit__`, and `__call__`", False, "Incorrect. Context managers and callables, respectively."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Descriptors",
        "difficulty": "ADVANCED",
        "content": "What is the distinction between a Data Descriptor and a Non-Data Descriptor?",
        "code_snippet": "class DescriptorA:\n    def __get__(self, instance, owner): return 1\n    def __set__(self, instance, value): pass\n\nclass DescriptorB:\n    def __get__(self, instance, owner): return 2",
        "explanation": "A Data Descriptor defines both `__get__` and `__set__` (or `__delete__`). A Non-Data Descriptor defines only `__get__`. During attribute lookup, Data Descriptors take precedence over an instance's `__dict__`, whereas instance `__dict__` takes precedence over Non-Data Descriptors.",
        "options": [
            ("Data descriptors implement `__set__` and take precedence over instance `__dict__`; non-data descriptors implement only `__get__`", True, "Correct. This lookup precedence explains why methods (non-data descriptors) can be shadowed by instance attributes, but @property (data descriptor) cannot."),
            ("Data descriptors store data in SQLite; non-data descriptors store data in RAM", False, "Incorrect. Descriptors are Python attribute protocol objects."),
            ("Data descriptors are thread-safe; non-data descriptors are not", False, "Incorrect. Thread safety depends on implementation."),
            ("Non-data descriptors can only return strings", False, "Incorrect. Any object type can be returned."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "MRO",
        "difficulty": "ADVANCED",
        "content": "Why does Python reject this class definition with a `TypeError: Cannot create a consistent method resolution order (MRO)`?",
        "code_snippet": "class A:\n    pass\nclass B(A):\n    pass\nclass C(A, B):  # What happens here?\n    pass",
        "explanation": "In class `C`, the base class list `(A, B)` specifies that `A` should take precedence over `B`. However, `B` subclasses `A`, requiring `B` to precede `A` in MRO. This creates an unresolvable cyclic order conflict in C3 Linearization.",
        "options": [
            ("C3 Linearization cannot resolve conflicting class ordering: `C(A, B)` orders A before B, but B inherits from A", True, "Correct. A subclass must not appear after its parent in the inheritance list when C3 evaluates precedence."),
            ("Python does not allow multiple inheritance from more than one class", False, "Incorrect. Python fully supports multiple inheritance."),
            ("Class names must be longer than one letter in Python 3", False, "Incorrect. Single letter class names are completely valid."),
            ("Subclasses must declare abstract methods", False, "Incorrect. None of these classes are abstract."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Python Internals",
        "difficulty": "ADVANCED",
        "content": "What is the role of `co_code` in a Python function object's `__code__` attribute?",
        "code_snippet": "def add(a, b):\n    return a + b\n\nprint(add.__code__.co_code)",
        "explanation": "`co_code` is a bytes object representing the sequence of raw bytecode instructions compiled from Python source code by the CPython compiler for the Python Virtual Machine (PVM).",
        "options": [
            ("Contains the raw compiled bytecode instructions executed by the CPython PVM", True, "Correct. You can inspect human-readable disassembly of co_code using the `dis` module."),
            ("Stores the original uncompiled Python source code text", False, "Incorrect. Source code is not retained in co_code; inspect.getsource uses source files."),
            ("Contains the compiled machine assembly for the host CPU", False, "Incorrect. CPython compiles to bytecode, not native machine code."),
            ("Stores the function docstring", False, "Incorrect. Docstrings are stored on __doc__."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Python Internals",
        "difficulty": "ADVANCED",
        "content": "What optimization did Python 3.11 introduce to significantly speed up bytecode execution?",
        "code_snippet": "# Python 3.11 Faster CPython Initiative",
        "explanation": "Python 3.11 introduced the Specializing Adaptive Interpreter (PEP 659): bytecodes observe runtime types and adaptively replace generic opcodes with specialized inline opcodes (e.g. `LOAD_ATTR_MODULE` or `BINARY_OP_ADD_INT`).",
        "options": [
            ("Specializing Adaptive Interpreter (PEP 659) that inlines and specializes common opcodes at runtime", True, "Correct. It dynamically optimizes frequently executed bytecodes based on observed types without needing full JIT."),
            ("Replacement of CPython with Rust", False, "Incorrect. CPython remains written in C."),
            ("Elimination of all reference counting in favor of zero-cost ARC", False, "Incorrect. Reference counting is preserved."),
            ("Converting all Python lists to C++ std::vector", False, "Incorrect. Lists remain PyListObject dynamic arrays."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Performance Optimization",
        "difficulty": "ADVANCED",
        "content": "What does `@functools.lru_cache(maxsize=128)` do and what requirement must cached function arguments meet?",
        "code_snippet": "from functools import lru_cache\n\n@lru_cache(maxsize=128)\ndef fib(n):\n    if n < 2: return n\n    return fib(n-1) + fib(n-2)",
        "explanation": "`lru_cache` memoizes the results of expensive function calls using a Least Recently Used eviction policy. Because arguments are used as dictionary keys to look up cached results, all arguments must be hashable.",
        "options": [
            ("Memoizes function return values using an LRU cache; all arguments must be hashable", True, "Correct. Passing unhashable arguments (like lists or dicts) raises a TypeError: unhashable type."),
            ("Compiles the function into native C code", False, "Incorrect. It is a pure Python / C memoization wrapper."),
            ("Restricts the function to 128 executions per thread before terminating", False, "Incorrect. maxsize limits the number of distinct argument permutations cached."),
            ("Caches results on disk in SQLite", False, "Incorrect. LRU cache is in-memory only."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Type Hints",
        "difficulty": "ADVANCED",
        "content": "Does Python's runtime enforce static type hints by default?",
        "code_snippet": "def calculate_total(price: float, qty: int) -> float:\n    return price * qty\n\n# What happens if we call calculate_total(\"5\", \"3\")?",
        "explanation": "Type hints in Python (PEP 484) are purely informational metadata and are not enforced at runtime by the CPython interpreter. Calling the function with strings will execute normally (or fail on multiplication type mismatch). Type checking is done by static analyzers like Mypy or Pyright.",
        "options": [
            ("No, type hints are ignored at runtime by CPython and require external static analyzers (Mypy/Pyright)", True, "Correct. Python remains dynamically typed; type annotations are stored in __annotations__."),
            ("Yes, CPython raises a TypeError if an argument type doesn't match the annotation", False, "Incorrect. CPython does not perform runtime type checking on annotations."),
            ("Yes, but only in debug mode with python -O", False, "Incorrect. Type hints are never enforced by CPython regardless of flags."),
            ("Only for primitive types (int, float, str)", False, "Incorrect. No types are enforced by default."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Type Hints",
        "difficulty": "ADVANCED",
        "content": "What is the difference between `typing.Any` and `object` in Python type hinting?",
        "code_snippet": "from typing import Any\ndef f1(x: Any): ...\ndef f2(x: object): ...",
        "explanation": "`Any` disables static type checking: any operation is permitted on an `Any` value and it can be passed anywhere. `object` is the top type: every value is an instance of `object`, but static type checkers will disallow arbitrary operations (like `.quack()`) unless narrowed.",
        "options": [
            ("`Any` opts out of type checking for that value; `object` is safe: only base object methods can be called", True, "Correct. Static checkers flag invalid attribute accesses on `object`, but allow anything on `Any`."),
            ("`Any` is only for primitive types; `object` is for classes", False, "Incorrect. Both can represent any Python instance."),
            ("`object` is deprecated in Python 3.10+", False, "Incorrect. object is the universal root class in Python."),
            ("There is no semantic difference between them", False, "Incorrect. Type checkers treat them completely differently."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Advanced Decorators",
        "difficulty": "ADVANCED",
        "content": "How do you write a decorator that works seamlessly on both regular functions and async coroutines?",
        "code_snippet": "import inspect\nfrom functools import wraps\n\ndef universal_decorator(fn):\n    if inspect.iscoroutinefunction(fn):\n        @wraps(fn)\n        async def async_wrapper(*args, **kwargs):\n            return await fn(*args, **kwargs)\n        return async_wrapper\n    else:\n        @wraps(fn)\n        def sync_wrapper(*args, **kwargs):\n            return fn(*args, **kwargs)\n        return sync_wrapper",
        "explanation": "Use `inspect.iscoroutinefunction(fn)` to check whether the target is an async coroutine function. If so, return an `async def` wrapper awaiting the result; otherwise, return a standard synchronous `def` wrapper.",
        "options": [
            ("Inspect `inspect.iscoroutinefunction(fn)` and return an `async def` or sync `def` wrapper accordingly", True, "Correct. This pattern is widely used in modern production frameworks like FastAPI and Django."),
            ("Wrap everything in `asyncio.run()`", False, "Incorrect. Calling asyncio.run() inside a running event loop causes RuntimeError."),
            ("Decorators automatically adapt to async functions without separate wrappers", False, "Incorrect. Calling an async function from a sync wrapper returns an unawaited coroutine."),
            ("Use the `@dataclass` decorator on the wrapper", False, "Incorrect. Dataclasses are for data structures, not function wrapping."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Design Patterns",
        "difficulty": "ADVANCED",
        "content": "Which Python dunder method is most commonly overridden to implement the Singleton design pattern?",
        "code_snippet": "class DatabasePool:\n    _instance = None\n    def __new__(cls, *args, **kwargs):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance",
        "explanation": "Overriding `__new__` intercepts instance creation before memory is allocated. By checking if a cached instance exists, `__new__` can return the existing singleton instance rather than creating a new one.",
        "options": [
            ("`__new__`", True, "Correct. __new__ controls object instantiation, allowing reuse of a cached singleton instance."),
            ("`__init__`", False, "Incorrect. __init__ is called after instance creation and must return None."),
            ("`__del__`", False, "Incorrect. __del__ is called upon object finalization."),
            ("`__call__`", False, "Incorrect. __call__ makes instances callable."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Design Patterns",
        "difficulty": "ADVANCED",
        "content": "Why are module-level variables in Python naturally suited for the Singleton pattern without complex class logic?",
        "code_snippet": "# client.py\nclass APIClient: pass\ndefault_client = APIClient()  # module-level singleton",
        "explanation": "Python's import mechanism executes module code only once upon first import and caches the loaded module in `sys.modules`. All subsequent imports across the application receive the same module instance and shared objects.",
        "options": [
            ("Python modules are imported once and cached in `sys.modules`, making module-level instances singletons", True, "Correct. 'Python modules are already singletons' is a celebrated Pythonic design tenet."),
            ("Python modules run in isolated OS threads", False, "Incorrect. Modules exist within the shared interpreter namespace."),
            ("Variables defined in modules are stored in CPU registers", False, "Incorrect. Module attributes are stored in the module's __dict__."),
            ("Module code is recompiled on every import", False, "Incorrect. sys.modules caching prevents recompilation."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "SOLID Principles",
        "difficulty": "ADVANCED",
        "content": "Which SOLID principle is violated when a subclass overrides a parent method with a narrower type or incompatible signature?",
        "code_snippet": "class Bird:\n    def fly(self, altitude: float) -> None: pass\n\nclass Penguin(Bird):\n    def fly(self, altitude: float) -> None:\n        raise NotImplementedError(\"Penguins cannot fly!\")",
        "explanation": "This violates the Liskov Substitution Principle (LSP). LSP states that objects of a superclass should be replaceable with objects of its subclasses without breaking application correctness.",
        "options": [
            ("Liskov Substitution Principle (LSP)", True, "Correct. If a Penguin cannot fly, substituting Penguin for Bird breaks client code expecting valid fly() behavior."),
            ("Single Responsibility Principle (SRP)", False, "Incorrect. SRP concerns reasons for a class to change."),
            ("Interface Segregation Principle (ISP)", False, "Incorrect. ISP suggests splitting bloated interfaces."),
            ("Open/Closed Principle (OCP)", False, "Incorrect. OCP focuses on extensibility without modifying existing code."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "SOLID Principles",
        "difficulty": "ADVANCED",
        "content": "How does Dependency Inversion Principle (DIP) apply to Python backend architecture?",
        "code_snippet": "class UserService:\n    def __init__(self, repository: UserRepositoryProtocol):\n        self.repo = repository",
        "explanation": "High-level business logic modules (UserService) should not depend directly on low-level infrastructure modules (SqliteUserRepository). Both should depend on abstractions (Protocols or ABCs), allowing flexible swapping and testing.",
        "options": [
            ("High-level modules should depend on abstractions/protocols rather than concrete implementations", True, "Correct. UserService accepts an abstraction, enabling seamless mock injection or database migration."),
            ("All database queries must be written in raw SQL", False, "Incorrect. DIP is independent of SQL."),
            ("Classes must inherit from at least three base classes", False, "Incorrect. Deep inheritance is often an anti-pattern."),
            ("Dependencies must be defined exclusively in JSON config files", False, "Incorrect. DIP is an architectural code principle, not file configuration."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Testing and Mocking",
        "difficulty": "ADVANCED",
        "content": "Why is the rule 'mock where an object is looked up, not where it is defined' critical when using `unittest.mock.patch`?",
        "code_snippet": "# In services.py: from os import remove\n# In test_services.py:\n@patch('services.remove')  # Correct\n# vs\n@patch('os.remove')        # May fail if services already imported it",
        "explanation": "If `services.py` executes `from os import remove`, it binds `remove` into its own module namespace. Patching `os.remove` modifies the `os` module attribute, but `services.py` continues calling its already-imported local reference.",
        "options": [
            ("Because the consumer module imports and binds its own reference to the object at load time", True, "Correct. Always patch the target path in the module under test: 'my_app.services.remove'."),
            ("Because patching original modules permanently corrupts the Python installation", False, "Incorrect. Mocking only alters runtime memory."),
            ("Because unittest.mock cannot access standard library modules", False, "Incorrect. It can access standard library modules, but lookup binding matters."),
            ("Because Python prohibits mocking C extensions", False, "Incorrect. unittest.mock works on C extensions when patched at consumer lookup."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Testing and Mocking",
        "difficulty": "ADVANCED",
        "content": "What is the difference between `Mock` and `MagicMock` in Python's `unittest.mock` module?",
        "code_snippet": "from unittest.mock import Mock, MagicMock\n\nm1 = Mock()\nm2 = MagicMock()\n# len(m2) works, but len(m1) raises TypeError",
        "explanation": "`MagicMock` is a subclass of `Mock` that comes pre-configured with default implementations for most Python magic/dunder methods (such as `__len__`, `__iter__`, `__enter__`, `__exit__`, `__getitem__`), whereas base `Mock` does not.",
        "options": [
            ("`MagicMock` comes pre-populated with implementations for standard magic/dunder methods", True, "Correct. MagicMock supports context managers, iterators, and operator protocols out-of-the-box."),
            ("`Mock` is thread-safe while `MagicMock` is async-only", False, "Incorrect. Neither makes threading guarantees."),
            ("`MagicMock` compiles into C bytecode for faster test execution", False, "Incorrect. It is standard Python mock class."),
            ("`Mock` is deprecated in Python 3.12+", False, "Incorrect. Both are active standard library classes."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Asyncio",
        "difficulty": "ADVANCED",
        "content": "What does `asyncio.gather(*tasks)` do when one of the tasks raises an unhandled exception by default?",
        "code_snippet": "results = await asyncio.gather(task1(), task2_fails(), task3())",
        "explanation": "By default (`return_exceptions=False`), the first exception raised is immediately propagated to the caller awaiting `gather()`. The other concurrent tasks continue running in the background unless explicitly cancelled.",
        "options": [
            ("Immediately raises that exception to the caller, while other tasks continue running unless cancelled", True, "Correct. Set `return_exceptions=True` to instead capture exceptions as result values."),
            ("Automatically cancels and kills all other tasks instantly", False, "Incorrect. Other tasks continue running unless manually handled or using TaskGroup in Python 3.11+."),
            ("Retries the failed task up to 3 times", False, "Incorrect. asyncio does not provide built-in automatic retries."),
            ("Suppresses the exception and returns None for that task", False, "Incorrect. It does not suppress exceptions by default."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Asyncio",
        "difficulty": "ADVANCED",
        "content": "What major enhancement did `asyncio.TaskGroup` bring to Python 3.11 for structured concurrency?",
        "code_snippet": "async with asyncio.TaskGroup() as tg:\n    tg.create_task(task_a())\n    tg.create_task(task_b())",
        "explanation": "`TaskGroup` enforces structured concurrency: if any child task in the group raises an exception, the remaining tasks are automatically cancelled, and unhandled exceptions are aggregated cleanly in an `ExceptionGroup` upon exiting the context manager.",
        "options": [
            ("Guarantees structured concurrency: automatically cancels sibling tasks if one fails and wraps errors in ExceptionGroup", True, "Correct. Prevents orphaned background tasks and leaks when failures occur."),
            ("Allows async code to run without an event loop", False, "Incorrect. It still operates inside an active asyncio event loop."),
            ("Compiles tasks to WebAssembly", False, "Incorrect. TaskGroup is standard Python asyncio orchestration."),
            ("Disables the GIL for all tasks within the block", False, "Incorrect. It does not alter GIL behavior."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "GIL",
        "difficulty": "ADVANCED",
        "content": "What PEP introduces the free-threaded build option (disabling the GIL) in modern CPython?",
        "code_snippet": "# python3.13 -X gil=0",
        "explanation": "PEP 703 ('Making the Global Interpreter Lock Optional in CPython') introduces a build configuration where the GIL is disabled, using mimalloc, immortal objects, and biased reference counting for true multi-threaded parallel execution.",
        "options": [
            ("PEP 703 (Making the GIL Optional in CPython)", True, "Correct. PEP 703 makes free-threaded CPython available starting in Python 3.13."),
            ("PEP 8 (Style Guide for Python Code)", False, "Incorrect. PEP 8 is formatting and conventions."),
            ("PEP 484 (Type Hints)", False, "Incorrect. PEP 484 introduced type annotations."),
            ("PEP 572 (Assignment Expressions / Walrus Operator)", False, "Incorrect. PEP 572 is the := operator."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Performance Optimization",
        "difficulty": "ADVANCED",
        "content": "What is the computational benefit of using Python `__slots__` in high-throughput data structures?",
        "code_snippet": "class Coordinate:\n    __slots__ = ('lat', 'lon')",
        "explanation": "Without `__slots__`, every Python instance allocates an internal `__dict__` dictionary (typically 100-150+ bytes per instance). `__slots__` stores values in a flat C-array structure, cutting memory usage by 60-70% and providing faster attribute access.",
        "options": [
            ("Eliminates per-instance `__dict__` dictionary overhead, drastically cutting RAM and speeding attribute access", True, "Correct. Crucial when storing millions of objects in memory."),
            ("Forces attributes to be stored in CPU L1 cache", False, "Incorrect. Python does not manage hardware cache lines."),
            ("Enables automatic multithreaded writes without locking", False, "Incorrect. __slots__ does not provide thread synchronization."),
            ("Turns all attributes into PostgreSQL columns", False, "Incorrect. It is a pure CPython object model construct."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Type Hints",
        "difficulty": "ADVANCED",
        "content": "What does `typing.Protocol` enable in Python static type checking (PEP 544)?",
        "code_snippet": "from typing import Protocol\n\nclass Renderable(Protocol):\n    def render(self) -> str: ...",
        "explanation": "`Protocol` provides structural subtyping (static duck typing). A class is considered a valid subtype of a `Protocol` simply by implementing the specified methods and attributes, without needing to explicitly inherit from the Protocol class.",
        "options": [
            ("Structural subtyping (static duck typing) without requiring explicit class inheritance", True, "Correct. Classes don't need to inherit from Renderable; if they have .render() -> str, they pass type checks."),
            ("Network protocol serialization for WebSockets", False, "Incorrect. typing.Protocol is purely a type hint construct."),
            ("Binary packing for ctypes struct interfaces", False, "Incorrect. That is struct or ctypes."),
            ("Cryptographic signing of Python functions", False, "Incorrect. Protocol does not perform cryptography."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Metaclasses",
        "difficulty": "ADVANCED",
        "content": "What method on a class is called when another class inherits from it without needing a full metaclass (PEP 487)?",
        "code_snippet": "class PluginBase:\n    def __init_subclass__(cls, **kwargs):\n        super().__init_subclass__(**kwargs)\n        print(f\"Registered plugin: {cls.__name__}\")",
        "explanation": "`__init_subclass__` (PEP 487) is called whenever the containing class is subclassed. It provides a clean, readable alternative to writing full metaclasses for registering plugins or validating subclass attributes.",
        "options": [
            ("`__init_subclass__`", True, "Correct. __init_subclass__ simplifies hook registration without requiring complex custom metaclasses."),
            ("`__new_subclass__`", False, "Incorrect. No such method exists."),
            ("`__subclass_init__`", False, "Incorrect. The standardized name is __init_subclass__."),
            ("`__post_inherit__`", False, "Incorrect. Invalid method name."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Coroutines",
        "difficulty": "ADVANCED",
        "content": "What is the return type of calling an `async def` function directly without `await`?",
        "code_snippet": "async def greet():\n    return 'hello'\n\nresult = greet()",
        "explanation": "Calling an `async def` function does not immediately execute its code. Instead, it instantiates and returns a `coroutine` object that must be scheduled on an event loop or awaited.",
        "options": [
            ("A `coroutine` object", True, "Correct. You will see `<coroutine object greet at 0x...>` until it is awaited."),
            ("The string `'hello'`", False, "Incorrect. Code inside the coroutine does not execute without being scheduled or awaited."),
            ("A generator object", False, "Incorrect. Standard async def creates native coroutines, not generators."),
            ("A Future object", False, "Incorrect. Futures wrap tasks; calling the function directly returns a coroutine."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Python Internals",
        "difficulty": "ADVANCED",
        "content": "What data structure does CPython use internally to store object attributes in `__dict__`?",
        "code_snippet": "class User:\n    pass\nu = User()\nu.name = 'Ada'",
        "explanation": "CPython uses a specialized compact combined dictionary (PEP 509 / PEP 412 shared keys). For instances of a class sharing the same attribute names, keys are shared in the class table while instances store only an array of values.",
        "options": [
            ("Compact dictionary with shared keys (PEP 412) to minimize memory overhead across instances", True, "Correct. Shared keys reduce memory consumption across multiple instances of the same class."),
            ("Linked list of string tuples", False, "Incorrect. Lookups would be O(N) instead of O(1)."),
            ("B-Tree stored in disk page cache", False, "Incorrect. Dictionaries are in-memory hash tables."),
            ("Red-Black binary search tree", False, "Incorrect. CPython uses open-addressing hash tables, not trees."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Performance Optimization",
        "difficulty": "ADVANCED",
        "content": "Why is `\"\".join(list_of_strings)` significantly faster than repeated string concatenation `s += item` in a loop?",
        "code_snippet": "# Approach A:\ns = ''\nfor w in words: s += w\n\n# Approach B:\ns = ''.join(words)",
        "explanation": "Strings in Python are immutable. Repeated `+=` concatenation allocates a new string in memory and copies all existing characters on every single iteration, leading to O(N^2) quadratic time. `str.join()` calculates total memory required in advance and constructs the result in a single pass O(N).",
        "options": [
            ("Repeated `+=` reallocates and copies memory on every step O(N^2); `.join()` precomputes total buffer length O(N)", True, "Correct. join allocates the final string buffer once and copies characters directly."),
            ("join runs in parallel on GPU hardware", False, "Incorrect. join is a standard C runtime memory copy."),
            ("The `+=` operator is deprecated in Python 3", False, "Incorrect. += is valid, but inefficient in loops."),
            ("join compresses the string using Huffman coding", False, "Incorrect. No compression is applied."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Multiprocessing",
        "difficulty": "ADVANCED",
        "content": "Why must multiprocessing entry code on Windows and macOS be guarded by `if __name__ == '__main__':`?",
        "code_snippet": "from multiprocessing import Process\n\ndef worker(): pass\n\nif __name__ == '__main__':\n    p = Process(target=worker)\n    p.start()",
        "explanation": "On Windows and macOS (which use `spawn` rather than Unix `fork`), worker processes import the main script anew to set up the environment. Without the `__main__` guard, the worker process would re-execute the process creation code recursively, causing an infinite process spawning crash.",
        "options": [
            ("Because `spawn` re-imports the main script in child processes, causing an infinite process fork loop without the guard", True, "Correct. Guarding prevents child processes from re-running startup and spawning logic recursively."),
            ("Because Windows does not support Python functions", False, "Incorrect. Python runs natively on Windows."),
            ("Because the operating system requires elevated administrator rights", False, "Incorrect. Standard permissions apply."),
            ("To disable antivirus scanning on child processes", False, "Incorrect. OS processes are unaffected by __name__."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Descriptors",
        "difficulty": "ADVANCED",
        "content": "What does the `__set_name__` dunder method do on a descriptor (PEP 487)?",
        "code_snippet": "class Field:\n    def __set_name__(self, owner, name):\n        self.name = name",
        "explanation": "`__set_name__(self, owner, name)` is automatically called at class creation time, giving the descriptor knowledge of the attribute name it was assigned to on the class without requiring metaclass introspection.",
        "options": [
            ("Automatically informs the descriptor of the attribute name it was assigned to in the class", True, "Correct. Saves developers from manually passing attribute names like `field = Field('field')`."),
            ("Sets the name of the database table in SQLite", False, "Incorrect. It is part of the Python class creation protocol."),
            ("Renames the class in the module namespace", False, "Incorrect. It operates on attribute descriptors."),
            ("Sets thread-local storage key identifiers", False, "Incorrect. Not related to threading."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "GIL",
        "difficulty": "ADVANCED",
        "content": "What is the check interval mechanism in CPython's GIL scheduler for preempting long-running threads?",
        "code_snippet": "import sys\nprint(sys.getswitchinterval())",
        "explanation": "CPython uses a switch interval (default 5 milliseconds, configurable via `sys.setswitchinterval()`). After this elapsed duration, the running thread is instructed to release the GIL so other waiting threads can acquire it.",
        "options": [
            ("A time-based switch interval (default 5ms) after which the running thread releases the GIL for other waiting threads", True, "Correct. In Python 3.2+, GIL switching transitioned from opcode count (100 ticks) to time-based (5ms)."),
            ("A hardware timer clock in CPU firmware", False, "Incorrect. It is managed by CPython runtime thread state."),
            ("An OS page fault counter", False, "Incorrect. It is time-based."),
            ("A count of memory allocations exceeding 1MB", False, "Incorrect. It regulates CPU thread scheduling."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Testing and Mocking",
        "difficulty": "ADVANCED",
        "content": "How do you test that an exception is raised using Python's `unittest` framework?",
        "code_snippet": "import unittest\n\nclass TestMath(unittest.TestCase):\n    def test_div_zero(self):\n        with self.assertRaises(ZeroDivisionError):\n            1 / 0",
        "explanation": "`self.assertRaises(ExceptionClass)` acts as a context manager (or accepts a callable) that passes the test if the specified exception is raised within the block, and fails if no exception is raised.",
        "options": [
            ("Using `with self.assertRaises(ExpectedException):` context manager", True, "Correct. It asserts that the code inside the with block raises the specified exception."),
            ("Wrapping the code in a manual try/except block without assertions", False, "Incorrect. Manual try/except won't fail if the exception fails to raise unless explicit fail() is called."),
            ("Using `assert raises(ExpectedException)`", False, "Incorrect. 'assert raises' is not valid Python syntax."),
            ("Adding `@unittest.expect_error` decorator", False, "Incorrect. The standard mechanism is assertRaises or pytest.raises."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "MRO",
        "difficulty": "ADVANCED",
        "content": "What property of C3 Linearization ensures that if Class A precedes Class B in a parent's MRO, it will never follow B in any subclass MRO?",
        "code_snippet": "# Class hierarchy monotonicity in Python MRO",
        "explanation": "Monotonicity is the mathematical property of C3 Linearization guaranteeing that the relative precedence order of classes is preserved across all subclasses without inversion.",
        "options": [
            ("Monotonicity", True, "Correct. Monotonicity guarantees consistent relative ordering across the entire inheritance hierarchy."),
            ("Associativity", False, "Incorrect. Associativity relates to grouping in operations."),
            ("Idempotence", False, "Incorrect. Idempotence means repeated execution yields identical result."),
            ("Commutativity", False, "Incorrect. Commutativity allows reordering, whereas MRO strictly forbids arbitrary reordering."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Asyncio",
        "difficulty": "ADVANCED",
        "content": "How should long-running CPU-bound calculations be integrated into an `asyncio` application without freezing the event loop?",
        "code_snippet": "loop = asyncio.get_running_loop()\nresult = await loop.run_in_executor(process_pool, cpu_heavy_func, arg)",
        "explanation": "CPU-bound work should be offloaded to a process pool executor using `loop.run_in_executor()` or `asyncio.to_thread()` (if GIL-releasing C-extensions) so the event loop remains responsive to I/O events.",
        "options": [
            ("Offload the calculation to a `ProcessPoolExecutor` using `loop.run_in_executor()`", True, "Correct. Spawns worker processes that execute on separate CPU cores while the event loop continues processing I/O."),
            ("Wrap the calculation in an empty `async def` and `await` it", False, "Incorrect. Awaiting a synchronous loop in a coroutine still blocks the single thread."),
            ("Call `time.sleep(0)` between calculation steps", False, "Incorrect. time.sleep blocks; asyncio.sleep(0) yields, but still shares the single CPU core."),
            ("Increase the Python interpreter recursion limit", False, "Incorrect. Recursion limit does not relieve CPU blocking."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Type Hints",
        "difficulty": "ADVANCED",
        "content": "What does `typing.TypeVar` with `bound` or `covariant=True` enable in generic programming?",
        "code_snippet": "from typing import TypeVar\nT = TypeVar('T', bound='BaseModel', covariant=True)",
        "explanation": "`TypeVar` defines generic type parameters. `bound` restricts allowed types to a specific class or its subclasses. `covariant=True` preserves subtyping relationships (if Cat is an Animal, Sequence[Cat] is a subtype of Sequence[Animal]).",
        "options": [
            ("Defines generic type parameters with subclass constraints and variance relationships", True, "Correct. Essential for building type-safe container libraries, ORMs, and repositories."),
            ("Allocates shared memory between multiple processes", False, "Incorrect. TypeVar is purely a static type annotation utility."),
            ("Compiles Python generics to C++ templates", False, "Incorrect. Python runtime does not compile to C++ templates."),
            ("Enforces database foreign key constraints", False, "Incorrect. TypeVar is Python type hinting."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Python Internals",
        "difficulty": "ADVANCED",
        "content": "What is the PyObject struct in CPython source code?",
        "code_snippet": "/* CPython object.h */\ntypedef struct _object {\n    _PyObject_HEAD_EXTRA\n    Py_ssize_t ob_refcnt;\n    struct _typeobject *ob_type;\n} PyObject;",
        "explanation": "`PyObject` is the foundational C struct that every Python object in CPython starts with in memory. It contains the reference count (`ob_refcnt`) and a pointer to the object's type descriptor (`ob_type`).",
        "options": [
            ("The universal C header struct containing the reference count and type pointer for every Python object", True, "Correct. Every CPython object memory allocation begins with the PyObject header."),
            ("The Python compiler's bytecode parser", False, "Incorrect. PyObject is runtime object representation."),
            ("The database driver for SQLite", False, "Incorrect. Not related to databases."),
            ("The operating system thread handle for worker threads", False, "Incorrect. Threads use PyThreadState."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "Advanced Decorators",
        "difficulty": "ADVANCED",
        "content": "What problem occurs if a decorator fails to accept `*args` and `**kwargs` in its wrapper function?",
        "code_snippet": "def broken_decorator(fn):\n    def wrapper():  # Missing *args, **kwargs\n        return fn()\n    return wrapper",
        "explanation": "If the decorated function takes arguments, calling it will raise a `TypeError` because the wrapper function signature cannot accept positional or keyword arguments passed by the caller.",
        "options": [
            ("Calling the decorated function with any arguments raises a `TypeError`", True, "Correct. Wrapper functions must accept `*args, **kwargs` to forward parameters transparently."),
            ("The function executes twice automatically", False, "Incorrect. It fails on the first invocation with TypeError."),
            ("The return value is converted to a dictionary", False, "Incorrect. The call fails before reaching return."),
            ("Memory leaks in the Python interpreter", False, "Incorrect. It is a signature mismatch exception."),
        ]
    },
    {
        "category": "Python Advanced",
        "topic": "SOLID Principles",
        "difficulty": "ADVANCED",
        "content": "How does the Interface Segregation Principle (ISP) guide designing Python protocols or interfaces?",
        "code_snippet": "# ISP in Python Protocols:\nclass Reader(Protocol):\n    def read(self) -> bytes: ...\nclass Writer(Protocol):\n    def write(self, data: bytes) -> None: ...",
        "explanation": "Clients should not be forced to depend on methods they do not use. Instead of one large monolithic interface, prefer smaller, cohesive, role-specific interfaces (like `Reader` and `Writer` instead of a combined `ReadWriteSeekFlush` interface).",
        "options": [
            ("Favor smaller, highly cohesive, role-specific interfaces rather than bloated monolithic ones", True, "Correct. Prevents classes from having to implement dummy methods for unused capabilities."),
            ("Every class must have exactly one method", False, "Incorrect. ISP does not restrict classes to single methods."),
            ("Interfaces must be compiled into C shared libraries", False, "Incorrect. ISP is an architectural design guideline."),
            ("All interfaces must be inherited using multiple inheritance", False, "Incorrect. Composition and duck typing are encouraged."),
        ]
    }
]

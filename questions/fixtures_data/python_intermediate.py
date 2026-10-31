# 40 Python Intermediate Questions with 4 options and detailed technical explanations

PYTHON_INTERMEDIATE_QUESTIONS = [
    {
        "category": "Python Intermediate",
        "topic": "OOP",
        "difficulty": "INTERMEDIATE",
        "content": "What is the primary difference between a class variable and an instance variable in Python?",
        "code_snippet": "class Worker:\n    company = 'Acme Corp'  # class variable\n    def __init__(self, name):\n        self.name = name   # instance variable",
        "explanation": "A class variable is shared across all instances of the class and defined within the class body. An instance variable is unique to each instance, bound to `self` typically inside `__init__`.",
        "options": [
            ("Class variables are shared by all instances; instance variables are unique to each instance", True, "Correct. Modifying Worker.company alters it for all instances accessing the class attribute."),
            ("Class variables are public; instance variables are strictly private", False, "Incorrect. Python does not enforce access specifiers through variable scoping."),
            ("Instance variables must be immutable; class variables can be mutable", False, "Incorrect. Both can hold mutable or immutable objects."),
            ("Class variables cannot be accessed via self", False, "Incorrect. self.company resolves the class variable if not shadowed by an instance attribute."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Classes and Objects",
        "difficulty": "INTERMEDIATE",
        "content": "What is the difference between `__str__` and `__repr__` in Python?",
        "code_snippet": "class Item:\n    def __repr__(self):\n        return f\"Item(id={self.id})\"\n    def __str__(self):\n        return f\"{self.name}\"",
        "explanation": "`__repr__` is intended for developers, providing an unambiguous string representation that often resembles valid Python code to recreate the object. `__str__` provides a human-readable representation for end users. If `__str__` is not defined, Python falls back to `__repr__`.",
        "options": [
            ("`__repr__` aims for unambiguous developer/debugging representation; `__str__` is human-readable", True, "Correct. Standard rule: __repr__ is unambiguous; __str__ is readable."),
            ("`__str__` is for developers; `__repr__` is for database queries", False, "Incorrect. That is not the purpose of either dunder method."),
            ("`__repr__` is called by print(); `__str__` is called only in REPL", False, "Incorrect. print() calls __str__ first; REPL evaluates __repr__."),
            ("There is no technical difference between them in Python 3", False, "Incorrect. Python fallback mechanism explicitly checks for __str__ then __repr__."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Inheritance",
        "difficulty": "INTERMEDIATE",
        "content": "What is the purpose of `super().__init__()` in a subclass constructor?",
        "code_snippet": "class Base:\n    def __init__(self, x):\n        self.x = x\n\nclass Child(Base):\n    def __init__(self, x, y):\n        super().__init__(x)\n        self.y = y",
        "explanation": "`super()` delegates method calls to the next class in the Method Resolution Order (MRO). Calling `super().__init__()` ensures parent class initialization logic is executed properly.",
        "options": [
            ("Delegates attribute initialization to the parent class based on MRO", True, "Correct. It invokes the parent's __init__ using MRO without hardcoding the parent class name."),
            ("Prevents child classes from overriding parent attributes", False, "Incorrect. super() does not prevent attribute overrides."),
            ("Instantiates a new instance of the parent class", False, "Incorrect. No new instance is created; it initializes the current instance self."),
            ("Cleans up memory from previous instances", False, "Incorrect. Garbage collection handles memory cleanup."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Polymorphism",
        "difficulty": "INTERMEDIATE",
        "content": "What concept enables polymorphism in Python via 'Duck Typing'?",
        "code_snippet": "def play_sound(duck):\n    duck.quack()",
        "explanation": "'Duck typing' is a programming concept where an object's suitability is determined by the presence of certain methods and properties rather than its inheritance hierarchy ('If it walks like a duck and quacks like a duck, it's a duck').",
        "options": [
            ("An object is evaluated by its interface and behavior rather than its explicit class inheritance", True, "Correct. Python checks whether an object can execute quack(), regardless of whether it inherits from Duck."),
            ("Inheritance from an abstract C-extension base class", False, "Incorrect. Duck typing is dynamic and does not mandate abstract inheritance."),
            ("Overloading function signatures with different argument count", False, "Incorrect. Python does not support classic C++ style static method overloading by default."),
            ("Dynamic compilation using PyPy", False, "Incorrect. Duck typing is a core design philosophy of CPython."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Encapsulation",
        "difficulty": "INTERMEDIATE",
        "content": "How does Python enforce private attribute protection when prefixing an attribute with double underscores `__name`?",
        "code_snippet": "class Account:\n    def __init__(self):\n        self.__balance = 1000",
        "explanation": "Attributes with double leading underscores (and at most one trailing underscore) undergo name mangling: Python renames `__balance` internally to `_ClassName__balance` to avoid naming conflicts in subclasses, rather than enforcing true runtime access restriction.",
        "options": [
            ("Through Name Mangling: it transforms the attribute name to `_ClassName__attribute`", True, "Correct. You can still access obj._Account__balance; it is not private in the C++/Java sense."),
            ("By throwing a security runtime segmentation fault if accessed outside the class", False, "Incorrect. Python has no memory segmentation guards for private attributes."),
            ("By encrypting the attribute value in the Python bytecode", False, "Incorrect. Python does not encrypt variable values in memory."),
            ("By registering the attribute in a hidden thread-local dictionary", False, "Incorrect. Attributes remain on the object's __dict__."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Abstraction",
        "difficulty": "INTERMEDIATE",
        "content": "How do you define an abstract base class with mandatory abstract methods in Python?",
        "code_snippet": "from abc import ABC, abstractmethod\n\nclass Repository(ABC):\n    @abstractmethod\n    def get_by_id(self, id):\n        pass",
        "explanation": "Python's `abc` module provides `ABC` and `@abstractmethod`. If a subclass does not implement all abstract methods, attempting to instantiate the subclass raises `TypeError: Can't instantiate abstract class with abstract methods`.",
        "options": [
            ("Inherit from `abc.ABC` and decorate required methods with `@abstractmethod`", True, "Correct. This triggers TypeError upon instantiation if any abstract method is unimplemented."),
            ("Add `__abstract__ = True` at the top of the class definition", False, "Incorrect. That is an ORM idiom (like in Django models), not standard Python ABCs."),
            ("Raise `NotImplementedError` inside a standard class method without abc inheritance", False, "Incorrect. Raising NotImplementedError only fails at method runtime call, not upon class instantiation."),
            ("Decorate the class with `@dataclass(abstract=True)`", False, "Incorrect. dataclasses do not define abstract classes."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Decorators",
        "difficulty": "INTERMEDIATE",
        "content": "What is a decorator in Python at a fundamental level?",
        "code_snippet": "@timer\ndef compute():\n    pass",
        "explanation": "A decorator is a callable that takes a function as an argument, extends or alters its behavior without permanently modifying the original function's source code, and returns a callable. `@timer def compute():` is syntactic sugar for `compute = timer(compute)`.",
        "options": [
            ("A callable that accepts a function, wraps its behavior, and returns a new callable", True, "Correct. `@dec` syntax is equivalent to `fn = dec(fn)`."),
            ("A compiler directive that optimizes Python bytecode for CPU registers", False, "Incorrect. Decorators are pure runtime callables."),
            ("A special class constructor for singletons", False, "Incorrect. Decorators can be used for singletons, but that is not their definition."),
            ("An asynchronous event handler built into the asyncio loop", False, "Incorrect. Decorators are general-purpose."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Decorators",
        "difficulty": "INTERMEDIATE",
        "content": "Why is `functools.wraps` used when authoring custom decorators?",
        "code_snippet": "from functools import wraps\n\ndef my_decorator(fn):\n    @wraps(fn)\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper",
        "explanation": "`functools.wraps` copies metadata (such as `__name__`, `__doc__`, `__module__`, and annotations) from the original function to the wrapper function, preventing reflection tools and debuggers from losing function identity.",
        "options": [
            ("Preserves the original function's metadata (__name__, __doc__, annotations)", True, "Correct. Without @wraps, fn.__name__ would erroneously display 'wrapper'."),
            ("Prevents the wrapped function from raising exceptions", False, "Incorrect. wraps does not suppress exceptions."),
            ("Automatically executes the wrapper in a parallel thread", False, "Incorrect. Execution remains in the caller thread."),
            ("Enforces strict argument type checking at runtime", False, "Incorrect. wraps copies docstrings and attributes, it does not validate types."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Generators",
        "difficulty": "INTERMEDIATE",
        "content": "What happens when execution encounters a `yield` statement inside a Python function?",
        "code_snippet": "def count_up():\n    yield 1\n    yield 2\n    yield 3",
        "explanation": "The `yield` statement pauses the generator function's execution and produces a value to the caller. The function's execution frame and local variables are preserved on the stack until `next()` is called again.",
        "options": [
            ("Pauses the function, yields the value to the caller, and retains execution state", True, "Correct. Execution resumes immediately following the yield statement on the next next() invocation."),
            ("Terminates the function and cleans up all local variables permanently", False, "Incorrect. That is the behavior of return."),
            ("Executes the remainder of the function in a background worker process", False, "Incorrect. Generators run synchronously in the same thread."),
            ("Converts the yielded value into a NumPy array", False, "Incorrect. Yield produces whatever object is evaluated."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Generators",
        "difficulty": "INTERMEDIATE",
        "content": "What exception is raised when a generator runs out of items to yield?",
        "code_snippet": "g = (x for x in [1])\nnext(g)\nnext(g)  # What exception is raised here?",
        "explanation": "When an iterator or generator reaches its end with no further elements to yield, it raises `StopIteration`. For loops catch this exception automatically to cleanly terminate.",
        "options": [
            ("StopIteration", True, "Correct. Standard iteration protocol signals completion via StopIteration."),
            ("IndexError", False, "Incorrect. Iterators do not track numerical indices."),
            ("GeneratorExit", False, "Incorrect. GeneratorExit is raised when a generator's close() method is called."),
            ("EOFError", False, "Incorrect. EOFError occurs during end-of-file conditions on I/O streams."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Iterators",
        "difficulty": "INTERMEDIATE",
        "content": "What two dunder methods must a class implement to fulfill Python's Iterator Protocol?",
        "code_snippet": "class CountDown:\n    def __iter__(self):\n        return self\n    def __next__(self):\n        ...",
        "explanation": "Python's iterator protocol requires `__iter__()` (which returns the iterator object itself) and `__next__()` (which returns the next element or raises `StopIteration`).",
        "options": [
            ("`__iter__()` and `__next__()`", True, "Correct. __iter__ returns the iterator instance, and __next__ yields values."),
            ("`__len__()` and `__getitem__()`", False, "Incorrect. Those form the Sequence protocol, not the Iterator protocol."),
            ("`__enter__()` and `__exit__()`", False, "Incorrect. Those form the Context Manager protocol."),
            ("`__start__()` and `__step__()`", False, "Incorrect. No such built-in iterator dunder methods exist."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Iterators",
        "difficulty": "INTERMEDIATE",
        "content": "What is the memory advantage of using a generator expression `(x for x in range(10**7))` over a list comprehension `[x for x in range(10**7)]`?",
        "code_snippet": "gen = (x * 2 for x in range(10_000_000))\nlst = [x * 2 for x in range(10_000_000)]",
        "explanation": "A generator produces items lazily on-demand one item at a time, consuming constant O(1) memory. A list comprehension builds and stores the entire 10-million element list in RAM at once, consuming several hundred megabytes.",
        "options": [
            ("Generators evaluate values lazily on-demand with O(1) auxiliary memory footprint", True, "Correct. Memory consumption remains minimal regardless of sequence size."),
            ("Generators bypass the Python interpreter and run in GPU VRAM", False, "Incorrect. Generators run in standard CPython memory."),
            ("List comprehensions are lazy while generators are eagerly evaluated", False, "Incorrect. List comprehensions are eager; generators are lazy."),
            ("Generators can be indexed directly with gen[500]", False, "Incorrect. Generators do not support indexing or slicing without itertools.islice."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Context Managers",
        "difficulty": "INTERMEDIATE",
        "content": "What arguments does `__exit__` receive in a custom context manager class?",
        "code_snippet": "class Transaction:\n    def __enter__(self):\n        return self\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        ...",
        "explanation": "`__exit__` receives three arguments: `exc_type` (the exception class), `exc_val` (the exception instance), and `exc_tb` (the traceback object). If no exception occurred, all three are `None`.",
        "options": [
            ("exc_type, exc_val, exc_tb (exception class, instance, and traceback)", True, "Correct. Returning True from __exit__ suppresses the exception."),
            ("self, status_code, message", False, "Incorrect. Context managers receive exception diagnostics, not status codes."),
            ("self, return_value", False, "Incorrect. __exit__ handles resource teardown and exception inspection."),
            ("self, timeout, killed", False, "Incorrect. Context managers do not take timeout arguments in __exit__."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Context Managers",
        "difficulty": "INTERMEDIATE",
        "content": "How can you suppress an exception inside a custom `__exit__` method?",
        "code_snippet": "class SuppressZeroDivision:\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        if exc_type is ZeroDivisionError:\n            return True",
        "explanation": "If `__exit__` returns a truthy value (such as `True`), Python suppresses the exception and continues execution normally immediately after the `with` block.",
        "options": [
            ("Return `True` from the `__exit__` method", True, "Correct. Returning True signals to Python that the exception was handled and should not propagate."),
            ("Call `sys.exit(0)` inside `__exit__`", False, "Incorrect. sys.exit terminates the entire Python process."),
            ("Return `None` or `False`", False, "Incorrect. Returning False or None causes the exception to be re-raised."),
            ("Set `self.suppress = True`", False, "Incorrect. The return value of __exit__ governs suppression."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "*args and **kwargs",
        "difficulty": "INTERMEDIATE",
        "content": "How do you enforce keyword-only arguments in a Python function definition?",
        "code_snippet": "def configure(timeout, *, retries=3, backoff=1.5):\n    pass",
        "explanation": "A bare asterisk `*` in the parameter list indicates that all parameters following it can only be passed as keyword arguments (PEP 3102). Calling `configure(10, 3, 1.5)` raises a `TypeError`.",
        "options": [
            ("Place a bare `*` before the keyword-only parameters", True, "Correct. Any arguments after a bare `*` must be passed by keyword name."),
            ("Prefix parameter names with `@kwarg`", False, "Incorrect. Python does not support decorator prefixes on parameter names."),
            ("Set default value to `None`", False, "Incorrect. Default values can still be provided positionally unless placed after `*`."),
            ("Enclose parameter names in curly braces `{}`", False, "Incorrect. Curly braces are invalid parameter syntax."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Shallow Copy vs Deep Copy",
        "difficulty": "INTERMEDIATE",
        "content": "What is the key difference between `copy.copy()` and `copy.deepcopy()` in the `copy` module?",
        "code_snippet": "import copy\noriginal = [[1, 2], [3, 4]]\nshallow = copy.copy(original)\ndeep = copy.deepcopy(original)",
        "explanation": "`copy.copy()` creates a new outer collection, but inserts references to the nested objects. `copy.deepcopy()` recursively copies all objects and child objects found within the original.",
        "options": [
            ("Shallow copy copies the outer object referencing original nested children; deep copy recursively copies all nested objects", True, "Correct. Modifying shallow[0].append(99) mutates original[0], while deep does not."),
            ("Shallow copy works on primitives; deep copy works only on classes", False, "Incorrect. Both work on composite objects."),
            ("Shallow copy is immutable; deep copy is mutable", False, "Incorrect. Copy operations preserve container mutability."),
            ("Shallow copy is thread-safe; deep copy is not", False, "Incorrect. Neither makes threading guarantees."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Mutable vs Immutable",
        "difficulty": "INTERMEDIATE",
        "content": "What happens when you pass a mutable list into a function and append an item to it inside the function?",
        "code_snippet": "def add_item(lst):\n    lst.append(99)\n\nnums = [1, 2]\nadd_item(nums)\nprint(nums)",
        "explanation": "Python uses 'call-by-object-reference' (or call-by-sharing). Passing a mutable object passes a reference to that object; modifying it in-place modifies the original object in the caller's scope, printing `[1, 2, 99]`.",
        "options": [
            ("The caller's list is modified in-place to `[1, 2, 99]`", True, "Correct. Because lists are mutable and passed by reference, in-place mutations affect the caller."),
            ("The caller's list remains `[1, 2]` because Python passes copies", False, "Incorrect. Python never creates implicit defensive copies of arguments."),
            ("Raises an UnboundLocalError", False, "Incorrect. In-place mutation does not rebind the variable name."),
            ("Raises an ImmutableObjectError", False, "Incorrect. Lists are fully mutable."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Memory Management",
        "difficulty": "INTERMEDIATE",
        "content": "What primary mechanism does CPython use for memory deallocation?",
        "code_snippet": "import sys\nx = []\nprint(sys.getrefcount(x))",
        "explanation": "CPython's primary memory management mechanism is reference counting: each object tracks how many references point to it. When the reference count reaches 0, the object is immediately deallocated. A cyclic garbage collector runs periodically to detect reference cycles.",
        "options": [
            ("Reference counting supplemented by a cyclic generational garbage collector", True, "Correct. Objects with refcount 0 are deallocated instantly; the gc module catches cyclic references."),
            ("Pure stop-the-world tracing garbage collection like the JVM", False, "Incorrect. CPython does not use a primary stop-the-world tracing collector."),
            ("Manual malloc() and free() calls written by the developer", False, "Incorrect. Memory is managed automatically by Python runtime."),
            ("Static stack allocation during AST compilation", False, "Incorrect. Python objects live on the heap."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Garbage Collection",
        "difficulty": "INTERMEDIATE",
        "content": "Why does Python require a cyclic garbage collector (the `gc` module) in addition to reference counting?",
        "code_snippet": "class Node:\n    def __init__(self):\n        self.neighbor = None\n\na = Node()\nb = Node()\na.neighbor = b\nb.neighbor = a\ndel a, b",
        "explanation": "Reference counting cannot clean up cyclic references (where object A points to B and B points to A). Even after deleting `a` and `b`, each object's refcount remains 1, causing a memory leak unless detected by Python's generational cyclic garbage collector.",
        "options": [
            ("To detect and reclaim isolated circular reference cycles that reference counting cannot resolve", True, "Correct. Cyclic graphs retain positive refcounts even when disconnected from the root."),
            ("To compact fragmented heap memory every 60 seconds", False, "Incorrect. CPython does not perform heap compaction."),
            ("To release GIL lock contention across worker threads", False, "Incorrect. The GIL is thread synchronization, unrelated to memory cycles."),
            ("To free string literals loaded in bytecode", False, "Incorrect. Interned string literals persist for the interpreter lifespan."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "OOP",
        "difficulty": "INTERMEDIATE",
        "content": "What does `@classmethod` receive as its first argument compared to `@staticmethod`?",
        "code_snippet": "class MathService:\n    @classmethod\n    def from_string(cls, data):\n        pass\n    @staticmethod\n    def add(a, b):\n        pass",
        "explanation": "A `@classmethod` receives the class itself (`cls`) as its first argument, allowing access to class state and factory constructors. A `@staticmethod` receives neither `self` nor `cls`; it behaves like an ordinary function namespaced inside the class.",
        "options": [
            ("`@classmethod` receives `cls` (the class object); `@staticmethod` receives no implicit first argument", True, "Correct. Class methods can inspect or instantiate the class; static methods are pure utility functions."),
            ("`@classmethod` receives `self`; `@staticmethod` receives `cls`", False, "Incorrect. Instance methods receive self."),
            ("`@staticmethod` is private; `@classmethod` is public", False, "Incorrect. Both have identical visibility."),
            ("`@classmethod` cannot be called on an instance", False, "Incorrect. Both class and static methods can be invoked on instances or classes."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "OOP",
        "difficulty": "INTERMEDIATE",
        "content": "What is the purpose of the `@property` decorator in Python?",
        "code_snippet": "class Circle:\n    def __init__(self, radius):\n        self._radius = radius\n    @property\n    def radius(self):\n        return self._radius\n    @radius.setter\n    def radius(self, value):\n        if value < 0: raise ValueError()\n        self._radius = value",
        "explanation": "`@property` defines a getter (and optionally setters and deleters) that allows a method to be accessed using standard attribute lookup syntax (`circle.radius`), enabling validation and encapsulation without changing public API syntax.",
        "options": [
            ("Defines getters and setters accessible with attribute access syntax", True, "Correct. It implements descriptor protocol to intercept attribute reads/writes cleanly."),
            ("Converts an instance method into a background thread", False, "Incorrect. property has nothing to do with threads."),
            ("Makes an attribute immutable at the OS level", False, "Incorrect. Python attributes are not locked at OS level."),
            ("Automatically serializes the property to JSON", False, "Incorrect. property does not perform serialization."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Classes and Objects",
        "difficulty": "INTERMEDIATE",
        "content": "What is `__slots__` used for in Python classes?",
        "code_snippet": "class Point:\n    __slots__ = ('x', 'y')\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y",
        "explanation": "`__slots__` tells Python not to use a dynamic `__dict__` dictionary for storing instance attributes. Instead, it allocates a fixed set of attributes, significantly reducing memory overhead per instance and preventing arbitrary attribute assignment.",
        "options": [
            ("Prevents creation of instance `__dict__`, saving memory and preventing undeclared attributes", True, "Correct. Ideal for millions of small objects to save RAM footprint."),
            ("Enforces type hinting at compilation time", False, "Incorrect. __slots__ limits attribute names, not types."),
            ("Creates database columns automatically in SQLite", False, "Incorrect. __slots__ is pure Python object model."),
            ("Allows classes to inherit from multiple metaclasses", False, "Incorrect. __slots__ does not affect metaclass inheritance."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Inheritance",
        "difficulty": "INTERMEDIATE",
        "content": "How does Python resolve method calls in multiple inheritance?",
        "code_snippet": "class A:\n    pass\nclass B(A):\n    pass\nclass C(A):\n    pass\nclass D(B, C):\n    pass\nprint(D.__mro__)",
        "explanation": "Python uses the C3 Linearization algorithm to determine the Method Resolution Order (MRO), ensuring monotonicity and preserving local precedence ordering in multiple inheritance diamond hierarchies.",
        "options": [
            ("Using the C3 Linearization algorithm to establish the MRO (Method Resolution Order)", True, "Correct. Python inspects classes according to the C3 MRO order visible in Class.__mro__."),
            ("Depth-first search traversing the left-most branch first indefinitely", False, "Incorrect. Python 2.2+ abandoned old depth-first search in favor of C3 linearization to handle diamond problems."),
            ("Random selection between conflicting parent classes", False, "Incorrect. Resolution is strictly deterministic."),
            ("The latest declared class always overwrites all prior classes", False, "Incorrect. MRO maintains strict hierarchy rules."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Decorators",
        "difficulty": "INTERMEDIATE",
        "content": "How do you pass arguments to a decorator itself (decorator factory)?",
        "code_snippet": "@repeat(num_times=3)\ndef greet():\n    print(\"Hello\")",
        "explanation": "A decorator that takes arguments is a 'decorator factory'—an outer function that accepts the configuration arguments and returns the actual decorator function, which in turn accepts the target function.",
        "options": [
            ("Wrap the decorator in an outer factory function that returns the decorator", True, "Correct. 3 nested functions: factory(args) -> decorator(fn) -> wrapper(*args, **kwargs)."),
            ("Pass the arguments into *args of the target function", False, "Incorrect. Decorator configuration belongs to the decorator factory."),
            ("Use the `@dataclass` decorator with parameters", False, "Incorrect. Dataclass is a specific standard library utility."),
            ("Modify `sys.set_decorator_args()`", False, "Incorrect. No such Python function exists."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Generators",
        "difficulty": "INTERMEDIATE",
        "content": "What does `yield from` do when used inside a generator?",
        "code_snippet": "def generator_a():\n    yield from [1, 2, 3]\n    yield from range(4, 6)",
        "explanation": "`yield from <iterable>` delegates part of its operations to another generator or iterable, transparently passing yielded values out and bi-directionally forwarding `send()`, `throw()`, and `close()` calls.",
        "options": [
            ("Delegates generation to a sub-iterable or sub-generator transparently", True, "Correct. Introduced in PEP 380 to cleanly flatten and delegate nested generator pipelines."),
            ("Terminates the generator and returns a list", False, "Incorrect. yield from continues yielding values one-by-one."),
            ("Imports generator functions from another file", False, "Incorrect. It is generator delegation syntax, not module import."),
            ("Spawns a greenlet coroutine", False, "Incorrect. It is standard synchronous generator delegation."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Context Managers",
        "difficulty": "INTERMEDIATE",
        "content": "How can you easily write a context manager using a generator function instead of a class?",
        "code_snippet": "from contextlib import contextmanager\n\n@contextmanager\ndef managed_resource():\n    print(\"Acquired\")\n    try:\n        yield \"Resource\"\n    finally:\n        print(\"Released\")",
        "explanation": "`contextlib.contextmanager` turns a generator function into a context manager. Code prior to `yield` acts as `__enter__`, the yielded value is bound to the `as` variable, and code in `finally` acts as `__exit__`.",
        "options": [
            ("Use `@contextlib.contextmanager` with a generator containing a `try...finally` block", True, "Correct. Everything before yield is setup; code after yield in finally is teardown."),
            ("Decorate the function with `@staticmethod`", False, "Incorrect. staticmethod does not provide enter/exit context protocol."),
            ("Add `return with self` inside the generator", False, "Incorrect. Invalid syntax."),
            ("Context managers can only be written as classes", False, "Incorrect. contextlib.contextmanager is the idiomatic Python shortcut."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Mutable vs Immutable",
        "difficulty": "INTERMEDIATE",
        "content": "What is the result of `t = (1, 2, [3, 4]); t[2].append(5)` in Python?",
        "code_snippet": "t = (1, 2, [3, 4])\nt[2].append(5)\nprint(t)",
        "explanation": "A tuple is immutable in that its references cannot be changed (`t[2] = ...` fails). However, the referenced objects themselves can be mutable. Appending to the nested list mutates the list in-place, resulting in `(1, 2, [3, 4, 5])`.",
        "options": [
            ("(1, 2, [3, 4, 5]) - the nested mutable object is modified successfully", True, "Correct. Immutability applies to the tuple's bindings, not to the internal states of referenced objects."),
            ("TypeError: 'tuple' object does not support item assignment", False, "Incorrect. .append() mutates the list in-place without reassigning the tuple slot."),
            ("ValueError: nested list is frozen", False, "Incorrect. Python does not freeze nested objects inside tuples."),
            ("(1, 2, [3, 4]) - the mutation is silently discarded", False, "Incorrect. The mutation takes effect immediately."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Memory Management",
        "difficulty": "INTERMEDIATE",
        "content": "What is Python 'String Interning' and when does CPython perform it automatically?",
        "code_snippet": "s1 = \"interview_master\"\ns2 = \"interview_master\"\nprint(s1 is s2)",
        "explanation": "Interning ensures that only one copy of distinct string objects is stored in memory. CPython automatically interns compile-time constants that resemble Python identifiers (alphanumeric and underscores), so `s1 is s2` evaluates to `True`.",
        "options": [
            ("Reusing identical immutable string instances in memory so `s1 is s2` is True", True, "Correct. Saves memory and allows fast pointer comparisons instead of full character comparisons."),
            ("Compressing strings using zlib during runtime", False, "Incorrect. Strings are not compressed in RAM."),
            ("Converting all strings into ASCII byte arrays", False, "Incorrect. Python 3 strings are Unicode (PEP 393 flexible string representation)."),
            ("Encrypting sensitive strings from core memory dumps", False, "Incorrect. Interning is an optimization, not encryption."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "OOP",
        "difficulty": "INTERMEDIATE",
        "content": "What is the difference between `__new__` and `__init__` in Python?",
        "code_snippet": "class Singleton:\n    def __new__(cls, *args, **kwargs):\n        ...\n    def __init__(self):\n        ...",
        "explanation": "`__new__` is a static method that creates and returns a new instance of the class (allocator). `__init__` initializes the created instance (`self`) after it has been created. `__new__` is used to implement singletons or customize immutable object creation.",
        "options": [
            ("`__new__` creates and returns the instance object; `__init__` initializes that instance", True, "Correct. __new__ is the real constructor; __init__ is the initializer."),
            ("`__init__` allocates memory; `__new__` is called on garbage collection", False, "Incorrect. __del__ is the destructor on deallocation."),
            ("`__new__` is only used in Python 2; `__init__` in Python 3", False, "Incorrect. Both exist and serve identical roles in Python 3."),
            ("`__init__` returns the object to the caller", False, "Incorrect. __init__ must always return None; returning a value raises TypeError."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Classes and Objects",
        "difficulty": "INTERMEDIATE",
        "content": "What does `hasattr(obj, 'prop')` do under the hood in Python?",
        "code_snippet": "if hasattr(user, 'profile'):\n    print(user.profile)",
        "explanation": "`hasattr(obj, name)` calls `getattr(obj, name)` and checks whether an `AttributeError` is raised. If `getattr` succeeds, it returns `True`; if `AttributeError` is caught, it returns `False`.",
        "options": [
            ("Calls `getattr(obj, name)` and catches `AttributeError`", True, "Correct. It tests attribute access by attempting retrieval and catching AttributeError."),
            ("Directly checks `obj.__dict__` keys without triggering property getters", False, "Incorrect. hasattr DOES trigger @property getters!"),
            ("Inspects Python AST token tables", False, "Incorrect. hasattr is a runtime introspection function."),
            ("Scans module bytecode symbols", False, "Incorrect. It operates on live instance attributes and descriptors."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Decorators",
        "difficulty": "INTERMEDIATE",
        "content": "Can a class be used as a decorator in Python?",
        "code_snippet": "class CountCalls:\n    def __init__(self, fn):\n        self.fn = fn\n        self.calls = 0\n    def __call__(self, *args, **kwargs):\n        self.calls += 1\n        return self.fn(*args, **kwargs)",
        "explanation": "Yes. Any class that implements the `__call__` dunder method is callable and can act as a decorator, maintaining state across invocations via instance attributes.",
        "options": [
            ("Yes, by implementing the `__call__` dunder method on the class", True, "Correct. Instances of the class become callable and can wrap functions while maintaining state."),
            ("No, only functions defined with `def` can be decorators", False, "Incorrect. Any Python callable can be a decorator."),
            ("Yes, but only if the class inherits from `DecoratorBase`", False, "Incorrect. No special base class is required."),
            ("No, classes cannot intercept function calls", False, "Incorrect. __call__ enables full function interception."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Garbage Collection",
        "difficulty": "INTERMEDIATE",
        "content": "What is the purpose of generations (0, 1, 2) in Python's garbage collection?",
        "code_snippet": "import gc\nprint(gc.get_count())\nprint(gc.get_threshold())",
        "explanation": "Python's cyclic GC is generational based on the weak generational hypothesis: most objects die young. Gen 0 is collected most frequently. Surviving objects are promoted to Gen 1, and eventually Gen 2, which is collected least often.",
        "options": [
            ("Optimizes GC frequency based on object age: younger objects (Gen 0) are scanned more frequently", True, "Correct. Generation 0 is collected frequently; long-lived objects in Gen 2 are scanned rarely."),
            ("Separates variables by their thread ID", False, "Incorrect. Generations are age tiers, not thread pools."),
            ("Tracks variables allocated in C extensions versus pure Python", False, "Incorrect. Both can be tracked in the same GC heaps."),
            ("Allocates memory across CPU cache L1, L2, and L3", False, "Incorrect. Generations are Python heap classifications, not hardware caches."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Shallow Copy vs Deep Copy",
        "difficulty": "INTERMEDIATE",
        "content": "What happens if you slice a list with `a[:]`?",
        "code_snippet": "a = [[1], [2]]\nb = a[:]\nb[0].append(99)\nprint(a)",
        "explanation": "Slicing `a[:]` creates a shallow copy of the list. The outer list is a new object, but it references the same nested list elements, so `a` becomes `[[1, 99], [2]]`.",
        "options": [
            ("It creates a shallow copy of the list", True, "Correct. Slicing copies the top-level list container only, not nested mutable objects."),
            ("It creates a full deep copy of all elements recursively", False, "Incorrect. Slicing never performs deep copies."),
            ("It creates a read-only immutable view of the list", False, "Incorrect. The slice is a normal mutable list."),
            ("It freezes the list memory block", False, "Incorrect. Python does not freeze list memory."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Generators",
        "difficulty": "INTERMEDIATE",
        "content": "What does the `.send(value)` method do on an active generator?",
        "code_snippet": "def echo():\n    while True:\n        val = yield\n        print(f\"Received: {val}\")\n\ng = echo()\nnext(g)\ng.send(\"Django\")",
        "explanation": "`.send(value)` resumes the generator and sends a value into the generator function that becomes the result of the current `yield` expression.",
        "options": [
            ("Resumes the generator, injecting the value as the result of the `yield` expression", True, "Correct. This enables coroutine-style bidirectional data passing."),
            ("Sends a message to an OS thread queue", False, "Incorrect. send() operates within the single generator execution frame."),
            ("Restarts the generator from the first line", False, "Incorrect. Execution resumes exactly where it was paused at yield."),
            ("Changes the generator return type to string", False, "Incorrect. Generator types do not change."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "OOP",
        "difficulty": "INTERMEDIATE",
        "content": "What dunder method is invoked when an object is called like a function `obj()`?",
        "code_snippet": "class Greeter:\n    def __call__(self, name):\n        return f\"Hello {name}\"\n\ng = Greeter()\nprint(g(\"Elena\"))",
        "explanation": "The `__call__` method allows an instance of a class to be called as a function. Any object with `__call__` returns `True` for `callable(obj)`.",
        "options": [
            ("`__call__`", True, "Correct. Implementing __call__ makes an instance callable like a function."),
            ("`__invoke__`", False, "Incorrect. __invoke__ is not a Python dunder method (it exists in PHP)."),
            ("`__run__`", False, "Incorrect. __run__ is not part of standard Python data model."),
            ("`__exec__`", False, "Incorrect. Python uses exec() function, not __exec__ method."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "OOP",
        "difficulty": "INTERMEDIATE",
        "content": "What is the output of `isinstance(True, int)` in Python?",
        "code_snippet": "print(isinstance(True, int))\nprint(issubclass(bool, int))",
        "explanation": "In Python, `bool` is an explicit subclass of `int` (`issubclass(bool, int) is True`). `True` has the integer value `1` and `False` has `0`, so `isinstance(True, int)` is `True`.",
        "options": [
            ("True - because `bool` is a subclass of `int` in Python", True, "Correct. Historically and architecturally in Python, bool inherits directly from int."),
            ("False - boolean is a distinct primitive unrelated to integers", False, "Incorrect. bool subclasses int directly in Python."),
            ("Raises a TypeError", False, "Incorrect. isinstance accepts valid types and instances."),
            ("None", False, "Incorrect. isinstance always returns a boolean."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Classes and Objects",
        "difficulty": "INTERMEDIATE",
        "content": "What happens when you define `__eq__` on a custom class without defining `__hash__` in Python 3?",
        "code_snippet": "class Person:\n    def __init__(self, name):\n        self.name = name\n    def __eq__(self, other):\n        return self.name == other.name\n\np = Person('Sam')\ns = {p}  # What happens here?",
        "explanation": "In Python 3, if a class overrides `__eq__` but does not define `__hash__`, Python automatically sets `__hash__ = None`. Instances of the class become unhashable, raising `TypeError: unhashable type: 'Person'` when placed in a set or dictionary.",
        "options": [
            ("The class becomes unhashable (`__hash__ = None`), raising TypeError in sets/dicts", True, "Correct. To maintain the hash contract (equal objects must have equal hashes), Python disables hashing."),
            ("It falls back to hashing the memory ID of the object", False, "Incorrect. In Python 2 it did, but Python 3 explicitly sets __hash__ = None."),
            ("It automatically computes the MD5 hash of the class name", False, "Incorrect. Python does not auto-generate MD5 hashes."),
            ("Instances can be used in sets without error", False, "Incorrect. A TypeError is raised."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Context Managers",
        "difficulty": "INTERMEDIATE",
        "content": "What built-in module provides utility context managers like `closing`, `suppress`, and `redirect_stdout`?",
        "code_snippet": "from contextlib import suppress\n\nwith suppress(FileNotFoundError):\n    os.remove('temp.log')",
        "explanation": "The `contextlib` module in Python's standard library provides utilities for common context manager patterns, including `suppress`, `closing`, `nullcontext`, and `ExitStack`.",
        "options": [
            ("`contextlib`", True, "Correct. contextlib is the standard library module for context manager helpers."),
            ("`os.context`", False, "Incorrect. No such module exists."),
            ("`functools`", False, "Incorrect. functools provides higher-order functions like lru_cache, partial, wraps."),
            ("`itertools`", False, "Incorrect. itertools provides iterator building blocks."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "OOP",
        "difficulty": "INTERMEDIATE",
        "content": "What is the purpose of `__getattr__` versus `__getattribute__` in Python?",
        "code_snippet": "class DynamicModel:\n    def __getattr__(self, name):\n        return f\"Dynamic {name}\"\n    def __getattribute__(self, name):\n        return super().__getattribute__(name)",
        "explanation": "`__getattribute__` is called unconditionally for every single attribute access. `__getattr__` is called only as a fallback when the requested attribute was NOT found in the object's `__dict__` or class hierarchy.",
        "options": [
            ("`__getattribute__` is invoked on every access; `__getattr__` is called only when the attribute is not found", True, "Correct. __getattr__ is the safe fallback; __getattribute__ intercepts all lookups."),
            ("`__getattr__` is called on every access; `__getattribute__` is called on failure", False, "Incorrect. The roles are reversed."),
            ("`__getattr__` is for private variables only", False, "Incorrect. Visibility does not dictate invocation."),
            ("`__getattribute__` was deprecated in Python 3.10", False, "Incorrect. It is fundamental to Python's descriptor engine."),
        ]
    },
    {
        "category": "Python Intermediate",
        "topic": "Mutable vs Immutable",
        "difficulty": "INTERMEDIATE",
        "content": "Which of the following built-in collection types in Python is immutable?",
        "code_snippet": "a = frozenset([1, 2, 3])\nb = set([1, 2, 3])\nc = bytearray(b'hello')\nd = dict(a=1)",
        "explanation": "`frozenset` is the immutable version of a Python `set`. Because it is immutable and hashable, a frozenset can be used as a dictionary key or an element of another set.",
        "options": [
            ("`frozenset`", True, "Correct. frozenset is immutable and hashable, unlike standard set."),
            ("`bytearray`", False, "Incorrect. bytearray is a mutable sequence of bytes; bytes is immutable."),
            ("`set`", False, "Incorrect. set is mutable via add/remove."),
            ("`dict`", False, "Incorrect. dict is mutable."),
        ]
    }
]

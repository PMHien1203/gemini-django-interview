# 40 Python Beginner Questions with 4 options and detailed explanations

PYTHON_BEGINNER_QUESTIONS = [
    {
        "category": "Python Fundamentals",
        "topic": "Variables and Data Types",
        "difficulty": "BEGINNER",
        "content": "Which of the following data types in Python is mutable?",
        "code_snippet": "a = [1, 2, 3]\nb = (1, 2, 3)\nc = \"123\"\nd = 123",
        "explanation": "Lists in Python are mutable, meaning their elements can be modified in-place without altering the object's identity. Tuples, strings, and integers are immutable.",
        "options": [
            ("List (e.g., [1, 2, 3])", True, "Correct! Lists allow in-place item assignment, append, pop, and mutation."),
            ("Tuple (e.g., (1, 2, 3))", False, "Incorrect. Tuples are immutable once initialized."),
            ("String (e.g., '123')", False, "Incorrect. Strings in Python cannot have characters changed in-place."),
            ("Integer (e.g., 123)", False, "Incorrect. Primitive numbers are immutable value objects."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Variables and Data Types",
        "difficulty": "BEGINNER",
        "content": "What will be the output of type(10 / 2) in Python 3?",
        "code_snippet": "result = 10 / 2\nprint(type(result))",
        "explanation": "In Python 3, the standard division operator `/` always produces a float, even if the division has no remainder (10 / 2 results in 5.0). Use `//` for integer floor division.",
        "options": [
            ("<class 'float'>", True, "Correct. Standard division `/` always yields a float in Python 3."),
            ("<class 'int'>", False, "Incorrect. True division yields 5.0 (a float)."),
            ("<class 'double'>", False, "Incorrect. Python does not have a distinct 'double' primitive type; floating point numbers are 'float'."),
            ("<class 'number'>", False, "Incorrect. 'number' is not a built-in Python type."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Strings",
        "difficulty": "BEGINNER",
        "content": "What does the string method .strip() do by default?",
        "code_snippet": "text = \"   Python Developer   \"\ncleaned = text.strip()",
        "explanation": "By default, `.strip()` removes all leading and trailing whitespace characters (spaces, tabs, newlines) from a string without modifying the internal characters.",
        "options": [
            ("Removes leading and trailing whitespace", True, "Correct. It strips whitespace from both ends."),
            ("Removes all spaces everywhere inside the string", False, "Incorrect. Internal whitespace is preserved."),
            ("Converts the string into a list of characters", False, "Incorrect. That would be list(text)."),
            ("Splits the string by commas", False, "Incorrect. That is text.split(',')."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Strings",
        "difficulty": "BEGINNER",
        "content": "What is the result of the slice text[::-1] on a string in Python?",
        "code_snippet": "s = \"Django\"\nprint(s[::-1])",
        "explanation": "The slice syntax `[start:stop:step]` with a step of `-1` and omitted start and stop traverses the sequence backwards, reversing the string.",
        "options": [
            ("It reverses the string to 'ognajD'", True, "Correct. Step of -1 reverses any sequence in Python."),
            ("It produces an IndexError", False, "Incorrect. Python slicing does not raise IndexError for negative indices or steps."),
            ("It returns only the last character 'o'", False, "Incorrect. Accessing s[-1] returns the last character."),
            ("It prints 'Django' without modification", False, "Incorrect. The negative step reverses iteration direction."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Numbers",
        "difficulty": "BEGINNER",
        "content": "What is the difference between `//` and `%` in Python arithmetic?",
        "code_snippet": "a = 17 // 5\nb = 17 % 5",
        "explanation": "`//` computes integer floor division (17 // 5 == 3), whereas `%` is the modulo operator that returns the remainder of division (17 % 5 == 2).",
        "options": [
            ("// returns the quotient rounded down (floor division), % returns remainder", True, "Correct. 17 // 5 is 3 and 17 % 5 is 2."),
            ("// returns power, % returns square root", False, "Incorrect. Power operator is **."),
            ("// is bitwise shift, % is percentage", False, "Incorrect. Bitwise shift is >> and <<."),
            ("Both operators perform exact floating-point division", False, "Incorrect. Exact division is single slash /."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Lists",
        "difficulty": "BEGINNER",
        "content": "What happens when you call .append([4, 5]) on a list [1, 2, 3]?",
        "code_snippet": "nums = [1, 2, 3]\nnums.append([4, 5])\nprint(nums)",
        "explanation": "`append()` adds its argument as a single element at the end of the list, resulting in a nested list [1, 2, 3, [4, 5]]. To flatten items into the list, you should use `extend()`.",
        "options": [
            ("[1, 2, 3, [4, 5]]", True, "Correct! append() adds the list as a single nested element."),
            ("[1, 2, 3, 4, 5]", False, "Incorrect. That is the behavior of extend() or +=."),
            ("TypeError: cannot append list to list", False, "Incorrect. Python lists can contain any arbitrary object type."),
            ("[4, 5, 1, 2, 3]", False, "Incorrect. append() places elements at the end, not the start."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Lists",
        "difficulty": "BEGINNER",
        "content": "How do you access the last item of a Python list without knowing its length?",
        "code_snippet": "items = ['python', 'django', 'fastapi', 'flask']",
        "explanation": "Negative indexing in Python counts backward from the end, so `items[-1]` returns the final element.",
        "options": [
            ("items[-1]", True, "Correct. Index -1 refers to the last element in any sequence."),
            ("items[end]", False, "Incorrect. 'end' is not a built-in sequence keyword."),
            ("items.last()", False, "Incorrect. Built-in Python lists do not have a .last() method."),
            ("items[len(items)]", False, "Incorrect. This will raise IndexError because indices are 0-based."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Tuples",
        "difficulty": "BEGINNER",
        "content": "How do you create a tuple with exactly one single element?",
        "code_snippet": "x = (42,)",
        "explanation": "In Python, parentheses alone do not create a tuple; the comma `,` defines the tuple syntax. `(42)` is just the integer 42 inside grouping parentheses, while `(42,)` is a 1-tuple.",
        "options": [
            ("(42,)", True, "Correct. A trailing comma is required for a single-element tuple."),
            ("(42)", False, "Incorrect. Parentheses without a comma are evaluated as arithmetic grouping, yielding int 42."),
            ("tuple[42]", False, "Incorrect. This syntax is type hint subscripting in modern Python, not instantiation."),
            ("new tuple(42)", False, "Incorrect. 'new' is not a Python keyword."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Tuples",
        "difficulty": "BEGINNER",
        "content": "Why are tuples commonly preferred over lists for dictionary keys in Python?",
        "code_snippet": "locations = {(40.7128, -74.0060): 'New York City'}",
        "explanation": "Dictionary keys must be hashable. Because tuples are immutable (assuming their elements are also hashable), they implement `__hash__`, unlike mutable lists.",
        "options": [
            ("Tuples are immutable and hashable, whereas lists are unhashable", True, "Correct. Dict keys must be hashable to compute hash bucket offsets."),
            ("Tuples use less syntax and compile faster", False, "Incorrect. While tuples are compact, hashability is the strict technical requirement."),
            ("Lists cannot store numbers or strings", False, "Incorrect. Lists can store any Python objects."),
            ("Python dictionaries only accept tuple keys", False, "Incorrect. Any hashable type (int, str, frozenset) can be a key."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Sets",
        "difficulty": "BEGINNER",
        "content": "What is the primary characteristic of a Python set?",
        "code_snippet": "s = {1, 2, 2, 3, 3, 3}\nprint(len(s))",
        "explanation": "A set is an unordered collection of unique, hashable elements. Duplicate entries are automatically discarded, so `len({1, 2, 2, 3, 3, 3})` is 3.",
        "options": [
            ("Unordered collection of unique elements", True, "Correct. Sets enforce uniqueness and do not maintain duplicate values."),
            ("Ordered sequence that allows duplicates", False, "Incorrect. That describes a list or tuple."),
            ("Key-value mapping where keys can be duplicated", False, "Incorrect. That resembles a multimap, which is not built-in set behavior."),
            ("Immutable sequence that only accepts integers", False, "Incorrect. Sets are mutable and accept any hashable elements."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Sets",
        "difficulty": "BEGINNER",
        "content": "Which operator performs set union in Python?",
        "code_snippet": "a = {1, 2}\nb = {2, 3}\nc = a | b",
        "explanation": "The pipe operator `|` computes the union of two sets, returning all unique elements from both sets ({1, 2, 3}). `&` is intersection, and `-` is difference.",
        "options": [
            ("| operator or .union()", True, "Correct. `a | b` or `a.union(b)` merges unique items."),
            ("& operator", False, "Incorrect. & computes intersection."),
            ("+ operator", False, "Incorrect. The + operator is not supported between sets."),
            ("^ operator", False, "Incorrect. ^ computes symmetric difference."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Dictionaries",
        "difficulty": "BEGINNER",
        "content": "What will d.get('age', 25) return if 'age' is not present in dictionary d?",
        "code_snippet": "d = {'name': 'Alice'}\nprint(d.get('age', 25))",
        "explanation": "The `.get(key, default)` method looks up `key`. If found, it returns the value; if missing, it returns the supplied default argument (25) without raising a KeyError.",
        "options": [
            ("25", True, "Correct. The second parameter serves as the fallback default when the key is absent."),
            ("KeyError exception", False, "Incorrect. .get() avoids raising KeyError by design."),
            ("None", False, "Incorrect. None is only returned if no default argument is provided."),
            ("False", False, "Incorrect. Python does not default missing dictionary lookups to False."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Dictionaries",
        "difficulty": "BEGINNER",
        "content": "What does d.items() return in Python 3?",
        "code_snippet": "user = {'id': 1, 'role': 'admin'}\nfor k, v in user.items():\n    pass",
        "explanation": "In Python 3, `d.items()` returns a dynamic dict_items view object containing (key, value) 2-tuples that reflects changes made to the dictionary in real-time.",
        "options": [
            ("A dynamic view of (key, value) pairs as tuples", True, "Correct. dict_items provides an iterable view of key-value tuples."),
            ("A static static list of only keys", False, "Incorrect. That is d.keys()."),
            ("A list of values only", False, "Incorrect. That is d.values()."),
            ("A single JSON string", False, "Incorrect. You need json.dumps() for JSON serialization."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Conditional Statements",
        "difficulty": "BEGINNER",
        "content": "Which of the following values evaluates to False in a boolean context in Python?",
        "code_snippet": "values = [0, '', [], None, set()]\nfor v in values:\n    print(bool(v))",
        "explanation": "In Python, numeric zero (0, 0.0), empty strings (''), empty containers ([], {}, set(), ()), and `None` all evaluate to `False` (truthiness rules).",
        "options": [
            ("All of the above (0, '', [], None)", True, "Correct. All empty sequences, zero numbers, and None are falsy in Python."),
            ("Only None", False, "Incorrect. 0, empty string, and empty list are also falsy."),
            ("Only 0 and None", False, "Incorrect. Empty containers are falsy as well."),
            ("Only negative numbers", False, "Incorrect. Negative numbers evaluate to True in boolean contexts."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Conditional Statements",
        "difficulty": "BEGINNER",
        "content": "What is the ternary operator syntax in Python?",
        "code_snippet": "status = 'Adult' if age >= 18 else 'Minor'",
        "explanation": "Python's conditional expression (ternary) follows the syntax: `value_if_true if condition else value_if_false`.",
        "options": [
            ("x = true_val if condition else false_val", True, "Correct. Python uses the readable 'if/else' expression syntax."),
            ("x = condition ? true_val : false_val", False, "Incorrect. C/JavaScript ternary operator syntax is not valid in Python."),
            ("x = if (condition) true_val else false_val", False, "Incorrect. 'if' cannot lead inline assignment without parens."),
            ("x = condition and true_val or false_val only", False, "Incorrect. While an old idiom, it fails when true_val is falsy."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Loops",
        "difficulty": "BEGINNER",
        "content": "When is the `else` block of a Python `for` or `while` loop executed?",
        "code_snippet": "for n in range(5):\n    if n == 10:\n        break\nelse:\n    print('Completed without break')",
        "explanation": "The `else` clause attached to a loop executes only when the loop terminates normally (exhausts the iterable or while condition becomes False), and is skipped if the loop is terminated by a `break` statement.",
        "options": [
            ("Only when the loop completes without encountering a `break` statement", True, "Correct. A break statement bypasses the loop's else branch entirely."),
            ("Only when the loop encounters an exception", False, "Incorrect. Exceptions are handled by try/except/else blocks."),
            ("Every time after each iteration", False, "Incorrect. It runs only once upon loop conclusion."),
            ("Only when the loop iterable was completely empty at start", False, "Incorrect. It also runs if empty, but primarily when not broken."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Loops",
        "difficulty": "BEGINNER",
        "content": "What is the purpose of the built-in enumerate() function?",
        "code_snippet": "frameworks = ['Django', 'FastAPI']\nfor idx, item in enumerate(frameworks, start=1):\n    print(idx, item)",
        "explanation": "`enumerate(iterable, start=0)` returns an enumerate iterator that yields pairs containing a count (from start) and the values obtained from iterating over iterable.",
        "options": [
            ("Yields pairs of (index, item) during iteration", True, "Correct. It cleanly provides loop counter and sequence value together."),
            ("Sorts the list before iterating", False, "Incorrect. That is sorted()."),
            ("Filters out duplicate values", False, "Incorrect. That is done with set()."),
            ("Measures the execution time of each loop iteration", False, "Incorrect. enumerate does not measure time."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Functions",
        "difficulty": "BEGINNER",
        "content": "What is the default return value of a Python function that does not contain a return statement?",
        "code_snippet": "def greet(name):\n    print(f\"Hello, {name}\")\n\nval = greet(\"Bob\")",
        "explanation": "In Python, any function that reaches the end of its block without an explicit `return` statement returns `None` implicitly.",
        "options": [
            ("None", True, "Correct. Python functions implicitly return None by default."),
            ("0", False, "Incorrect. Python does not return integer zero."),
            ("False", False, "Incorrect. Python does not return boolean False."),
            ("Empty string \"\"", False, "Incorrect. It returns None object."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Functions",
        "difficulty": "BEGINNER",
        "content": "Why should you never use a mutable object (like a list or dict) as a default argument in Python functions?",
        "code_snippet": "def append_to(item, target=[]):\n    target.append(item)\n    return target",
        "explanation": "Default arguments are evaluated once when the function is defined, not each time the function is called. A mutable default persists mutations across subsequent calls.",
        "options": [
            ("The default object is evaluated once at definition time and shared across calls", True, "Correct. Mutating it in one call affects all subsequent calls without an explicit arg."),
            ("Python will raise a SyntaxError at compile time", False, "Incorrect. Python allows it syntactically, but it causes unintended state retention."),
            ("It causes an immediate memory leak that crashes Python", False, "Incorrect. It does not crash, it simply retains the mutated object reference."),
            ("Variables inside functions cannot be modified", False, "Incorrect. Function variables are modifiable."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Lambda Functions",
        "difficulty": "BEGINNER",
        "content": "What is a lambda function in Python?",
        "code_snippet": "square = lambda x: x ** 2",
        "explanation": "A lambda function is a small, anonymous function defined with the `lambda` keyword that can take any number of arguments but can only evaluate a single expression.",
        "options": [
            ("An anonymous, single-expression inline function", True, "Correct. Lambdas are lightweight functions restricted to a single evaluated expression."),
            ("A function that runs asynchronously in a background thread", False, "Incorrect. Lambdas are synchronous standard callables."),
            ("A method used strictly for memory deallocation", False, "Incorrect. Memory is managed by gc and refcounting."),
            ("A decorator used exclusively for class constructors", False, "Incorrect. Lambdas are general anonymous callables."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "List Comprehensions",
        "difficulty": "BEGINNER",
        "content": "What will be the output of this list comprehension?",
        "code_snippet": "nums = [1, 2, 3, 4, 5]\nevsq = [x ** 2 for x in nums if x % 2 == 0]\nprint(evsq)",
        "explanation": "The comprehension filters numbers where `x % 2 == 0` (which gives 2 and 4), and then squares each element, producing [4, 16].",
        "options": [
            ("[4, 16]", True, "Correct. 2**2 = 4, and 4**2 = 16."),
            ("[1, 4, 9, 16, 25]", False, "Incorrect. The if condition filters out odd numbers 1, 3, and 5."),
            ("[2, 4]", False, "Incorrect. The expression x ** 2 squares the filtered values."),
            ("[16, 4]", False, "Incorrect. List comprehensions preserve the source iteration order."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "List Comprehensions",
        "difficulty": "BEGINNER",
        "content": "Which comprehension syntax creates a dictionary in Python?",
        "code_snippet": "squares = {x: x**2 for x in range(4)}",
        "explanation": "Dictionary comprehensions use curly braces with a `key: value` colon expression (`{k: v for ...}`). Set comprehensions use curly braces without colons.",
        "options": [
            ("{key: value for item in iterable}", True, "Correct. The colon separator distinguishes dict comprehensions from set comprehensions."),
            ("[key: value for item in iterable]", False, "Incorrect. Square brackets with colon is invalid syntax."),
            ("dict(item for item in iterable)", False, "Incorrect. dict() constructor expects an iterable of 2-tuples or kwargs."),
            ("<key: value for item in iterable>", False, "Incorrect. Angle brackets are not comprehension syntax in Python."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Exception Handling",
        "difficulty": "BEGINNER",
        "content": "What is the purpose of the `finally` block in a `try...except...finally` structure?",
        "code_snippet": "f = open('data.txt')\ntry:\n    content = f.read()\nfinally:\n    f.close()",
        "explanation": "The `finally` block always executes when leaving the try/except statement, whether an exception was raised, caught, or even if return/break was invoked.",
        "options": [
            ("Always executes regardless of whether an exception occurred or was handled", True, "Correct. Used for guaranteed cleanup like closing file descriptors or connections."),
            ("Executes only if no exception was raised in the try block", False, "Incorrect. That describes the 'else' block."),
            ("Executes only if an uncaught exception crashes the program", False, "Incorrect. It runs on both normal and exceptional exits."),
            ("Suppresses all exceptions silently", False, "Incorrect. Finally does not suppress exceptions."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Exception Handling",
        "difficulty": "BEGINNER",
        "content": "Which base class should all custom user-defined exceptions inherit from in Python?",
        "code_snippet": "class InterviewValidationError(Exception):\n    pass",
        "explanation": "Custom user-defined exceptions should inherit from `Exception` (or a subclass thereof). Inheriting directly from `BaseException` bypasses standard `except Exception:` catch blocks.",
        "options": [
            ("Exception", True, "Correct. Standard Python practice is inheriting from Exception, allowing standard handlers to catch it."),
            ("BaseException", False, "Incorrect. BaseException is reserved for system-exiting exceptions like KeyboardInterrupt and SystemExit."),
            ("StandardError", False, "Incorrect. StandardError was removed in Python 3."),
            ("ErrorClass", False, "Incorrect. No built-in ErrorClass exists in Python."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "File Handling",
        "difficulty": "BEGINNER",
        "content": "Why is the `with` statement recommended for opening files in Python?",
        "code_snippet": "with open('report.txt', 'r') as file:\n    data = file.read()",
        "explanation": "The `with` statement utilizes Python's context manager protocol (`__enter__` and `__exit__`), guaranteeing that the file stream is closed immediately upon exit even if an exception occurs.",
        "options": [
            ("Automatically closes the file even if an exception is raised inside the block", True, "Correct. It ensures resource deallocation via the context manager protocol."),
            ("Locks the file on disk so other OS processes cannot read it", False, "Incorrect. It does not enforce OS-level file locking."),
            ("Compiles the file contents into bytecode for speed", False, "Incorrect. It is standard file I/O."),
            ("Prevents the file from being opened more than once", False, "Incorrect. It does not enforce singleton file access."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "File Handling",
        "difficulty": "BEGINNER",
        "content": "What file mode should be used to write data to a file without overwriting existing content?",
        "code_snippet": "with open('log.txt', mode=...) as f:\n    f.write(\"New entry\\n\")",
        "explanation": "Mode `'a'` (append mode) opens the file for writing and places the file pointer at the end of the file. Existing content is preserved, and new data is appended.",
        "options": [
            ("'a' (Append mode)", True, "Correct. 'a' appends new writes to the end of existing file content."),
            ("'w' (Write mode)", False, "Incorrect. 'w' truncates the file to 0 bytes on open, erasing existing contents."),
            ("'r' (Read mode)", False, "Incorrect. 'r' is read-only and will raise UnsupportedOperation if write is called."),
            ("'x' (Exclusive creation)", False, "Incorrect. 'x' raises FileExistsError if the file already exists."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Modules and Packages",
        "difficulty": "BEGINNER",
        "content": "What file traditionally identifies a directory as a regular Python package?",
        "code_snippet": "mypackage/\n├── __init__.py\n├── module_a.py\n└── module_b.py",
        "explanation": "`__init__.py` marks a directory as a regular Python package and executes when the package is imported. (In Python 3.3+, namespace packages can exist without it).",
        "options": [
            ("__init__.py", True, "Correct. `__init__.py` signals to Python that the folder should be treated as a package."),
            ("__main__.py", False, "Incorrect. `__main__.py` defines the entry point when running a package with `python -m package`."),
            ("package.json", False, "Incorrect. package.json is used in Node.js, not Python."),
            ("__setup__.py", False, "Incorrect. Packaging uses setup.py or pyproject.toml, not __setup__.py."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Modules and Packages",
        "difficulty": "BEGINNER",
        "content": "What is the purpose of the `if __name__ == '__main__':` construct in a Python module?",
        "code_snippet": "def run():\n    print(\"Running engine\")\n\nif __name__ == '__main__':\n    run()",
        "explanation": "When a Python file is run directly, its `__name__` attribute is set to `'__main__'`. If it is imported by another module, `__name__` is set to the module's import path. This construct allows code to run only upon direct execution.",
        "options": [
            ("Executes code only when the script is run directly, not when imported as a module", True, "Correct. It prevents test or CLI execution code from running upon import."),
            ("Defines the entry point required by the Python compiler", False, "Incorrect. Python does not require a main function or compiler entry point."),
            ("Enables multiprocessing support for the current script", False, "Incorrect. While often used with multiprocessing on Windows, its direct purpose is execution guards."),
            ("Initializes the class constructor", False, "Incorrect. Class constructors use __init__."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Strings",
        "difficulty": "BEGINNER",
        "content": "What is the output of ' - '.join(['Python', 'Django', 'PostgreSQL'])?",
        "code_snippet": "res = ' - '.join(['Python', 'Django', 'PostgreSQL'])\nprint(res)",
        "explanation": "The `.join()` method concatenates sequence elements with the string delimiter placed between each element, resulting in 'Python - Django - PostgreSQL'.",
        "options": [
            ("'Python - Django - PostgreSQL'", True, "Correct. The delimiter is inserted between each iterable element."),
            ("['Python - Django - PostgreSQL']", False, "Incorrect. .join() returns a single string, not a list."),
            ("' - Python - Django - PostgreSQL - '", False, "Incorrect. join does not append leading or trailing delimiters."),
            ("TypeError: join takes only tuples", False, "Incorrect. join accepts any iterable containing strings."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Strings",
        "difficulty": "BEGINNER",
        "content": "How do formatted string literals (f-strings) evaluate expressions in Python?",
        "code_snippet": "val = 4\nmsg = f\"Square is {val * val}\"",
        "explanation": "Introduced in Python 3.6 (PEP 498), f-strings evaluate expressions enclosed within curly braces `{}` at runtime in the caller's scope.",
        "options": [
            ("Evaluates Python expressions inside curly braces `{}` at runtime", True, "Correct. f-strings provide fast, readable string interpolation."),
            ("Replaces %s tokens using a tuple of parameters", False, "Incorrect. That is printf-style % formatting."),
            ("Requires .format() invocation at the end of the string", False, "Incorrect. str.format() is the older .format() syntax."),
            ("Parses only static variable names without arithmetic operations", False, "Incorrect. f-strings can evaluate arbitrary valid Python expressions."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Lists",
        "difficulty": "BEGINNER",
        "content": "What is the time complexity of looking up an item by index in a Python list (e.g., `items[5]`)?",
        "code_snippet": "val = my_list[100]",
        "explanation": "Python lists are implemented as dynamic arrays (contiguous arrays of pointers). Index lookups calculate the memory offset directly, taking O(1) constant time.",
        "options": [
            ("O(1) - Constant time", True, "Correct. Access by numerical index is an instant pointer arithmetic lookup."),
            ("O(n) - Linear time", False, "Incorrect. Linear search O(n) occurs when using `item in my_list` by value."),
            ("O(log n) - Logarithmic time", False, "Incorrect. Logarithmic lookups occur in binary search trees or bisect."),
            ("O(n log n)", False, "Incorrect. That is the complexity of Timsort."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Lists",
        "difficulty": "BEGINNER",
        "content": "What is the difference between `list.sort()` and `sorted(list)` in Python?",
        "code_snippet": "a = [3, 1, 2]\nb = sorted(a)\na.sort()",
        "explanation": "`list.sort()` sorts the list in-place and returns `None`. In contrast, the built-in `sorted()` function creates and returns a new sorted list without modifying the original.",
        "options": [
            ("`list.sort()` sorts in-place returning None; `sorted()` returns a new sorted list", True, "Correct. Remember .sort() mutates the caller, sorted() produces a fresh list."),
            ("`sorted()` modifies the original list in-place", False, "Incorrect. sorted() leaves the source object untouched."),
            ("`list.sort()` only works on numbers, `sorted()` works on strings", False, "Incorrect. Both work on any comparable types."),
            ("Both return a new sorted list", False, "Incorrect. .sort() returns None."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Dictionaries",
        "difficulty": "BEGINNER",
        "content": "What happens when you execute `del d['missing_key']` on a dictionary?",
        "code_snippet": "d = {'name': 'Leo'}\ndel d['age']",
        "explanation": "Using the `del` keyword with a key that does not exist in the dictionary raises a `KeyError`. To delete safely without raising, use `d.pop('age', None)`.",
        "options": [
            ("Raises a KeyError", True, "Correct. Deleting a nonexistent key with del raises KeyError."),
            ("Returns None silently", False, "Incorrect. del raises KeyError on missing keys."),
            ("Returns False", False, "Incorrect. It does not return a boolean."),
            ("Adds the key with value None", False, "Incorrect. del removes items, never adds."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Functions",
        "difficulty": "BEGINNER",
        "content": "What does the `*args` syntax in a function definition permit?",
        "code_snippet": "def calculate_sum(*args):\n    return sum(args)",
        "explanation": "`*args` collects any number of extra positional arguments passed to the function into a tuple.",
        "options": [
            ("Allows the function to accept an arbitrary number of positional arguments as a tuple", True, "Correct. Any surplus positional arguments are packed into the tuple named args."),
            ("Allows arbitrary keyword arguments as a dictionary", False, "Incorrect. That is **kwargs."),
            ("Forces the caller to pass only keyword arguments", False, "Incorrect. Bare * in parameters enforces keyword-only arguments."),
            ("Unpacks a pointer in memory", False, "Incorrect. Python does not support manual pointer manipulation."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Functions",
        "difficulty": "BEGINNER",
        "content": "What does `**kwargs` represent in a Python function definition?",
        "code_snippet": "def log_event(message, **kwargs):\n    for k, v in kwargs.items():\n        print(f\"{k}: {v}\")",
        "explanation": "`**kwargs` captures any arbitrary keyword arguments passed to the function and stores them in a standard dictionary named `kwargs`.",
        "options": [
            ("A dictionary containing arbitrary keyword arguments passed to the function", True, "Correct. Double asterisks bundle keyword arguments into a dict."),
            ("A list of positional arguments", False, "Incorrect. That is *args."),
            ("A pointer to another function", False, "Incorrect. Python functions are first-class objects, not C function pointers."),
            ("A decorator definition flag", False, "Incorrect. Decorators wrap functions using closures."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Variables and Data Types",
        "difficulty": "BEGINNER",
        "content": "What is the result of `bool([])` and `bool([False])` in Python?",
        "code_snippet": "a = bool([])\nb = bool([False])",
        "explanation": "An empty list `[]` has length 0 and is falsy (`bool([]) == False`). A list containing `False` has length 1 and is non-empty, so it is truthy (`bool([False]) == True`).",
        "options": [
            ("False and True", True, "Correct! Empty collections evaluate to False, but any non-empty container evaluates to True!"),
            ("False and False", False, "Incorrect. [False] is a non-empty container with length 1."),
            ("True and False", False, "Incorrect. [] is falsy."),
            ("True and True", False, "Incorrect. [] is not truthy."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Numbers",
        "difficulty": "BEGINNER",
        "content": "Why does `0.1 + 0.2 == 0.3` evaluate to `False` in Python?",
        "code_snippet": "print(0.1 + 0.2 == 0.3)\nprint(0.1 + 0.2)",
        "explanation": "Standard Python floats use IEEE 754 double-precision binary representation. Base-10 fractions like 0.1 and 0.2 cannot be represented exactly in binary floating point, resulting in `0.30000000000000004`.",
        "options": [
            ("IEEE 754 floating-point rounding representation in binary arithmetic", True, "Correct. Standard binary float representation has tiny precision discrepancies. Use math.isclose() or decimal.Decimal."),
            ("Python bug in Python 3.12 arithmetic parser", False, "Incorrect. This is universal across IEEE 754 conforming languages (C, JS, Java, Python)."),
            ("0.1 is automatically cast to an integer", False, "Incorrect. 0.1 remains a float."),
            ("The equality operator is not implemented for floats", False, "Incorrect. == is implemented for floats."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Loops",
        "difficulty": "BEGINNER",
        "content": "What does the `continue` statement do inside a loop?",
        "code_snippet": "for i in range(5):\n    if i == 2:\n        continue\n    print(i)",
        "explanation": "`continue` skips the remainder of the current loop iteration and proceeds immediately to the next iteration of the loop.",
        "options": [
            ("Skips the rest of the current iteration and jumps to the next cycle", True, "Correct. Execution moves to the loop header for the next value."),
            ("Terminates the loop completely and exits", False, "Incorrect. That is the break statement."),
            ("Restarts the loop from the beginning (index 0)", False, "Incorrect. Loops cannot be restarted using continue."),
            ("Pauses execution for 1 second", False, "Incorrect. That is time.sleep(1)."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Variables and Data Types",
        "difficulty": "BEGINNER",
        "content": "What is the difference between `==` and `is` in Python?",
        "code_snippet": "a = [1, 2, 3]\nb = [1, 2, 3]\nprint(a == b)\nprint(a is b)",
        "explanation": "`==` checks for value equality (invoking `__eq__`), while `is` tests for object identity (checks whether both variables reference the exact same memory address `id(a) == id(b)`).",
        "options": [
            ("`==` compares value equality; `is` checks memory object identity", True, "Correct. Two distinct list instances with the same content are == but not 'is'."),
            ("`==` checks object identity; `is` compares values", False, "Incorrect. The definitions are reversed."),
            ("`is` is only used for numbers, `==` is used for lists", False, "Incorrect. 'is' is commonly used for None and singletons."),
            ("They are completely synonymous in Python 3", False, "Incorrect. Identity and equality are distinct concepts."),
        ]
    },
    {
        "category": "Python Fundamentals",
        "topic": "Sets",
        "difficulty": "BEGINNER",
        "content": "Can a list be added as an element of a Python `set`?",
        "code_snippet": "s = set()\ns.add([1, 2])",
        "explanation": "No. Set elements must be hashable. Because lists are mutable, they do not implement `__hash__` and adding a list to a set raises `TypeError: unhashable type: 'list'`. You can add a tuple instead.",
        "options": [
            ("No, it raises `TypeError: unhashable type: 'list'`", True, "Correct. Mutable collections lack fixed hashes and cannot be stored inside sets."),
            ("Yes, lists are automatically converted into tuples", False, "Incorrect. Python does not implicitly convert lists to tuples inside set.add()."),
            ("Yes, but only if the list has fewer than 10 elements", False, "Incorrect. Length does not affect hashability."),
            ("Yes, all Python objects can be stored in sets", False, "Incorrect. Only hashable objects can be members of a set."),
        ]
    }
]

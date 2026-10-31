# 40 Django Advanced Questions with 4 options and detailed technical explanations

DJANGO_ADVANCED_QUESTIONS = [
    {
        "category": "Django Advanced",
        "topic": "Django Request Lifecycle",
        "difficulty": "ADVANCED",
        "content": "What is the complete sequence of events during a Django request lifecycle from HTTP socket connection to response?",
        "code_snippet": "# Web Server -> WSGI/ASGI -> Middleware -> URLconf -> View -> Template/JSON -> Response",
        "explanation": "1. Web server (Nginx) receives HTTP and passes via WSGI/ASGI to Django. 2. `SecurityMiddleware` and request middleware execute top-down. 3. URL resolver matches the path in `ROOT_URLCONF`. 4. View middleware runs. 5. View function executes business logic and models. 6. Template renders. 7. Response middleware executes bottom-up. 8. WSGI handler sends HTTP response back to client.",
        "options": [
            ("WSGI/ASGI -> Request Middleware -> URL Resolver -> View Middleware -> View -> Response Middleware -> Client", True, "Correct. Represents the complete architectural lifecycle traversed by every Django request."),
            ("View -> Database -> Template -> WSGI -> Middleware", False, "Incorrect. Middleware wraps views both before and after execution."),
            ("Template -> View -> Middleware -> URLconf -> Database", False, "Incorrect. Flow begins with WSGI and URL routing before any template rendering."),
            ("URL Resolver -> Template -> Database -> View -> WSGI", False, "Incorrect. Views orchestrate databases and templates, not vice versa."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Database Transactions",
        "difficulty": "ADVANCED",
        "content": "What is the purpose of `transaction.atomic()` in Django?",
        "code_snippet": "from django.db import transaction\n\nwith transaction.atomic():\n    attempt.status = 'COMPLETED'\n    attempt.save()\n    record_score(attempt)",
        "explanation": "`transaction.atomic()` creates an atomic database transaction. If the code block executes successfully, the database changes are committed. If an uncaught exception is raised, all database changes inside the block are automatically rolled back, guaranteeing ACID consistency.",
        "options": [
            ("Guarantees atomicity: all operations inside the block commit together or roll back completely on exception", True, "Correct. Essential for critical flows like quiz submissions, payments, and multi-table updates."),
            ("Locks the entire database file from being read by other threads", False, "Incorrect. It defines transaction boundary, not full database file locks."),
            ("Executes operations in parallel across multiple worker threads", False, "Incorrect. It manages SQL BEGIN/COMMIT/ROLLBACK on the current connection."),
            ("Caches the results in Redis automatically", False, "Incorrect. transaction.atomic is pure relational database transaction control."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "select_for_update()",
        "difficulty": "ADVANCED",
        "content": "What SQL statement does `select_for_update()` generate and what problem does it prevent?",
        "code_snippet": "with transaction.atomic():\n    attempt = QuizAttempt.objects.select_for_update().get(id=attempt_id)\n    if attempt.status != 'COMPLETED':\n        attempt.status = 'COMPLETED'\n        attempt.save()",
        "explanation": "`select_for_update()` generates `SELECT ... FOR UPDATE`, locking the selected rows until the current transaction commits or rolls back. This prevents race conditions and lost updates caused by concurrent requests trying to mutate the same record simultaneously.",
        "options": [
            ("Generates `SELECT ... FOR UPDATE`, locking target rows to prevent concurrent race conditions", True, "Correct. Prevents duplicate submissions or concurrent modifications to the same attempt."),
            ("Automatically updates rows without requiring .save()", False, "Incorrect. It is a locking SELECT query, not an UPDATE."),
            ("Schedules an asynchronous update task in Celery", False, "Incorrect. It is a synchronous SQL row lock."),
            ("Checks for updates to Django framework source code", False, "Incorrect. It is a database query locking method."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Atomic Transactions",
        "difficulty": "ADVANCED",
        "content": "Why is invoking external side effects (like sending emails or payment webhooks) directly inside a `transaction.atomic()` block risky?",
        "code_snippet": "with transaction.atomic():\n    order.status = 'PAID'\n    order.save()\n    send_confirmation_email(user)  # If DB rollback occurs later, email already sent!",
        "explanation": "If an error occurs after the email/API call, the database transaction rolls back, but the external side effect cannot be rolled back (the user receives an email for a transaction that never saved). Use `transaction.on_commit(callback)` instead.",
        "options": [
            ("If the transaction rolls back, external side-effects cannot be undone; use `transaction.on_commit()` instead", True, "Correct. `transaction.on_commit()` guarantees callbacks only run after successful DB commit."),
            ("Because email sending causes SQLite to throw a syntax error", False, "Incorrect. SQLite does not know about email protocols."),
            ("Because Django prohibits network calls inside views", False, "Incorrect. Network calls are syntactically permitted, but architecturally unsafe inside transactions."),
            ("Because atomic blocks terminate all internet connections", False, "Incorrect. They only control database transactions."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Caching",
        "difficulty": "ADVANCED",
        "content": "What are the primary caching levels available in Django?",
        "code_snippet": "# settings.py CACHES configuration:\n# Memcached / Redis / Database / Local memory",
        "explanation": "Django supports four main caching tiers: 1. Site-wide caching (via `UpdateCacheMiddleware` and `FetchFromCacheMiddleware`), 2. Per-view caching (via `@cache_page`), 3. Template fragment caching (`{% cache %}`), and 4. Low-level cache API (`cache.get()`, `cache.set()`).",
        "options": [
            ("Site-wide cache, per-view cache (`@cache_page`), template fragment cache (`{% cache %}`), and low-level cache API", True, "Correct. Django provides granular caching from full HTTP responses down to individual key-value data."),
            ("Browser localStorage and sessionStorage only", False, "Incorrect. Django caching is server-side."),
            ("Hardware CPU L1/L2 cache integration", False, "Incorrect. Django does not interface directly with CPU registers."),
            ("Static file minification only", False, "Incorrect. Caching stores rendered data or query results."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Redis Integration Concepts",
        "difficulty": "ADVANCED",
        "content": "Why is Redis commonly preferred over Memcached as a Django cache backend in modern architectures?",
        "code_snippet": "CACHES = {\n    'default': {\n        'BACKEND': 'django.core.cache.backends.redis.RedisCache',\n        'LOCATION': 'redis://127.0.0.1:6379',\n    }\n}",
        "explanation": "Redis supports rich in-memory data structures (lists, sets, sorted sets, hashes), persistence to disk (RDB/AOF), pub/sub messaging (used by Django Channels for WebSockets), and acts as a broker/result-backend for Celery, whereas Memcached is a pure key-value string store.",
        "options": [
            ("Supports rich data structures, persistence to disk, pub/sub for WebSockets (Channels), and Celery task brokering", True, "Correct. Redis serves as cache, message broker, and real-time pub/sub hub simultaneously."),
            ("Redis runs inside the Python interpreter without external services", False, "Incorrect. Redis is a standalone daemon."),
            ("Memcached was deprecated in Django 2.0", False, "Incorrect. Memcached is still supported in Django."),
            ("Redis replaces SQLite completely without an ORM", False, "Incorrect. Redis is an in-memory store; relational databases remain primary data stores."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Celery Integration Concepts",
        "difficulty": "ADVANCED",
        "content": "Why should long-running tasks (like generating PDF interview reports or training analytics) be offloaded to Celery?",
        "code_snippet": "@shared_task\ndef generate_pdf_report(attempt_id):\n    # Long 15-second operation",
        "explanation": "HTTP web server worker threads should respond within milliseconds. If a view executes a 15-second PDF compilation synchronously, the worker thread is blocked from serving other requests, leading to server timeouts and pool exhaustion. Offloading to Celery queues the job asynchronously.",
        "options": [
            ("Prevents blocking HTTP worker threads, avoiding request timeouts and server thread pool exhaustion", True, "Correct. Keeps the web layer responsive while Celery worker processes handle heavy lifting."),
            ("Because Python does not allow PDF generation in views", False, "Incorrect. Views can generate PDFs, but long execution blocks the web worker."),
            ("Celery reduces database storage space", False, "Incorrect. Celery is a distributed task queue."),
            ("Celery compiles Python into C++", False, "Incorrect. Celery executes Python tasks."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Security",
        "difficulty": "ADVANCED",
        "content": "How does Django ORM inherently protect against SQL Injection attacks?",
        "code_snippet": "# Safe:\nQuestion.objects.filter(content=user_input)\n# Dangerous:\nQuestion.objects.raw(f\"SELECT * FROM questions WHERE content = '{user_input}'\")",
        "explanation": "Django ORM uses parameterized queries (prepared statements). User input is passed as parameter values separate from the SQL query structure, preventing malicious input from escaping into executable SQL commands.",
        "options": [
            ("Uses parameterized queries (prepared statements) that separate user data from the SQL command structure", True, "Correct. The database engine treats parameters strictly as data values, not executable syntax."),
            ("By stripping all punctuation and apostrophes from strings", False, "Incorrect. Django does not alter user string values arbitrarily."),
            ("By converting all queries into base64 strings", False, "Incorrect. Parameters are bound using standard database driver protocols."),
            ("By running all queries through an external antivirus sandbox", False, "Incorrect. Security is achieved via database parameterization."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "CSRF",
        "difficulty": "ADVANCED",
        "content": "How does Django's CSRF protection mechanism validate that a request came from an authenticated session rather than a malicious site?",
        "code_snippet": "# Cookie: csrftoken=abc123\n# Form / Header: X-CSRFToken=abc123",
        "explanation": "Django uses the Double-Submit Cookie pattern with secret masking. When a form is submitted, Django verifies that the token submitted in the form payload or `X-CSRFToken` header matches the secret stored in the user's `csrftoken` cookie. Malicious cross-origin sites cannot read this cookie due to Same-Origin Policy.",
        "options": [
            ("Double-Submit Cookie pattern: matches the submitted form/header token against the secret in the user's cookie", True, "Correct. Same-Origin Policy prevents attacker sites from reading the cookie value to forge the header."),
            ("By inspecting the user's GPS location", False, "Incorrect. Not related to geolocation."),
            ("By checking if the user's password contains special characters", False, "Incorrect. CSRF protects against cross-site request forgery, not weak passwords."),
            ("By logging the client's MAC address in SQLite", False, "Incorrect. MAC addresses are not exposed in HTTP requests."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "XSS",
        "difficulty": "ADVANCED",
        "content": "How does the Django Template Engine protect against Cross-Site Scripting (XSS) by default, and how can a developer inadvertently bypass it?",
        "code_snippet": "# Safe: {{ user_input }}\n# Dangerous: {{ user_input|safe }}",
        "explanation": "Django templates automatically HTML-escape all variable output (converting `<`, `>`, `&`, `'`, and `\"` into HTML entities). Developers bypass this protection by using the `|safe` filter or `{% autoescape off %}`, which renders raw HTML without escaping.",
        "options": [
            ("Auto-escapes HTML characters (`<`, `>`, `&`, `\"`); bypassed by using the `|safe` filter or `{% autoescape off %}`", True, "Correct. Never use `|safe` on unvalidated or unsanitized user-generated input!"),
            ("Compiles HTML into WebAssembly bytecode; bypassed by using JavaScript", False, "Incorrect. It is standard string entity escaping."),
            ("Blocks all JavaScript tags from being downloaded over HTTP", False, "Incorrect. Browsers download script tags; escaping renders them as text."),
            ("Encodes variables using AES-256 encryption", False, "Incorrect. It is HTML entity replacement."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "ORM Optimization",
        "difficulty": "ADVANCED",
        "content": "What is the difference between `Prefetch('options', queryset=...)` and basic `'options'` inside `prefetch_related()`?",
        "code_snippet": "from django.db.models import Prefetch\n\nquestions = Question.objects.prefetch_related(\n    Prefetch('options', queryset=AnswerOption.objects.filter(is_correct=True), to_attr='correct_options')\n)",
        "explanation": "The `Prefetch` object allows customizing the prefetch query: filtering related objects (e.g. only correct options), ordering them, and storing the filtered results in a custom attribute (`to_attr`), whereas basic `'options'` fetches all related objects unfiltered.",
        "options": [
            ("`Prefetch` allows filtering, ordering, and assigning preloaded results to a custom attribute (`to_attr`)", True, "Correct. Extremely powerful for pre-filtering related objects without hitting the DB in subsequent loops."),
            ("`Prefetch` executes an SQL JOIN instead of a separate query", False, "Incorrect. prefetch_related always executes separate queries; select_related does JOINs."),
            ("`Prefetch` is deprecated in Django 5.x", False, "Incorrect. It is actively maintained and standard practice."),
            ("`Prefetch` runs on a separate database connection", False, "Incorrect. It runs on the configured database router connection."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Database Indexing",
        "difficulty": "ADVANCED",
        "content": "How do you define composite indexes and unique constraints in modern Django models (Django 2.2+ / 5.x)?",
        "code_snippet": "class Meta:\n    indexes = [\n        models.Index(fields=['difficulty', 'is_active'], name='q_diff_active_idx'),\n    ]\n    constraints = [\n        models.UniqueConstraint(fields=['attempt', 'question'], name='unique_attempt_question'),\n    ]",
        "explanation": "Django modern conventions use `Meta.indexes` with `models.Index` objects and `Meta.constraints` with `models.UniqueConstraint` / `models.CheckConstraint`, replacing older `index_together` and `unique_together`.",
        "options": [
            ("Using `Meta.indexes` with `models.Index()` and `Meta.constraints` with `models.UniqueConstraint()`", True, "Correct. Modern syntax allows naming indexes, setting condition filters, and specifying check expressions."),
            ("Writing raw SQL `CREATE INDEX` statements in views.py", False, "Incorrect. Indexes should be declared on model Meta so migrations manage them."),
            ("Adding `@indexed` decorators on model fields", False, "Incorrect. Single field indexes use `db_index=True`, composite use `Meta.indexes`."),
            ("Configuring indexes in settings.py", False, "Incorrect. Indexes belong on model definitions."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "ASGI vs WSGI",
        "difficulty": "ADVANCED",
        "content": "What is the key difference between WSGI and ASGI in Python web development?",
        "code_snippet": "# wsgi.py (Synchronous) vs asgi.py (Asynchronous)",
        "explanation": "WSGI (Web Server Gateway Interface) is synchronous: each worker thread handles one request at a time sequentially. ASGI (Asynchronous Server Gateway Interface) supports asynchronous coroutines, long-lived connections, WebSockets, and HTTP/2 multiplexing on an event loop.",
        "options": [
            ("WSGI is synchronous (1 request per worker thread); ASGI supports async coroutines, WebSockets, and long-lived connections", True, "Correct. ASGI (via Uvicorn/Daphne) unlocks modern real-time WebSockets and async views."),
            ("WSGI is for Python 3; ASGI is for Python 2", False, "Incorrect. Both run on Python 3; ASGI is the modern asynchronous standard."),
            ("WSGI runs on Linux; ASGI runs only on Windows", False, "Incorrect. Both are cross-platform."),
            ("ASGI eliminates the need for HTTP responses", False, "Incorrect. ASGI handles standard HTTP requests as well as WebSockets."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Async Django",
        "difficulty": "ADVANCED",
        "content": "What exception does Django raise if you attempt to call a synchronous ORM query inside an `async def` view without using `sync_to_async`?",
        "code_snippet": "async def my_view(request):\n    # Synchronous query inside async view:\n    q = Question.objects.first()",
        "explanation": "Django raises `django.core.exceptions.SynchronousOnlyOperation`. Calling synchronous blocking code in the main thread of an async event loop would block the event loop. Wrap the call in `sync_to_async(Question.objects.first)()` or use async ORM methods (`afirst()`, `acount()`).",
        "options": [
            ("`SynchronousOnlyOperation`", True, "Correct. Django protects the event loop from being blocked by synchronous database drivers."),
            ("`AsyncNotImplementedError`", False, "Incorrect. The exact exception is SynchronousOnlyOperation."),
            ("`OperationalError`", False, "Incorrect. OperationalError is a database driver connection error."),
            ("`DatabaseBlockedException`", False, "Incorrect. No such exception in Django."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Async Django",
        "difficulty": "ADVANCED",
        "content": "What async ORM methods did Django 4.1+ introduce for non-blocking database queries?",
        "code_snippet": "async def quiz_stat_view(request):\n    count = await Question.objects.filter(is_active=True).acount()\n    first_q = await Question.objects.afirst()",
        "explanation": "Django introduced native async equivalents prefixed with `a`: `aget()`, `acreate()`, `afirst()`, `acount()`, `aexists()`, `aupdate()`, `adelete()`, and async iteration (`async for item in qs`).",
        "options": [
            ("Methods prefixed with `a` like `aget()`, `acreate()`, `afirst()`, `acount()`, `aexists()`", True, "Correct. Allows clean non-blocking database queries inside async views without manual sync_to_async wrappers."),
            ("Methods suffixed with `_async` like `get_async()`", False, "Incorrect. Django standardized on the `a` prefix."),
            ("Prefixing with `await` on normal methods like `await qs.count()`", False, "Incorrect. Standard count() is not a coroutine; acount() is."),
            ("Calling `django.async_query()`", False, "Incorrect. Queries use model manager methods directly."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Signals and Performance",
        "difficulty": "ADVANCED",
        "content": "Why can Django signals cause severe performance degradation during bulk operations (like `bulk_create` or `QuerySet.update()`)?",
        "code_snippet": "# Notice that bulk operations skip signals:\nQuestion.objects.bulk_create(questions)  # Does NOT trigger post_save!",
        "explanation": "Signals execute synchronously in Python per-instance. Because executing signals for 100,000 items in a bulk query would destroy throughput, Django intentionally bypasses `pre_save` and `post_save` signals during `bulk_create()` and `QuerySet.update()`. Business logic relying on signals won't fire during bulk actions.",
        "options": [
            ("Bulk operations explicitly bypass model signals for performance, meaning signal logic won't execute", True, "Correct. A critical architectural caveat: relying on post_save means bulk_create skips your logic!"),
            ("Signals cause database deadlock errors on bulk operations", False, "Incorrect. Django avoids deadlocks by skipping signal execution."),
            ("Signals convert bulk queries into slow recursive functions", False, "Incorrect. Bulk operations run directly in SQL without signal hooks."),
            ("Signals run in separate threads that exceed connection limits", False, "Incorrect. Signals are synchronous."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Scalability",
        "difficulty": "ADVANCED",
        "content": "In a high-traffic production deployment, why should Django applications be designed to be completely stateless?",
        "code_snippet": "# Stateless Application Tier behind Load Balancer",
        "explanation": "Stateless application servers store no session state, files, or persistent in-memory data on their local disks. This allows autoscaling instances horizontally behind a load balancer, routing requests to any node without sticky sessions or data loss.",
        "options": [
            ("Allows horizontal autoscaling behind a load balancer: any instance can handle any user request", True, "Correct. Sessions live in Redis/DB; uploads live in S3/cloud storage; app nodes are disposable."),
            ("Reduces Python memory footprint to exactly 0 bytes", False, "Incorrect. Processes still require RAM for application code and runtimes."),
            ("Eliminates the need for a database", False, "Incorrect. Stateless apps depend heavily on shared databases."),
            ("Stateless apps do not require security patches", False, "Incorrect. Security patching is always required."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Deployment",
        "difficulty": "ADVANCED",
        "content": "Why should `DEBUG = True` NEVER be left enabled in a production Django deployment?",
        "code_snippet": "# settings.py\nDEBUG = False  # Mandatory for production",
        "explanation": "When `DEBUG = True`: 1. Detailed interactive tracebacks expose environment variables, secret keys, database credentials, and source code to attackers on any unhandled exception. 2. Django stores every SQL query in memory (`connection.queries`), leading to a gradual memory leak.",
        "options": [
            ("Exposes database credentials, secret keys, and source code in tracebacks, and leaks memory via `connection.queries`", True, "Correct. A critical security and operational risk in production."),
            ("Slows down CSS file loading by 10 seconds", False, "Incorrect. The primary danger is severe information disclosure and memory leakage."),
            ("Prevents database migrations from running", False, "Incorrect. Migrations run with DEBUG True or False."),
            ("Disables user authentication completely", False, "Incorrect. Auth functions, but secrets are exposed."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Deployment",
        "difficulty": "ADVANCED",
        "content": "What is WhiteNoise and how does it simplify deploying Django applications?",
        "code_snippet": "MIDDLEWARE = [\n    'django.middleware.security.SecurityMiddleware',\n    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise\n    ...\n]",
        "explanation": "WhiteNoise embeds static file serving directly into the Python WSGI application with Gzip/Brotli compression, cache-control headers, and unique content hashes, eliminating the requirement to configure a separate Nginx or S3 setup for static assets.",
        "options": [
            ("Enables Django to serve its own static files efficiently in production with compression and caching headers", True, "Correct. Eliminates external Nginx/CDN dependencies for static files in containerized environments."),
            ("A sound generator for meditation apps", False, "Incorrect. It is a Python static file serving library."),
            ("An ORM replacement for SQLite", False, "Incorrect. WhiteNoise serves static files."),
            ("A compiler that converts Django templates into React", False, "Incorrect. Not related to frontend frameworks."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Testing Strategies",
        "difficulty": "ADVANCED",
        "content": "What is the difference between `django.test.TestCase` and `unittest.TestCase` in a Django project?",
        "code_snippet": "from django.test import TestCase\n\nclass QuizTest(TestCase):\n    def test_score_calculation(self):\n        ...",
        "explanation": "`django.test.TestCase` wraps every test method in an atomic database transaction that is automatically rolled back at the end of the test, ensuring tests do not pollute the database. It also provides a pre-configured test `client` and custom Django assertions.",
        "options": [
            ("`django.test.TestCase` wraps each test in a database transaction that rolls back on completion, and provides test `client`", True, "Correct. Guarantees clean database isolation between test runs."),
            ("`unittest.TestCase` can only test HTML strings", False, "Incorrect. unittest.TestCase is Python's standard testing class."),
            ("`django.test.TestCase` runs on live production databases", False, "Incorrect. Django creates a dedicated test database (or in-memory SQLite)."),
            ("There is no technical difference between them", False, "Incorrect. Django TestCase adds transaction rollback, client, and assertions."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Middleware Internals",
        "difficulty": "ADVANCED",
        "content": "How can a custom middleware prematurely return an `HttpResponse` (short-circuiting the request pipeline) without calling the view?",
        "code_snippet": "class IPBlockerMiddleware:\n    def __call__(self, request):\n        if is_blacklisted(request):\n            return HttpResponseForbidden(\"Access Denied\")\n        return self.get_response(request)",
        "explanation": "If a middleware returns an `HttpResponse` directly (such as `HttpResponseForbidden`) instead of calling `self.get_response(request)`, Django stops the request pipeline immediately. Subsequent middleware and the view function are never executed.",
        "options": [
            ("Return an `HttpResponse` directly without invoking `self.get_response(request)`", True, "Correct. Short-circuiting is used for rate-limiting, IP blocking, and maintenance mode checks."),
            ("Raise a `KeyboardInterrupt` exception", False, "Incorrect. That terminates the Python process."),
            ("Set `request.stop = True`", False, "Incorrect. Django does not inspect a stop attribute."),
            ("Call `sys.exit()`", False, "Incorrect. sys.exit kills the web worker thread."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "ORM Optimization",
        "difficulty": "ADVANCED",
        "content": "What is the difference between `bulk_update(objs, fields=['status'])` and calling `.save()` on each instance in a loop?",
        "code_snippet": "QuizAttempt.objects.bulk_update(attempts, ['status', 'score'])",
        "explanation": "`bulk_update()` updates the specified columns for a list of model instances using a single SQL query (often using a `CASE...WHEN` statement), avoiding N separate SQL UPDATE round-trips to the database.",
        "options": [
            ("`bulk_update()` executes 1 batched SQL query using `CASE...WHEN`, avoiding N separate database round-trips", True, "Correct. Substantially faster than iterating and saving individual model instances."),
            ("`bulk_update()` modifies the SQLite schema directly", False, "Incorrect. It updates row values, not table schema."),
            ("`.save()` in a loop is faster because of internal caching", False, "Incorrect. Loop saves cause severe database latency overhead."),
            ("`bulk_update()` cannot update integer fields", False, "Incorrect. It updates any valid model fields."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Security",
        "difficulty": "ADVANCED",
        "content": "What is an Insecure Direct Object Reference (IDOR) vulnerability and how do you prevent it in Django views?",
        "code_snippet": "# Vulnerable:\nattempt = QuizAttempt.objects.get(id=attempt_id)\n# Protected:\nattempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)",
        "explanation": "IDOR occurs when an application exposes a reference to an internal object (like `attempt_id=42`) and fails to verify that the requesting user owns or has permission to view that object. Prevent it by always filtering objects by `user=request.user` or asserting `attempt.user == request.user`.",
        "options": [
            ("Accessing another user's private records by guessing/changing the ID; prevented by filtering `user=request.user`", True, "Correct. Never query an object by PK alone without validating ownership or permissions."),
            ("A SQL injection in Django migrations", False, "Incorrect. IDOR is an access control / authorization vulnerability."),
            ("Using HTTP instead of HTTPS", False, "Incorrect. Insecure transport is a distinct vulnerability."),
            ("Exposing database credentials in settings.py", False, "Incorrect. That is credential exposure."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Testing Strategies",
        "difficulty": "ADVANCED",
        "content": "How do you test authenticated views using Django's test `client` without going through the web login form?",
        "code_snippet": "def test_dashboard(self):\n    user = User.objects.create_user(username='testuser', password='pwd')\n    self.client.force_login(user)\n    response = self.client.get('/dashboard/')\n    self.assertEqual(response.status_code, 200)",
        "explanation": "`self.client.force_login(user)` bypasses authentication backend password verification and immediately populates the test client's session with the user credentials, speeding up test suites.",
        "options": [
            ("`self.client.force_login(user)`", True, "Correct. Instantly authenticates the test client without the overhead of password hashing."),
            ("`self.client.skip_auth()`", False, "Incorrect. No such method on test client."),
            ("Setting `settings.AUTH = False`", False, "Incorrect. Settings does not have an AUTH flag."),
            ("Writing cookies directly using Chrome DevTools", False, "Incorrect. Automated tests execute headless without Chrome DevTools."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "SQL Injection",
        "difficulty": "ADVANCED",
        "content": "When executing raw SQL queries in Django using `.raw()`, how should parameters be passed to maintain SQL injection immunity?",
        "code_snippet": "# Safe raw query with parameters:\nQuestion.objects.raw(\"SELECT * FROM questions_question WHERE difficulty = %s\", [difficulty_param])",
        "explanation": "Always pass parameters as a separate list or tuple in the `params` argument using `%s` placeholders. Django's database backend automatically quotes and escapes parameters, preventing SQL injection. Never use Python f-strings or `%` string interpolation to construct raw SQL.",
        "options": [
            ("Pass parameters in the `params` argument list using `%s` placeholders separate from the SQL string", True, "Correct. Parameter binding ensures the SQL engine treats parameters as literal values."),
            ("Use Python f-strings: `f\"SELECT ... WHERE id = {user_input}\"`", False, "Incorrect. f-strings directly inject raw untrusted input, causing critical SQL injection."),
            ("Use string `.format()` interpolation", False, "Incorrect. String formatting is vulnerable to SQL injection."),
            ("Raw queries cannot be made secure in Django", False, "Incorrect. Parameterized raw queries are fully secure."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Database Transactions",
        "difficulty": "ADVANCED",
        "content": "What is the behavior of nested `transaction.atomic()` blocks in Django?",
        "code_snippet": "with transaction.atomic():  # Outer transaction\n    do_something()\n    with transaction.atomic():  # Inner transaction (Savepoint)\n        do_something_else()",
        "explanation": "Django implements nested atomic blocks using database SAVEPOINTS. If the inner atomic block raises an exception, only changes within the inner block are rolled back to the savepoint; the outer transaction can catch the exception and proceed to commit.",
        "options": [
            ("Inner atomic blocks create database SAVEPOINTs, allowing partial rollbacks without aborting the outer transaction", True, "Correct. Standard SQL savepoints enable modular error recovery within a broader transaction."),
            ("Raises a NestedTransactionError", False, "Incorrect. Django fully supports nested atomic blocks."),
            ("Inner blocks commit immediately before outer blocks finish", False, "Incorrect. Commits occur when the outermost atomic block exits successfully."),
            ("Inner blocks run in a separate background process", False, "Incorrect. They share the same database connection and thread."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "ORM Optimization",
        "difficulty": "ADVANCED",
        "content": "How do you inspect the exact raw SQL queries generated by Django during a request or in shell?",
        "code_snippet": "from django.db import connection\n# After executing ORM queries:\nprint(len(connection.queries))\nprint(connection.queries)",
        "explanation": "When `DEBUG = True`, Django records every executed query in `django.db.connection.queries`, which is a list of dictionaries with `'sql'` and `'time'`. You can also inspect `str(queryset.query)` on a specific QuerySet.",
        "options": [
            ("Inspect `django.db.connection.queries` (when DEBUG=True) or `str(queryset.query)`", True, "Correct. Invaluable for profiling query count and debugging N+1 bottlenecks."),
            ("Open the SQLite binary file in a text editor", False, "Incorrect. SQLite database files are binary, not plain text."),
            ("Check browser cookies", False, "Incorrect. SQL queries are not stored in cookies."),
            ("Check git commit diffs", False, "Incorrect. Queries execute at runtime against live databases."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Caching",
        "difficulty": "ADVANCED",
        "content": "How do you cache an expensive computation using Django's low-level cache API with a 15-minute expiration?",
        "code_snippet": "from django.core.cache import cache\n\ndata = cache.get('daily_stats')\nif not data:\n    data = compute_heavy_analytics()\n    cache.set('daily_stats', data, timeout=900)",
        "explanation": "`cache.get(key)` checks if the cached value exists. If missing (`None`), compute the value and save it with `cache.set(key, value, timeout=900)` (900 seconds = 15 minutes).",
        "options": [
            ("Use `cache.get(key)` and `cache.set(key, value, timeout=900)`", True, "Correct. Standard 'cache-aside' (lazy loading) pattern."),
            ("Call `django.save_cache(key, value, minutes=15)`", False, "Incorrect. Django cache API uses cache.set with timeout in seconds."),
            ("Write the result to a static .txt file", False, "Incorrect. Cache API provides memory/redis-backed storage."),
            ("Store the object in request.session", False, "Incorrect. Sessions are user-specific, not application-wide caches."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Security",
        "difficulty": "ADVANCED",
        "content": "What is Clickjacking and how does Django protect against it out of the box?",
        "code_snippet": "MIDDLEWARE = [\n    ...\n    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n]",
        "explanation": "Clickjacking is an attack where a malicious site embeds your application inside an invisible `<iframe>` to trick users into clicking buttons they did not intend to click. Django's `XFrameOptionsMiddleware` sets the `X-Frame-Options: DENY` (or `SAMEORIGIN`) HTTP header to prevent unauthorized iframe embedding.",
        "options": [
            ("An attack embedding sites in transparent iframes; prevented by `XFrameOptionsMiddleware` setting `X-Frame-Options`", True, "Correct. Tells modern browsers not to render the page inside third-party iframes."),
            ("A brute force attack on passwords; prevented by Captcha", False, "Incorrect. Brute-force is credential guessing."),
            ("An SQL injection attack through mouse clicks", False, "Incorrect. Clickjacking is UI redressing."),
            ("Intercepting Wi-Fi packets", False, "Incorrect. That is packet sniffing, mitigated by HTTPS/TLS."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Scalability",
        "difficulty": "ADVANCED",
        "content": "What is the purpose of database read replicas and how does Django support them via Database Routers?",
        "code_snippet": "class PrimaryReplicaRouter:\n    def db_for_read(self, model, **hints): return 'replica'\n    def db_for_write(self, model, **hints): return 'default'",
        "explanation": "Read replicas offload SELECT queries from the primary database to read-only replicas. Django supports custom Database Routers (`db_for_read` and `db_for_write`) to direct read queries to replicas and write queries (`INSERT`/`UPDATE`) to the primary database.",
        "options": [
            ("Routes read queries to read-only replicas and writes to primary database via custom Database Routers", True, "Correct. Significantly scales read-heavy web platforms like quiz and content sites."),
            ("Creates automatic daily SQLite backups", False, "Incorrect. Database routers manage runtime query distribution."),
            ("Translates SQL into MongoDB queries", False, "Incorrect. Django ORM targets relational engines."),
            ("Disables primary keys on read queries", False, "Incorrect. Schemas remain identical across replicas."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Database Transactions",
        "difficulty": "ADVANCED",
        "content": "What does `CONN_MAX_AGE` configure in Django database settings and what problem does it mitigate?",
        "code_snippet": "DATABASES = {\n    'default': {\n        'ENGINE': 'django.db.backends.postgresql',\n        'CONN_MAX_AGE': 600,  # 10 minutes\n    }\n}",
        "explanation": "By default (`CONN_MAX_AGE = 0`), Django opens a new database connection at the beginning of each HTTP request and closes it at the end. Setting `CONN_MAX_AGE` enables persistent connections: connections stay open across requests up to the max age, eliminating the heavy TLS/TCP connection handshake overhead per request.",
        "options": [
            ("Enables persistent database connections, reusing existing connections across requests up to the max age", True, "Correct. Dramatically reduces connection establishment latency under sustained web traffic."),
            ("Automatically terminates slow queries running over 600 seconds", False, "Incorrect. Query timeout is managed via database server parameters or statement_timeout."),
            ("Backs up database tables every 600 seconds", False, "Incorrect. It configures connection pooling persistence."),
            ("Restricts each user to 600 queries per day", False, "Incorrect. It is a server connection setting, not rate-limiting."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "ORM Optimization",
        "difficulty": "ADVANCED",
        "content": "What do `Subquery` and `OuterRef` allow developers to construct in Django ORM?",
        "code_snippet": "from django.db.models import OuterRef, Subquery\n\nlatest_score = QuizAttempt.objects.filter(\n    user=OuterRef('pk'), status='COMPLETED'\n).order_by('-completed_at').values('score')[:1]\n\nusers = User.objects.annotate(last_score=Subquery(latest_score))",
        "explanation": "`Subquery` allows embedding an explicit SQL subquery inside another QuerySet's annotations or filters. `OuterRef` allows referencing a field from the outer (parent) query inside the inner subquery, creating correlated subqueries without loading intermediate data into Python.",
        "options": [
            ("Correlated SQL subqueries where the inner query references columns from the outer query via `OuterRef`", True, "Correct. Powerful for annotating the latest child record or computed scalar value in a single query."),
            ("Recursive Common Table Expressions (CTEs) across multiple databases", False, "Incorrect. While subqueries can be nested, CTEs require raw SQL or third-party packages."),
            ("Automated database schema migrations", False, "Incorrect. Subquery is a DQL query expression."),
            ("Thread-safe memory caches in RAM", False, "Incorrect. It executes in the SQL database engine."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Deployment",
        "difficulty": "ADVANCED",
        "content": "How should zero-downtime database migrations be performed when modifying large production tables?",
        "code_snippet": "# Strategy: Expand -> Migrate Code -> Contract",
        "explanation": "Zero-downtime migrations use the multi-step 'Expand and Contract' pattern: 1. Add new column/table as nullable or with default (Expand). 2. Deploy application code that reads from old/new and writes to both. 3. Backfill data in background batches. 4. Switch code to read from new column only. 5. Drop old column/table in a subsequent release (Contract).",
        "options": [
            ("The 'Expand and Contract' phased approach: add nullable column -> dual write -> backfill -> contract", True, "Correct. Ensures running instances never crash while new instances with updated schemas deploy."),
            ("Shut down the web server for 2 hours during peak hours", False, "Incorrect. Downtime is unacceptable in modern high-availability applications."),
            ("Drop the table and re-run makemigrations from scratch", False, "Incorrect. Results in total permanent data destruction."),
            ("Migrations cannot be performed without stopping the web server", False, "Incorrect. Phased migrations allow 100% uptime."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Async Django",
        "difficulty": "ADVANCED",
        "content": "What is the primary role of a 'Channel Layer' in Django Channels (WebSockets)?",
        "code_snippet": "# channels.layers.get_channel_layer()\n# RedisChannelLayer",
        "explanation": "A Channel Layer is a message queue/bus (typically backed by Redis) that allows multiple consumer instances running across different server processes and machines to communicate, broadcast group messages, and push real-time updates to connected WebSocket clients.",
        "options": [
            ("A distributed pub/sub message bus (backed by Redis) allowing consumers across worker processes to broadcast messages", True, "Correct. Enables multi-server group broadcasts and real-time push to WebSockets."),
            ("An SSL certificate manager for HTTPS connections", False, "Incorrect. Channel Layer is application pub/sub."),
            ("A SQLite database driver replacement", False, "Incorrect. Channel Layer handles transient message passing."),
            ("A CSS preprocessor for Django templates", False, "Incorrect. Channels is for async networking and WebSockets."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Security",
        "difficulty": "ADVANCED",
        "content": "What is the purpose of Content Security Policy (CSP) headers in a secured Django web application?",
        "code_snippet": "# Content-Security-Policy: default-src 'self'; script-src 'self' cdn.jsdelivr.net",
        "explanation": "CSP is an HTTP response header that instructs the browser on approved sources of scripts, stylesheets, images, and other resources. It severely restricts attackers' ability to execute unauthorized malicious JavaScript even if an XSS vulnerability exists.",
        "options": [
            ("Restricts approved origins for scripts, styles, and assets, severely neutralizing XSS exploitation", True, "Correct. Tells the browser not to execute inline scripts or scripts from unapproved domains."),
            ("Encrypts SQLite database files on disk", False, "Incorrect. CSP is a browser client security header."),
            ("Prevents search engines from indexing the site", False, "Incorrect. robots.txt and X-Robots-Tag handle indexing."),
            ("Compresses static files using Brotli", False, "Incorrect. Compression is handled by WhiteNoise or Nginx."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Database Indexing",
        "difficulty": "ADVANCED",
        "content": "What is a 'Partial Index' (or conditional index) in PostgreSQL/SQLite and how do you declare it in Django?",
        "code_snippet": "models.Index(\n    fields=['status'],\n    condition=models.Q(status='IN_PROGRESS'),\n    name='active_attempts_idx'\n)",
        "explanation": "A partial index only indexes rows matching a specified condition (e.g. `WHERE status = 'IN_PROGRESS'`). It reduces index storage size and speeds up writes because only matching rows are indexed, making lookups for that subset extremely fast.",
        "options": [
            ("An index covering only rows satisfying a `condition=Q(...)`, saving disk space and speeding write throughput", True, "Correct. Supported on PostgreSQL and SQLite, declared via `models.Index(condition=Q(...))`."),
            ("An index that covers only half of a string's characters", False, "Incorrect. It filters rows, not character length."),
            ("An index that updates only on weekends", False, "Incorrect. Indexes update synchronously on matching writes."),
            ("An index created without a name", False, "Incorrect. All modern indexes should be named."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Django Request Lifecycle",
        "difficulty": "ADVANCED",
        "content": "What happens if an unhandled exception occurs inside a Django view during request processing?",
        "code_snippet": "# Exception during view execution:\ndef buggy_view(request):\n    raise RuntimeError(\"Unexpected server error\")",
        "explanation": "Django catches the unhandled exception, invokes `process_exception` on active middleware in reverse order, emits the `got_request_exception` signal, and if still unhandled, renders the standard 500 server error template (`handler500`), returning HTTP 500.",
        "options": [
            ("Middleware `process_exception` is called, `got_request_exception` signal emits, and HTTP 500 error page is rendered", True, "Correct. Clean graceful server failure without crashing the WSGI server process."),
            ("The operating system kills the Python server immediately", False, "Incorrect. WSGI workers catch exceptions gracefully."),
            ("The database is completely wiped to prevent corruption", False, "Incorrect. Transactions roll back, but databases are not wiped."),
            ("The client is redirected to Google homepage", False, "Incorrect. Django returns a 500 Internal Server Error response."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "ORM Optimization",
        "difficulty": "ADVANCED",
        "content": "How do you generate an SQL `EXPLAIN` query plan on a Django QuerySet to inspect database execution strategies?",
        "code_snippet": "plan = Question.objects.filter(difficulty='ADVANCED', is_active=True).explain(analyze=True)\nprint(plan)",
        "explanation": "Django QuerySets provide `.explain(verbose=True, analyze=True)`. It executes SQL `EXPLAIN` (or `EXPLAIN ANALYZE` on PostgreSQL), returning the database query planner's execution plan including index usage, scan types, and execution costs.",
        "options": [
            ("`.explain(analyze=True)` - returns the database query execution plan and index scan diagnostics", True, "Correct. Essential for diagnosing index scans vs sequential table scans."),
            ("`print(queryset.sql_plan)`", False, "Incorrect. QuerySet has no sql_plan attribute."),
            ("Running `python manage.py inspect_query`", False, "Incorrect. Not a built-in management command."),
            ("Checking Django settings file", False, "Incorrect. Query plans are database engine diagnostics."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Middleware Internals",
        "difficulty": "ADVANCED",
        "content": "What is the role of `async def` middleware in an ASGI Django application?",
        "code_snippet": "class AsyncMiddleware:\n    async def __call__(self, request):\n        response = await self.get_response(request)\n        return response",
        "explanation": "In an ASGI environment, an `async def` middleware executes non-blocking asynchronous coroutine operations without requiring thread-switching, maintaining high concurrency throughout the entire ASGI request/response pipeline.",
        "options": [
            ("Processes requests and responses asynchronously within the ASGI event loop without blocking or thread switching", True, "Correct. Fully native asynchronous middleware for ASGI applications."),
            ("Converts all responses into JSON strings", False, "Incorrect. Middleware processes whatever response the view returns."),
            ("Forces requests to run on a background Celery worker", False, "Incorrect. Middleware runs in the web server process."),
            ("Disables all database transactions", False, "Incorrect. Transactions are independent of async middleware."),
        ]
    },
    {
        "category": "Django Advanced",
        "topic": "Celery Integration Concepts",
        "difficulty": "ADVANCED",
        "content": "How do you achieve task idempotency and prevent duplicate concurrent task execution in Celery using Redis?",
        "code_snippet": "# Redis distributed lock pattern for Celery tasks:\nwith redis_client.lock('lock:process_payout', timeout=60):\n    execute_payout()",
        "explanation": "To ensure task idempotency and avoid duplicate execution when tasks are retried or duplicated by message brokers, acquire a distributed Redis lock (e.g., using `redis.lock()`) with an expiration timeout and unique lock key before running critical logic.",
        "options": [
            ("Acquire a distributed Redis lock (`redis.lock()`) with an expiration timeout before executing critical task logic", True, "Correct. Guarantees that only one worker instance can execute the task concurrently."),
            ("Set `task_always_eager = True` in production", False, "Incorrect. task_always_eager forces synchronous in-process execution, which blocks web workers."),
            ("Set the Celery task retry count to 0 and disable logging", False, "Incorrect. Does not prevent concurrent execution from multiple task dispatches."),
            ("Store task results in the browser's cookies", False, "Incorrect. Celery is backend server worker infrastructure."),
        ]
    }
]


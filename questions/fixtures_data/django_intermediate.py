# 40 Django Intermediate Questions with 4 options and detailed technical explanations

DJANGO_INTERMEDIATE_QUESTIONS = [
    {
        "category": "Django Intermediate",
        "topic": "select_related()",
        "difficulty": "INTERMEDIATE",
        "content": "What is the key performance difference between `select_related()` and `prefetch_related()` in Django ORM?",
        "code_snippet": "# Query A: Question.objects.select_related('topic')\n# Query B: Question.objects.prefetch_related('options')",
        "explanation": "`select_related()` follows single-valued relationships (`ForeignKey`, `OneToOne`) by executing an SQL `INNER JOIN` or `LEFT OUTER JOIN` in a single query. `prefetch_related()` does a separate lookup query for multi-valued relationships (`ManyToMany`, reverse `ForeignKey`) and performs the joining in Python memory.",
        "options": [
            ("`select_related` uses SQL JOINs in 1 query for ForeignKey/OneToOne; `prefetch_related` executes separate queries for ManyToMany/reverse FK and joins in Python", True, "Correct. select_related creates SQL joins; prefetch_related runs batch lookups for multi-valued relations."),
            ("`select_related` is for ManyToMany; `prefetch_related` is for OneToOne", False, "Incorrect. The roles are reversed: ManyToMany requires prefetch_related."),
            ("Both execute SQL JOINs on the database server", False, "Incorrect. prefetch_related executes separate SQL queries and stitches relations in Python memory."),
            ("`prefetch_related` caches data in Redis, while `select_related` does not", False, "Incorrect. Both populate model instance caches in Python RAM."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What is the classic 'N+1 queries problem' in Django and how is it resolved?",
        "code_snippet": "# N+1 Problem:\nquestions = Question.objects.all()[:50]\nfor q in questions:\n    print(q.topic.name)  # 1 initial query + 50 individual queries!",
        "explanation": "The N+1 problem occurs when fetching N objects in 1 query, and then accessing a related foreign key inside a loop, triggering 1 additional database query per object (total 1 + N queries). It is resolved by eager loading with `.select_related()` or `.prefetch_related()`.",
        "options": [
            ("Triggering an individual SQL query for each loop iteration; resolved using `select_related()` or `prefetch_related()`", True, "Correct. Reduces N+1 queries to a single joined query or 2 batch queries."),
            ("Running N database migrations simultaneously without locking", False, "Incorrect. N+1 refers to ORM query multiplication."),
            ("Having N foreign keys pointing to 1 primary key", False, "Incorrect. That is standard relational normalization."),
            ("A concurrency race condition on database row updates", False, "Incorrect. Race conditions are resolved with select_for_update or F expressions."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What does the `F()` expression in Django ORM enable?",
        "code_snippet": "from django.db.models import F\n# Increment score without loading to Python:\nQuizAttempt.objects.filter(id=attempt.id).update(correct_count=F('correct_count') + 1)",
        "explanation": "`F()` represents the value of a model field directly in the database SQL expression. It allows database operations (like increments or comparing two columns) to execute directly in the database without pulling values into Python memory, avoiding concurrency race conditions.",
        "options": [
            ("Refers to database field values directly in SQL expressions, avoiding race conditions and memory loading", True, "Correct. Generates `UPDATE ... SET correct_count = correct_count + 1` directly at database level."),
            ("Filters QuerySets using fuzzy regular expressions", False, "Incorrect. Q objects handle boolean logic; F handles field-level expressions."),
            ("Formats dates and times in template context", False, "Incorrect. That is the date template filter."),
            ("Forces a QuerySet to execute synchronously on a background thread", False, "Incorrect. F() has no threading implications."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Middleware",
        "difficulty": "INTERMEDIATE",
        "content": "What order does Django middleware execute during the request and response cycle?",
        "code_snippet": "MIDDLEWARE = [\n    'MiddlewareA',\n    'MiddlewareB',\n    'MiddlewareC',\n]",
        "explanation": "During the request phase, middleware is executed top-to-bottom (`A -> B -> C`). During the response phase, middleware is executed in reverse order bottom-to-top (`C -> B -> A`). Think of it like layers of an onion.",
        "options": [
            ("Request phase: top-down (A -> B -> C); Response phase: bottom-up (C -> B -> A)", True, "Correct. Request enters from top to bottom; response travels back up from bottom to top."),
            ("Both request and response phases execute top-down (A -> B -> C)", False, "Incorrect. Response handlers wrap views in reverse order."),
            ("Middleware execution order is randomized for security", False, "Incorrect. Order is strictly deterministic based on MIDDLEWARE list."),
            ("Only the first middleware in the list is executed", False, "Incorrect. All middleware layers are traversed."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Middleware",
        "difficulty": "INTERMEDIATE",
        "content": "How do you author a standard callable middleware in modern Django?",
        "code_snippet": "class SimpleMiddleware:\n    def __init__(self, get_response):\n        self.get_response = get_response\n\n    def __call__(self, request):\n        # Code before view (request phase)\n        response = self.get_response(request)\n        # Code after view (response phase)\n        return response",
        "explanation": "A Django middleware is a callable initialized with `get_response`. When called with `request`, it can process code before calling `self.get_response(request)` and process or modify the `response` before returning it.",
        "options": [
            ("A callable initialized with `get_response`, executing logic before and after calling `self.get_response(request)`", True, "Correct. This is the standard PEP 3333 / Django callable middleware pattern."),
            ("Inherit from `django.middleware.BaseMiddleware` and implement `process_view` only", False, "Incorrect. BaseMiddleware is not required in modern Django; any callable with get_response works."),
            ("Decorate views with `@middleware`", False, "Incorrect. Middleware wraps all requests globally in settings.MIDDLEWARE."),
            ("Define an Express middleware function", False, "Incorrect. Express is Node.js."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Signals",
        "difficulty": "INTERMEDIATE",
        "content": "What are Django signals and what is a common architectural criticism of overusing them?",
        "code_snippet": "from django.db.models.signals import post_save\nfrom django.dispatch import receiver\n\n@receiver(post_save, sender=User)\ndef user_created_handler(sender, instance, created, **kwargs): ...",
        "explanation": "Signals allow decoupled applications to get notified when actions occur elsewhere in the framework (e.g. `post_save`, `post_delete`). However, overuse makes control flow implicit and difficult to trace, debug, and test, compared to explicit service layer functions.",
        "options": [
            ("Publish-subscribe hooks for decoupled events; criticism: implicit control flow makes debugging and testing difficult", True, "Correct. Explicit service calls are often preferred over sprawling implicit signals."),
            ("Asynchronous background Celery task runners", False, "Incorrect. Standard Django signals execute synchronously in the same thread and database transaction!"),
            ("Operating system POSIX kill signals (SIGTERM/SIGINT)", False, "Incorrect. Django signals are internal application-level pub/sub hooks."),
            ("Real-time WebSocket event emitters", False, "Incorrect. Django signals do not emit WebSocket messages automatically."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Signals",
        "difficulty": "INTERMEDIATE",
        "content": "Do standard Django signals execute synchronously or asynchronously?",
        "code_snippet": "@receiver(post_save, sender=QuizAttempt)\ndef notify_admin(sender, instance, **kwargs):\n    # Will this run in a background thread?",
        "explanation": "Django signals are 100% synchronous by default. Every receiver executes in the same thread and process, within the caller's request-response lifecycle (and inside the same database transaction if active). Long tasks will block the user's HTTP response.",
        "options": [
            ("Synchronously in the same thread and execution context as the sender", True, "Correct. A common misconception is that signals are asynchronous; they are fully synchronous!"),
            ("Asynchronously in a Celery background queue", False, "Incorrect. Offloading to Celery requires explicit task dispatch."),
            ("In a separate OS process via fork()", False, "Incorrect. Standard signals do not spawn processes."),
            ("In a client-side JavaScript service worker", False, "Incorrect. Signals are pure backend Python."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Class-Based Views",
        "difficulty": "INTERMEDIATE",
        "content": "What method turns a Class-Based View (CBV) into a callable view function for `urls.py`?",
        "code_snippet": "urlpatterns = [\n    path('quizzes/', QuizListView.as_view(), name='quiz_list'),\n]",
        "explanation": "The `.as_view()` class method creates and returns a callable view function that takes an `HttpRequest`, instantiates the class, assigns `self.request = request`, and dispatches to the appropriate HTTP verb handler (`get()`, `post()`, etc.).",
        "options": [
            ("`.as_view()`", True, "Correct. Transforms the CBV into a callable for Django's URL resolver."),
            ("`.to_view()`", False, "Incorrect. Method name is as_view()."),
            ("`.dispatch()`", False, "Incorrect. dispatch() is an internal instance method called during request handling."),
            ("`.render_view()`", False, "Incorrect. No such class method exists."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Class-Based Views",
        "difficulty": "INTERMEDIATE",
        "content": "Which built-in Generic Class-Based View is designed to display a single model detail record?",
        "code_snippet": "from django.views.generic import DetailView\n\nclass QuestionDetail(DetailView):\n    model = Question\n    template_name = 'questions/detail.html'",
        "explanation": "`DetailView` is designed to display a single object. It automatically queries `model.objects.get()` using the `pk` or `slug` captured from the URLconf and places the object in the template context as `object` and lowercase model name.",
        "options": [
            ("`DetailView`", True, "Correct. Standard generic view for single-object presentation."),
            ("`SingleView`", False, "Incorrect. Django does not have SingleView."),
            ("`RecordView`", False, "Incorrect. Django uses DetailView."),
            ("`ItemView`", False, "Incorrect. ItemView does not exist in Django generics."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Function-Based Views",
        "difficulty": "INTERMEDIATE",
        "content": "What is the primary advantage of Function-Based Views (FBVs) over complex Class-Based View hierarchies?",
        "code_snippet": "def quiz_take_view(request, attempt_id):\n    # Explicit, linear reading order",
        "explanation": "Function-Based Views offer explicit, linear code flow that is easy to read, trace, and debug from top to bottom, without hidden method dispatching or multi-layer mixin inheritance hierarchies.",
        "options": [
            ("Explicit, straightforward procedural flow that is easy to read and debug without hidden inheritance layers", True, "Correct. FBVs are simple and transparent; CBVs shine for standard CRUD via reuse."),
            ("FBVs execute twice as fast as CBVs in CPython", False, "Incorrect. Performance difference is negligible."),
            ("FBVs do not require URL routing", False, "Incorrect. Both require URLconf routing."),
            ("FBVs bypass CSRF verification automatically", False, "Incorrect. Both enforce CSRF."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Authentication",
        "difficulty": "INTERMEDIATE",
        "content": "What does Django's `authenticate(request, username=username, password=password)` function do?",
        "code_snippet": "user = authenticate(request, username='alice', password='secretpassword')",
        "explanation": "`authenticate()` checks the credentials against configured authentication backends. If valid (hashes match via PBKDF2/argon2), it returns the authenticated `User` instance; if invalid, it returns `None`. It does not log the user into the session.",
        "options": [
            ("Verifies credentials against configured backends and returns the User object if valid, or None if invalid", True, "Correct. Note that authenticate() verifies credentials, while login() binds the user to the session."),
            ("Directly logs the user into the session and issues a cookie", False, "Incorrect. `login(request, user)` binds the user into the session."),
            ("Encrypts the password and stores it in the database", False, "Incorrect. set_password() handles hashing and storage."),
            ("Creates a new user account if one doesn't exist", False, "Incorrect. User.objects.create_user() handles account creation."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Authentication",
        "difficulty": "INTERMEDIATE",
        "content": "What algorithm does Django use by default for password hashing?",
        "code_snippet": "PASSWORD_HASHERS = [\n    'django.contrib.auth.hashers.PBKDF2PasswordHasher',\n    ...\n]",
        "explanation": "Django uses PBKDF2 with a SHA-256 hash by default (with hundreds of thousands of work factor iterations and a cryptographic salt), which is recommended by NIST.",
        "options": [
            ("PBKDF2 with SHA-256 and cryptographic per-password salt", True, "Correct. Django's default hasher is PBKDF2PasswordHasher with high iteration count."),
            ("Plain MD5 hash without salt", False, "Incorrect. MD5 is insecure and rejected by modern frameworks."),
            ("Plain text encoded with Base64", False, "Incorrect. Base64 is reversible encoding, not hashing."),
            ("Single-pass SHA-1", False, "Incorrect. SHA-1 is cryptographically broken."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Authorization",
        "difficulty": "INTERMEDIATE",
        "content": "What decorator protects a view so only authenticated logged-in users can access it?",
        "code_snippet": "from django.contrib.auth.decorators import login_required\n\n@login_required\ndef user_dashboard(request):\n    ...",
        "explanation": "`@login_required` checks `request.user.is_authenticated`. If true, the view executes. If false, it redirects the user to `settings.LOGIN_URL` with a `?next=/target/` parameter for seamless post-login redirection.",
        "options": [
            ("`@login_required`", True, "Correct. Redirects unauthenticated users to LOGIN_URL."),
            ("`@auth_only`", False, "Incorrect. No such decorator."),
            ("`@user_passes_test` only", False, "Incorrect. While user_passes_test is a base helper, @login_required is the dedicated decorator."),
            ("`@protected_route`", False, "Incorrect. That is a React Router idiom."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Authorization",
        "difficulty": "INTERMEDIATE",
        "content": "What mixin provides `@login_required` functionality for Class-Based Views?",
        "code_snippet": "from django.contrib.auth.mixins import LoginRequiredMixin\n\nclass DashboardView(LoginRequiredMixin, TemplateView):\n    template_name = 'dashboard.html'",
        "explanation": "`LoginRequiredMixin` must be placed as the leftmost superclass in a CBV definition. It intercepts `dispatch()` and ensures the user is authenticated before proceeding.",
        "options": [
            ("`LoginRequiredMixin` (placed as the leftmost parent class)", True, "Correct. Python MRO requires mixins to precede base generic views."),
            ("`AuthRequiredMixin`", False, "Incorrect. The standardized name is LoginRequiredMixin."),
            ("`UserAuthenticatedMixin`", False, "Incorrect. No such mixin in Django core."),
            ("`SessionRequiredMixin`", False, "Incorrect. Django uses LoginRequiredMixin."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Sessions",
        "difficulty": "INTERMEDIATE",
        "content": "Where does Django store session data by default?",
        "code_snippet": "# settings.py default session engine:\n# SESSION_ENGINE = 'django.contrib.sessions.backends.db'",
        "explanation": "By default, Django uses database-backed sessions (`django.contrib.sessions.backends.db`). Session data is serialized, signed, and stored in the `django_session` table, while only a session key is sent to the client's browser in a cookie.",
        "options": [
            ("Database table `django_session` (server-side), with only the session key stored in the browser cookie", True, "Correct. Secure default: client only holds an opaque session key."),
            ("Directly in the client's localStorage in plain JSON", False, "Incorrect. Django sessions are server-side HTTP cookies."),
            ("In plaintext inside the URL query string", False, "Incorrect. Storing session tokens in URLs is a security vulnerability."),
            ("In a local text file on the client's computer", False, "Incorrect. Sessions are managed by server and cookies."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Cookies",
        "difficulty": "INTERMEDIATE",
        "content": "What security flags should be set on Django session cookies in production?",
        "code_snippet": "SESSION_COOKIE_HTTPONLY = True\nSESSION_COOKIE_SECURE = True\nSESSION_COOKIE_SAMESITE = 'Lax'",
        "explanation": "`HttpOnly` prevents client-side JavaScript from accessing the cookie (mitigating XSS). `Secure` ensures the cookie is only transmitted over HTTPS. `SameSite='Lax'` prevents cross-site request leakage (mitigating CSRF).",
        "options": [
            ("`HttpOnly=True` (anti-XSS), `Secure=True` (HTTPS-only), and `SameSite='Lax'` or `'Strict'` (anti-CSRF)", True, "Correct. Standard trifecta for hardened web application session cookies."),
            ("`AllowAllOrigins=True` and `Public=True`", False, "Incorrect. These are not valid cookie security flags."),
            ("`DisableEncryption=True`", False, "Incorrect. Insecure."),
            ("Cookies do not support security flags", False, "Incorrect. Modern browsers enforce cookie security flags."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Pagination",
        "difficulty": "INTERMEDIATE",
        "content": "How does Django's `Paginator` split a QuerySet into pages?",
        "code_snippet": "from django.core.paginator import Paginator\n\npaginator = Paginator(questions, 10)\npage_obj = paginator.get_page(request.GET.get('page'))",
        "explanation": "Django's `Paginator(queryset, per_page)` uses SQL `LIMIT` and `OFFSET` slicing when a page is requested. `.get_page()` safely handles invalid page numbers (non-integers default to page 1, out-of-range numbers return the last page).",
        "options": [
            ("Uses SQL `LIMIT` and `OFFSET` slicing on the QuerySet; `.get_page()` safely handles invalid page indices", True, "Correct. Only the rows for the requested page are loaded from the database."),
            ("Loads the entire database into a Python dictionary and splits strings", False, "Incorrect. Paginator slices the underlying QuerySet efficiently."),
            ("Sends all 10,000 records to the browser and lets JavaScript paginate", False, "Incorrect. Server-side pagination minimizes data transfer."),
            ("Generates static HTML files for each page on disk", False, "Incorrect. Pages are rendered dynamically per request."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "File Upload",
        "difficulty": "INTERMEDIATE",
        "content": "What HTML attribute is required on a `<form>` to allow file uploads in Django?",
        "code_snippet": "<form method=\"POST\" enctype=\"multipart/form-data\">\n  {% csrf_token %}\n  <input type=\"file\" name=\"resume\">\n</form>",
        "explanation": "`enctype=\"multipart/form-data\"` tells the browser to encode form data into MIME multipart format, which transmits binary file payloads. Without this, files will not appear in `request.FILES` in Django.",
        "options": [
            ("`enctype=\"multipart/form-data\"`", True, "Correct. Required for binary file uploads to populate `request.FILES`."),
            ("`enctype=\"application/x-www-form-urlencoded\"`", False, "Incorrect. That is standard text-only form encoding."),
            ("`upload=\"true\"`", False, "Incorrect. Not a valid HTML form attribute."),
            ("`file_mode=\"stream\"`", False, "Incorrect. Invalid attribute."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Custom Managers",
        "difficulty": "INTERMEDIATE",
        "content": "How do you define a Custom Manager to provide a reusable `.active()` query method on a model?",
        "code_snippet": "class QuestionManager(models.Manager):\n    def active(self):\n        return self.filter(is_active=True)\n\nclass Question(models.Model):\n    objects = QuestionManager()",
        "explanation": "Subclass `models.Manager` and define methods that return filtered QuerySets (`self.filter(...)`). Assign an instance of this manager to `objects = QuestionManager()` on the model class.",
        "options": [
            ("Subclass `models.Manager` and define custom methods returning filtered QuerySets", True, "Correct. Enables clean domain-driven queries like `Question.objects.active()`."),
            ("Add static methods inside views.py", False, "Incorrect. Managers encapsulate model-level database queries."),
            ("Modify `django.db.models.manager` in site-packages", False, "Incorrect. Never modify third-party framework code."),
            ("Managers can only be created via Django migrations", False, "Incorrect. Managers are pure Python classes defined in models.py."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Custom Model Methods",
        "difficulty": "INTERMEDIATE",
        "content": "Why are custom model methods (e.g. `attempt.is_passed` or `user.profile.update_streak()`) considered good Django architecture?",
        "code_snippet": "class QuizAttempt(models.Model):\n    score = models.FloatField()\n    @property\n    def is_passed(self):\n        return self.score >= 70.0",
        "explanation": "Placing business logic directly on models follows the 'Fat Models, Skinny Views' architectural best practice. It encapsulates data logic in one place, avoiding duplicate business rules scattered across multiple views or management commands.",
        "options": [
            ("Follows 'Fat Models, Skinny Views' to centralize business logic and keep code DRY across views", True, "Correct. Ensures data logic and state transitions remain cohesive and reusable."),
            ("Forces SQLite to create stored procedures", False, "Incorrect. SQLite does not support stored procedures."),
            ("Allows model methods to execute in the browser client", False, "Incorrect. Model methods run strictly on the server."),
            ("Model methods automatically generate REST endpoints", False, "Incorrect. REST endpoints require DRF serializers and views."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Django REST Framework fundamentals",
        "difficulty": "INTERMEDIATE",
        "content": "What is the primary role of a `Serializer` in Django REST Framework (DRF)?",
        "code_snippet": "from rest_framework import serializers\n\nclass QuestionSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Question\n        fields = '__all__'",
        "explanation": "A DRF Serializer converts complex Django model instances and QuerySets into native Python datatypes that can easily be rendered into JSON/XML (serialization), and deserializes incoming parsed JSON into validated data or model instances (deserialization).",
        "options": [
            ("Converts model instances to JSON (serialization) and validates incoming JSON into model instances (deserialization)", True, "Correct. Acts as the bidirectional bridge between HTTP payloads and Django ORM models."),
            ("Compiles Python code into machine language", False, "Incorrect. Serialization is data conversion, not compilation."),
            ("Encrypts SQL database connections", False, "Incorrect. TLS handles database connection encryption."),
            ("Replaces Django template engine with Vite", False, "Incorrect. DRF is an API framework."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What does `values_list('id', flat=True)` return compared to `values('id')` in Django?",
        "code_snippet": "flat_pks = Question.objects.values_list('id', flat=True)\n# vs\ndict_pks = Question.objects.values('id')",
        "explanation": "`values_list('id', flat=True)` returns a flat QuerySet of single values: `[1, 2, 3]`. `values('id')` returns a QuerySet of dictionaries: `[{'id': 1}, {'id': 2}, {'id': 3}]`.",
        "options": [
            ("`values_list(..., flat=True)` returns a list of raw values `[1, 2, 3]`; `values()` returns dictionaries `[{'id': 1}]`", True, "Correct. flat=True is optimal when you only need a list of IDs for IN queries or random sampling."),
            ("`values()` returns tuples; `values_list()` returns dictionaries", False, "Incorrect. values_list() returns tuples (or flat values if flat=True)."),
            ("`values()` modifies the database table", False, "Incorrect. Both are read-only QuerySet projections."),
            ("They return identical output", False, "Incorrect. One produces dictionaries, the other flat primitives."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "select_related()",
        "difficulty": "INTERMEDIATE",
        "content": "Can `select_related()` be used on a `ManyToManyField` in Django?",
        "code_snippet": "# Can we do Question.objects.select_related('tags') for a ManyToMany?",
        "explanation": "No. `select_related()` only works on single-valued relationships (`ForeignKey` and `OneToOneField`) because it relies on single-row SQL JOINs. Attempting to use `select_related()` on a `ManyToManyField` raises a `FieldError`. Use `prefetch_related()` instead.",
        "options": [
            ("No, it raises a `FieldError`; ManyToMany requires `prefetch_related()`", True, "Correct. select_related cannot handle multi-valued relationships without duplicating rows."),
            ("Yes, it performs an outer cross-join automatically", False, "Incorrect. Django explicitly disallows it."),
            ("Yes, but only if the through table has an integer primary key", False, "Incorrect. It is rejected regardless of through table schema."),
            ("Only on PostgreSQL, not on SQLite", False, "Incorrect. The constraint is enforced in Django ORM across all databases."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Sessions",
        "difficulty": "INTERMEDIATE",
        "content": "How do you store and retrieve custom data in a user's session in a Django view?",
        "code_snippet": "# Storing and retrieving in view:\nrequest.session['theme'] = 'dark'\ncurrent_theme = request.session.get('theme', 'light')",
        "explanation": "`request.session` behaves like a standard Python dictionary. You can set keys with `request.session[key] = val` and read keys with `request.session.get(key, default)`.",
        "options": [
            ("Using `request.session` like a standard Python dictionary: `request.session['key'] = value`", True, "Correct. Django automatically handles serialization and persistence to the session backend."),
            ("Calling `django.contrib.sessions.set('key', value)`", False, "Incorrect. Sessions are accessed via the request object."),
            ("Editing the browser cookie using JavaScript document.cookie", False, "Incorrect. Session data is stored server-side for security."),
            ("Inserting rows directly into auth_user table", False, "Incorrect. User table is for credentials and profile, not transient sessions."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What is the difference between `.exists()` and `bool(queryset)` in Django ORM?",
        "code_snippet": "has_questions = Question.objects.filter(is_active=True).exists()",
        "explanation": "`.exists()` executes a minimal SQL query `SELECT (1) AS a FROM table LIMIT 1`, which is extremely fast and transfers virtually no data. `bool(queryset)` evaluates the entire QuerySet, loading model instances into Python memory before checking length.",
        "options": [
            ("`.exists()` issues SQL `SELECT 1 ... LIMIT 1` without loading rows; `bool(qs)` loads results into memory", True, "Correct. Always use .exists() when you only need to verify record existence."),
            ("`.exists()` is slower than `bool(qs)`", False, "Incorrect. exists() is orders of magnitude faster on large tables."),
            ("`bool(qs)` raises an exception if the table is empty", False, "Incorrect. bool() returns False on empty QuerySets."),
            ("They execute identical SQL queries", False, "Incorrect. One is LIMIT 1, the other is full SELECT *."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Authentication",
        "difficulty": "INTERMEDIATE",
        "content": "What function must be called after a user changes their password to prevent their current session from being logged out?",
        "code_snippet": "from django.contrib.auth import update_session_auth_hash\n\ndef change_pwd(request):\n    form = PasswordChangeForm(request.user, request.POST)\n    if form.is_valid():\n        user = form.save()\n        update_session_auth_hash(request, user)",
        "explanation": "Changing a user's password updates their session authentication hash. Calling `update_session_auth_hash(request, user)` rotates the session's stored hash so the active user is not logged out upon password change.",
        "options": [
            ("`update_session_auth_hash(request, user)`", True, "Correct. Prevents active user session invalidation after password update."),
            ("`request.session.keep_alive()`", False, "Incorrect. No such function."),
            ("`user.refresh_from_db()`", False, "Incorrect. refresh_from_db reloads model fields from database."),
            ("`auth.relogin(request)`", False, "Incorrect. update_session_auth_hash is the official Django function."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Signals",
        "difficulty": "INTERMEDIATE",
        "content": "Why should you check the `created` boolean argument inside a `post_save` signal receiver?",
        "code_snippet": "@receiver(post_save, sender=User)\ndef handle_user_save(sender, instance, created, **kwargs):\n    if created:\n        UserProfile.objects.create(user=instance)",
        "explanation": "`post_save` fires both when a new record is created AND whenever an existing record is updated. The `created` argument is `True` only on initial creation (`INSERT`), and `False` on updates (`UPDATE`). Without checking `created`, you may attempt duplicate creations.",
        "options": [
            ("`created` is True only on `INSERT` (new record) and False on `UPDATE`, preventing duplicate action on existing records", True, "Correct. Essential for provisioning profiles or sending welcome emails once upon registration."),
            ("`created` indicates whether the database transaction committed", False, "Incorrect. post_save fires before transaction commit unless transaction.on_commit is used."),
            ("`created` indicates whether the user is an administrator", False, "Incorrect. That is user.is_staff or is_superuser."),
            ("`created` is a timestamp object", False, "Incorrect. It is a boolean flag."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Class-Based Views",
        "difficulty": "INTERMEDIATE",
        "content": "What method in a Django Class-Based View is responsible for populating the template context dictionary?",
        "code_snippet": "class DashboardView(TemplateView):\n    def get_context_data(self, **kwargs):\n        context = super().get_context_data(**kwargs)\n        context['stats'] = get_stats()\n        return context",
        "explanation": "`get_context_data(**kwargs)` prepares and returns the dictionary to be passed to the template. Always call `super().get_context_data(**kwargs)` first to preserve default context values.",
        "options": [
            ("`get_context_data(**kwargs)`", True, "Correct. Standard method to inject custom variables into CBV template context."),
            ("`set_context()`", False, "Incorrect. Django uses get_context_data."),
            ("`context_processor()`", False, "Incorrect. Context processors are project-wide callables, not CBV methods."),
            ("`render_context()`", False, "Incorrect. Invalid method name."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What method on a QuerySet updates multiple rows in the database in a single SQL query without calling `.save()` on individual instances?",
        "code_snippet": "Question.objects.filter(is_active=False).update(is_active=True)",
        "explanation": "`.update(**kwargs)` issues a single SQL `UPDATE` statement affecting all matching rows. Because it runs directly in SQL, it does NOT call the model's `.save()` method or trigger `pre_save` / `post_save` signals.",
        "options": [
            ("`.update(**kwargs)`", True, "Correct. Fast bulk update directly in SQL; bypasses individual model .save() methods and signals."),
            ("`.bulk_save()`", False, "Incorrect. Django provides bulk_create and bulk_update, not bulk_save."),
            ("`.modify()`", False, "Incorrect. No .modify() on QuerySet."),
            ("`.save_all()`", False, "Incorrect. QuerySet has no save_all method."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What is the difference between `bulk_create()` and repeated `.create()` calls in a loop?",
        "code_snippet": "UserAnswer.objects.bulk_create(answers_list)",
        "explanation": "`bulk_create()` inserts multiple rows into the database using a single batched SQL `INSERT` statement. Calling `.create()` in a loop executes a separate `INSERT` query on each iteration, causing significant database network round-trip overhead.",
        "options": [
            ("`bulk_create()` inserts all objects in a single batch SQL query; `.create()` executes 1 query per object", True, "Correct. Drastically improves throughput when seeding or creating quiz answers."),
            ("`bulk_create()` runs on a worker thread in the background", False, "Incorrect. It runs synchronously on the current connection."),
            ("`.create()` cannot insert foreign keys", False, "Incorrect. Both handle foreign keys."),
            ("`bulk_create()` is only supported on MySQL", False, "Incorrect. Supported across SQLite, PostgreSQL, MySQL, and Oracle."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Django REST Framework fundamentals",
        "difficulty": "INTERMEDIATE",
        "content": "What status code does DRF return by default when creating a resource via a `POST` request on a `ModelViewSet`?",
        "code_snippet": "# POST /api/quizzes/\n# HTTP Response status",
        "explanation": "In accordance with RESTful HTTP standards, DRF returns HTTP `201 Created` upon successful resource creation.",
        "options": [
            ("`201 Created`", True, "Correct. HTTP 201 indicates that a new resource has been created."),
            ("`200 OK`", False, "Incorrect. 200 is standard for GET/PUT/PATCH, but creation uses 201 Created."),
            ("`204 No Content`", False, "Incorrect. 204 is typical for DELETE operations."),
            ("`202 Accepted`", False, "Incorrect. 202 is used for asynchronous/queued job requests."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What is the purpose of `only()` and `defer()` on a Django QuerySet?",
        "code_snippet": "questions = Question.objects.only('id', 'content')",
        "explanation": "`only('id', 'content')` instructs Django to load only the specified fields in the initial SQL query. `defer('explanation')` loads all fields except the deferred ones. If a deferred field is later accessed, Django executes a separate query to fetch it.",
        "options": [
            ("Optimizes queries by loading only specified columns (`only`) or postponing loading heavy columns (`defer`)", True, "Correct. Prevents loading large text or binary columns into memory when unneeded."),
            ("Locks columns from being edited by administrators", False, "Incorrect. It is a SELECT query optimization."),
            ("Controls database indexing", False, "Incorrect. Indexing is defined in model Meta."),
            ("Hides fields from JSON serializers", False, "Incorrect. Serializer fields are defined in DRF."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Authorization",
        "difficulty": "INTERMEDIATE",
        "content": "How do you check if a user has a specific permission `questions.change_question` in a view?",
        "code_snippet": "if request.user.has_perm('questions.change_question'):\n    # Allow editing",
        "explanation": "`user.has_perm('app_label.codename')` checks whether the user (or any of their assigned groups) possesses that permission. Superusers automatically return `True` for all permissions.",
        "options": [
            ("`request.user.has_perm('app_label.codename')`", True, "Correct. Standard Django permission checking method."),
            ("`request.user.check_permission('change_question')`", False, "Incorrect. Method name is has_perm()."),
            ("`request.user.permissions.contains('change_question')`", False, "Incorrect. has_perm resolves group and user permissions."),
            ("Inspect `settings.PERMISSIONS`", False, "Incorrect. Permissions are managed dynamically in database."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What does `.aggregate()` return compared to `.annotate()` in Django ORM?",
        "code_snippet": "# Example A: avg = QuizAttempt.objects.aggregate(Avg('score'))\n# Example B: topics = Topic.objects.annotate(q_count=Count('questions'))",
        "explanation": "`.aggregate()` calculates summary values over the entire QuerySet and returns a plain Python dictionary of results (e.g. `{'score__avg': 82.5}`). `.annotate()` calculates aggregations per-item and returns a modified QuerySet where each object has the annotated value attached.",
        "options": [
            ("`aggregate()` returns a dictionary of summary values for the whole query; `annotate()` adds per-row aggregated fields to each object in a QuerySet", True, "Correct. Think of annotate as SQL GROUP BY per object, and aggregate as SQL aggregate across all rows."),
            ("`annotate()` returns a dictionary; `aggregate()` returns a QuerySet", False, "Incorrect. The outputs are reversed."),
            ("`aggregate()` works only on numbers; `annotate()` works only on dates", False, "Incorrect. Both support count, avg, sum, min, max."),
            ("There is no technical difference between them", False, "Incorrect. Fundamental distinction in ORM grouping."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Authentication",
        "difficulty": "INTERMEDIATE",
        "content": "What is the recommended approach for extending Django's built-in `User` model when you only need extra profile attributes (like bio, target role)?",
        "code_snippet": "class UserProfile(models.Model):\n    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')\n    bio = models.TextField()",
        "explanation": "For application profile fields, creating a separate `UserProfile` model with a `OneToOneField(User)` is the cleanest, least disruptive pattern. It preserves Django's default auth mechanics while providing flexible user metadata.",
        "options": [
            ("Creating a `UserProfile` model linked via a `OneToOneField` to `User`", True, "Correct. Idiomatic, modular, and does not require complex custom user model migrations."),
            ("Directly editing the auth_user table schema in SQLite", False, "Incorrect. Breaks migrations and framework upgrades."),
            ("Storing all profile data in browser cookies", False, "Incorrect. Insecure and non-persistent across devices."),
            ("Adding monkey-patched properties to the User class at runtime", False, "Incorrect. Does not persist in the database."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Middleware",
        "difficulty": "INTERMEDIATE",
        "content": "How can a custom middleware intercept and handle exceptions raised in views?",
        "code_snippet": "class ExceptionLoggerMiddleware:\n    def __init__(self, get_response):\n        self.get_response = get_response\n    def process_exception(self, request, exception):\n        logger.error(f\"View crashed: {exception}\")\n        return HttpResponse(\"Server Error\", status=500)",
        "explanation": "Django middleware can define the special method `process_exception(request, exception)`. When a view raises an uncaught exception, Django calls `process_exception` in reverse middleware order. Returning an `HttpResponse` stops subsequent exception handlers.",
        "options": [
            ("By implementing the `process_exception(request, exception)` hook in the middleware class", True, "Correct. Invoked when a view raises an exception, allowing custom logging or custom error responses."),
            ("Wrapping settings.py in a try/except block", False, "Incorrect. settings.py is executed at application boot, not per-request."),
            ("Decorating urls.py with `@catch_errors`", False, "Incorrect. Middleware handles cross-cutting request exceptions."),
            ("Using the `sys.excepthook` standard library function", False, "Incorrect. Django provides process_exception."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Django REST Framework fundamentals",
        "difficulty": "INTERMEDIATE",
        "content": "What is the benefit of using `APIView` or `@api_view` in DRF compared to standard Django views?",
        "code_snippet": "from rest_framework.views import APIView\nfrom rest_framework.response import Response\n\nclass QuestionListAPI(APIView):\n    def get(self, request):\n        return Response({'status': 'ok'})",
        "explanation": "`APIView` wraps the request in DRF's `Request` object (providing `request.data` for JSON parsing), manages authentication/permission classes, and handles content negotiation to render browsable API HTML or JSON automatically.",
        "options": [
            ("Provides DRF `Request` with `request.data`, built-in authentication/permission enforcement, and content negotiation", True, "Correct. Automatically parses JSON payloads and enforces token/session auth policies."),
            ("Compiles Python endpoints to Go binaries", False, "Incorrect. It is standard Python."),
            ("Automatically provisions an AWS Lambda serverless function", False, "Incorrect. APIView runs on your Django WSGI/ASGI server."),
            ("Disables all database security checks", False, "Incorrect. DRF integrates with Django ORM security."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What does `distinct()` do on a Django QuerySet?",
        "code_snippet": "topics = Topic.objects.filter(questions__difficulty='ADVANCED').distinct()",
        "explanation": "`distinct()` adds `SELECT DISTINCT` to the SQL query, eliminating duplicate rows that occur when filtering across many-to-many or reverse foreign key relationships.",
        "options": [
            ("Emits SQL `SELECT DISTINCT` to eliminate duplicate rows returned from relational joins", True, "Correct. Essential when filtering on joined reverse relations to avoid repeated parent objects."),
            ("Sorts the QuerySet alphabetically", False, "Incorrect. Sorting is handled by order_by()."),
            ("Clears all cached QuerySets in memory", False, "Incorrect. QuerySet cache is internal to the instance."),
            ("Filters records where ID is an odd number", False, "Incorrect. distinct handles SQL row uniqueness."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "Class-Based Views",
        "difficulty": "INTERMEDIATE",
        "content": "What is the purpose of `form_valid(self, form)` in Django's `FormView` or `CreateView`?",
        "code_snippet": "class QuestionCreate(CreateView):\n    def form_valid(self, form):\n        form.instance.created_by = self.request.user\n        return super().form_valid(form)",
        "explanation": "`form_valid()` is called when the submitted form successfully passes validation. It provides the hook to modify the model instance (e.g., assign `created_by = request.user`), save it, and return a redirect response to `get_success_url()`.",
        "options": [
            ("Executes after form validation passes, allowing custom instance mutation before saving and redirecting", True, "Correct. Standard hook to associate request.user or trigger post-save side effects."),
            ("Runs custom JavaScript in the user's browser", False, "Incorrect. form_valid executes on the backend server."),
            ("Renders form errors back to the user", False, "Incorrect. form_invalid() handles rendering errors."),
            ("Validates CSRF tokens", False, "Incorrect. CsrfViewMiddleware handles CSRF."),
        ]
    },
    {
        "category": "Django Intermediate",
        "topic": "QuerySets",
        "difficulty": "INTERMEDIATE",
        "content": "What is the difference between `iterator()` and standard iteration on a large QuerySet?",
        "code_snippet": "for q in Question.objects.all().iterator(chunk_size=1000):\n    process(q)",
        "explanation": "Standard QuerySet iteration evaluates the query and caches all model instances in the QuerySet's internal cache (`_result_cache`). `.iterator()` streams results directly using server-side cursors without caching them in memory, saving vast RAM on massive datasets.",
        "options": [
            ("`.iterator()` reads results directly from the database stream without caching in Python RAM, preventing out-of-memory errors", True, "Correct. Ideal for processing hundreds of thousands of rows in batch jobs."),
            ("`.iterator()` runs on GPU threads", False, "Incorrect. It is standard database cursor streaming."),
            ("Standard iteration does not support for loops", False, "Incorrect. Standard QuerySets are fully iterable."),
            ("`.iterator()` modifies rows in-place", False, "Incorrect. iterator is a read stream optimization."),
        ]
    }
]

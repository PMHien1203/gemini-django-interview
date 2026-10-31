# 40 Django Beginner Questions with 4 options and detailed technical explanations

DJANGO_BEGINNER_QUESTIONS = [
    {
        "category": "Django Fundamentals",
        "topic": "Django Architecture",
        "difficulty": "BEGINNER",
        "content": "What architectural pattern does Django fundamentally follow, and what do the letters stand for?",
        "code_snippet": "# Django architectural design pattern",
        "explanation": "Django follows the MVT (Model-View-Template) pattern. Model handles data logic and ORM, View handles business logic and HTTP processing, and Template handles the UI presentation layer.",
        "options": [
            ("MVT (Model-View-Template)", True, "Correct. In Django MVT, View acts like the Controller in traditional MVC, and Template is the View."),
            ("MVC (Model-View-Controller) where View is HTML and Controller is views.py", False, "Incorrect. Django officially classifies its architecture as MVT."),
            ("MVVM (Model-View-ViewModel)", False, "Incorrect. MVVM is used primarily in client-side desktop and reactive frontend frameworks."),
            ("Microkernel architecture", False, "Incorrect. Django is a batteries-included monolithic web framework."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "MVT Pattern",
        "difficulty": "BEGINNER",
        "content": "In Django's MVT pattern, which component corresponds to the 'Controller' in traditional MVC?",
        "code_snippet": "# MVT vs MVC mapping in Django",
        "explanation": "In Django, the 'View' (`views.py`) functions as the Controller: it receives HTTP requests, coordinates with Models for database operations, and selects and renders Templates with context data.",
        "options": [
            ("The View (`views.py`)", True, "Correct. The Django View acts as the Controller orchestrating business logic and response preparation."),
            ("The Template (`.html`)", False, "Incorrect. The Template corresponds to the View in traditional MVC."),
            ("The URLconf (`urls.py`)", False, "Incorrect. URLs route requests to views, but business orchestration occurs in the View."),
            ("The Model (`models.py`)", False, "Incorrect. Models encapsulate database schema and queries."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Project vs App",
        "difficulty": "BEGINNER",
        "content": "What is the key difference between a Django Project and a Django App?",
        "code_snippet": "# django-admin startproject mysite\n# python manage.py startapp blog",
        "explanation": "A project is an entire web application configuration containing settings, base URLs, and databases. An app is a modular, self-contained Python package that provides a specific functionality (e.g., blog, auth, billing) and can be reused across multiple projects.",
        "options": [
            ("A project is the overall site configuration; an app is a reusable, modular component with specific business functionality", True, "Correct. A project contains configuration (settings.py, urls.py) and connects multiple apps."),
            ("A project is for frontend; an app is for backend", False, "Incorrect. Django apps encompass backend models, views, and templates together."),
            ("A project can only contain exactly one app", False, "Incorrect. A project typically contains many apps."),
            ("An app is deployed to Docker, while a project runs locally", False, "Incorrect. Deployment applies to the whole project."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "URL Routing",
        "difficulty": "BEGINNER",
        "content": "How do you capture an integer URL path parameter named `article_id` in modern Django `path()`?",
        "code_snippet": "urlpatterns = [\n    path('articles/<...:article_id>/', views.article_detail, name='detail'),\n]",
        "explanation": "Django's `path()` uses path converters. `<int:article_id>` matches one or more decimal digits and converts the captured string directly into an integer before passing it to the view.",
        "options": [
            ("`path('articles/<int:article_id>/', views.article_detail)`", True, "Correct. `<int:name>` is the built-in integer path converter."),
            ("`path('articles/(?P<article_id>\\d+)/', views.article_detail)`", False, "Incorrect. That is the older regex-based re_path() syntax."),
            ("`path('articles/:article_id', views.article_detail)`", False, "Incorrect. Colon-prefixed parameters are Express/React Router syntax, not Django."),
            ("`path('articles/{article_id:int}', views.article_detail)`", False, "Incorrect. OpenAPI/FastAPI syntax, not Django."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "URL Routing",
        "difficulty": "BEGINNER",
        "content": "What is the purpose of the `app_name` attribute in an app's `urls.py`?",
        "code_snippet": "from django.urls import path\nfrom . import views\n\napp_name = 'quizzes'\nurlpatterns = [...]",
        "explanation": "`app_name` defines an application namespace. This allows reverse URL resolution using `quizzes:detail`, preventing naming collisions when multiple apps have views named `detail`.",
        "options": [
            ("Defines the URL namespace for reverse lookups (e.g., `{% url 'quizzes:detail' %}`)", True, "Correct. Namespacing isolates URL pattern names across different apps."),
            ("Registers the app with Django's WSGI server", False, "Incorrect. Apps are registered in INSTALLED_APPS."),
            ("Sets the title of the HTML page", False, "Incorrect. HTML titles are set in templates."),
            ("Creates database tables for the URL routes", False, "Incorrect. URL routes do not create database tables."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Views",
        "difficulty": "BEGINNER",
        "content": "What must every Django view function accept as its first argument and return as its result?",
        "code_snippet": "def my_view(request):\n    return HttpResponse(\"Hello World\")",
        "explanation": "A Django view function must take an `HttpRequest` object as its first argument (conventionally named `request`) and return an `HttpResponse` object (or an exception/subclass like `JsonResponse` or `HttpResponseRedirect`).",
        "options": [
            ("Accepts `HttpRequest` as the first argument and returns an `HttpResponse` object", True, "Correct. Views transform an incoming HttpRequest into an outgoing HttpResponse."),
            ("Accepts `url` and returns a string", False, "Incorrect. Views accept HttpRequest and must return an HttpResponse object, not a raw string."),
            ("Accepts `db_cursor` and returns a dict", False, "Incorrect. Django abstracts cursors through the ORM."),
            ("Accepts no arguments and returns HTML text", False, "Incorrect. Views must accept the request object."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Views",
        "difficulty": "BEGINNER",
        "content": "What does the `render()` shortcut function do in Django views?",
        "code_snippet": "from django.shortcuts import render\n\ndef home(request):\n    return render(request, 'home.html', {'title': 'Home'})",
        "explanation": "`render(request, template_name, context)` loads the specified template, fills it with the context dictionary, renders the resulting HTML string, and returns an `HttpResponse` object with status 200.",
        "options": [
            ("Loads a template, populates it with context, and returns an HttpResponse object", True, "Correct. `render()` is the idiomatic shortcut combining template loading and response creation."),
            ("Compiles the template into React JSX components", False, "Incorrect. Django uses server-side Django Template Engine."),
            ("Saves context data into the SQLite database", False, "Incorrect. render() handles HTTP presentation, not DB storage."),
            ("Redirects the browser to a new URL", False, "Incorrect. That is redirect()."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Templates",
        "difficulty": "BEGINNER",
        "content": "How do you output a variable and execute a template tag in the Django Template Language (DTL)?",
        "code_snippet": "# In template.html:\n<h1>Welcome, {{ user.username }}</h1>\n{% for item in items %}\n    <p>{{ item }}</p>\n{% endfor %}",
        "explanation": "In DTL, variables are surrounded by double curly braces `{{ variable }}`. Template tags (control flow, loops, blocks, loading filters) are surrounded by curly braces with percent signs `{% tag %}`.",
        "options": [
            ("`{{ variable }}` for variables and `{% tag %}` for logic/tags", True, "Correct. `{{ }}` evaluates variables; `{% %}` executes tags like for, if, and block."),
            ("`{% variable %}` for variables and `{{ tag }}` for tags", False, "Incorrect. The syntax is reversed."),
            ("`${variable}` and `<% tag %>`", False, "Incorrect. That is JSP/ES6 template literal syntax."),
            ("`[[ variable ]]` and `(( tag ))`", False, "Incorrect. Not valid Django template syntax."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Templates",
        "difficulty": "BEGINNER",
        "content": "What is the purpose of template inheritance via `{% extends 'base.html' %}` and `{% block content %}`?",
        "code_snippet": "{% extends 'base.html' %}\n\n{% block content %}\n  <h2>Dashboard</h2>\n{% endblock %}",
        "explanation": "Template inheritance allows developers to define a base skeleton template containing shared HTML structure (headers, navbars, footers, scripts) and define named blocks that child templates override.",
        "options": [
            ("Allows child templates to inherit a shared skeleton layout and selectively override specific content blocks", True, "Correct. Promotes DRY (Don't Repeat Yourself) code across all pages."),
            ("Merges multiple HTML files into a single zip archive", False, "Incorrect. It is a server-side rendering pattern."),
            ("Enables server-sent events for real-time updates", False, "Incorrect. Template inheritance is pure HTML templating."),
            ("Automatically generates database models from HTML tags", False, "Incorrect. Templates do not generate database models."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Models",
        "difficulty": "BEGINNER",
        "content": "What must a Django model class inherit from?",
        "code_snippet": "from django.db import models\n\nclass Question(models.Model):\n    content = models.TextField()",
        "explanation": "Every Django model class must inherit from `django.db.models.Model`. This gives the class access to Django's ORM database mapping, validation, and QuerySet APIs.",
        "options": [
            ("`django.db.models.Model`", True, "Correct. models.Model is the foundational base class for all Django ORM models."),
            ("`django.core.DatabaseObject`", False, "Incorrect. No such class exists in Django."),
            ("`django.orm.Table`", False, "Incorrect. Django uses models.Model."),
            ("`object` directly", False, "Incorrect. Standard Python objects lack ORM metadata and database bindings."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Models",
        "difficulty": "BEGINNER",
        "content": "What is the difference between `null=True` and `blank=True` in a Django model field?",
        "code_snippet": "class UserProfile(models.Model):\n    bio = models.TextField(blank=True, default='')\n    birth_date = models.DateField(null=True, blank=True)",
        "explanation": "`null=True` is database-related: it allows the column in the database to store `NULL` values. `blank=True` is validation-related: it allows the field to be left empty in forms and the Django admin.",
        "options": [
            ("`null=True` sets database column to NULL; `blank=True` allows empty values during form validation", True, "Correct. null is database-level; blank is application/form validation-level."),
            ("`blank=True` is database-level; `null=True` is form validation", False, "Incorrect. The roles are reversed."),
            ("They are completely identical and interchangeable", False, "Incorrect. One is DB constraint, the other is form validation rule."),
            ("`null=True` is for strings only, `blank=True` is for numbers", False, "Incorrect. For string fields, Django convention recommends avoiding null=True and using default='' with blank=True."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django ORM",
        "difficulty": "BEGINNER",
        "content": "Are Django QuerySets evaluated eagerly or lazily?",
        "code_snippet": "questions = Question.objects.filter(is_active=True)\n# No database query has executed yet!",
        "explanation": "Django QuerySets are lazy. Creating a QuerySet does not touch the database. The SQL query is only executed when the QuerySet is evaluated (e.g., iterating with `for`, slicing with a step, calling `len()`, `list()`, or `bool()`).",
        "options": [
            ("Lazily: queries are not sent to the database until the QuerySet is iterated or evaluated", True, "Correct. Lazy evaluation allows chaining filters without executing premature SQL queries."),
            ("Eagerly: queries execute instantly on every .filter() call", False, "Incorrect. filter() returns an un-evaluated QuerySet."),
            ("Only during application startup", False, "Incorrect. Queries run dynamically at runtime."),
            ("Only when running in production mode", False, "Incorrect. Laziness is core ORM behavior in all environments."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django ORM",
        "difficulty": "BEGINNER",
        "content": "What is the difference between `Question.objects.get(id=1)` and `Question.objects.filter(id=1)`?",
        "code_snippet": "q_get = Question.objects.get(id=1)\nq_filter = Question.objects.filter(id=1)",
        "explanation": "`.get()` returns a single model instance, raising `DoesNotExist` if not found or `MultipleObjectsReturned` if more than one match exists. `.filter()` always returns a `QuerySet` (collection) which may contain 0, 1, or many objects without raising an exception.",
        "options": [
            ("`.get()` returns a single object and raises an exception if not found; `.filter()` returns a QuerySet", True, "Correct. get() expects exactly one match; filter() returns a list-like collection."),
            ("`.filter()` raises DoesNotExist; `.get()` returns an empty list", False, "Incorrect. filter() returns an empty QuerySet without error."),
            ("`.get()` writes to the database; `.filter()` reads from the database", False, "Incorrect. Both are read operations."),
            ("There is no difference in return type", False, "Incorrect. get() returns an instance; filter() returns a QuerySet."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Migrations",
        "difficulty": "BEGINNER",
        "content": "What is the difference between `makemigrations` and `migrate` in Django?",
        "code_snippet": "# python manage.py makemigrations\n# python manage.py migrate",
        "explanation": "`makemigrations` inspects changes made to your `models.py` files and generates new migration Python scripts. `migrate` executes those migration files against the database, creating or altering the actual SQL database tables.",
        "options": [
            ("`makemigrations` creates migration files from model changes; `migrate` applies them to the database", True, "Correct. makemigrations prepares the instructions; migrate executes the SQL schema changes."),
            ("`migrate` creates migration files; `makemigrations` applies them", False, "Incorrect. The command responsibilities are reversed."),
            ("`makemigrations` runs on SQLite; `migrate` runs only on PostgreSQL", False, "Incorrect. Both commands apply to any configured database engine."),
            ("Both commands apply schema changes directly to the database", False, "Incorrect. makemigrations only writes Python files."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django Admin",
        "difficulty": "BEGINNER",
        "content": "How do you register a custom model `Question` so it appears in the Django Admin interface?",
        "code_snippet": "from django.contrib import admin\nfrom .models import Question\n\n# How to register Question?",
        "explanation": "You can register a model using `admin.site.register(Question)` or using the decorator syntax `@admin.register(Question)` on a custom `ModelAdmin` class in `admin.py`.",
        "options": [
            ("`admin.site.register(Question)` or `@admin.register(Question)`", True, "Correct. Both register the model with the default AdminSite."),
            ("Add `is_admin = True` in models.py", False, "Incorrect. Models do not configure admin registration inside models.py."),
            ("Add 'django.admin.Question' to INSTALLED_APPS", False, "Incorrect. Only app config modules belong in INSTALLED_APPS."),
            ("Create an admin.json file in the root directory", False, "Incorrect. Admin is configured in Python code."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Forms",
        "difficulty": "BEGINNER",
        "content": "What method must you call on a Django form before accessing `form.cleaned_data`?",
        "code_snippet": "form = ContactForm(request.POST)\nif form.is_valid():\n    email = form.cleaned_data['email']",
        "explanation": "You must call `form.is_valid()`. This runs form validation across all fields and populates the `form.cleaned_data` dictionary with normalized Python data. Accessing `cleaned_data` before validation raises an AttributeError.",
        "options": [
            ("`form.is_valid()`", True, "Correct. is_valid() triggers full_clean() which validates inputs and builds cleaned_data."),
            ("`form.validate()`", False, "Incorrect. The method name in Django is is_valid()."),
            ("`form.clean()` directly", False, "Incorrect. Call is_valid(), which internally invokes clean()."),
            ("`form.save()`", False, "Incorrect. form.save() is for ModelForms, and only after validation."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "ModelForms",
        "difficulty": "BEGINNER",
        "content": "What is a `ModelForm` in Django and how does it reduce boilerplate code?",
        "code_snippet": "class QuestionForm(forms.ModelForm):\n    class Meta:\n        model = Question\n        fields = ['content', 'difficulty', 'explanation']",
        "explanation": "A `ModelForm` automatically generates HTML form fields, validation logic, and a `.save()` method directly from a specified Django model, eliminating redundant form declarations.",
        "options": [
            ("A form class that automatically generates form fields and validation directly from a Model", True, "Correct. It maps model fields to appropriate form widgets and handles saving to DB."),
            ("A form that writes directly to the SQLite file bypassing Django views", False, "Incorrect. Views still handle HTTP validation and saving."),
            ("A form designed exclusively for the Django Admin", False, "Incorrect. ModelForms are used everywhere in web apps."),
            ("A form that converts React components into SQL queries", False, "Incorrect. It is a server-side Django form construct."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Static Files",
        "difficulty": "BEGINNER",
        "content": "Which template tag is required before referencing static assets like CSS and JS in Django templates?",
        "code_snippet": "{% load static %}\n<link rel=\"stylesheet\" href=\"{% static 'css/style.css' %}\">",
        "explanation": "You must load the static tag library at the top of the template using `{% load static %}` before using the `{% static 'path' %}` tag.",
        "options": [
            ("`{% load static %}`", True, "Correct. `{% load static %}` imports the static URL resolution tag into the template context."),
            ("`{% import static %}`", False, "Incorrect. The tag keyword is load, not import."),
            ("`{% static_files %}`", False, "Incorrect. No such tag exists."),
            ("`{% include 'static' %}`", False, "Incorrect. include is for rendering sub-templates."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Media Files",
        "difficulty": "BEGINNER",
        "content": "What is the difference between `STATIC_ROOT` and `MEDIA_ROOT` in Django?",
        "code_snippet": "# settings.py\nSTATIC_ROOT = BASE_DIR / 'staticfiles'\nMEDIA_ROOT = BASE_DIR / 'media'",
        "explanation": "`STATIC_ROOT` is the directory where collected static files (CSS, JS, site logos) are gathered by `collectstatic` for production deployment. `MEDIA_ROOT` is the directory where user-uploaded files (avatars, attachments, media) are stored at runtime.",
        "options": [
            ("`STATIC_ROOT` stores collected site assets (CSS/JS); `MEDIA_ROOT` stores user-uploaded files at runtime", True, "Correct. Static files are developer-authored; media files are dynamic user uploads."),
            ("`STATIC_ROOT` is for production; `MEDIA_ROOT` is for local development only", False, "Incorrect. Both exist in both environments."),
            ("`MEDIA_ROOT` stores video and audio only", False, "Incorrect. MEDIA_ROOT stores any user-uploaded files (PDFs, images, docs)."),
            ("They are interchangeable aliases for the same directory", False, "Incorrect. Mixing them causes security and deployment issues."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "URL Routing",
        "difficulty": "BEGINNER",
        "content": "What does the `name` argument in a `path()` function call enable?",
        "code_snippet": "path('quiz/config/', views.quiz_config, name='config')",
        "explanation": "The `name` parameter allows reverse URL resolution using `reverse('quizzes:config')` in Python or `{% url 'quizzes:config' %}` in templates, decoupling view code from hardcoded URL paths.",
        "options": [
            ("Enables reverse URL resolution in templates and Python code without hardcoding URLs", True, "Correct. If URL paths change later, reversed names continue working without breaking links."),
            ("Sets the browser window title", False, "Incorrect. Browser title is determined by HTML <title>."),
            ("Sets the HTTP cookie session name", False, "Incorrect. Cookie session name is configured in settings.py."),
            ("Defines the database table name", False, "Incorrect. Database table names are defined in model Meta db_table."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django ORM",
        "difficulty": "BEGINNER",
        "content": "How do you write an `OR` condition using Django ORM?",
        "code_snippet": "from django.db.models import Q\n# Find questions where difficulty is 'BEGINNER' OR topic_id is 5",
        "explanation": "Django ORM uses `Q` objects combined with the pipe operator `|` to represent SQL `OR` clauses: `Question.objects.filter(Q(difficulty='BEGINNER') | Q(topic_id=5))`.",
        "options": [
            ("Using `Q` objects combined with the pipe operator `|`: `filter(Q(...) | Q(...))`", True, "Correct. Q objects allow complex logical queries including OR (`|`), AND (`&`), and NOT (`~`)."),
            ("`Question.objects.filter(difficulty='BEGINNER').or_filter(topic_id=5)`", False, "Incorrect. There is no .or_filter() method in Django QuerySet."),
            ("Passing `operator='OR'` as a keyword argument", False, "Incorrect. Standard filter kwargs are always joined with AND."),
            ("Using SQL UNION syntax with two raw strings", False, "Incorrect. Q objects are the native, safe ORM mechanism."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Views",
        "difficulty": "BEGINNER",
        "content": "What decorator restricts a Django view function to only accept `POST` requests?",
        "code_snippet": "from django.views.decorators.http import require_POST\n\n@require_POST\ndef submit_answer(request):\n    ...",
        "explanation": "The `@require_POST` decorator ensures that the view only accepts HTTP `POST` requests. If a `GET` or other method is used, Django automatically returns an `HttpResponseNotAllowed` (status code 405).",
        "options": [
            ("`@require_POST`", True, "Correct. Automatically returns HTTP 405 Method Not Allowed on non-POST requests."),
            ("`@post_only`", False, "Incorrect. No such decorator exists in Django."),
            ("`@http_method('POST')`", False, "Incorrect. Django provides @require_http_methods(['POST'])."),
            ("`@csrf_protect`", False, "Incorrect. @csrf_protect enforces CSRF tokens, not HTTP method restrictions."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django Architecture",
        "difficulty": "BEGINNER",
        "content": "What file in a Django project serves as the primary WSGI gateway entry point for production servers?",
        "code_snippet": "# mysite/\n# ├── wsgi.py\n# └── settings.py",
        "explanation": "`wsgi.py` exposes the WSGI callable named `application` used by production web servers (such as Gunicorn, uWSGI, Nginx) to forward HTTP requests to Django.",
        "options": [
            ("`wsgi.py`", True, "Correct. wsgi.py exposes `application = get_wsgi_application()`."),
            ("`server.js`", False, "Incorrect. Node.js file, not Django."),
            ("`manage.py`", False, "Incorrect. manage.py is a CLI utility for administration tasks and local runserver."),
            ("`urls.py`", False, "Incorrect. urls.py defines URL routing."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django Admin",
        "difficulty": "BEGINNER",
        "content": "How do you create an administrator account to log into `/admin/` in a new Django project?",
        "code_snippet": "# CLI command to generate admin user",
        "explanation": "The management command `python manage.py createsuperuser` prompts for username, email, and password to create a User with `is_staff=True` and `is_superuser=True`.",
        "options": [
            ("`python manage.py createsuperuser`", True, "Correct. Generates a root administrative user with all permissions."),
            ("`python manage.py make_admin`", False, "Incorrect. Command does not exist."),
            ("Insert a row directly into the auth_user table using raw SQL", False, "Incorrect. Password hashing wouldn't be computed properly."),
            ("Register an account on the website with username 'admin'", False, "Incorrect. Standard registration does not grant is_staff privileges."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Forms",
        "difficulty": "BEGINNER",
        "content": "Why must every Django HTML form that uses `method='POST'` include `{% csrf_token %}`?",
        "code_snippet": "<form method=\"POST\">\n  {% csrf_token %}\n  <button type=\"submit\">Submit</button>\n</form>",
        "explanation": "`{% csrf_token %}` outputs a hidden input containing a secure Cross-Site Request Forgery token. Django's `CsrfViewMiddleware` verifies this token on POST requests to protect users against unauthorized malicious form submissions from third-party sites.",
        "options": [
            ("Protects against Cross-Site Request Forgery (CSRF) attacks by ensuring requests originate from your site", True, "Correct. Django rejects POST submissions without a valid CSRF token with a 403 Forbidden."),
            ("Encrypts the password before sending it across HTTP", False, "Incorrect. HTTPS / TLS handles transport layer encryption."),
            ("Stores the form data in Redis cache", False, "Incorrect. It is a security verification mechanism."),
            ("Validates that form inputs are not empty", False, "Incorrect. Form validation is performed in forms.py."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Models",
        "difficulty": "BEGINNER",
        "content": "What does `on_delete=models.CASCADE` do on a `ForeignKey` in Django?",
        "code_snippet": "class Topic(models.Model):\n    category = models.ForeignKey(Category, on_delete=models.CASCADE)",
        "explanation": "`models.CASCADE` specifies that when the referenced parent object (Category) is deleted, all related child objects (Topics) that point to it are automatically deleted as well.",
        "options": [
            ("Deletes all related child objects automatically when the parent object is deleted", True, "Correct. Standard relational database cascading delete behavior."),
            ("Prevents the parent object from ever being deleted", False, "Incorrect. That is models.PROTECT or models.RESTRICT."),
            ("Sets the foreign key to NULL in child rows", False, "Incorrect. That is models.SET_NULL."),
            ("Creates an automatic database backup before deletion", False, "Incorrect. Django does not auto-backup before deletions."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Templates",
        "difficulty": "BEGINNER",
        "content": "What filter formats a floating point score into a percentage or rounds it in Django templates?",
        "code_snippet": "{{ attempt.score|floatformat:1 }}%",
        "explanation": "The `floatformat:1` filter formats a floating point number to one decimal place (e.g., 85.666 becomes 85.7).",
        "options": [
            ("`floatformat` filter (e.g., `{{ val|floatformat:1 }}`)", True, "Correct. Rounds floating point numbers to the specified decimal precision."),
            ("`round` filter", False, "Incorrect. DTL uses floatformat, not round."),
            ("`number_format` filter", False, "Incorrect. That is PHP/Twig."),
            ("`to_percent` filter", False, "Incorrect. No built-in to_percent filter exists in DTL."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django ORM",
        "difficulty": "BEGINNER",
        "content": "How do you sort a QuerySet in descending order by `created_at` in Django?",
        "code_snippet": "questions = Question.objects.order_by('-created_at')",
        "explanation": "Prefixing the field name with a minus sign `-` in `.order_by('-created_at')` orders the QuerySet in descending order (newest first).",
        "options": [
            ("Prefix the field name with a minus sign: `.order_by('-created_at')`", True, "Correct. `-` specifies DESC, while no prefix specifies ASC in SQL ORDER BY."),
            ("Pass `desc=True`: `.order_by('created_at', desc=True)`", False, "Incorrect. order_by does not take a desc keyword argument."),
            ("Call `.order_by('created_at').reverse()` only", False, "Incorrect. While .reverse() exists, '-field' is the standard idiomatic way."),
            ("Call `.sort(reverse=True)`", False, "Incorrect. QuerySets do not have a .sort() method."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django ORM",
        "difficulty": "BEGINNER",
        "content": "What method counts records in a QuerySet most efficiently in Django?",
        "code_snippet": "# Best way to count active questions:\ncount = Question.objects.filter(is_active=True).count()",
        "explanation": "`.count()` generates a `SELECT COUNT(*)` SQL query directly in the database, returning only the count integer without loading model instances into Python memory. Calling `len(qs)` fetches all rows into memory first.",
        "options": [
            ("`.count()` - executes SQL `SELECT COUNT(*)` directly in the database", True, "Correct. Far more efficient than loading instances into Python memory."),
            ("`len(Question.objects.all())`", False, "Incorrect. len() evaluates the QuerySet, loading every single row into memory."),
            ("`Question.objects.all().length`", False, "Incorrect. QuerySet has no length property."),
            ("`sum(1 for _ in Question.objects.all())`", False, "Incorrect. Inefficient iteration over all rows in Python."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Views",
        "difficulty": "BEGINNER",
        "content": "What shortcut function retrieves an object from the database or raises a 404 Http404 exception if not found?",
        "code_snippet": "from django.shortcuts import get_object_or_404\n\nquestion = get_object_or_404(Question, id=question_id)",
        "explanation": "`get_object_or_404(Model, **kwargs)` calls `get()` on the model or queryset. If the object does not exist, it automatically raises `django.http.Http404` instead of `DoesNotExist`, cleanly rendering a 404 page.",
        "options": [
            ("`get_object_or_404()`", True, "Correct. Standard idiomatic Django shortcut for safe object retrieval in views."),
            ("`find_or_404()`", False, "Incorrect. No such function exists in Django."),
            ("`Model.objects.get_or_404()`", False, "Incorrect. It is a shortcut in django.shortcuts, not a manager method."),
            ("`safe_get()`", False, "Incorrect. safe_get is not a Django standard function."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django Admin",
        "difficulty": "BEGINNER",
        "content": "What `ModelAdmin` attribute specifies the columns displayed on the change list page?",
        "code_snippet": "class QuestionAdmin(admin.ModelAdmin):\n    list_display = ('content', 'difficulty', 'is_active', 'created_at')",
        "explanation": "`list_display` is a tuple or list of field names that defines which columns are shown in the Django Admin change list table for that model.",
        "options": [
            ("`list_display`", True, "Correct. Controls table column headers and values in the admin list view."),
            ("`columns`", False, "Incorrect. Django admin uses list_display."),
            ("`table_fields`", False, "Incorrect. Invalid attribute name."),
            ("`display_fields`", False, "Incorrect. The standardized name is list_display."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django Admin",
        "difficulty": "BEGINNER",
        "content": "What `ModelAdmin` attribute adds a sidebar filter for easy filtering by category or difficulty?",
        "code_snippet": "class QuestionAdmin(admin.ModelAdmin):\n    list_filter = ('difficulty', 'is_active', 'topic__category')",
        "explanation": "`list_filter` activates the right-hand sidebar filter in Django Admin, letting administrators filter records by field values or relationships.",
        "options": [
            ("`list_filter`", True, "Correct. Generates the filtering sidebar on the right of the admin list page."),
            ("`filters`", False, "Incorrect. Attribute name is list_filter."),
            ("`sidebar_filters`", False, "Incorrect. Invalid attribute name."),
            ("`search_fields`", False, "Incorrect. search_fields creates the text search box, not sidebar filters."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django Admin",
        "difficulty": "BEGINNER",
        "content": "How do you display related child objects (like `AnswerOptions`) directly inside the parent `Question` edit page in Django Admin?",
        "code_snippet": "class AnswerOptionInline(admin.TabularInline):\n    model = AnswerOption\n\nclass QuestionAdmin(admin.ModelAdmin):\n    inlines = [AnswerOptionInline]",
        "explanation": "Django provides `InlineModelAdmin` (`TabularInline` and `StackedInline`). Adding an inline to `inlines = [AnswerOptionInline]` allows editing child foreign-key records directly on the parent form.",
        "options": [
            ("Using `TabularInline` or `StackedInline` registered in the parent's `inlines` attribute", True, "Correct. Enables editing multiple child foreign key rows directly on the parent admin page."),
            ("Adding `show_children = True` in models.py", False, "Incorrect. Admin UI is configured in admin.py."),
            ("Writing custom JavaScript to fetch child rows", False, "Incorrect. Django Admin supports inlines natively."),
            ("It is not supported in Django without third-party packages", False, "Incorrect. Inlines are built into Django's core admin."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Migrations",
        "difficulty": "BEGINNER",
        "content": "Where are migration operations recorded in the database to track which migrations have already been applied?",
        "code_snippet": "SELECT * FROM django_migrations;",
        "explanation": "Django maintains a special internal database table named `django_migrations` that records every app name, migration name, and the timestamp it was applied.",
        "options": [
            ("The `django_migrations` database table", True, "Correct. Django queries this table to determine unapplied migrations on `python manage.py migrate`."),
            ("Inside `settings.py` file", False, "Incorrect. Settings does not track database migration history."),
            ("In browser cookies", False, "Incorrect. Migrations are strictly server/database-side."),
            ("In the git commit log", False, "Incorrect. Database state is tracked in django_migrations table."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django Architecture",
        "difficulty": "BEGINNER",
        "content": "What middleware in Django is responsible for populating `request.user` on incoming HTTP requests?",
        "code_snippet": "MIDDLEWARE = [\n    ...\n    'django.contrib.auth.middleware.AuthenticationMiddleware',\n]",
        "explanation": "`AuthenticationMiddleware` associates users with requests using sessions. It inspects session data and attaches the `User` object (or `AnonymousUser`) to `request.user`.",
        "options": [
            ("`django.contrib.auth.middleware.AuthenticationMiddleware`", True, "Correct. Sets request.user based on active session cookies."),
            ("`django.middleware.security.SecurityMiddleware`", False, "Incorrect. SecurityMiddleware handles SSL redirects, HSTS, and X-Content-Type headers."),
            ("`django.contrib.sessions.middleware.SessionMiddleware`", False, "Incorrect. SessionMiddleware sets request.session; AuthenticationMiddleware sets request.user."),
            ("`django.middleware.common.CommonMiddleware`", False, "Incorrect. CommonMiddleware handles URL appending slashes and user-agents."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Static Files",
        "difficulty": "BEGINNER",
        "content": "What management command collects all static files from apps into `STATIC_ROOT` for production deployment?",
        "code_snippet": "# Preparing static assets for Nginx/WhiteNoise",
        "explanation": "`python manage.py collectstatic` scans all installed apps and directories in `STATICFILES_DIRS` and copies static files into the single directory defined by `STATIC_ROOT`.",
        "options": [
            ("`python manage.py collectstatic`", True, "Correct. Gathers all static files for production serving."),
            ("`python manage.py build_static`", False, "Incorrect. Command does not exist in standard Django."),
            ("`python manage.py publish`", False, "Incorrect. Not a Django command."),
            ("`npm run build` only", False, "Incorrect. collectstatic is Django's native static collection command."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Forms",
        "difficulty": "BEGINNER",
        "content": "How do you add custom CSS classes (e.g. Bootstrap `'form-control'`) to a Django Form field widget?",
        "code_snippet": "username = forms.CharField(\n    widget=forms.TextInput(attrs={'class': 'form-control'})\n)",
        "explanation": "You pass an `attrs` dictionary containing HTML attributes (including `{'class': 'form-control'}`) to the widget constructor in the form field definition.",
        "options": [
            ("Pass `attrs={'class': 'form-control'}` into the field's `widget` argument", True, "Correct. Renders HTML input with `class=\"form-control\"`."),
            ("Add `css_class = 'form-control'` on the form class", False, "Incorrect. Attributes must be attached to the field widget."),
            ("Write an inline style tag in HTML", False, "Incorrect. Not the Pythonic way to configure widgets."),
            ("Django forms cannot render CSS classes", False, "Incorrect. Django form widgets are fully customizable."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Django ORM",
        "difficulty": "BEGINNER",
        "content": "What does the `__icontains` lookup do in a Django ORM query?",
        "code_snippet": "questions = Question.objects.filter(content__icontains='decorator')",
        "explanation": "`__icontains` performs a case-insensitive containment test, translating to SQL `ILIKE '%decorator%'` (Postgres) or `LIKE '%decorator%'` (SQLite case-insensitive). Without the `i`, `__contains` is case-sensitive.",
        "options": [
            ("Case-insensitive substring match (SQL `ILIKE` or `LIKE`)", True, "Correct. The 'i' prefix denotes case-insensitivity across Django field lookups."),
            ("Case-sensitive exact match", False, "Incorrect. Exact match is `__exact`."),
            ("Index containment for integer arrays", False, "Incorrect. It is a string search lookup."),
            ("Identity comparison in Python RAM", False, "Incorrect. It executes in the database SQL engine."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Templates",
        "difficulty": "BEGINNER",
        "content": "What built-in template tag outputs the current year or formats dates in Django?",
        "code_snippet": "{{ attempt.started_at|date:\"M d, Y H:i\" }}",
        "explanation": "The `date` filter formats a date object according to the given format string (e.g. `\"M d, Y H:i\"` prints 'Oct 30, 2026 23:00'). You can also use `{% now 'Y' %}` for the current year.",
        "options": [
            ("The `date` filter (e.g. `{{ var|date:\"Y-m-d\" }}`) and `{% now \"Y\" %}` tag", True, "Correct. Provides comprehensive PHP-style date formatting in DTL."),
            ("The `datetime` tag", False, "Incorrect. Filter name is date."),
            ("The `strftime` filter", False, "Incorrect. DTL uses date filter, not strftime directly."),
            ("The `timestamp` tag", False, "Incorrect. No such built-in tag."),
        ]
    },
    {
        "category": "Django Fundamentals",
        "topic": "Media Files",
        "difficulty": "BEGINNER",
        "content": "What model field type is used in Django to store and validate uploaded images?",
        "code_snippet": "class Profile(models.Model):\n    avatar = models.ImageField(upload_to='avatars/', blank=True)",
        "explanation": "`models.ImageField` inherits from `FileField` and adds image validation using the Pillow library, ensuring that the uploaded file is a valid image before saving.",
        "options": [
            ("`models.ImageField` (requires Pillow library)", True, "Correct. Validates image dimensions, formats, and integrity."),
            ("`models.PictureField`", False, "Incorrect. No PictureField exists in Django."),
            ("`models.BinaryImage`", False, "Incorrect. BinaryField stores raw bytes, not validated image uploads."),
            ("`models.BlobField`", False, "Incorrect. Django does not have a BlobField."),
        ]
    }
]

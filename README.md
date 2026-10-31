# Python & Django Interview Master

**Python & Django Interview Master** is a production-grade technical interview preparation platform architected with **Django 5 (MVT)** and **SQLite3**, featuring **240+ verified interview questions** spanning beginner, intermediate, and advanced tiers across core Python and Django frameworks.

---

## 🚀 Key Highlights & Architecture

- **Clean Django MVT Architecture**: Decoupled into four domain-focused apps:
  - `accounts`: User authentication, registration, profiles with experience levels, target roles, bio, and login streaks.
  - `questions`: Question bank, categories, topics, difficulty tiers, code snippet formatting, and administrative management.
  - `quizzes`: Quiz generation engine, stateful attempt tracking, real-time AJAX answer autosaving, timer sync, and atomic server-side grading.
  - `progress`: Topic accuracy aggregation, Chart.js radar & timeline feeds, weakest-topic heuristics, and syllabus study planner.
- **240 Production-Ready Questions**: Exactly 40 questions per tier across 6 distinct categories with code snippets, 4 options each, and detailed architectural rationales.
- **4 Distinct Quiz Modes**:
  1. **Practice Mode**: Untimed, instant answer reveal with in-depth technical explanations and live retries.
  2. **Exam Mode**: Strict countdown timer, answers hidden until completion, auto-submission on timeout, and rigorous server-side evaluation.
  3. **Topic Practice**: Laser-focused practice filtered by single topic, difficulty, and question count.
  4. **Full Mock Interview**: Randomized realistic technical interview balancing Python and Django fundamentals to advanced concepts.
- **Server-Authoritative Evaluation**:
  - Scores are calculated strictly on the backend inside atomic database transactions (`transaction.atomic()`).
  - Robust Insecure Direct Object Reference (IDOR) protection: Attempts are verified against `request.user`.
  - Double-submission guards: Submitted attempts are locked and cannot be re-evaluated.
- **Modern Responsive UI**:
  - Bootstrap 5.3.3 + Bootstrap Icons.
  - Light/Dark mode with dynamic CSS custom properties and client-side persistence.
  - Interactive Chart.js analytics for score progression, Python vs. Django competency, and granular topic accuracy.
  - Question jump palette, status badges (Answered, Unanswered, Flagged for Review), and sticky countdown timers.

---

## 📊 Question Bank Distribution (240 Questions)

| Category | Difficulty | Questions | Key Topics Covered |
| :--- | :--- | :---: | :--- |
| **Python Fundamentals** | Beginner | 40 | Variables, Mutability, Strings, Slicing, Lists, Tuples, Sets, Dictionaries, Loops, Comprehensions, Functions, Lambdas, Exception Handling, File I/O, Imports |
| **Python Intermediate** | Intermediate | 40 | OOP, Inheritance, Polymorphism, Encapsulation, Decorators, Generators, Iterators, Context Managers, `*args` / `**kwargs`, Copy semantics, Memory allocation, Ref counts, GC |
| **Python Advanced** | Advanced | 40 | GIL internals, Multithreading vs Multiprocessing, Asyncio event loops, Metaclasses, Descriptors, MRO (C3 Linearization), Bytecode, Dunder methods, Memory optimization, Weakrefs |
| **Django Fundamentals** | Beginner | 40 | MVT Architecture, Project vs App, URL routing, View functions, Templates, Models, Migrations, Django Admin, Forms, ModelForms, Staticfiles, Settings |
| **Django Intermediate** | Intermediate | 40 | QuerySets, `select_related`, `prefetch_related`, Custom Managers, Middleware flow, Signals, Class-Based Views, Authentication & Authorization, Sessions, Pagination, Model validation |
| **Django Advanced** | Advanced | 40 | Request lifecycle internals, Database transactions & `select_for_update()`, Caching strategies (Redis/Memcached), Celery distributed locks, Security (CSRF, XSS, SQLi), ASGI, Performance profiling |
| **Total** | | **240** | **960 curated multiple-choice options with explanations** |

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, Django 5.1.15
- **Database**: SQLite3 (with indexed ForeignKeys and composite indexes)
- **Frontend**: HTML5, Django Templates, Bootstrap 5.3.3, Bootstrap Icons, Chart.js 4.4.2
- **Static Assets**: WhiteNoise middleware for standalone production asset delivery
- **Testing**: Django `TestCase` with in-memory SQLite runner (15 automated unit & integration tests)

---

## 💻 Local Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.11 or higher installed on your system:
```bash
python3 --version
```

### 2. Clone Repository & Setup Virtual Environment
```bash
git clone <repository-url>
cd python-django-interview-master

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Seed Questions & Demo User
Run the custom idempotent seeding command:
```bash
python manage.py seed_questions
```
This seeds:
- 2 Categories (`Python`, `Django`)
- 95+ Curated Topics
- 240 Multiple Choice Questions with 960 options and technical explanations
- 1 Pre-configured Demo User with past quiz history for immediate dashboard visualization:
  - **Username**: `demo_developer`
  - **Password**: `Password123!`

### 6. Create Superuser (Optional - For Django Admin)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver 0.0.0.0:3000
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧪 Running the Test Suite

Execute the automated test suite covering models, services, quiz flows, and API endpoints:
```bash
python manage.py test
```
All 15 tests verify:
- User profile creation and streak calculations
- Question categorization, topic filtering, and answer validation
- Quiz attempt lifecycle (start, autosave answer, atomic submission)
- Server-side score computation and pass/fail thresholds
- IDOR access boundaries and double-submit prevention

---

## 📂 Project Directory Structure

```text
├── accounts/                  # User auth, profile, and streak models & views
│   ├── models.py              # UserProfile model with streak & career tracking
│   ├── views.py               # Login, register, profile, password change
│   └── tests.py               # Authentication and profile unit tests
├── questions/                 # Question bank, categories, topics, & admin
│   ├── models.py              # Category, Topic, Question, AnswerOption
│   ├── fixtures_data/         # 240 Curated questions across 6 Python & Django tiers
│   ├── management/commands/   # seed_questions management command
│   └── tests.py               # Question bank unit tests
├── quizzes/                   # Core quiz engine
│   ├── models.py              # Quiz, QuizAttempt, UserAnswer
│   ├── services.py            # Atomic attempt generator, server-side grading
│   ├── views.py               # Config, start, take, autosave API, submit, review
│   └── tests.py               # Quiz lifecycle and grading unit tests
├── progress/                  # Dashboard and analytics service
│   ├── services.py            # Metric aggregation, Chart.js dataset generation
│   └── views.py               # Dashboard and syllabus progress views
├── templates/                 # Modular Django HTML5 templates
│   ├── base.html              # Core layout with theme toggle & navigation
│   ├── dashboard/             # Dashboard, landing, and syllabus templates
│   ├── accounts/              # Auth forms and profile management
│   ├── questions/             # Question explorer and detail pages
│   └── quizzes/               # Quiz configuration, taking room, and results review
├── static/                    # Custom CSS & JS assets
│   ├── css/custom.css         # Dark/light theme styles, code formatting, badges
│   ├── js/theme.js            # Theme switcher with localStorage memory
│   └── js/quiz.js             # Timer, autosave AJAX, jump palette, practice reveal
├── config/                    # Django project configuration (settings, urls, wsgi)
├── manage.py                  # Django CLI management script
├── requirements.txt           # Project dependencies
└── README.md                  # Comprehensive documentation
```

---

## 🔒 Security & Best Practices

1. **Server-Side Grading**: The frontend never calculates scores or transmits final marks; every question is resolved against database records.
2. **Access Control**: Users can only interact with or review quiz attempts linked directly to their user ID.
3. **CSRF Protection**: All form submissions and asynchronous AJAX endpoints require valid CSRF tokens.
4. **Password Hashing**: Built-in PBKDF2 with SHA-256 password hashing.
5. **Database Indexing**: Indexed foreign keys and lookup fields (`category`, `difficulty`, `is_active`) ensure sub-millisecond query performance on large question banks.

---

## 📜 License
Apache-2.0 License.

# Contributing to AI Voice IT Helpdesk Agent

Thank you for your interest in contributing to the **AI Voice IT Helpdesk Agent** repository! We welcome contributions from developers, technical writers, and AI enthusiasts.

---

## Code of Conduct

We expect all contributors to adhere to polite, collaborative, and inclusive communication. Please treat everyone with respect.

---

## How to Get Started

### 1. Fork and Clone the Repository

```bash
# Clone your fork (or main repository)
git clone https://github.com/<your-username>/AI-Voice-IT-Agent.git
cd AI-Voice-IT-Agent
```

### 2. Set Up Environment

Create a clean virtual environment and install development dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` for local testing:

```bash
cp .env.example .env
```

### 3. Initialize Local Test Database

```bash
python3 -m backend.database.init_db
```

---

## Development Workflow

### Creating a Feature Branch

Always create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
# or for bugfixes
git checkout -b fix/issue-description
```

### Running Tests

Before submitting a Pull Request, verify that all automated tests pass:

```bash
pytest -v
```

### Code Style Guidelines

- **Python Standard**: Follow PEP 8 style conventions.
- **Type Annotations**: Use Python 3.10+ type hints (`str | None`, `list[dict]`, etc.).
- **Async Code**: Ensure async handlers use `async def` and non-blocking database queries via SQLAlchemy 2.0 Async (`AsyncSession`).
- **Docstrings**: Maintain docstrings for API route handlers and service layer functions.

---

## Submitting a Pull Request (PR)

1. Commit your changes with descriptive commit messages:
   ```bash
   git commit -m "feat(software): add validation for multi-software approval rules"
   ```
2. Push your branch to your GitHub fork:
   ```bash
   git push origin feature/your-feature-name
   ```
3. Open a Pull Request on GitHub. Fill out the PR template with details on what was changed, how it was tested, and any linked issues.

---

## Reporting Issues

If you encounter a bug or have a feature request:
- Check existing [GitHub Issues](https://github.com/your-username/AI-Voice-IT-Agent/issues) to avoid duplicates.
- Open a new issue using our **Bug Report** or **Feature Request** template.

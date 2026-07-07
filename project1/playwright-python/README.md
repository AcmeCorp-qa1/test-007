# Playwright Python Project

## Project Structure
```
playwright_project/
│
├── conftest.py              # Fixtures (browser, context, page)
├── pytest.ini               # pytest configuration
├── requirements.txt         # Dependencies
│
├── pages/                   # Page Object Models
│   ├── base_page.py         # Base class for all pages
│   └── home_page.py         # Home page object
│
├── tests/                   # Test files
│   ├── test_home_page.py    # Home page tests
│   └── test_cross_browser.py# Cross browser tests
│
├── utils/                   # Helpers (add as needed)
└── reports/                 # HTML reports + screenshots
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install browsers
```bash
playwright install
```

---

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific file
```bash
pytest tests/test_home_page.py
```

### Run in headless mode
```bash
pytest --headless
```

### Run on specific browser
```bash
pytest --browser firefox
pytest --browser webkit
pytest --browser chromium
```

### Run in parallel
```bash
pytest -n 4          # 4 workers
pytest -n auto       # auto detect CPU cores
```

### Run cross browser tests
```bash
pytest tests/test_cross_browser.py
```

### Run all browsers in parallel
```bash
pytest --browser chromium --browser firefox --browser webkit -n auto
```

### Generate HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

---

## Fixtures Available (conftest.py)

| Fixture | Scope | Use For |
|---|---|---|
| `browser_instance` | session | Shared browser |
| `context` | function | Isolated per test |
| `page` | function | Fresh page per test |
| `cross_browser_page` | function | Cross browser testing |
| `base_url` | session | Base URL |

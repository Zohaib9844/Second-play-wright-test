# Playwright + API Hybrid Test Framework

This repository is a practical QA automation project built around **Playwright (Python)** with a hybrid strategy:

- **API-first setup** for fast and reliable test data creation.
- **UI validation** for real end-user behavior checks.
- **Reusable fixtures + Page Object Model (POM)** to keep tests maintainable.

The goal of this project is to validate key Automation Exercise workflows end-to-end while keeping execution stable and scalable.

---

## What I built (tasks completed)

### 1) Foundation and project structure
- Set up a clean test automation structure with separate folders for:
  - `pages/` (UI page objects)
  - `tests/api/` (API tests)
  - `tests/e2e/` (UI/API hybrid E2E tests)
  - `utils/` (API client, data factory, assertions)
- Added shared pytest fixtures at root level (`conftest.py`) for browser config, API context, and test user lifecycle.

### 2) API client abstraction
- Implemented `AEApiClient` as a thin wrapper around Playwright `APIRequestContext`.
- Added dedicated methods for:
  - Products endpoints (`get_products`, `search_product`)
  - User endpoints (`create_user`, `update_user`, `delete_user`, `get_user_by_email`)
  - Authentication endpoint (`verify_login`)
- This keeps tests readable and avoids repeating endpoint paths in test files.

### 3) Data generation strategy
- Added `UserFactory` (Faker-based) to generate valid, random, unique user payloads.
- This reduces collisions (especially duplicate-email conflicts) and keeps tests isolated.

### 4) Page Object Model implementation
- Implemented a `BasePage` with common navigation/screenshot utilities.
- Built page objects for:
  - `LoginPage`
  - `ProductsPage`
  - `SignupPage`
- Kept selectors inside page classes, so tests stay focused on behavior, not locators.

### 5) Reusable fixture lifecycle
- Added `registered_user` fixture:
  - Creates a fresh user before each test.
  - Automatically deletes the user in teardown.
- Added `make_user` fixture:
  - Factory-style helper to create multiple users in one test.
  - Cleans all created users at teardown.
- Added `authenticated_page` fixture:
  - Returns a page already logged in after API-backed credential preparation.

### 6) API test coverage
Implemented API test suites for:
- **Products API**:
  - success response validation
  - response schema checks
  - required field checks
  - search behavior
  - negative tests for missing params / wrong method
- **User & Auth API**:
  - user creation and retrieval
  - duplicate user rejection
  - user update verification
  - nonexistent user handling
  - login validation for positive/negative/malformed method cases

### 7) Hybrid end-to-end user journey coverage
Implemented E2E tests that combine API + UI to validate realistic flows:
- API user registration -> UI login success
- Existing user + wrong password -> UI error shown
- API login verification -> UI login verification
- API product search cross-checked with UI product search results

---

## What I tested

### API tests
- Product listing endpoint returns expected success response.
- Product response includes `products` list with required fields per item.
- Product search returns non-empty results for valid keyword.
- Error handling works for invalid/missing request parameters.
- Unsupported HTTP methods return expected API response codes.

### User and authentication tests
- Account creation flow works and user can be fetched by email.
- Duplicate registration is rejected correctly.
- Account update operations persist data.
- Invalid/nonexistent account queries return expected not-found behavior.
- Login verification endpoint handles valid, invalid, and malformed requests correctly.

### UI + hybrid checks
- Login UI accepts valid credentials created via API.
- Login UI rejects incorrect password and displays error message.
- API and UI are cross-validated in the same test flow to catch data consistency issues.
- Search behavior is checked on both API and UI side for the same keyword.

---

## Why this approach

### Faster execution
Creating users via API is significantly faster than creating users through UI forms in every test.

### Better reliability
UI-only setup flows are often flaky due to ads/load timing/popups. API-first setup reduces instability and isolates failures.

### Easier debugging
If API verification passes but UI login fails, the problem is likely UI-side; this narrows root-cause quickly.

### Scalable maintenance
POM + fixtures + utility wrappers make it easy to expand the suite without copy-paste and brittle tests.

---

## How to run the tests

Install dependencies, then run:

```bash
pytest -m api -v
pytest -m e2e -v
pytest -v
```

Optional targeted execution:

```bash
pytest tests/api/test_products_api.py -v
pytest tests/api/test_user_api.py -v
pytest tests/e2e/test_user_journey.py -v
```

---

## Notes

- The test target is `https://automationexercise.com`.
- API and UI tests are intentionally mixed for practical QA workflows.
- Fixtures are designed to keep tests isolated and clean up created data automatically.

# Procedure Lab

![pytest](https://github.com/the-remakers/procedures-lab/actions/workflows/pytest.yml/badge.svg)

Our goal here is to implement small, testable procedures, wire them into a local Flask web server, write/verify tests, then discover and fix a simple reflected XSS vulnerability (Yes! You are hacking your own site!). 

This lab teaches *how to design, call, and test procedures* and gives a short, practical security lesson about escaping

Work incrementally. After each small task, run the tests and try the server forms. If something fails, fix it before moving on (small, frequent commits help).


## Setup (do this only once)

1. Create the virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2. Run the test suite (it will fail initially -- that's expected):
    ```bash
    pytest -q
    ```
    ```bash
    (venv) ➜  procedures-lab (master) ✗ pytest -v --tb=no
    ============================================================================================ test session starts ============================================================================================
    platform linux -- Python 3.13.7, pytest-7.4.2, pluggy-1.6.0 -- /home/mataiodoxion/School/CSP/procedures-lab/venv/bin/python
    cachedir: .pytest_cache
    rootdir: /home/mataiodoxion/School/CSP/procedures-lab
    configfile: pytest.ini
    collected 8 items                                                                                                                                                                                           

    tests/test_endpoints.py::test_add_endpoint FAILED                                                                                                                                                     [ 12%]
    tests/test_endpoints.py::test_fib_endpoint FAILED                                                                                                                                                     [ 25%]
    tests/test_endpoints.py::test_item_crud FAILED                                                                                                                                                        [ 37%]
    tests/test_endpoints.py::test_vulnerable_echo_reflection PASSED                                                                                                                                       [ 50%]
    tests/test_endpoints.py::test_vulnerable_echo_fixed FAILED                                                                                                                                            [ 62%]
    tests/test_utils.py::test_add_simple FAILED                                                                                                                                                           [ 75%]
    tests/test_utils.py::test_fib_basic FAILED                                                                                                                                                            [ 87%]
    tests/test_utils.py::test_db_crud FAILED                                                                                                                                                              [100%]

    ========================================================================================== short test summary info ==========================================================================================
    FAILED tests/test_endpoints.py::test_add_endpoint - NotImplementedError
    FAILED tests/test_endpoints.py::test_fib_endpoint - NotImplementedError
    FAILED tests/test_endpoints.py::test_item_crud - NotImplementedError
    FAILED tests/test_endpoints.py::test_vulnerable_echo_fixed - assert False
    FAILED tests/test_utils.py::test_add_simple - NotImplementedError
    FAILED tests/test_utils.py::test_fib_basic - NotImplementedError
    FAILED tests/test_utils.py::test_db_crud - NotImplementedError
    ======================================================================================== 7 failed, 1 passed in 0.01s ========================================================================================
    (venv) ➜  procedures-lab (master) ✗ 
    ```
    > Do note that you can use `pytest -q --tb=no` to get a summary only output.

1. Start the server for testing:
    ```bash
    ./run.sh
    # Visit http://127.0.0.1:8000/
    ```


## Project Layout
```bash
py-web-assignment/
├─ app/
│  ├─ server.py    # Flask endpoints (some already provided)
│  └─ utils.py     # Your functions to implement
├─ tests/
│  ├─ test_utils.py
│  └─ test_endpoints.py
└─ run.sh
```

**You will mainly edit `app/utils.py` and make a *small* change to `app/server.py` (adding one POST endpoint, and later a mitigation).**


## The Lab

Follow these steps in order. After each step, run `pytest -q` and (for endpoints) exercise the server in the browser or with `curl`.


### Part A: Small pure procedures (tests will check thest)

1. Implement `add(a, b)` in `app/utils.py`
   - Behavior: return the sum of the two `float` arguments.
   - Tests expect exact numeric edition
      - Ex. `add(2, 3) == 5` 

2. Implement `fib(n)` in `app/utils.py`
   - Behavior: return the n-th Fibonacci number with `fib(0) == 0`, `fib(1) == 1`.
   - Hint: look up what the Fibonacci sequence is if you need help!

3. Run `pytest -q`. `test_utils.py` should pass once `add` and `fib` are correct.


### Part B: Simple CRUD (the "database")

`app/utils.py` already declares `_DB: Dict[str, Dict] = {}`. Implement these functions operating on that dictionary:

4. `create_item(key: str, value: Dict) -> None`
   - Store a copy of `value` under `key`. Replacing existing value is fine.

5. `read_item(key: str) -> Optional[Dict]`
   - Return a copy of the stored dict or `None` if absent.

6. `update_item(key: str, patch: Dict) -> bool`
   - If the key exists, merge patch into the stored dict (`existing.update(patch)` semantics) and return `True`. If key missing, return `False`.

7. `delete_item(key: str) -> bool`
   - Delete the key if present; return `True` if deleted, `False` otherwise.

8. `clear_db()` is provided for tests -- do not remove it.

Run `pytest -q`. `test_db_crud` and `test_endpoints` related to items should pass for the utils level behavior.

#### Bonus

If you're really curious, you can try using `curl` to try sending requests to your own web server! We'll be doing this int he next part anyway.

```bash
curl 'http://127.0.0.1:8000/add?a=4&b=1.5'
```

### Part C: Endpoints and a small addition

9. The server already exposes endpoints for `/add`, `/fib`, and `/items/<key>` (GET/PUT/PATCH/DELETE). Confirm these behaviors by running the server using `./run.sh` (if you haven't already) and using the forms by manually typing in your query into the browser or using `curl` from your terminal like this:

```bash
# add
curl 'http://127.0.0.1:8000/add?a=4&b=1.5'

# fib
curl 'http://127.0.0.1:8000/fib?n=6'

# create item (PUT)
curl -X PUT -H 'Content-Type: application/json' \
  -d '{"name":"alice"}' \
  http://127.0.0.1:8000/items/user1

# read item (GET)
curl http://127.0.0.1:8000/items/user1
```

10. Tests: make sure all endpoint tests in `tests/test_endpoints.py` pass. If they fail, read the test failure message and fix the code.


### Part D: Hacking your server

This is a very short section. You will discover a vulnerable endpoint and fix it.

12. **Discovery**
    - Open `http://127.0.0.1:8000/` and use the form that points to `/vulnerable_echo`. Submit this as the input:
        ```html
        name=<script>alert(1)</script>
        ```
    (or paste it in the address bar as `?name=<script>alert(1)</script>`). Observe that the browser executes the script (an alert appears).
    - When you submit this assignment, include a little section explaining:
      - *What you sent*;
      - *What happened in the browser*;
      - *Why the server was vulnerable*;
      - See [How to submit](#how-to-submit)
    - You just hacked your own website!

13. **Mitigation**
    - Replace the vulnerable echo with a safe version: use `markupsafe.escape(name)` (or render via a template that escapes by default so user input is HTML-escaped before insertion).
    - Add a `Content-Security-Policy` header to the response(s) that disallows inline scripts (for example: `Content-Security-Policy: default-src 'self'; script-src 'self'`).
  
14. **Run a test** asserting the raw `"<script>...</script>"` string no longer appears in the body returned by `/vulnerable_echo`.
    - Run `pytest -q`. If you made the right fix, then:
      - `test_vulnerable_echo_reflection` should $${\color{red}\text{FAIL}}$$
      - `test_vulnerable_echo_fix` should $${\color{green}\text{PASS}}$$

15. Run `pytest -q` and ensure all tests pass.


## Submission

Submit your code with:

1. Implements `app/utils.py` and updates `app/server.py` (XSS mitigation).
2. All tests in `tests/` pass (`pytest -q`).
3. A small section explaining the exploit (mentioned in Part D).

### Checklist

- [ ] `pytest -q` shows all tests passing
- [ ] Server starts and the forms work at `http://127.0.0.1:8000/`
- [ ] You can `PUT/GET/PATCH/DELETE` items
- [ ] Security report (Part D) is present and explains the XSS and mitigations
- [ ] `/vulnerable_echo` no longer reflects raw `<script>` tags (verified by `pytest -q`)

### How to Submit

1. Push your work to your repository:
    ```bash
    git add .
    git commit -m "Your message here"
    git push origin master
    ```

    Your repository should automatically run the *CI workflow* on every push. You can see passing/failing tests in the "Actions" tab.

2. Create a new `.md` file in the directory root (can be named anything)
    For example:
    ```bash
    procedures-lab/
    ├── app
    │   ├── __init__.py
    │   ├── server.py
    │   └── utils.py
    ├── pytest.ini
    ├── README.md
    ├── report.md # <-- like this, for example
    ├── requirements.txt
    ├── run.sh
    └── tests
        ├── conftest.py
        ├── test_endpoints.py
        └── test_utils.py
    ```

3. Ensure the tests pass in CI:
   - Open the **Actions** tab on GitHub --> latest workflow run --> ensure it shows *green checkmarks*.
     - You can embed this in your write up like so:
        ```md
        ![pytest](https://github.com/<your-username>/procedures-lab/actions/workflows/pytest.yml/badge.svg)
        ```
   - Optionally, you can run `pytest -q --tb=no` locally and put the output somewhere to link:
     - The output should look something like this:
        ```bash
        (venv) ➜  procedures-lab git:(master) ✗ pytest -v --tb=no
        ================================================================= test session starts =================================================================
        platform linux -- Python 3.13.7, pytest-7.4.2, pluggy-1.6.0 -- /home/mataiodoxion/School/CSP/procedures-lab/venv/bin/python
        cachedir: .pytest_cache
        rootdir: /home/mataiodoxion/School/CSP/procedures-lab
        configfile: pytest.ini
        collected 8 items                                                                                                                                     

        tests/test_endpoints.py::test_add_endpoint PASSED                                                                                               [ 12%]
        tests/test_endpoints.py::test_fib_endpoint PASSED                                                                                               [ 25%]
        tests/test_endpoints.py::test_item_crud PASSED                                                                                                  [ 37%]
        tests/test_endpoints.py::test_vulnerable_echo_reflection SKIPPED (Reflection test ignored because fixed test passes)                            [ 50%]
        tests/test_endpoints.py::test_vulnerable_echo_fixed PASSED                                                                                      [ 62%]
        tests/test_utils.py::test_add_simple PASSED                                                                                                     [ 75%]
        tests/test_utils.py::test_fib_basic PASSED                                                                                                      [ 87%]
        tests/test_utils.py::test_db_crud PASSED                                                                                                        [100%]

        ============================================================ 7 passed, 1 skipped in 0.02s =============================================================
        (venv) ➜  procedures-lab git:(master) ✗ 
        ```
        - Add this output to your writeup.

4. Submit a link to your `.md` writeup on GitHub to the grading sheet!
   - See here for an example: [report](report.md)
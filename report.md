# Example Report
> This is just an example template, but feel free to edit it and make it your own.

Author: *mataiodoxion*


## Security Report
- *What you sent*;
- *What happened in the browser*;
- *Why the server was vulnerable*;


## Pytest
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
import sys
import os
# Add src to sys.path for test imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import azure.functions as func
from function_app import multiply, divide


def make_request(path: str, params: dict) -> func.HttpRequest:
    return func.HttpRequest(method="GET", url=f"http://localhost{path}", headers={}, params=params, body=b"")


def test_multiply_success():
    req = make_request("/api/multiply", {"A": "3", "B": "5"})
    res = multiply(req)
    assert res.status_code == 200
    assert res.headers.get("Content-Type") == "text/plain; charset=utf-8"
    assert res.get_body().decode("utf-8") == "15"


def test_divide_success_integer_result():
    req = make_request("/api/divide", {"A": "10", "B": "5"})
    res = divide(req)
    assert res.status_code == 200
    assert res.get_body().decode("utf-8") == "2.0"


def test_divide_success_float_result():
    req = make_request("/api/divide", {"A": "10", "B": "4"})
    res = divide(req)
    assert res.status_code == 200
    assert res.get_body().decode("utf-8") == "2.5"


def test_divide_zero_denominator():
    req = make_request("/api/divide", {"A": "10", "B": "0"})
    res = divide(req)
    assert res.status_code == 400
    assert res.get_body().decode("utf-8") == "Bに0は指定できません"


def test_invalid_params_non_integer():
    req = make_request("/api/multiply", {"A": "1.2", "B": "3"})
    res = multiply(req)
    assert res.status_code == 400
    assert res.get_body().decode("utf-8") == "パラメータA,Bは整数で指定してください"


def test_missing_params():
    req = make_request("/api/multiply", {"A": "1"})
    res = multiply(req)
    assert res.status_code == 400
    assert res.get_body().decode("utf-8") == "パラメータA,Bは整数で指定してください"

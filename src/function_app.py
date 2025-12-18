import re
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

_INT_PATTERN = re.compile(r"^[+-]?\d+$")


def _text_response(body: str, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        body,
        status_code=status_code,
        headers={"Content-Type": "text/plain; charset=utf-8"},
    )


def _parse_int_param(req: func.HttpRequest, key: str):
    val = req.params.get(key)
    if val is None or not _INT_PATTERN.fullmatch(val):
        return None
    try:
        return int(val)
    except ValueError:
        return None


@app.route(route="multiply", methods=["GET"])  # -> GET /api/multiply
def multiply(req: func.HttpRequest) -> func.HttpResponse:
    a = _parse_int_param(req, "A")
    b = _parse_int_param(req, "B")
    if a is None or b is None:
        return _text_response("パラメータA,Bは整数で指定してください", 400)

    result = a * b
    return _text_response(str(result), 200)


@app.route(route="divide", methods=["GET"])  # -> GET /api/divide
def divide(req: func.HttpRequest) -> func.HttpResponse:
    a = _parse_int_param(req, "A")
    b = _parse_int_param(req, "B")
    if a is None or b is None:
        return _text_response("パラメータA,Bは整数で指定してください", 400)

    if b == 0:
        return _text_response("Bに0は指定できません", 400)

    result = a / b
    return _text_response(str(result), 200)

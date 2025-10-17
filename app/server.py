from flask import Flask, request, jsonify
from markupsafe import escape
from . import utils

app = Flask(__name__)


@app.after_request
def add_csp_header(response):
    """
    Add a basic Content-Security-Policy header to HTML responses to disallow
    inline scripts/styles and reduce XSS impact.
    """
    # Only add the header for HTML responses to avoid interfering with JSON API
    ctype = response.content_type or ""
    if ctype.startswith("text/html"):
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self';"
        )
    return response

@app.route("/")
def index():
    # simple HTML form for manual testing
    html = """
    <h1>Procedure Lab</h1>
    <p>Use the API endpoints or the simple forms below.</p>
    <form action="/vulnerable_echo" method="get">
      Name: <input name="name" />
      <button>Echo (vulnerable)</button>
    </form>
    <form action="/safe_echo" method="get">
      Name: <input name="name" />
      <button>Echo (safe)</button>
    </form>
    """
    return html

@app.route("/add")
def add_endpoint():
    # Accepts ?a=...&b=...
    a = request.args.get("a", default="0")
    b = request.args.get("b", default="0")
    try:
        a_f = float(a)
        b_f = float(b)
    except ValueError:
        return jsonify({"error":"invalid numbers"}), 400
    return jsonify({"result": utils.add(a_f, b_f)})

@app.route("/fib")
def fib_endpoint():
    # ?n=10
    n = request.args.get("n", default="0")
    try:
        n_i = int(n)
    except ValueError:
        return jsonify({"error":"invalid integer"}), 400
    if n_i < 0:
        return jsonify({"error":"n must be >= 0"}), 400
    return jsonify({"n": n_i, "fib": utils.fib(n_i)})

# CRUD endpoints using JSON bodies
@app.route("/items/<key>", methods=["GET", "PUT", "PATCH", "DELETE"])
def item_endpoint(key):
    if request.method == "GET":
        v = utils.read_item(key)
        if v is None:
            return jsonify({"error":"not found"}), 404
        return jsonify({"key": key, "value": v})
    if request.method == "PUT":
        data = request.get_json(force=True)
        utils.create_item(key, data)
        return jsonify({"result":"created"}), 201
    if request.method == "PATCH":
        data = request.get_json(force=True)
        ok = utils.update_item(key, data)
        if not ok:
            return jsonify({"error":"not found"}), 404
        return jsonify({"result":"updated"})
    if request.method == "DELETE":
        ok = utils.delete_item(key)
        if not ok:
            return jsonify({"error":"not found"}), 404
        return jsonify({"result":"deleted"})
    
# Vulnerable endpoint: reflects name into HTML without escaping
@app.route("/vulnerable_echo")
def vulnerable_echo():
    name = request.args.get("name", "")
    # Mitigation: escape user input so it is not reflected raw into HTML
    html = f"<h2>Hello {escape(name)}</h2>"
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}

# "Safe" echo uses escaping
@app.route("/safe_echo")
def safe_echo():
    name = request.args.get("name", "")
    return f"<h2>Hello {escape(name)}</h2>", 200, {"Content-Type": "text/html; charset=utf-8"}
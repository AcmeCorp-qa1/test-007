"""
reachability_examples.py
=============================================================================
Purpose: Minimal "sink" call sites for each CVE in requirements.txt, used to
test whether an SCA / reachability scanner (pip-audit --require-hashes,
Semgrep, CodeQL, Snyk Code, etc.) correctly distinguishes:
  - "vulnerable package is a dependency" (dependency-tree match only)
  vs.
  - "vulnerable function is actually reachable/called from your code"
    (true reachability - the harder, more valuable signal)

Each function below calls the vulnerable API with a variable sourced from
"untrusted_input" (simulating user-controlled data), which is exactly what
reachability analyzers trace: source -> vulnerable sink.

INTENTIONALLY OMITTED: actual exploit payloads (malicious YAML tags, forged
JWTs, sandbox-escape strings, crafted image bytes, etc.). Those are the
difference between "this code path is reachable" and "here is a working
exploit" - only the former is included here. If you need real PoC payloads
for validating that a fix actually closes the hole, pull them from the
CVE's own reference links (nvd.nist.gov) or the GitHub Security Advisory
Database - not from this file.
=============================================================================
"""

# --- CVE-2020-14343: PyYAML unsafe load -------------------------------------
import yaml

def parse_config(untrusted_input: str):
    """Reachable: yaml.load() without a safe Loader on attacker-controlled
    text is exactly the sink this CVE concerns. No payload included -
    calling this with ordinary YAML is harmless; the CVE is about what
    *could* be in untrusted_input, not what's shown here."""
    return yaml.load(untrusted_input, Loader=yaml.FullLoader)


# --- CVE-2019-10906: Jinja2 sandbox escape ----------------------------------
from jinja2.sandbox import SandboxedEnvironment

def render_user_template(untrusted_input: str, context: dict):
    """Reachable: rendering a SandboxedEnvironment template built directly
    from user input is the sink. The CVE concerns what template syntax
    *could* escape the sandbox - not demonstrated here."""
    env = SandboxedEnvironment()
    template = env.from_string(untrusted_input)
    return template.render(**context)


# --- CVE-2018-1000656: Flask DoS via crafted JSON ---------------------------
from flask import Flask, request

app = Flask(__name__)

@app.route("/submit", methods=["POST"])
def submit():
    """Reachable: request.get_json() parsing attacker-supplied request
    bodies is the sink for this DoS. No crafted payload included."""
    data = request.get_json()
    return {"received": bool(data)}


# --- CVE-2022-28346: Django SQLi via QuerySet.explain() ---------------------
# (illustrative - requires an actual Django model in a real project)
def explain_query(Model, untrusted_format: str):
    """Reachable: passing user-controlled data into explain(format=...)
    is the sink. No injection string included."""
    return Model.objects.all().explain(format=untrusted_format)


# --- CVE-2021-25287: Pillow buffer overflow (SGI decoder) ------------------
from PIL import Image

def load_user_image(untrusted_file_path: str):
    """Reachable: Image.open() on a user-uploaded file is the sink for
    decoder-level memory bugs. No crafted malformed image included."""
    return Image.open(untrusted_file_path)


# --- CVE-2019-6446: numpy unsafe pickle in np.load --------------------------
import numpy as np

def load_user_array(untrusted_file_path: str):
    """Reachable: np.load() on an attacker-controlled .npy/.npz file with
    default allow_pickle behavior is the sink. No malicious pickle
    included."""
    return np.load(untrusted_file_path, allow_pickle=True)


# --- CVE-2021-43818: lxml XSS via clean_html --------------------------------
from lxml.html.clean import clean_html

def sanitize_user_html(untrusted_input: str):
    """Reachable: passing raw user HTML into clean_html() and trusting the
    output as safe is the sink. No bypass markup included."""
    return clean_html(untrusted_input)


# --- CVE-2017-11424: PyJWT algorithm confusion ------------------------------
import jwt

def decode_user_token(untrusted_token: str, key: str):
    """Reachable: decoding a token without pinning `algorithms=[...]`
    leaves the algorithm chosen by the token itself - the sink for this
    CVE. No forged token included."""
    return jwt.decode(untrusted_token, key)  # missing `algorithms=` param


# --- CVE-2018-7750: paramiko auth bypass ------------------------------------
import paramiko

def connect_user_host(untrusted_host: str, username: str, password: str):
    """Reachable: SSHClient.connect() driven by attacker-influenced
    host/credentials is the sink. No bypass technique included."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(untrusted_host, username=username, password=password)
    return client

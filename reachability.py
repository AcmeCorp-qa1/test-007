"""
sca_vulnerable_usage.py

Companion file to requirements.txt — each function below actually invokes
the vulnerable code path in the pinned package version, so an SCA tool with
reachability/call-graph analysis (e.g. Snyk, Semgrep SCA, Mend) will flag
these as "reachable" rather than just "installed but unused".
"""

import yaml
import requests
from lxml import etree
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from flask import Flask, request, render_template_string

app = Flask(__name__)


# ---------------------------------------------------------------------
# PyYAML 5.3.1 — CVE-2020-1747 / CVE-2017-18342
# yaml.load() without a SafeLoader allows arbitrary code execution via
# crafted YAML (e.g. !!python/object/apply tags).
# ---------------------------------------------------------------------
@app.route('/import_config', methods=['POST'])
def import_config():
    raw_yaml = request.data.decode('utf-8')
    config = yaml.load(raw_yaml)  # unsafe Loader, untrusted input reaches this call
    return f"Loaded config: {config}"


# ---------------------------------------------------------------------
# requests 2.19.1 — CVE-2018-18074
# Authorization headers are leaked to a different host on redirect
# because of improper handling of redirects to a different domain.
# ---------------------------------------------------------------------
@app.route('/proxy_fetch', methods=['POST'])
def proxy_fetch():
    target_url = request.form['url']
    headers = {'Authorization': f"Bearer {session_token()}"}
    resp = requests.get(target_url, headers=headers, allow_redirects=True)
    return resp.text


def session_token():
    return "static-demo-token-do-not-use"


# ---------------------------------------------------------------------
# lxml 4.6.2 — CVE-2021-43818 / general XXE exposure in older lxml
# when parser is built without resolve_entities=False.
# ---------------------------------------------------------------------
@app.route('/parse_lxml', methods=['POST'])
def parse_lxml():
    xml_data = request.data
    parser = etree.XMLParser()  # resolve_entities defaults True in this version
    root = etree.fromstring(xml_data, parser=parser)
    return f"Root tag: {root.tag}"


# ---------------------------------------------------------------------
# Pillow 8.1.0 — CVE-2021-25287 / CVE-2021-25288
# Heap buffer overflow / out-of-bounds read when processing crafted
# image files (e.g. malformed FLI/SGI/TIFF).
# ---------------------------------------------------------------------
@app.route('/thumbnail', methods=['POST'])
def make_thumbnail():
    file = request.files['image']
    img = Image.open(file.stream)   # vulnerable parsing path reached on untrusted upload
    img.thumbnail((128, 128))
    img.save('thumb.png')
    return "Thumbnail created"


# ---------------------------------------------------------------------
# cryptography 2.3 — CVE-2018-10903
# Uses of finalize_with_tag() skip minimum tag length verification,
# permitting GCM tag truncation / forgery attacks.
# ---------------------------------------------------------------------
@app.route('/decrypt', methods=['POST'])
def decrypt_payload():
    key = bytes.fromhex(request.form['key'])
    nonce = bytes.fromhex(request.form['nonce'])
    tag = bytes.fromhex(request.form['tag'])
    ciphertext = bytes.fromhex(request.form['ciphertext'])

    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce, tag, min_tag_length=1),  # weakened tag-length check
        backend=default_backend()
    ).decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode(errors='ignore')


# ---------------------------------------------------------------------
# Jinja2 2.10.1 — CVE-2019-10906 (autoescape bypass helpers) and general
# SSTI risk when render_template_string() is fed user-controlled input.
# ---------------------------------------------------------------------
@app.route('/render_snippet', methods=['POST'])
def render_snippet():
    template_str = request.form['template']
    return render_template_string(template_str)  # user input rendered as a Jinja2 template


# ---------------------------------------------------------------------
# Werkzeug 0.15.4 — CVE-2019-14806 (header injection via multipart
# boundary parsing) reachable through the default werkzeug dev server
# request-parsing path used by Flask's request.form/request.files above.
# No extra call needed — every route above using request.form/request.files
# already exercises the vulnerable multipart parser in this Werkzeug version.
# ---------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
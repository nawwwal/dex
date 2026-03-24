#!/usr/bin/env python3
"""Wrapper that patches httpx SSL for Zscaler corporate proxy before running a script.
Usage: python3 run_with_ssl.py <script.py> [args...]
"""
import ssl, httpx, sys, os

CA_BUNDLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'zscaler-combined-ca.pem')

def _make_ssl_ctx():
    ctx = ssl.create_default_context()
    if os.path.exists(CA_BUNDLE):
        ctx.load_verify_locations(CA_BUNDLE)
    ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return ctx

_Orig = httpx.AsyncClient
class _Patched(_Orig):
    def __init__(self, *a, **kw):
        if 'verify' not in kw:
            kw['verify'] = _make_ssl_ctx()
        super().__init__(*a, **kw)
httpx.AsyncClient = _Patched

real_script = sys.argv[1]
scripts_dir = os.path.dirname(real_script)
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)
sys.argv = sys.argv[1:]
with open(real_script) as f:
    code = f.read()
exec(compile(code, real_script, 'exec'), {'__file__': real_script, '__name__': '__main__'})

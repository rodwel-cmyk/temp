# -*- coding: utf-8 -*-
"""l1lint - the Layer 1 doc-linter engine as a modular package (869drd6uy split of the
frozen v0.2.8 monolith, sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7).

Entrypoint and public surface: the layer1_lint.py shim beside this package (invocation
unchanged). Import layering (DAG): loader -> parsing -> {checks, xdoc(+org_mirror), pins,
dochygiene, hygiene} -> engine -> selftest -> cli. Importing any submodule triggers the
manifest floor-load in l1lint.loader, exactly as importing the monolith did (F2:
INIT-FAILURE + exit 3 on a missing/tampered manifest).
"""

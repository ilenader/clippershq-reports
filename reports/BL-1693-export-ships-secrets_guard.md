# BL-1693 -- the code export dropped modules the 3090 needs

`NEVER` in tools/office/remote_fixer.py drops every file named config*/secret*/credential*. That also removed the CODE modules clippershq/secrets_guard.py and clippershq/config_defaults.py, so on the 3090 125 test files died at `import secrets_guard` and clippershq could not import config_defaults.
Fix: ALLOW_CODE lists exactly those two paths; every other config*/secrets* name stays blocked (test_exportable pins both sides: secrets_guard.py and config_defaults.py ship, secrets.py and config.py do not). The export's secret scan still runs, and a FAIL ships nothing.
Proof: tests/test_remote_fixer.py 12 passed. After HQ lands this and the next export, the 3090 gets the two modules.
HQ check please: confirm config_defaults.py holds no values before the next export (the scan will also catch it).

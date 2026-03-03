# conftest.py — pytest collection configuration for src/sno4py/tests/
#
# These files are standalone scripts (sys.exit at module level) and cannot
# be collected by pytest. They remain runnable directly: python3 test_bead.py
collect_ignore = [
    "test_bead.py",
    "test_bead_stage1.py",
    "test_json_fixed.py",
    "test_speed.py",
]
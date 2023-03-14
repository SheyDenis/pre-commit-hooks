## pre-commit hooks

Git hooks for personal use based on https://github.com/pre-commit/pre-commit .

### TODO

- [ ] Rewrite `setup.py` as `setup.cfg`.
- [ ] Cleanup `setup.py`.
- [ ] Add line numbers to dev-marker hook.
- [ ] Implement line endings hook.
- [ ] Implement `utilities.proc.wait_to_finish()` waiting and TO kill.
- [ ] Add `--dry-run` / `--no-dry-run` to `utilities.argparse.get_base_parser()`.
- [ ] Cleanup log messages.
- [ ] Log error messages if hook failed to execute.
- [>] Re-write hooks in Python for simplicity.
    - [x] clang_format
    - [x] isort
    - [x] mypy
    - [x] pylint
    - [ ] symbolic_links
    - [x] yapf

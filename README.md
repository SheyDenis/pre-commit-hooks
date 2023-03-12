## pre-commit hooks

Git hooks for personal use based on https://github.com/pre-commit/pre-commit .

### TODO

- [ ] Increment version automatically on merge.
    - [ ] Create git tag from version on merge.
    - [ ] Create github release on merge.
- [ ] Add line numbers to dev-marker hook.
- [x] Implement xenon hook.
- [ ] Implement yapf hook.
- [ ] Implement line endings hook.
- [ ] Implement `utilities.proc.wait_to_finish()` waiting and TO kill.
- [ ] Add `--dry-run` / `--no-dry-run` to `utilities.argparse.get_base_parser()`.
- [ ] Cleanup log messages.
- [ ] Get requirements from `Pipfile.lock`.
    - [ ] Generate and commit `pipfile_requirements.txt` post-commit or at least check it was updated pre-commit.
- [>] Re-write hooks in Python for simplicity.
    - [ ] clang_format
    - [x] isort
    - [ ] mypy
    - [ ] pylint
    - [ ] symbolic_links
    - [ ] yapf

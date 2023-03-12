## pre-commit hooks

Git hooks for personal use based on https://github.com/pre-commit/pre-commit .

### TODO

- [ ] Fix `setup.py` and where it specifies the files should be installed to.
- [ ] Verify config file exists in `utilities.constants.get_config_file_path()`.
- [ ] Increment version automatically on merge.
    - [ ] Create git tag from version on merge.
    - [ ] Create github release on merge.
- [ ] Add line numbers to dev-marker hook.
- [ ] Implement line endings hook.
- [ ] Implement `utilities.proc.wait_to_finish()` waiting and TO kill.
- [ ] Add `--dry-run` / `--no-dry-run` to `utilities.argparse.get_base_parser()`.
- [ ] Cleanup log messages.
- [ ] Log error messages if hook failed to execute.
- [ ] Get requirements from `Pipfile.lock`.
    - [ ] Generate and commit `pipfile_requirements.txt` post-commit or at least check it was updated pre-commit.
- [ ] Remove dependency on `toml` in `generate_requirements.py`.
- [>] Re-write hooks in Python for simplicity.
    - [ ] clang_format
    - [x] isort
    - [x] mypy
    - [x] pylint
    - [ ] symbolic_links
    - [x] yapf

## pre-commit hooks

Git hooks for personal use based on https://github.com/pre-commit/pre-commit .

### TODO

- [ ] Cleanup local repo yaml.
- [ ] Add line numbers to dev-marker hook.
- [ ] Implement xenon hook.
- [ ] Implement yapf hook.
- [ ] Implement `utilities.proc.wait_to_finish()` waiting and TO kill.
- [ ] Add `--dry-run` / `--no-dry-run` to `utilities.argparse.get_base_parser()`.
- [ ] Cleanup log messages.
- [ ] Add hook for unused / duplicate python imports.
- [>] Re-write hooks in Python for simplicity.
  - [ ] Get requirements from `Pipfile.lock`.
  - [ ] Increment version automatically on merge.

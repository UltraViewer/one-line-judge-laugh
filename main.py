#!/usr/bin/env python3
"""make.fun bounty entry: Make the AI Judge Laugh.

The entry is one funny line in entry.txt (137 characters). This
program copies it byte-for-byte to /output/entry.txt, where the
house scorer reads it. No network, no randomness, no arguments
that change the text: every run writes the same bytes.

  python3 main.py                  write entry.txt to /output/entry.txt
  python3 main.py [path]           write entry.txt to the given path
  python3 main.py --verify-only    check the destination already matches
  python3 main.py --self-test      copy into a temp dir and verify there
  python3 main.py --help           show this usage text

The source is checked before every write: it must be valid UTF-8
of 1 to 200 characters, the range the house gate accepts. The copy
is checked after every write by comparing SHA-256 digests, so a
partial write is reported as a failure instead of a quiet success.
Exit code is 0 on success, 1 on any failure.
"""
import hashlib
import os
import shutil
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE, "entry.txt")
DEFAULT_DEST = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200

HELP = """usage: main.py [path] [--verify-only] [--self-test] [--help]

  main.py                  copy entry.txt to /output/entry.txt
  main.py [path]           copy entry.txt to the given path
  main.py --verify-only    verify the destination matches entry.txt
                           without writing anything; exit 0 on match
  main.py --self-test      copy entry.txt into a fresh temporary
                           directory, verify the copy, remove the
                           directory; exit 0 on PASS
  main.py --help           show this usage text

The entry is one line of 1 to 200 UTF-8 characters. Every mode
verifies the source first and refuses to proceed when it is
missing, undecodable, empty, or over 200 characters.
"""


def digest(path):
    """SHA-256 hex digest of a file's bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(65536)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def load_entry():
    """Read and validate entry.txt.

    Returns (text, raw_bytes) on success, or prints the problem
    and returns None.
    """
    if not os.path.isfile(SOURCE):
        print("entry.txt not found next to main.py", file=sys.stderr)
        return None
    with open(SOURCE, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("entry.txt is not valid UTF-8", file=sys.stderr)
        return None
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        print(
            f"entry.txt is {len(text)} characters, outside the "
            f"{MIN_CHARS}-{MAX_CHARS} range the house gate accepts",
            file=sys.stderr,
        )
        return None
    if not text.strip():
        print("entry.txt is only whitespace", file=sys.stderr)
        return None
    return text, raw


def files_match(a, b):
    """True when two files exist with identical bytes."""
    return (
        os.path.isfile(a)
        and os.path.isfile(b)
        and os.path.getsize(a) == os.path.getsize(b)
        and digest(a) == digest(b)
    )


def run_verify(dest):
    """Check dest already holds the entry, writing nothing."""
    entry = load_entry()
    if entry is None:
        return 1
    _, raw = entry
    if not os.path.isfile(dest):
        print(f"verify-only: {dest} does not exist", file=sys.stderr)
        return 1
    if files_match(SOURCE, dest):
        print(f"verify-only: OK {dest} matches entry.txt "
              f"({len(raw)} bytes, sha256 {digest(dest)})")
        return 0
    print(f"verify-only: MISMATCH {dest} does not match entry.txt",
          file=sys.stderr)
    return 1


def run_self_test():
    """Copy into a temp dir, verify, clean up, report PASS/FAIL."""
    entry = load_entry()
    if entry is None:
        return 1
    _, raw = entry
    tmpdir = tempfile.mkdtemp(prefix="laugh-self-test-")
    try:
        probe = os.path.join(tmpdir, "entry.txt")
        shutil.copyfile(SOURCE, probe)
        if files_match(SOURCE, probe):
            print(f"self-test: PASS copy verified in {tmpdir} "
                  f"({len(raw)} bytes, sha256 {digest(probe)})")
            return 0
        print("self-test: FAIL copy does not match entry.txt",
              file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def run_write(dest):
    """Copy entry.txt to dest and verify the copy by SHA-256.

    After the byte check, the copy is re-read as UTF-8 and its
    character count is re-checked against the house gate, so a
    copy that is byte-identical but somehow miscounted can never
    be reported as a success.
    """
    entry = load_entry()
    if entry is None:
        return 1
    text, raw = entry
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    if not files_match(SOURCE, dest):
        print(f"copy verification failed: {dest} does not match "
              f"entry.txt after writing", file=sys.stderr)
        try:
            os.remove(dest)
        except OSError:
            pass
        return 1
    with open(dest, "rb") as f:
        written = f.read().decode("utf-8")
    if len(written) != len(text) or written != text:
        print(f"copy verification failed: {dest} reads back as "
              f"{len(written)} characters, expected {len(text)}",
              file=sys.stderr)
        try:
            os.remove(dest)
        except OSError:
            pass
        return 1
    print(f"wrote {dest} ({len(raw)} bytes, {len(text)} characters, "
          f"sha256 {digest(dest)})")
    return 0


def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    positional = [a for a in argv if not a.startswith("--")]
    if "--help" in flags:
        print(HELP, end="")
        return 0
    if "--verify-only" in flags and "--self-test" in flags:
        print("cannot combine --verify-only and --self-test",
              file=sys.stderr)
        return 1
    dest = positional[0] if positional else DEFAULT_DEST
    if "--verify-only" in flags:
        return run_verify(dest)
    if "--self-test" in flags:
        return run_self_test()
    return run_write(dest)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

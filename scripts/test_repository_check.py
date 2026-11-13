#!/usr/bin/env python3
"""Tests for the public repository contract checker."""

from pathlib import Path
import tempfile
import unittest

import check_repository as check


class RepositoryCheckTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.original_root = check.ROOT
        check.ROOT = Path(self.temporary.name)

    def tearDown(self):
        check.ROOT = self.original_root
        self.temporary.cleanup()

    def write(self, relative, content):
        target = check.ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def test_sensitive_path_is_rejected(self):
        self.write("note.md", "private: /" + "Users/example/source.txt\n")
        errors = []
        check.check_sensitive_text(errors)
        self.assertTrue(any("absolute user path" in error for error in errors))

    def test_broken_local_link_is_rejected(self):
        self.write("README.md", "[missing](docs/missing.md)\n")
        errors = []
        check.check_local_links(errors)
        self.assertTrue(any("broken local link" in error for error in errors))

    def test_valid_skill_metadata_passes(self):
        self.write(
            "SKILL.md",
            "---\n"
            "name: economic-reasoning-engineering\n"
            "description: Reconstruct traceable economic reasoning.\n"
            "---\n",
        )
        errors = []
        check.check_skill(errors)
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()

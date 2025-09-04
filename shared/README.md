Shared utilities for Sonfolio

This package is intended to host small helpers and scripts used across the repo.

- The `ly` CLI from python-ly is available in the devShell (via Nix).
- You can also import `ly` from Python here for programmatic transformations.

Examples (CLI ly)
- Convert LilyPond language (placeholder; adjust flags once finalized):
  - `ly --help`
  - `ly rewrite --language=italiano < input.ly > output.ly` (verify exact subcommand/options)

SPDX-License-Identifier: GPL-3.0-or-later


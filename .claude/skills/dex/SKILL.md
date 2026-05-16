---
name: dex
description: "Project-local dex maintainer workflow. Use when maintaining nawwwal/dex itself, especially for plugin releases, version bumps, tags, pushes, GitHub Releases, skill evals, benchmarking, and multi-round skill repair with skill-creator."
disable-model-invocation: true
---

# /dex - Project Maintainer Workflow

## Usage

`release <core|design|dev|tools> [patch|minor|major|initial]`
`eval <skill-path-or-plugin-skill> [rounds=N] [baseline=previous|none|snapshot]`

## Dispatch

**release** -> Read `./release.md`

**eval** -> Read `./eval.md`

**skill eval / benchmark / repair intent** -> Read `./eval.md`

If no argument: ask whether to run a plugin release or a skill eval.

# Design

## Context

See proposal.md. The current root properties, checks, and build targets assume one mod. Existing sources and published IDs must remain stable, and validation must not launch Minecraft.

## Goals / Non-Goals

Support module-local changes and outputs with one pinned platform. Do not add placeholder gameplay mods, a generator framework, shared gameplay libraries, automatic releases, or a guarantee of runtime isolation.

## Decisions

- Discover sorted immediate, non-hidden directories under `mods/`. Each requires `build.gradle` and `mod.json`; reject incomplete modules instead of silently omitting them. Avoid a central module list that concurrent additions would conflict on.
- Store each mod's identity, version, entry point, authors, and description in `mod.json`. JSON has matching standard parsers in Python and Gradle/Groovy, avoiding inherited Gradle properties and custom properties escaping. Keep Minecraft and NeoForge versions at the root.
- Apply a small shared Gradle script from each module after its plugins. Configure only the current project's source set, metadata, and archive. Root lifecycle tasks aggregate discovered projects; no implicit project dependency is introduced.
- Encode display text as TOML-compatible JSON strings during metadata expansion. Keep per-module loader metadata editable for explicit optional/required dependencies.
- Use the checker to produce the CI module list. Build jobs use a matrix with `fail-fast: false`; static/spec checks remain a shared prerequisite. Normal Gradle configuration still evaluates sibling build scripts, so configuration failures can affect all modules.
- Test discovery and invalid second-module cases in temporary directories. Use temporary two-mod build fixtures to inspect task selection and JAR separation. Keep only `core` as a real module.
- Document narrow module ownership and separate worktrees. Shared tooling changes require coordination, and combined gameplay still requires authorized runtime acceptance.

## Risks / Trade-offs

- Shared settings or convention changes affect all mods: validate all modules for such changes.
- Module discovery is implemented in Gradle and Python: regression tests and a two-module Gradle check must verify agreement.
- CI matrix jobs repeat dependency setup: keep the existing build cache integration; optimize only after measuring a real cost.

## Migration Plan

Move core metadata into its own manifest, preserving its ID, package, version, and `:core` target. Update checks, CI, and guidance together. Use a normal revert if rollback is needed; no saved-world migration or history rewrite is involved.

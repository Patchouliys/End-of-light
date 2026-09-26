# Proposal

## Why

The workspace registers one mod and hard-codes its identity, build targets, and checks. Maintainers need to develop additional mods independently without editing shared configuration for every new module.

## What Changes

- Discover mod directories automatically and share only platform/build conventions.
- Give each mod its own metadata, source tree, resources, version, and JAR.
- Build individual mods or all mods; check every module and reject identity collisions.
- Generate CI build jobs from the discovered module list, with independent failure reporting.
- Document adding modules, explicit dependencies, and separate worktrees for concurrent work.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `custom-mods`: Independently identified modules and selective/aggregate builds.
- `development-workflow`: Multi-module validation, CI coverage, and concurrent development boundaries.

## Impact

Changes Gradle settings/conventions, workspace checks, CI, documentation, and agent guidance. Keeps `:core`, `endoflight`, its Java package, and its version stable. Adds no gameplay, game mods, runtime dependencies, releases, or world-data changes. Game startup remains separately authorized.

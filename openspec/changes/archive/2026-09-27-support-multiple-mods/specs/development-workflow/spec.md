## ADDED Requirements

### Requirement: Complete multi-module checks
Workspace checks MUST validate every discovered mod's metadata, primary entry point, JSON resources, and shared-code client boundary. Incomplete modules MUST fail discovery. CI SHALL derive its module build jobs from the same module directory contract and report build failures independently without cancelling sibling build jobs.

#### Scenario: A new module has invalid resources
- **WHEN** a non-core module contains invalid JSON or a client reference in shared Java code
- **THEN** workspace checks fail with the affected module or file

#### Scenario: A module is added to CI
- **WHEN** a valid module is added without editing the workflow
- **THEN** the generated CI matrix includes its independent build job

### Requirement: Concurrent development ownership
Development guidance MUST require separate branches and worktrees for simultaneous independent editing sessions, with module-scoped changes and coordination for shared build, pack, and specification files. Published history SHALL use normal new commits without rewriting existing commits unless separately requested.

#### Scenario: Two mods are developed concurrently
- **WHEN** independent editing sessions work on different mods
- **THEN** each uses its own checkout and module scope, and shared changes are coordinated before integration

# development-workflow Specification

## Purpose
Guide AI development with traceable specifications and distinct evidence for static checks, compilation, and separately authorized game acceptance.

## Requirements

### Requirement: Project-local specification workflow
The project MUST use pinned OpenSpec tooling and project-level agent instructions. Behavior changes MUST include proposal, specs, design, and tasks, and be archived only when their agreed scope is complete.

#### Scenario: A behavior change is requested
- **WHEN** a request changes gameplay, dependencies, persistence, or networking
- **THEN** the agent reads current specs and versions, creates change artifacts, implements the change, and records validation evidence

### Requirement: Development checks without automatic game startup
Default development checks MUST NOT automatically launch Minecraft clients, servers, GameTest, or game-initializing datagen. Game acceptance SHALL require separate authorization. Reports MUST distinguish static checks, compilation, and runtime acceptance.

#### Scenario: The workspace passes static checks
- **WHEN** static and specification checks succeed without game startup
- **THEN** only those checks are reported as successful and runtime acceptance remains unexecuted

#### Scenario: The build runs in CI
- **WHEN** CI builds the custom mod
- **THEN** it compiles and packages with Java 21 without launching the game or treating compilation as runtime acceptance

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

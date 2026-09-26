## ADDED Requirements

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

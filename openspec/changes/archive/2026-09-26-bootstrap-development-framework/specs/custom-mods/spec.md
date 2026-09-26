## ADDED Requirements

### Requirement: Versioned NeoForge development skeleton
Custom mods MUST target Minecraft 1.21.1, a pinned NeoForge version, and Java 21. Sources MUST reside in `mods/core` and build through the verified Gradle wrapper.

#### Scenario: The core module is built
- **WHEN** an environment with Java 21 and dependency access executes `:core:build`
- **THEN** it produces a JAR containing the entry point and expanded NeoForge metadata without launching the game

### Requirement: Shared code and compatibility boundaries
Shared code MUST avoid client-only classes. The server SHALL own authoritative state. Changes to released resource IDs or saved-data fields SHALL include a migration strategy.

#### Scenario: Client functionality is added
- **WHEN** a change introduces rendering, UI, or client input
- **THEN** client classes are isolated from shared initialization and dedicated-server acceptance is tracked separately

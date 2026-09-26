## MODIFIED Requirements

### Requirement: Versioned NeoForge development skeleton
Custom mods MUST target Minecraft 1.21.1, a pinned NeoForge version, and Java 21. Each mod MUST reside in `mods/<module>` with its own identity, version, entry point, sources, resources, and build output. Builds MUST use the verified Gradle wrapper and preserve the existing `:core` module and `endoflight` identity.

#### Scenario: The core module is built
- **WHEN** an environment with Java 21 and dependency access executes `:core:build`
- **THEN** it produces a JAR containing the entry point and expanded NeoForge metadata without launching the game

#### Scenario: Another independent module is added
- **WHEN** a complete module with a unique identity is added under `mods/`
- **THEN** it is available as a build target without editing shared module lists
- **AND** building that target compiles and packages only that module and its explicitly declared dependencies

#### Scenario: All modules are built
- **WHEN** the root build is requested
- **THEN** all discovered modules are built into their respective output directories

## ADDED Requirements

### Requirement: Explicit module relationships
Mods MUST NOT implicitly depend on `core` or another workspace mod. Cross-mod dependencies SHALL be explicitly declared in build configuration and loader metadata. Module identity collisions MUST fail validation.

#### Scenario: One independent mod changes
- **WHEN** a mod's code, resources, or version changes
- **THEN** another independent mod retains its own metadata and sources

#### Scenario: Two mods share an identity
- **WHEN** two modules declare the same Mod ID or primary entry point
- **THEN** validation fails and identifies the conflicting modules

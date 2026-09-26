# modpack Specification

## Purpose
Manage compatible pack content through pinned text metadata and hashes, with explicit provenance for third-party and custom-mod distribution.

## Requirements

### Requirement: Text-based reproducible pack metadata
The pack MUST use packwiz text metadata for Minecraft, NeoForge, dependency versions, and content hashes. The repository MUST exclude third-party mod JARs, game instances, personal saves, and credentials.

#### Scenario: A mod dependency changes
- **WHEN** a dependency is added, upgraded, or removed
- **THEN** its metadata and indexes are updated with source, side, compatibility, and distribution information

### Requirement: Build and pack versions stay aligned
Build and pack Minecraft/NeoForge versions MUST match. Indexed file contents MUST match their recorded hashes.

#### Scenario: A version or indexed file drifts
- **WHEN** build and pack versions differ or indexed content no longer matches its hash
- **THEN** static validation exits with a nonzero status and identifies the mismatch

### Requirement: Custom mod distribution is explicit
Custom mods SHALL enter the pack through versioned downloads with content hashes. The initial empty pack MUST NOT be presented as a playable release containing the core mod.

#### Scenario: Only the initial skeleton exists
- **WHEN** the custom mod has not been published and added to pack metadata
- **THEN** documentation identifies the pack as an empty baseline with custom-mod integration and game acceptance pending

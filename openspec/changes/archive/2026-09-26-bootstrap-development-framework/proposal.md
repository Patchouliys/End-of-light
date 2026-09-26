## Why

The modpack needs a consistent AI workflow, target platform, code/pack boundaries, and separate static, build, and game-acceptance evidence.

## What Changes

- Add pinned OpenSpec tooling and project-level Minecraft guidance.
- Create a Java 21 / Minecraft 1.21.1 NeoForge core mod and Gradle wrapper.
- Create an empty packwiz baseline with matching game and loader versions.
- Add agent instructions, development guidance, ignore rules, and CI checks without game startup.

## Capabilities

### New Capabilities

- `development-workflow`: Specification-driven development and validation boundaries.
- `custom-mods`: Versioned custom-mod skeleton with client/server separation.
- `modpack`: Auditable packwiz dependency metadata.

### Modified Capabilities

None; this establishes the initial baseline.

## Impact

Adds development configuration, npm lockfile, Gradle wrapper, and GitHub Actions. No worlds, player data, gameplay, or third-party mods require migration.

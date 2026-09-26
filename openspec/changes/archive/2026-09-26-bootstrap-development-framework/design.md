## Context

End of Light targets Minecraft 1.21.1 + NeoForge and shares one repository for custom mods and pack metadata. Default checks cover static validation and compilation; game acceptance is separate.

## Goals / Non-Goals

**Goals:** A maintainable layout, usable specification tooling, aligned build versions, and explicit validation levels.

**Non-Goals:** Gameplay, third-party game mods, pack releases, and runtime acceptance.

## Decisions

1. Pin OpenSpec 1.13.2 with the `spec-driven` schema for artifact validation and archival. Avoid a second specification system.
2. Aggregate `mods/core` under Gradle, using the fixed NeoForge MDK as a reference, Java 21, and verified wrapper artifacts. Keep the entry point minimal.
3. Use packwiz metadata and keep only distributable content in `pack/`. Add the custom JAR through an immutable, hashed download after publication.
4. Keep the custom skill focused on versions, sides, persistence, dependencies, and evidence. Do not copy cross-version code or automatic game-launch steps from community skills.
5. Use common static/build commands in development and CI. CI also checks packwiz indexes and export format; no default task launches a game.
6. Retain all rights for original content and preserve third-party licenses.

## Risks / Trade-offs

- Static checks, compilation, and game acceptance provide distinct evidence.
- An empty mod build cannot establish gameplay or dedicated-server compatibility.
- Exact NeoForge pins prevent drift but require coordinated build/pack upgrades.
- Project instructions must constrain the general-purpose generated OpenSpec skills.

## Migration Plan

No existing data needs migration. Handle later version and compatibility changes through separate OpenSpec changes. Build configuration must not modify game instances.

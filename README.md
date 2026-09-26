# End of Light

A **Minecraft 1.21.1 + NeoForge** modpack and custom-mod workspace using **OpenSpec**, project-level AI skills, and **packwiz** metadata.

The initial `endoflight` mod contains only its entry point. No gameplay or third-party mods are included yet.

## Quick start

Requirements: Node.js 22+ (24 LTS recommended), Python 3.11+, and JDK 21 for compilation. The committed Gradle wrapper downloads Gradle.

```sh
npm ci --ignore-scripts
npm run check
./gradlew :core:build
```

Build output: `mods/core/build/libs/`. On Windows, use `gradlew.bat :core:build`. These commands do not launch Minecraft.

## AI development

Start with [AGENTS.md](AGENTS.md). Example request:

> Propose a light-decay mechanic with OpenSpec. Define server behavior, configuration, save compatibility, and acceptance scenarios before implementation.

Use `$openspec-propose` or `$minecraft-neoforge`, or ask the agent to read the corresponding `.agents/skills/*/SKILL.md` directly.

```sh
npm run spec -- new change add-light-decay
npm run spec -- instructions proposal --change add-light-decay
npm run spec -- status --change add-light-decay
npm run spec:validate
```

See [development](docs/development.md), [workflow](docs/workflow.md), [validation](docs/testing.md), and [references](docs/references.md). Repository documentation and specifications use English.

## Layout

| Path | Purpose |
| --- | --- |
| `mods/core/` | Custom NeoForge mod; Gradle project `:core` |
| `pack/` | packwiz metadata and distributable configuration |
| `openspec/specs/` | Current requirements |
| `openspec/changes/` | Active changes and archives |
| `.agents/skills/` | OpenSpec and Minecraft development skills |
| `docs/` | Development, validation, and dependency guidance |
| `.github/workflows/` | Automated development checks |

## Continuous integration

GitHub Actions checks specifications, compiles the mod with Java 21, and validates packwiz indexes and export format on main-branch pushes, pull requests, or manual dispatch. CI is optional automation for development; it neither launches games nor publishes releases.

## Pack maintenance

Install the pinned packwiz version as described in [development](docs/development.md). From `pack/`, add dependencies with `packwiz modrinth install <project-or-version-url>` or `packwiz curseforge install <project-or-file-url>`. Select Minecraft 1.21.1 / NeoForge versions, then run from the repository root:

```sh
npm run pack:refresh
npm run pack:check
```

Commit `.pw.toml` metadata and refreshed indexes, not downloaded JARs. The initial pack is empty and **does not include the custom mod's build output**. Add the mod through a versioned download with a content hash when it is published; see [dependencies](docs/dependencies.md).

No open-source license has been selected for original project content. See [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md).

# NeoForge 1.21.1 Documentation Index

Use this index when choosing documentation for a concrete feature. Read only the
relevant row, then follow links needed to resolve the actual question.

## Version and authority

- Target Minecraft 1.21.1 / Java 21. Read the exact NeoForge version from
  `gradle.properties` (initial baseline: 21.1.251).
- Use the [1.21.1 guide](https://docs.neoforged.net/docs/1.21.1/gettingstarted/).
  Its site label is **1.21 - 1.21.1**; it is not a promise of identical APIs across
  every NeoForge 21.1 patch release. Recheck the page version after redirects.
- Resolve signatures against the actual dependency sources. The initial version's
  [official source JAR](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.251/neoforge-21.1.251-sources.jar)
  is a fallback when resolved sources are unavailable. Update the coordinate when
  the dependency changes; do not commit dependency or decompiled game sources.
- For build-plugin questions, use [ModDevGradle](https://github.com/neoforged/ModDevGradle)
  documentation/source matching the plugin version in `build.gradle`. NeoGradle
  examples are not interchangeable with this project's plugin.

## Topics

Markdown paths are relative to `versioned_docs/version-1.21.1/` in the official
Documentation repository. `index.md` maps to the containing documentation URL.

| Task | Official chapter | Markdown path |
| --- | --- | --- |
| Mod metadata and dependency declarations | [Mod files](https://docs.neoforged.net/docs/1.21.1/gettingstarted/modfiles/) | `gettingstarted/modfiles.md` |
| Register items, blocks, or other content | [Registries](https://docs.neoforged.net/docs/1.21.1/concepts/registries/) | `concepts/registries.md` |
| Event handlers and event buses | [Events](https://docs.neoforged.net/docs/1.21.1/concepts/events/) | `concepts/events.md` |
| Shared logic versus client-only code | [Sides](https://docs.neoforged.net/docs/1.21.1/concepts/sides/) | `concepts/sides.md` |
| Item behavior and per-stack data | [Items](https://docs.neoforged.net/docs/1.21.1/items/) / [Data components](https://docs.neoforged.net/docs/1.21.1/items/datacomponents/) | `items/index.md`, `items/datacomponents.md` |
| Blocks, states, and persistent block behavior | [Blocks](https://docs.neoforged.net/docs/1.21.1/blocks/) / [Block entities](https://docs.neoforged.net/docs/1.21.1/blockentities/) | `blocks/index.md`, `blocks/states.md`, `blockentities/index.md` |
| Inventory and mod interoperability | [Capabilities](https://docs.neoforged.net/docs/1.21.1/inventories/capabilities/) | `inventories/capabilities.md` |
| Custom packets and synchronization | [Payloads](https://docs.neoforged.net/docs/1.21.1/networking/payload/) / [Stream codecs](https://docs.neoforged.net/docs/1.21.1/networking/streamcodecs/) | `networking/payload.md`, `networking/streamcodecs.md` |
| Entity/chunk attachments and world persistence | [Attachments](https://docs.neoforged.net/docs/1.21.1/datastorage/attachments/) / [Saved data](https://docs.neoforged.net/docs/1.21.1/datastorage/saveddata/) | `datastorage/attachments.md`, `datastorage/saveddata.md` |
| Mod configuration | [Configuration](https://docs.neoforged.net/docs/1.21.1/misc/config/) | `misc/config.md` |
| Recipes, tags, loot, and their data generators | [Recipes](https://docs.neoforged.net/docs/1.21.1/resources/server/recipes/) / [Tags](https://docs.neoforged.net/docs/1.21.1/resources/server/tags/) / [Loot tables](https://docs.neoforged.net/docs/1.21.1/resources/server/loottables/) | `resources/server/recipes/index.md`, `resources/server/tags.md`, `resources/server/loottables/index.md` |
| Models, generated models, and language files | [Models](https://docs.neoforged.net/docs/1.21.1/resources/client/models/) / [Model generation](https://docs.neoforged.net/docs/1.21.1/resources/client/models/datagen/) / [Localization](https://docs.neoforged.net/docs/1.21.1/resources/client/i18n/) | `resources/client/models/index.md`, `resources/client/models/datagen.md`, `resources/client/i18n.md` |
| Server menus and client screens | [Menus](https://docs.neoforged.net/docs/1.21.1/gui/menus/) / [Screens](https://docs.neoforged.net/docs/1.21.1/gui/screens/) | `gui/menus.md`, `gui/screens.md` |
| World generation changes | [Biome modifiers](https://docs.neoforged.net/docs/1.21.1/worldgen/biomemodifier/) | `worldgen/biomemodifier.md` |
| Plan runtime acceptance or performance measurement | [GameTest](https://docs.neoforged.net/docs/1.21.1/misc/gametest/) / [Debug profiler](https://docs.neoforged.net/docs/1.21.1/misc/debugprofiler/) | `misc/gametest.md`, `misc/debugprofiler.md` |

## Markdown fallback

Source: [NeoForged Documentation](https://github.com/neoforged/Documentation/tree/816c03d31ff7948179c7bd4a58d23bcfda09c18a/versioned_docs/version-1.21.1),
commit `816c03d31ff7948179c7bd4a58d23bcfda09c18a` (index reviewed 2026-09-26).
This pins documentation content, not the project's NeoForge binary version.

Fetch an individual Markdown file using the listed path, for example:

```text
https://raw.githubusercontent.com/neoforged/Documentation/816c03d31ff7948179c7bd4a58d23bcfda09c18a/versioned_docs/version-1.21.1/concepts/events.md
```

If an offline cache becomes useful, retain its source commit, paths, and upstream
license. Keep it outside tracked project content unless vendoring is explicitly
requested. Do not build the documentation website just to read Markdown. For a
topic absent from this table, inspect the same versioned directory before seeking
community examples. Revisit this index when the Minecraft target changes.

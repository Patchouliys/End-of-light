# Multiple Mods

Each immediate, non-hidden directory under `mods/` is one mod and Gradle project. Directory names use lowercase letters, digits, underscores, or hyphens, starting with a letter. Every module requires `build.gradle` and `mod.json`; incomplete modules fail discovery.

## Ownership

| Scope | Files |
| --- | --- |
| Shared platform | Root `gradle.properties`, wrapper, plugin version, `gradle/neoforge-mod.gradle` |
| One mod | `mods/<module>/mod.json`, `build.gradle`, `src/`, `build/` |
| Pack integration | `pack/`, dependency records, published download metadata |

The module directory, Mod ID, and Java class name are distinct. For example, directory `ecology` can declare Mod ID `eol_ecology` and entry point `io.github.patchouliys.ecology.EcologyMod`. Every module needs a unique Mod ID and primary entry point. Core retains its existing identity and is not a required base library.

## Add a module

Create only modules needed by an agreed feature. Add these files under `mods/<module>/`; no central module list or CI edit is required:

1. `build.gradle`, using the shared convention:

```groovy
plugins {
    id 'java-library'
    id 'net.neoforged.moddev'
}

apply from: rootProject.file('gradle/neoforge-mod.gradle')
```

2. `mod.json`, with all eight fields, for example:

```json
{
  "mod_id": "eol_ecology",
  "mod_name": "End of Light Ecology",
  "mod_version": "0.1.0",
  "mod_group_id": "io.github.patchouliys.ecology",
  "mod_license": "All Rights Reserved",
  "mod_authors": "Patchouliys",
  "mod_description": "Ecology features for End of Light.",
  "mod_entrypoint": "io.github.patchouliys.ecology.EcologyMod"
}
```

Keep Minecraft/NeoForge versions at the root. Versions must be filename-safe, such as `0.1.0` or `0.2.0-beta.1`. Display text is escaped during TOML generation.

3. `src/main/resources/META-INF/neoforge.mods.toml`: copy the platform/placeholder template from core, inspect it, and retain only dependencies intended for this module. Identity/display fields are expanded from this module's manifest.
4. The Java file matching `mod_entrypoint`, with the matching package and class. Annotate it with `@Mod(EcologyMod.MOD_ID)` and define `public static final String MOD_ID = "eol_ecology";`. Add only required feature code and resources under its namespace.

Do not copy another module's `build/`, generated outputs, caches, or gameplay implementation. Merely adding a module does not add its JAR to the distributable pack; follow [distribution guidance](dependencies.md) when publishing.

## Commands

Run from the repository root; replace `core` with the module directory name:

```sh
python3 scripts/check_workspace.py --list-modules
npm run check
./gradlew :core:build
./gradlew :core:check
./gradlew :core:clean
./gradlew :build
./gradlew :check
./gradlew :clean
```

Module tasks target one mod plus explicitly declared dependencies. Root tasks cover all modules. Each JAR is written to `mods/<module>/build/libs/<mod_id>-<mod_version>.jar`.

For shared build changes, run `python3 scripts/test_mod_builds.py` with Java 21 and dependency access. It creates temporary modules, verifies selective builds despite an unrelated compile error, aggregate failure/success, separate JAR contents, escaped metadata, and selective/aggregate cleaning. It never launches the game.

## Dependencies and parallel work

Modules have no automatic dependencies on each other. If one needs another, add an explicit Gradle dependency such as `implementation project(':core')` in the consuming module and the corresponding dependency with the other Mod ID and supported version range in its NeoForge metadata. Avoid cycles; do not copy sources across modules.

Use separate branches and worktrees for concurrent editing sessions. Keep each change scoped to its module and OpenSpec change. Coordinate shared tooling, pack, and baseline-spec edits before merging. Build scripts are configured together, so a broken sibling build script can still block a selective build; separate directories do not provide process or runtime isolation.

CI discovers modules and gives each one a build job with sibling cancellation disabled. Shared static/spec checks gate those jobs. Combined gameplay compatibility requires separate authorized game acceptance.

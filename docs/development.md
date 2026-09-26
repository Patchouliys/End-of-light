# Development

## Toolchain

- Minecraft 1.21.1, NeoForge 21.1.251, Java 21.
- Gradle wrapper 9.2.1 and ModDevGradle 2.0.147.
- OpenSpec 1.13.2, locked through npm; Node.js 24 recommended, Python 3.11+ for checks.
- Each `mods/<module>` directory is an independent Gradle subproject; `core` is the initial mod. Add modules only for concrete, independently maintained mods. See [module development](modules.md).

`gradle.properties` owns shared Minecraft/NeoForge versions; `mods/<module>/mod.json` owns each mod's identity and version; `pack/pack.toml` owns pack versions. Mod and pack releases may differ, but Minecraft and NeoForge versions must match. Handle upgrades in a focused OpenSpec change; avoid dynamic versions and snapshots.

Install development dependencies with `npm ci --ignore-scripts`. Compile with JDK 21 and `./gradlew :<module>:build`, or `./gradlew :build` for all modules, from the root; use `gradlew.bat` on Windows. Module builds do not implicitly build core or sibling mods.

## packwiz

Pin packwiz to commit `ef87d964f8cbd52b3b13ea42453ef322290e2b9e`:

```sh
go install github.com/packwiz/packwiz@ef87d964f8cbd52b3b13ea42453ef322290e2b9e
```

Add Go's bin directory to PATH. Install mods inside `pack/`, verifying game/loader versions, dependencies, sides, and distribution terms. After changing dependencies or configuration, run `npm run pack:refresh` and `npm run check` from the root.

CI checks canonical packwiz output. The Python checker validates recorded hashes; it does not replace packwiz. Keep game instances outside `pack/`, which contains only distributable metadata, configuration, scripts, and resources.

## Java and Minecraft

- Use UTF-8, four-space indentation, explicit imports, PascalCase classes, lowerCamelCase members, and UPPER_SNAKE_CASE constants.
- Use the owning module's `mod_id` namespace and `mod_group_id` package prefix with snake_case resource paths. Core retains `endoflight` and `io.github.patchouliys.endoflight`.
- Register content through version-matched NeoForge APIs. Do not access worlds during static initialization or add example content without a requirement.
- The logical server owns inventory, rewards, permissions, and persistent state. Keep client-only classes out of common initialization paths.
- Validate payload direction, sender, permissions, distance, and field bounds. Schedule world mutations on the game thread.
- Prefer resources for recipes, tags, loot, and localization. Visible features need valid models, textures, and `en_us` / `zh_cn` strings; do not generate empty resources for nonexistent content.
- Registry, save, and config changes need migration and rollback notes. Never silently discard player data.
- Use Mixin or access transformers only when documented extension points cannot solve the requirement; define the compatibility scope.

## Git and dependencies

Use `feat/<change-id>`, `fix/<change-id>`, or `chore/<topic>` branches and Conventional Commits, such as `feat(light): add decay configuration`. Prefer pull requests for ongoing work.

Use separate worktrees for simultaneous editing sessions, with one module/change per branch. Coordinate shared build, pack, and baseline-spec changes. Add normal commits; do not rewrite published history or force-push without a separate request.

Update lockfiles, `docs/dependencies.md`, and affected specs with dependency changes. Do not update unrelated dependencies. Keep mod JARs out of Git; the Gradle wrapper JAR is the explicit exception.

Original project content retains all rights. License changes, third-party redistribution, and releases require separate authorization.

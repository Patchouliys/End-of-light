# End of Light: Agent Instructions

## Start here

- Read `README.md`, `docs/development.md`, relevant `openspec/specs/`, and the active change.
- Use platform versions from `gradle.properties`, the Gradle wrapper properties, `pack/pack.toml`, and lockfiles; read each mod's identity/version from `mods/<module>/mod.json`. Target Minecraft **1.21.1**, **NeoForge**, and **Java 21**; do not mix Forge, Fabric, or newer Minecraft APIs.
- For mod, pack, or compatibility work, read `.agents/skills/minecraft-neoforge/SKILL.md`. OpenSpec skills are in adjacent `openspec-*` directories.
- Write repository documentation, specifications, and agent guidance in concise **English**. Match the user's language in conversation. Keep a single uppercase `AGENTS.md`.
- Document reusable project decisions and procedures only. Exclude personal account status, machine details, private paths, and one-off environment diagnostics.

## Specification workflow

- For gameplay, dependency, persistence, networking, or cross-module changes, create an OpenSpec change with proposal, specs, design, and tasks before implementation. Proceed with clearly authorized work without repeated confirmation.
- Documentation, formatting, and small fixes within existing requirements may be edited directly. Update specs when behavior changes.
- `openspec/specs/` is the current baseline; change specs are deltas. Archive completed work with `npm run spec -- archive <change> --yes`. Check off only completed tasks.
- Use the pinned `npm run spec -- ...` CLI. Keep project rules outside generated OpenSpec skills so tool updates do not overwrite them.

## Implementation boundaries

- Put each custom mod in `mods/<module>/` with its own `mod.json`, sources, resources, and build output. Follow `docs/modules.md` when adding modules. Keep distributable pack content in `pack/` and documentation in `docs/`.
- Prefer data or configuration for data changes. Add Java for behavior, persistence, networking, or rendering. Do not introduce KubeJS, Mixin, or extra frameworks without a concrete need.
- Use version-matched NeoForge registration APIs and `<mod_id>:<snake_case>` resource IDs from the owning module's manifest (`endoflight` for core). Preserve released IDs, config keys, and saved-data fields unless a migration is defined.
- Modules have no implicit dependency on core or each other. Declare intended cross-mod dependencies in both Gradle and NeoForge metadata. Keep code and resource changes within the owning module.
- Simultaneous editing sessions use separate branches and worktrees. Coordinate edits to shared build conventions, pack files, and baseline specs before merging; shared configuration failures can affect all modules.
- Keep client-only classes out of shared code. The logical server owns authoritative state. Validate network direction, permissions, and bounds; mutate world state on the correct thread.
- Resolve uncertain APIs from the 1.21.1 official docs or dependency sources, not newer examples.
- Include resources and localization for visible content. Track generated game data, but exclude caches, game instances, saves, and third-party JARs.

## Validation and delivery

- Default checks cover static validation and compilation. Do not launch clients, servers, GameTest, or game-initializing datagen, or accept EULA, without explicit authorization for game acceptance.
- Run `npm ci --ignore-scripts` and `npm run check`. Compile with JDK 21 using `./gradlew :<module>:build`, or `./gradlew :build` for all modules. Shared build changes also need `python3 scripts/test_mod_builds.py`. CI does not launch games.
- Test meaningful behavior: unit tests for pure logic; separately authorized game acceptance for world behavior. Do not add empty tests for coverage.
- Distinguish implementation, static checks, compilation, and runtime acceptance. Report unexecuted checks accurately; a build does not prove gameplay works.
- Before committing, run `git diff --check` and inspect staged files. Exclude credentials, personal paths, caches, and saves. Use `type(scope): summary` commit messages.
- Add normal commits on feature branches; do not amend published commits, rewrite history, or force-push unless separately requested.
- Releases and redistribution require their own authorization. Public source availability does not grant a project license; see `LICENSE`.

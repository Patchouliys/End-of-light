---
name: minecraft-neoforge
description: Develop End of Light custom NeoForge mods and packwiz modpack changes for Minecraft 1.21.1, covering version-specific APIs, logical sides, data compatibility and development-only validation. Use for gameplay, resources, mod dependencies or compatibility work in this repository.
---

# End of Light Minecraft Development

## Ground the change

Read `AGENTS.md`, `gradle.properties`, the owning module's `mod.json`,
`pack/pack.toml` and relevant OpenSpec specs/change. Use `docs/modules.md` for module setup.
Target Minecraft 1.21.1, NeoForge and Java 21. Read the exact loader version from
`gradle.properties`; do not infer it from a documentation branch.

## Consult the right documentation

- Before adding or changing a NeoForge API integration, use the
  [topic index](references/neoforge-docs.md) to select the relevant 1.21.1 chapter.
  Read that chapter and only the linked sections needed for the current task.
- Use documentation for concepts and the exact resolved dependency sources for
  signatures and implementation details. If they disagree, follow the project's
  pinned dependency and record the discrepancy alongside the relevant change.
- Fetch official Markdown when rendered pages are hard to inspect. The index
  provides a fixed source snapshot and retrieval paths; do not assume latest docs
  or an unversioned NeoForge branch describes the current dependency.
- If neither version-matched docs nor sources establish an API, state the uncertainty
  and defer that API-dependent claim. Never invent methods or silently use Forge,
  Fabric, newer Minecraft examples, or a general search snippet as proof.
- Keep references concise: link the consulted chapter or exact source file/symbol
  when explaining a non-obvious API choice. Do not copy whole manuals into the
  change or load every topic into context. Documentation examples do not authorize
  game startup; preserve this project's execution boundary.

For behavior, dependency, persistence or network changes, use the project's
OpenSpec workflow described in `docs/workflow.md`. A clear user request already
supplies authorization for development; ask only for material missing decisions.

## Deliver the smallest complete implementation

- Treat the agreed requirements and acceptance scenarios as the scope. Implement
  them end to end, including relevant failure cases; never substitute a partial
  feature merely because it is shorter. Defer speculative features and extension
  points, not required behavior.
- Inspect the existing flow before editing. Reuse project code, version-matched
  NeoForge APIs, standard-library features, or installed dependencies when suitable.
  Add a dependency or abstraction only when it solves a concrete current problem.
  Prefer readable code over one-liners and fix shared causes rather than symptoms.
- Existing data/config solutions belong in `pack/`; new Java behavior belongs in
  the owning `mods/<module>/`. Do not install KubeJS, Mixin, libraries or unrelated mods by default.
- Keep each mod's identity, version, sources, resources, and output independent. Do not
  assume a dependency on core; declare cross-mod dependencies in Gradle and loader metadata.
  Concurrent editing sessions use separate branches/worktrees and coordinate shared files.
- Use NeoForge registration APIs and the owning manifest's `mod_id` namespace. Add models,
  textures, tags, recipes and en_us/zh_cn strings when the actual feature needs them.
- Pure calculations can remain Java code with focused unit tests. World-dependent
  behavior requires later game acceptance; a Java compilation is not that evidence.

## Keep performance proportional to the requirement

- For tick, world, inventory, or network work, identify expected scale and update
  frequency. Avoid unbounded scans, blocking I/O on the game thread, and unchanged
  state broadcasts. Prefer bounded work and event-driven updates where semantics allow.
- Add caches, asynchronous work, pooling, or custom indexes only for an established
  bottleneck or a required workload that the simple implementation cannot support.
  Define invalidation and thread ownership when introducing them.
- Measure before/after under comparable workloads when claiming improvement.
  Without authorized runtime measurements, label performance expectations as
  unverified. Fewer lines and successful compilation are not performance evidence.

## Apply Minecraft-specific constraints

- Keep `net.minecraft.client` out of shared classes and static initialization paths.
  Read the [sides guide](https://docs.neoforged.net/docs/1.21.1/concepts/sides/)
  for physical distribution versus logical side; single-player still has a server.
- Make the logical server authoritative for inventory, rewards and persistent state.
  For [payloads](https://docs.neoforged.net/docs/1.21.1/networking/payload/), validate
  sender, direction, permission and bounds, and schedule world mutations on the
  appropriate game thread.
- Treat released registry IDs, saved-data fields and config keys as compatibility
  contracts. Describe migrations and recovery before changing them. Never test on
  the user's actual save or assume an old world can be downgraded.
- For pack dependencies, confirm exact game/loader versions, transitive dependencies,
  side and distribution terms. Update `.pw.toml`, refresh hashes and record provenance
  in `docs/dependencies.md`; do not check in downloaded JARs.

## Validate within this project's execution boundary

Run `npm run check` across all modules. Compile with `./gradlew :<module>:build` or
`./gradlew :build` for all modules where JDK 21 is available; CI discovers each module.
For shared build changes, also run `python3 scripts/test_mod_builds.py`. If packwiz is available, run `npm run pack:refresh` and inspect
its changes. The Python index check verifies recorded hashes; CI checks canonical packwiz output.

Default development checks cover static validation and compilation. Do not launch client,
server, GameTest or game-initializing datagen, or accept EULA, without explicit authorization
for game acceptance. Keep personal account status, machine details and one-off environment
diagnostics out of project documentation.

Report implemented files, actual static/build results and unexecuted runtime scenarios
separately. Keep required unexecuted gameplay acceptance pending in the change tasks.
See `docs/testing.md` for scenario selection and `docs/references.md` for source provenance.

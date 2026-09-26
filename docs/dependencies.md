# Dependencies and Distribution

No third-party game mods are included initially. Record each added dependency's source, pinned version, side, and distribution basis.

| Component | Version / source | Purpose | Distribution |
| --- | --- | --- | --- |
| Minecraft | 1.21.1 / Mojang | Target game | Not included in the repository |
| NeoForge | 21.1.251 / NeoForged Maven | Loader | Declared in packwiz; resolved for builds |
| End of Light | 0.1.0 / `mods/core` | Custom mod | Source skeleton; not included in the pack |

For each added mod, record its project URL, version/file ID, game/loader compatibility, `client` / `server` / `both` side, dependencies, license or distribution permission, configuration impact, and upgrade risks. Store download URLs and hashes in `.pw.toml`.

To add a custom mod to the pack: build a fixed commit, publish an immutable JAR to an authorized location, record its version and SHA-256/SHA-512, create `.pw.toml`, refresh the index, and arrange game acceptance. Do not use machine-specific paths or temporary URLs, or commit the JAR.

Use `packwiz modrinth export` or `packwiz curseforge export` for release packaging. An empty-pack export checks format only. Redistribute third-party files only under appropriate permissions.

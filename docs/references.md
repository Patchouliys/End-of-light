# Design References

Sources reviewed on 2026-09-26 for Minecraft 1.21.1 + NeoForge.

| Source | Use |
| --- | --- |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) / [CLI](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md) | Pinned 1.13.2 proposal, specification, design, task, validation, and archive workflow |
| [NeoForge 1.21.1](https://docs.neoforged.net/docs/1.21.1/gettingstarted/) | Java 21 and version-specific development APIs |
| [NeoForge MDK](https://github.com/NeoForgeMDKs/MDK-1.21.1-ModDevGradle/tree/4e1be6e906e1b32a753e3580af4ea1bcc3dbc79e) | Gradle 9.2.1, ModDevGradle 2.0.147, NeoForge 21.1.251, and launcher scripts; wrapper JAR from official Gradle v9.2.1 with its published checksum |
| [packwiz setup](https://packwiz.infra.link/tutorials/creating/getting-started/) / [dependencies](https://packwiz.infra.link/tutorials/creating/adding-mods/) | Versioned metadata and hashes, separate from game instances and downloaded JARs |
| [NeoForge sides](https://docs.neoforged.net/docs/1.21.1/concepts/sides/) / [payloads](https://docs.neoforged.net/docs/1.21.1/networking/payload/) | Client isolation, server authority, and validated network messages |
| [Codex skills](https://learn.chatgpt.com/docs/build-skills) | Project-scoped `.agents/skills/` and `SKILL.md` |

OpenSpec supplies the required artifacts and CLI validation without maintaining a second specification system. No additional Spec Kit workflow is included.

## Community Minecraft skills

- [Jahrome907/minecraft-agent-skills](https://github.com/Jahrome907/minecraft-agent-skills), MIT: useful guidance on identifying versions/loaders, logical sides, and API verification. Its cross-version examples are not treated as 1.21.1 API templates.
- [Riloox/minecraft-mod-builder](https://github.com/Riloox/minecraft-mod-builder/blob/main/SKILL.md): useful end-to-end requirements, code, and resources workflow. Its license was not established, so its content was not copied. Automatic game startup is outside the default workflow.

The project's `minecraft-neoforge` skill is original, repository-specific guidance, not an official NeoForge skill. No community scripts or instruction bundles were installed. Prefer versioned official documentation and actual compiler evidence.

# Specification Workflow

Use OpenSpec's `spec-driven` schema and the pinned project CLI.

1. **Propose:** Read current specs and versions. Describe scope and impact in `proposal.md`; define observable scenarios in delta specs.
2. **Design:** Explain modules, sides, compatibility, alternatives, and validation. Proceed with clear user requirements; ask only for material missing decisions.
3. **Implement:** Follow `tasks.md`, update code and pack metadata, and revise artifacts when decisions change. Mark only completed tasks.
4. **Validate:** Run static checks and compile with Java 21. CI automates these checks; game acceptance is separately authorized.
5. **Archive:** Record evidence and merge deltas into the baseline. Keep required gameplay acceptance pending until executed; infrastructure changes may finish within their agreed static/build scope.

```sh
npm run spec -- new change add-light-decay
npm run spec -- instructions proposal --change add-light-decay
npm run spec -- instructions specs --change add-light-decay
npm run spec -- instructions design --change add-light-decay
npm run spec -- instructions tasks --change add-light-decay
npm run spec -- status --change add-light-decay
npm run spec:validate
npm run spec -- archive add-light-decay --yes
```

Available skills: `openspec-propose`, `openspec-explore`, `openspec-apply-change`, `openspec-update-change`, `openspec-sync-specs`, and `openspec-archive-change`. Natural-language requests also work; use the CLI when client-specific skill commands are unavailable.

Write concise English artifacts with parser-compatible headings: `## ADDED Requirements`, `### Requirement:`, `#### Scenario:`, and `WHEN` / `THEN`. Use `MUST` or `SHALL` for requirements. Resolve overlapping changes before merging specs.

To upgrade OpenSpec, update its exact dependency version and lockfile, run `npm run spec -- update`, and inspect generated skill changes. Preserve the separately maintained `minecraft-neoforge` skill and avoid changing global AI configuration.

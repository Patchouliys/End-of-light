# Tasks

## 1. Module builds

- [x] 1.1 Add automatic discovery, module manifests, and shared build conventions; verify `:core` keeps its identity and a temporary second module has a distinct target and JAR.
- [x] 1.2 Document module creation and selective/aggregate commands; exercise the documented structure with a temporary module.

## 2. Validation and CI

- [x] 2.1 Check all module identities, metadata, entry points, and resources; add passing two-module and failing collision/incomplete/resource regression tests.
- [x] 2.2 Derive independent CI jobs from discovered modules; verify valid matrix JSON and disabled sibling cancellation, and document shared failure boundaries.

## 3. Development guidance

- [x] 3.1 Update agent/skill/OpenSpec guidance for module ownership, explicit dependencies, and separate concurrent worktrees; validate the skill and remove active single-mod assumptions.

## 4. Integration verification

- [x] 4.1 Run static checks, regression tests, and strict OpenSpec validation; inspect the diff for private data and unintended files.
- [x] 4.2 Build core and temporary independent modules with Java 21, verify selected/aggregate task behavior and JAR contents, and record only observed results.

Game startup and combined gameplay acceptance are outside this infrastructure change and remain separately authorized. No runtime compatibility claim is made.

## Verification

- `npm run check`: workspace/pack checks, 12 regression tests, and strict specification validation passed.
- `./gradlew :core:build` and `./gradlew :build`: Java 21 compilation and packaging passed; core retains its ID, version, and entry point.
- `python3 scripts/test_mod_builds.py`: passed selective build with an unrelated compile error, aggregate failure detection and recovery, separate JAR contents, escaped metadata, and selective/aggregate clean.
- Skill validation, CI YAML/matrix inspection, and `git diff --check`: passed. Hosted CI execution is separate from these checks.

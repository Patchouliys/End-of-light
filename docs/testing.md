# Validation

Default development checks cover static validation and compilation. They do not launch clients, servers, GameTest, or game-initializing datagen, or accept EULA. Arrange game acceptance separately with explicit authorization.

| Level | Method | Evidence |
| --- | --- | --- |
| Static checks | `npm run check` | Version alignment, metadata, pack hashes, and specification format |
| Build | `./gradlew :core:build` with JDK 21 | Compilation, resource processing, and JAR generation |
| Unit tests | Add when pure logic warrants tests | The tested algorithm's behavior |
| Game acceptance | Authorized test environment | Loading, rendering, world behavior, multiplayer, and compatibility |

A successful build does not prove that the mod loads. Gradle `test NO-SOURCE` means no tests ran. Static client-import checks cannot prove every dedicated-server class-loading path is safe.

Gameplay acceptance evidence should identify the commit, game/loader/Java versions, mod set, scenario, expected and actual results, and relevant artifacts. Exclude personal environment diagnostics from project documentation. Select scenarios relevant to the change:

- World entry, resources, localization, and errors.
- Dedicated-server startup and two-client multiplayer.
- Reconnection, dimension changes, save/reload, and old-save migration.
- Invalid, unauthorized, or excessive network requests.
- Mod combinations, configuration changes, tick performance, and memory behavior.

Record only executed results. Add runtime configurations when needed for authorized acceptance, and keep the default build free of game launches.

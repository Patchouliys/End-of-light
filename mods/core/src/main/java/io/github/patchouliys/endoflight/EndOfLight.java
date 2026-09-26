package io.github.patchouliys.endoflight;

import com.mojang.logging.LogUtils;
import net.neoforged.fml.common.Mod;
import org.slf4j.Logger;

/** Entry point for shared End of Light mod logic. */
@Mod(EndOfLight.MOD_ID)
public final class EndOfLight {
    public static final String MOD_ID = "endoflight";
    private static final Logger LOGGER = LogUtils.getLogger();

    public EndOfLight() {
        LOGGER.info("Initializing {}", MOD_ID);
    }
}

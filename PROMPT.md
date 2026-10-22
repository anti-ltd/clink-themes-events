# Authoring Clink Events themes

Preserve stable IDs, `source: eventsRepository`, and exactly two `pairedVariants` (one light, one dark). Use `palettes.json` and `tools/generate.py` as the editable source. Preserve each pair's distinct personality and readable labels. Themes must not modify typing, keyboard layout, geometry, long-press placement or premium customizations. Do not include user photos. Spacebar Canvas artwork lives in Artwork/ as small transparent PNGs and is embedded by the generator as keyArtworkImages. Its repo-art- ID is the PNG SHA-256; keep the complete document below 128,000 bytes. Each pair shares one illustration across appearances. Seasonal theme packs remain free and available after the event; gift eligibility is handled separately by the app.

Regenerate all packs and the manifest, run the repository tests, and inspect both appearances in the real iOS and Android renderers before publishing.

# Authoring Clink Events themes

Preserve stable IDs, `source: eventsRepository`, and exactly two `pairedVariants` (one light, one dark). Use `palettes.json` and `tools/generate.py` as the editable source. Preserve each pair's distinct personality and readable labels. Themes must not modify typing, keyboard layout, geometry, long-press placement or premium customizations. Do not include user photos or artwork references in official downloadable packs. Seasonal theme packs remain free and available after the event; gift eligibility is handled separately by the app.

Regenerate all packs and the manifest, run the repository tests, and inspect both appearances in the real iOS and Android renderers before publishing.

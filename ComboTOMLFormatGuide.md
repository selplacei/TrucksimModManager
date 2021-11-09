# TrucksimModManager's combo TOML format

TSMM uses TOML files as the way to keep track of mod combos. One file is all you need to download and install a combo; you can easily share these files with others; and they're human-readable enough to be edited directly. This guide tells you how to create or update a combo TOML.

Note that as of right now, this format is subject to change.

If you need a quick guide on TOML files in general, look [here](https://toml.io/en/v1.0.0).

## Metadata

Metadata is stored as key-value pairs in the root table, i.e. on the top level. The following keys are recognized (all values are strings unless otherwise indicated):

- `name`
- `author`
- `homepage`
- `version` - to work with the update mechanism, must be numbers separated by dots, i.e. `^(\d+\.)*\d+$`
- `game` - either `ets2` or `ats`
- `game_version` - either one value you would use in `compatible_versions` in `manifest.sii`, i.e. a game version like "1.42.0" that may have an asterisk as the last number, or a list of such values
- `description` - multiline strings encouraged
- `source` - direct link to a (dynamically updated) newest version of this combo for the most recent version of the game
- `version_check` - direct link to a version check file for the newest version of this combo, which must be formatted as the combo version followed by a newline and then the value of its `game_version`

Example (from AllTheMaps):

```toml
name = "AllTheMaps"
version = "1.42.03"
game = "ets2"
game_version = "1.42.*"
description = '''
All major compatible map mods.
Based on https://forum.scssoft.com/viewtopic.php?t=293794
All credit for making and testing the load order goes to Vinnie Terranova.
This combo does not include English localization mods.
'''
author = "selplacei"
homepage = "https://github.com/selplacei/TrucksimModManagerCombos"
source = "https://raw.githubusercontent.com/selplacei/TrucksimModManagerCombos/main/AllTheMaps/AllTheMaps.toml"
version_check = "https://raw.githubusercontent.com/selplacei/TrucksimModManagerCombos/main/AllTheMaps/version"
```

## Mods

All information pertaining to the actual mods is stored in the `[mods]` table.

A "mod", in the context of combo TOMLs, is a logical group of one or more .scs files that comprise a single "thing" that the user installs - for example, ProMods Europe or Poland Rebuilding. It's different from the game sense, where every .scs file is technically a separate mod.

Note that fixes, hotfixes, RCs, etc. are mods separate from the main mod.

### Names

Every mod is referred to by its name, which must be a valid TOML key (only alphanumeric characters, underscores, and dashes allowed). Names can be made human-readable either with a custom display string, or by having their underscores automatically replaced with spaces in TSMM's GUI if no custom display string is specified (so, for example, use `Poland_rebuilding` instead of `polandRebuilding` to save coding time). Custom display strings are specified in the `[mods.names]` table.

Example:

```toml
[mods.names]
    # If not specified here, it would display as "ProMods-RusMap connection vRusMap"
    ProMods-RusMap_connection_vRusMap = "ProMods-RusMap connection (RusMap Murmansk)"
```

### Descriptions

Currently not implemented.

### Images

Currently not implemented.

### Equivalents

An Equivalent is a sort of "virtual mod" that is made of one or more mods, and the user can choose which mods make it up. All of these options must be equivalent, i.e. have the same position in the final load order. Equivalents are specified in the `[mods.equivalents]` table; the keys are new Equivalents, which can be treated as normal mod names elsewhere, and the values are lists of options for the user to choose from. Each option is either a string containing a mod name, or a list of mod names, ordered from highest to lowest load order (currently, they all must end up directly adjacent to each other).

Example:

```toml
[mods.equivalents]
    Background = [
        ["Background_crash_fix", "Satellite_background"],
        ["Background_crash_fix", "SCS_style_background"],
        ["Background_crash_fix", "SCS_thin_style_background"],
        "Promods_Afroeurasia_background"
    ]
```

### Links

While optional, it's highly encouraged that every mod used in a combo has its download link(s) listed (after all, this is one of the main features of TSMM). Due to the fact that most mod makers want to make money or at least keep stats of their downloads, TSMM opens download links in the browser and expects the user to download files manually. Therefore, please use official download links if possible.

Links are stored in the `[mods.links]` table. Keys are mod names and values are either a single string or a list of strings that lead to different files that make up the mod. The strings are links to be opened in the browser, optionally prefixed with any of the following (in any order) to indicate something about the link:

- `$` - paid download available but not mandatory
- `#` - paid download only
- `!` - requires an account
- `%` - there is a concurrent download limit and the user should refer to the website for details

Links don't have to directly lead to a file; since the user will download mods manually, it can be a download site like MediaFire or even something like an entire forum thread. However, a link should only contain files for the mod that it's associated with, and it should be obvious to the user where to click; there should also be as little clicking and scanning as possible. So, for example, if a forum thread lists a bunch of ShareMods links, use those links in your TOML file instead of linking to the thread. (Another reason to do this is that thread-type links may be updated over time, potentially breaking your combo.)

Note that it's fine for the downloads to be archives rather than .scs files - dealing with this is explained further down.

Sharemods links are treated in a special way that saves you coding time (more on this later), so use them if given the choice.

Example:

```toml
[mods.links]
    ProMods_Afroeurasia_background = "!https://truckymods.io/euro-truck-simulator-2/ui/promods-complete-afroeurasia-background-map/download/latest"
    ProMods = "$!%https://www.promods.net/setup.php?game=ets"
    The_Great_Steppe = [
        "https://sharemods.com/tddscfu85ddv/The_Great_Steppe_v2.0.zip.html",
        "https://sharemods.com/53dq8u1k8b2i/The_Great_Steppe_v2.0.z01.html",
        "https://sharemods.com/2yuzcjchx0kc/The_Great_Steppe_v2.0.z02.html"
    ]
```

### Filenames

For TSMM to do anything meaningful with downloaded mods, it must know what files it's associated with. Therefore, each mod must be associated with one or more filenames.

Mods that are made of only one downloaded file, a multi-part archive, or multiple archives are listed in the `[mods.filenames]` table. The key is the mod name and the value is the filename or list of archive filenames. Note that if a mod has been listed in `[mods.links]` and its link(s) are from ShareMods, TSMM will automatically detect the filename(s), so it doesn't have to be specified here.

For multi-part archives (only ZIP and 7z are supported), list them as a single filename with a .zip or .7z extension, respectively (TSMM will automatically detect other parts).

Mods that are made of multiple .scs files but don't have to be unarchived should not be listed here; they will be specified in the load order.

Example:

```toml
[mods.filenames]
    Background_crash_fix = "CRASHFIX_HUGE_COMBOS.scs"
    Satellite_background = "ETS2_LAMB_EU-AF-AS-OC_SAT_BG_v1.2_unzip_me.zip"
    RusMap = "RusMap_2.4.2.7z"
    WeirdMod = ["WeirdMod_def_unzip.7z", "WeirdMod_assets_unzip.7z"]
```

### Special mods

Currently, there are two types of mods that have to be treated in a special way. These mods are listed as elements of lists in the `[mods.special]` table. A mod can be in multiple special lists.

- `extract` - Any mod whose download file(s) are archives. While the archive names are listed in `[mods.filenames]` or deduced from ShareMods links, the corresponding mods must be listed here for TSMM to extract them.
- `update` - Mods whose `manifest.sii` file must be edited to be compatible with the game version specified in the combo's metadata. TSMM will add the value of `game_version` specified in the combo to the `compatible_versions` list.

Example:

```toml
[mods.special]
    extract = [
        "Satellite_background",
        "RusMap"
    ]
    update = [
        "Latvia_rebuild",
        "AfroMap"
    ]
```

### Load order

The load order is specified in the `mods.order` list, with entries to the left being above (higher priority) than on the right. Each element of the list is one of the following:

- A mod name - only allowed for mods that are either Equivalents or have a single .scs file (which could be extracted from an archive)
- A mod name followed by a slash and a filename - unlike the `[mods.filenames]` table, this specifies names of .scs files, whether they were downloaded separately or extracted from an archive
- An optional mod/feature specified as a list where the first element is a human-readable description of a feature, the second element is one of the above two things to be enabled if the feature is desired, and an optional third element to be enabled otherwise (note that entries with the same first element will be grouped together in the UI's list of features to enable)

Example:

```toml
mods.order = [
    "Background",
    [
        "Remove Black Sea ferries",
        "No_Black_Sea_ferries"
    ],
    "ProMods-RusMap_connection",
    "RusMap/RusMap-map_v2.4.2.scs",
    "RusMap/RusMap-model_v2.4.2.scs",
    "RusMap/RusMap-model2_v2.4.2.scs",
    [
        "Special Transport DLC",
        "North_Macedonia_rework/Macedonia_rework_def_st.scs",
        "North_Macedonia_rework/Macedonia_rework_def.scs"
    ],
    "North_Macedonia_rework/Macedonia_rework_map.scs",
    "North_Macedonia_rework/Macedonia_rework_mat&asset.scs",
    [
        "Special Transport DLC",
        "Poland_rebuilding/zz_PL_Rebuilding_2.5.2_ST.scs"
    ],
    "Poland_rebuilding/z1_PL_Rebuilding_2.5.2_def.scs",
    "Poland_rebuilding/z1_PL_Rebuilding_2.5.2_map.scs",
    # ... Other Poland Rebuilding files
    "ProMods/promods-def-v257.scs",
    "ProMods/promods-map-v257.scs",
    # ... Other ProMods files
    "RusMap/RusMap-def_v2.4.2.scs"
]
```

# TunerStudio tune files (Speeduino, rusEFI/FOME, MegaSquirt)

Reads tune files (.msq). TunerStudio logs (.mlg, .msl) are not read.

`parser/adapter.py` reads `.msq` XML and maps each family's tables to canonical roles:

| Role | Speeduino | rusEFI | MegaSquirt |
|---|---|---|---|
| ve | veTable / rpmBins / fuelLoadBins | veTable / veRpmBins / veLoadBins | veTable1 / frpm_table1 / fmap_table1 |
| ign_base | advTable1 / rpmBins2 / mapBins1 | ignitionTable / ignitionRpmBins / ignitionLoadBins | advanceTable1 / srpm_table1 / smap_table1 |
| lambda_target | afrTable / rpmBinsAFR / loadBinsAFR | lambdaTable / lambdaRpmBins / lambdaLoadBins | afrTable1 / arpm_table1 / amap_table1 |
| boost_target | boostTable / rpmBinsBoost / tpsBinsBoost | boostTableOpenLoop / boostRpmBins / boostTpsBins | not mapped |

Format notes:
- Row 0 of a table is the lowest load bin; columns follow the rpm bins.
- Older rusEFI files omit `rows`/`cols`; arrays are reshaped only when their length equals the bin product.
- Unused trailing bins repeat or fall; only the leading increasing part of each axis is used.
- Target tables are often stored as AFR; they are converted to lambda with the tune's own stoichiometric ratio.
- The load axis is taken as manifold pressure unless the fuel algorithm or bin units say throttle.
- MegaSquirt table names follow the MS documentation.

The XML parser refuses files with a DOCTYPE or entity declarations.

# Common Properties (RQ1)
This directory contains the analysis of common properties and patterns of static analysis issues. It answers RQ1 of the paper.

## Contents
- 'collect_specific_datapoints.ipynb': This notebook contains code of specific datapoints that are used in the paper.
- 'common_properties_figures.ipynb': This notebooks contains code to generate the figures from the common properties calculated in 'generate_common_properties.ipynb'. It produces the figures used in Figure 2. (Results can be found [here](../../results/figures/common_properties))
- 'generate_common_properties.ipynb': This notebook contains code to generate the common property statistics from the dataset.
- 'investigation.ipynb': This notebook contains code for investigating special or interesting observations from the results of the common properties (ex. the high number of LoC in certain issues) (Results can be found [here](../../results/csv/common_properties/investigation.csv)).
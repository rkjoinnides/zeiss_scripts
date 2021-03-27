The tif_extractor script is designed to extract metadata from a SmartSEM .tif images and place this information into
a csv file. The runtime behavior of the script can be modifed using the tif_extractor_config.ini file. This file also
contains a field "parameter selection mode". The relevant options for this are 0 (inclued all), 1 (include only 
parameters in the parameter section), or 2 (exclude parameters in the paramter section).
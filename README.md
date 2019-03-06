# MIBI_TMA_Solution
No more manual selection for TMA sample on MIBIscope, interactive srcipt to generate spots in XML file for miniMIBI.

1. (script) take in carousel image acquired by MIBI camera, based on (user) settings, process image and search for TMA spots
2. (user) manually adjust the position with SED for the cross labeled TMA spot from step 1 in miniMIBI, save a xml file
3. (script) add all other spots founded, correct error and write the positions and points into a XML file that read by miniMIBI software

Python 3.6.4, openCV

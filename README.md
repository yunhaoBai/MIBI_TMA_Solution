# MIBI_TMA_Solution
Python 3.6.4

No more manual selection for TMA sample on MIBIscope! Srcipts to generate spots in XML file for miniMIBI automatically.

1. (script) take in carousel image acquired by MIBI camera, based on (user) settings, process image and search for TMA spots  
2. (user) manually adjust the position with SED for the cross labeled TMA spot from step 1 in miniMIBI, save a xml file  
3. (script) add all other spots founded, correct error and write the positions and points into a XML file that read by miniMIBI software  
  
For the TMA_cutting.py:  
Parameter:   
[1] name of carousel image  
[2] type of TMA, choose from 'LRG' and 'SML', 'LRG' for 1.5 mm size TMA, 'SML' for 0.6 mm size TMA     
[3] position of sample, 'UP' indicate to process the upper slot of sample holder, 'DOWN' is the lower one.  
User operation.  
[4] xmlfilename: the name of XML file generated in user step  
  
> python TMA_cutting.py 081318_Ionpath_TMA_Tonsil.jpg[1] LRG[2] UP[3]  
> length of cnts: 64   
(pop-up an image)   
<img src=https://github.com/yunhaoBai/MIBI_TMA_Solution/blob/master/Sample_TMA_LRG_contour.png alt="drawing" width="500"/>

(Check the cross labeled region on popped-up carousel image (it will also be saved to current directory), use SED to adjust your position, then do all setup for this spot(depth/dwelling time, etc.), save the XML file. Close the popped-up image.)  
> Please input the XML file name with the selected point and settings.  
> please enter the name of xml File: test.xml[4]  
  
(got a xml file named ALL_test.xml)

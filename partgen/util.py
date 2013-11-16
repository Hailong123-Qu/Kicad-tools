#!/usr/bin/python
############################################################################
############################################################################
"""
##  util - Utility Functions used in Part Gen
## 
##  Designed by
##         A.D.H.A.R Labs Research,Bharat(India)
##            Abhijit Bose( info@adharlabs.in )
##                http://ahdarlabs.in
##
## License:
## Apache License, Version 2.0
"""
##
## Version History:
## version 0.0 - Initial Release (2013-02-22)
##
############################################################################
############################################################################
#IMPORTS>
############################################################################
############################################################################
#EXPORT>
############################################################################
__author__      = "Abhijit Bose(info@adharlabs.in)"
__author_email__= "info@adharlabs.in"
__version__     = "0.0"
__copyright__   = "Copyright (c) 2013, ADHAR Labs Research"
__license__     = "Apache License, Version 2.0"
############################################################################
#DEFINES>
############################################################################
############################################################################
#CLASSES>Lib
############################################################################
def mmtomil(mm):    
    ''' Function to convert the mm into mils even when its a string
         and return accordingly '''
    #{
    s = 0 #Status Var
    
    # First Check if the Type of input is a string
    if (type(mm) == type(" ")):
        #{
        try:
            mm = float(mm)
            s = 1 #Type conversion Successful
        except:
            raise Exception("Type Conversion Fault")
        #}
    # Now Convert the units
    mil = mm * 1000.0/25.4
    # Check if the Type was a String
    if s==1:
        mil = "%f"%mil #Convert to String
    return mil
    #}

def miltomm(mil):
    ''' Function to convert the mils into mm even when its a string
     and return accordingly '''
    #{
    s = 0 #Status Var
    
    # First Check if the Type of input is a string
    if (type(mil) == type(" ")):
        #{
        try:
            mil = float(mil)
            s = 1 #Type conversion Successful
        except:
            raise Exception("Type Conversion Fault")
        #}
    # Now Convert the units
    mm = mil * 25.4/1000
    # Check if the Type was a String
    if s==1:
        mm = "%f"%mm #Convert to String    
    return mm
    #}
    
############################################################################
# Main FUNCTION>
############################################################################
if __name__ == "__main__" :
    #{
    print (__doc__)
    print("This is an Support Module")
    print()
    print("Converting 20 mm to mil :%f"%(mmtomil(20)))
    print("Error Status: " + error_status)
    print()
    print("Converting 20 mil to mm :%f"%(miltomm(20)))
    print("Error Status: " + error_status)
    #}
############################################################################

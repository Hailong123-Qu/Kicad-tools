#!/usr/bin/python
############################################################################
############################################################################
"""
##  libcls - Classes for Generating the Schematics Library of Kicad
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
import os
from time import strftime, localtime
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
class libComponent:
    """ Abstract Base Class to define the Internals of a Component
        Object for of This Class type cant be created
        This would be included into several sub Classes to make custom
        components.
    """
    #{
    ##########################################
    ## Private Variables
    _name = "" #Component Type
    _valid = False #if Component is Valid
    ##########################################
    ## Public Variables
    ComponentName = "" # Component Name
    RefenceDesignator = "" # RefDes
    Description = "" # Description
    Keywords = [] #Array of Keywords
    FootprintList = [] #Array of Footprints
    compNameX = 0 #in Mils
    compNameY = 0 #in Mils
    compNameFontSize = 50
    refDesX = 0 #in Mils
    refDesY = 0 #in Mils
    refDesFontSize = 50
    bodyTopLeftX = 0 #in Mils
    bodyTopLeftY = 0 #in Mils
    bodyBottomRightX = 0 #in Mils
    bodyBottomRightY = 0 #in Mils
    pinNameVisible = True
    pinNumberVisible = True
    ComponentUnitsIdenticle = True
    pinNameTextOffset = 40
    TotalPins = 0 #Total Number of Pins
    pins = [] #Array Containing the Pin Text
    draws = [] #Array Containing Drawing Items
    pinspec = [] # Array Containing the [Pin Name,EType] tuples
    ComponentText = "" # Text String containing the Entire component
    DescriptionText = "" # Description Text
    ##########################################
    ## Constructor Functions
    def __init__(self):
        #{
        if self.__class__ != libComponent:
            self._valid = True
        else:
            raise Exception("Error Can call the Base Class Constructor")
        self._validate()
        #}
    ##########################################
    ## Private Functions
    def _validate(self):
        #{
        try:
            libComponent(self)
        except TypeError as e:
            # We do this for compatibility with py2.3
            raise Error(str(e))
        #}
    ##########################################
    ## Public Functions        
    def validate(self):
        if self._valid == False:
            raise TypeError("Error in Component Type")
    ############################
    def clear(self):
        """ Function to Clear the Data from the class """
        #{
        self.ComponentName = "" # Component Name
        self.RefenceDesignator = "" # RefDes
        self.Description = "" # Description
        self.Keywords = [] #Array of Keywords
        self.FootprintList = [] #Array of Footprints
        self.compNameX = 0 #in Mils
        self.compNameY = 0 #in Mils
        self.compNameFontSize = 50
        self.refDesX = 0 #in Mils
        self.refDesY = 0 #in Mils
        self.refDesFontSize = 50
        self.bodyTopLeftX = 0 #in Mils
        self.bodyTopLeftY = 0 #in Mils
        self.bodyBottomRightX = 0 #in Mils
        self.bodyBottomRightY = 0 #in Mils
        self.pinNameVisible = True
        self.pinNumberVisible = True
        self.ComponentUnitsIdenticle = True
        self.pinNameTextOffset = 40
        self.TotalPins = 0 #Total Number of Pins
        self.pins = [] #Array Containing the Pin Text
        self.draws = [] #Array Containing Drawing Items
        self.pinspec = [] # Array Containing the [Pin Name,EType] tuples
        self.ComponentText = "" # Text String containing the Entire component
        self.DescriptionText = "" # Description Text
        #}
    ############################
    def Populate(self):
        """ Abstract Function to Add the Pins and Drawings
            as per the location co-ordinates
            (Need to be implemented in Derived Classes)
        """
        pass
    ############################
    def RectInsert(self,startx,starty,endx,endy,thick=0,fill='N'):
        """ Function to Add a Rectangle to the Drawing Items """
        #{
        self.validate()
        # check the fill type
        if not fill in ('N','F','f'):
            raise Exception("Error in Fill Type")
        self.draws.append("S %d %d %d %d 0 1 %d %c"%( \
            startx,starty,endx,endy,thick,fill))
        #}
    ############################
    def CircleInsert(self,posx,posy,radius,thick=0,fill='N'):
        """ Function to Add a Rectangle to the Drawing Items """
        #{
        self.validate()
        # check radius
        if radius < 1:
            raise Exception("Error in Radius")
        # check the fill type
        if not fill in ('N','F','f'):
            raise Exception("Error in Fill Type")
        self.draws.append("C %d %d %d 0 1 %d %c"%( \
            posx,posy,radius,thick,fill))
        #}
    ############################
    def TextInsert(self,posx,posy,stext,size=100,orient=0,face="Normal",
                   bold=0,AlignV='C',AlignH='C'):
        """ Function to Add a Rectangle to the Drawing Items """
        #{
        self.validate()
        # check the orientation
        if not orient in (0,1):
            raise Exception("Error in Orientation Type")
        # check the face type
        if not face in ("Normal","Italic"):
            raise Exception("Error in Font Face Type")
        # check the Bols type
        if not bold in (0,1):
            raise Exception("Error in Font Bold Type")
        # check Alignment for Horizontal
        if not AlignH in ('C','R','L'):
            raise Exception("Error in Horizontal Alignment")
        # check Alignment for Vertical
        if not AlignV in ('C','T','B'):
            raise Exception("Error in Vertical Alignment")
        self.draws.append("T %d %d %d %d 0 0 0 %s  %s %d %c %c"%( \
            orient,posx,posy,size,stext,face,bold,AlignH,AlignV))
        #}
    ############################
    def pinInsert(self,PinNumber,PinName,posX,posY,Etype ='P',length=150, \
                 orientation='R',PinNumberTextSize=50,PinNameTextSize=50):
        """ Function to Add a Pin to the Pin Array """
        #{
        self.validate()
        # check Pin Number
        if PinNumber < 1:
            raise Exception("Error Pin Number Specified is Wrong")
        #check the EType of the Pin
        if not Etype in ('I','O','B','T','P','U','W','w','C','E','N'):
            raise Exception("Error in EType of Pin")
        # check for Lenght to be zero
        if length < 1:
            raise Exception("Error in Length of the Pin")
        # Check the orientation of the Pins
        if not orientation in ('U','D','R','L'):
            raise Exception("Error in Orientation of Pin")
        #add to the Pin Array
        self.pins.append("X %s %d %d %d %d %c %d %d 1 1 %c"%(\
            PinName,PinNumber,posX,posY,length,orientation, \
            PinNumberTextSize,PinNameTextSize,Etype))
        #}
    ############################
    def GenPinFromSpec(self,posx,posy,nStartFrom,nTotalPins, \
                       side,gentype='N'):
        """ Function takes an array of pin spec parameters
            To generate the pins of the component
            Pin Spec Array Format - [[Pin Name,EType],[..],...]
            Side - L(Left Side),R(Right Side),T(Top),B(Bottom)
               LN(Left Reverse),RN(Right Reverse),TN(Top Reverse),
               BN(Bottom Reverse)
            gentype - N(Normal All pins),E(Even Pins),O(Odd Pins)
            nStartFrom - Pin Number Starting
            nTotalPins - Total Number of Pins from the Begining
            """
        #{
        self.validate()
        # check the Side and Change orientation to suit Kicad
        if side == 'L' or side == 'LN':
            orient = 'R'
        elif side == 'R' or side == 'RN':
            orient = 'L'
        elif side == 'T' or side == 'TN':
            orient = 'D'
        elif side == 'B' or side == 'BN':
            orient = 'U'
        else:
            raise Exception("Error in Side Specifications")            
        # check for gentype
        if gentype == 'N':
            it = 1
        elif gentype == 'E':
            if nStartFrom%2 != 0:
                raise Exception("Cant start pin placement at Even order")
            it = 2
        elif gentype == 'O':
            if nStartFrom%2 == 0:
                raise Exception("Cant start pin placement at Odd order")
            it = 2
        else:
            raise Exception("Error in Generation Type Specifications")
        # check for size
        nStartFrom = int(nStartFrom - 1) #Zero Adjustment
        if nTotalPins > len(self.pinspec[nStartFrom:]):
            raise Exception("Error in Size Specification")
        # initialize counters
        y = int(posy)
        x = int(posx)
        # loop throught the Pins
        for i in range(nStartFrom,int(nStartFrom+nTotalPins),it):
            #{
            if side in ('L','R','LN','RN'):
                self.pinInsert(i+1,self.pinspec[i][0],posx,y, \
                               self.pinspec[i][1],150,orient)
                if side in ('L','R'):
                    y = int(y-100) #Decrement the Y axis
                else:
                    y = int(y+100) #increment the Y axis
            else:
                self.pinInsert(i+1,self.pinspec[i][0],x,posy, \
                               self.pinspec[i][1],150,orient)
                if side in ('T','B'):
                    x = int(x+100) #increment the X axis
                else:
                    x = int(x-100) #Decrement the X axis
            #}
        #}
    ############################
    def addCompHeader(self):
        """ Function to Generate the header needed for the Component
            defintion in the Lib
        """
        #{
        self.validate()
        self.ComponentText += "#\n"
        self.ComponentText += "# %s\n"%self.ComponentName
        self.ComponentText += "#\n"
        # decide on visibility
        if self.pinNameVisible == True:
            pinV = 'Y'
        else:
            pinV = 'N'
        if self.pinNumberVisible == True:
            numV = 'Y'
        else:
            numV = 'N'
        self.ComponentText += "DEF ~%s %s 0 %d %c %c 1 F N\n"%( \
            self.ComponentName,self.RefenceDesignator, \
            self.pinNameTextOffset,numV,pinV)
        self.ComponentText += "F0 \"%s\" %d %d %d H V C C N N\n"%( \
            self.RefenceDesignator,self.refDesX,self.refDesY, \
            self.refDesFontSize)
        self.ComponentText += "F1 \"%s\" %d %d %d H V C C N N\n"%( \
            self.ComponentName,self.compNameX,self.compNameY, \
            self.compNameFontSize)
        if len(self.FootprintList) != 0:
            self.ComponentText += "$FPLIST\n"
            for cm in self.FootprintList:
                self.ComponentText += " " + cm + "\n"
            self.ComponentText += "$ENDFPLIST\n"
        self.ComponentText += "DRAW\n"
        #Make Description
        self.DescriptionText += "#\n"
        self.DescriptionText += "$CMP %s\n"%(self.ComponentName)
        #}
    ############################
    def addDetails(self):
        """ Function to Add Drawing parts and Pins to the Component """
        #{
        self.validate()
        # Add the Drawing Parts
        for a in self.draws:
            self.ComponentText += a + "\n"
        # Add Pins
        for b in self.pins:
            self.ComponentText += b + "\n"
        # Description
        self.DescriptionText += "D %s\n"%(self.Description)
        #Keywords
        self.DescriptionText += "K"
        for k in self.Keywords:
            self.DescriptionText += " %s"%(k)
        self.DescriptionText += "\n"
        #}
    ############################
    def addCompFooter(self):
        """ Function to generate the Component Footer"""
        #{
        self.validate()
        self.ComponentText += "ENDDRAW\n"
        self.ComponentText += "ENDDEF\n"
        self.DescriptionText += "$ENDCMP\n"
        #}
    ############################
    def ToString(self):
        """ Generates the Complete component """
        #{
        self.validate()
        self.addCompHeader()
        self.addDetails()
        self.addCompFooter()
        return self.ComponentText
        #}
    ############################
    def PrintDetails(self):        
        """ Function to Print the Details of the component """
        #{
        print("Component Name: " + self.ComponentName)
        print("Refence Designator: " + self.RefenceDesignator)
        print("Total Number of Pins: " + str(self.TotalPins))
        print("Component Name (X,Y) : ( %d , %d )"%( \
            self.compNameX,self.compNameY))
        print("Reference Designator (X,Y) : ( %d , %d )"%( \
            self.refDesX,self.refDesY))
        print("Body TopLeft (X,Y) : ( %d , %d )"%( \
            self.bodyTopLeftX,self.bodyTopLeftY))
        print("Body BottomRight (X,Y) : ( %d , %d )"%( \
            self.bodyBottomRightX,self.bodyBottomRightY))
        print("Pins Spec Created: ",self.pinspec)
        print("Pins Array: ",self.pins)
        print("Component Text:")
        print(self.ComponentText)
        print("Description Text:")
        print(self.DescriptionText)
        #}
    ##########################################
    #}
##################################################
class libDIPpack(libComponent):
    #{
    ##########################################
    ## Private Variables
    _name = "DIP" #Component Type
    _valid = True #if Component is Valid
    ##########################################
    ## Public Variables    
    ##########################################
    ## Constructor Functions
    def __init__(self,compName,nPins,refDes='U',Descript="", Keyword=None, \
                 Footprints=None,PinNames=None,PinETypes=None):
        #{
        if nPins%2 != 0:
            raise Exception("Error DIP package needs even number of Pins")
        self.clear()
        self.ComponentName = compName
        self.RefenceDesignator = refDes
        self.TotalPins = nPins        
        self.compNameX = 0        
        self.refDesX = 0
        self.refDesY = 50
        sz = 3 + 1 # Default Name Size of 3Chars + 1 space
        # Create Default Pin Set
        for i in range(nPins):
            if PinNames == None:
                self.pinspec.append([str(i+1),'P'])
            else:
                if len(PinNames[i]) > (sz-1):
                    sz = len(PinNames[i])+1
                if PinETypes == None:
                    self.pinspec.append([PinNames[i],'P'])
                else:
                    self.pinspec.append([PinNames[i],PinETypes])
        # Asign Coordinates
        self.bodyTopLeftX = int(-50*sz) #in Mils
        self.bodyTopLeftY = 0 #in Mils
        self.bodyBottomRightX = int(50*sz) #in Mils
        self.bodyBottomRightY = int(-100*((self.TotalPins/2)+1))#in Mils
        self.compNameY = int(self.bodyBottomRightY - 50)
        # Add Description
        if Descript == "":
            self.Description = "DIP IC"
        else:
            self.Description = Descript
        # Add the Keywords
        if Keyword == None:
            self.Keywords.append(self.ComponentName)
        else:
            for a in Keyword:
                self.Keywords.append(a)
        # Add the Footprints
        if Footprints != None:
            for a in Footprints:
                self.FootprintList.append(a)
        #}
    ##########################################
    ## Public Function
    def Populate(self):
        #{
        self.RectInsert(startx=self.bodyTopLeftX, \
            starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
            endy=self.bodyBottomRightY,thick=0,fill='N')
        self.GenPinFromSpec(self.bodyTopLeftX-150,self.bodyTopLeftY-100, \
            nStartFrom=1,nTotalPins=(self.TotalPins/2), \
            side='L',gentype='N')
        self.GenPinFromSpec(self.bodyBottomRightX+150, \
            self.bodyBottomRightY+100,nStartFrom=(self.TotalPins/2)+1, \
            nTotalPins=(self.TotalPins/2),side='RN',gentype='N')
        #}    
    ##########################################
    #}
##################################################
class libCONN12pack(libComponent):
    #{
    ##########################################
    ## Private Variables
    _name = "CONN12" #Component Type
    _valid = True #if Component is Valid
    ##########################################
    ## Public Variables    
    ##########################################
    ## Constructor Functions
    def __init__(self,compName,nPins,refDes='U',Descript="", Keyword=None, \
                 Footprints=None,PinNames=None,PinETypes=None):
        #{
        if nPins%2 != 0:
            raise Exception("Error CONN12 package needs even number of Pins")
        self.clear()
        self.ComponentName = compName
        self.RefenceDesignator = refDes
        self.TotalPins = nPins        
        self.compNameX = 0        
        self.refDesX = 0
        self.refDesY = 50
        sz = 3 + 1 # Default Name Size of 3Chars + 1 space
        # Create Default Pin Set
        for i in range(nPins):
            if PinNames == None:
                self.pinspec.append([str(i+1),'P'])
            else:
                if len(PinNames[i]) > (sz-1):
                    sz = len(PinNames[i])+1
                if PinETypes == None:
                    self.pinspec.append([PinNames[i],'P'])
                else:
                    self.pinspec.append([PinNames[i],PinETypes])
        # Asign Coordinates
        self.bodyTopLeftX = int(-50*sz) #in Mils
        self.bodyTopLeftY = 0 #in Mils
        self.bodyBottomRightX = int(50*sz) #in Mils
        self.bodyBottomRightY = int(-100*((self.TotalPins/2)+1))#in Mils
        self.compNameY = int(self.bodyBottomRightY - 50)
        # Add Description
        if Descript == "":
            self.Description = "DIP IC"
        else:
            self.Description = Descript
        # Add the Keywords
        if Keyword == None:
            self.Keywords.append(self.ComponentName)
        else:
            for a in Keyword:
                self.Keywords.append(a)
        # Add the Footprints
        if Footprints != None:
            for a in Footprints:
                self.FootprintList.append(a)
        #}
    ##########################################
    ## Public Function
    def Populate(self):
        #{
        self.RectInsert(startx=self.bodyTopLeftX, \
            starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
            endy=self.bodyBottomRightY,thick=0,fill='N')
        self.GenPinFromSpec(self.bodyTopLeftX-150,self.bodyTopLeftY-100, \
            nStartFrom=1,nTotalPins=(self.TotalPins-1), \
            side='L',gentype='O')
        self.GenPinFromSpec(self.bodyBottomRightX+150, \
            self.bodyTopLeftY-100,nStartFrom=2, \
            nTotalPins=(self.TotalPins-1),side='R',gentype='E')
        #}    
    ##########################################
    #}
##################################################
class libSIPpack(libComponent):
    #{
    ##########################################
    ## Private Variables
    _name = "SIP" #Component Type
    _valid = True #if Component is Valid
    ##########################################
    ## Public Variables    
    ##########################################
    ## Constructor Functions
    def __init__(self,compName,nPins,refDes='J',Descript="", Keyword=None, \
                 Footprints=None,PinNames=None,PinETypes=None):
        #{
        self.clear()
        self.ComponentName = compName
        self.RefenceDesignator = refDes
        self.TotalPins = nPins        
        self.compNameX = 0        
        self.refDesX = 0
        self.refDesY = 50
        sz = 3 + 1 # Default Name Size of 3Chars + 1 space
        # Create Default Pin Set
        for i in range(nPins):
            if PinNames == None:
                self.pinspec.append([str(i+1),'P'])
            else:
                if len(PinNames[i]) > (sz-1):
                    sz = len(PinNames[i])+1
                if PinETypes == None:
                    self.pinspec.append([PinNames[i],'P'])
                else:
                    self.pinspec.append([PinNames[i],PinETypes])
        # Asign Coordinates
        self.bodyTopLeftX = 0 #in Mils
        self.bodyTopLeftY = 0 #in Mils
        self.bodyBottomRightX = int(50*sz) #in Mils
        self.bodyBottomRightY = int(-100*(self.TotalPins+1))#in Mils
        self.compNameY = int(self.bodyBottomRightY - 50)
        # Add Description
        if Descript == "":
            self.Description = "SIP Connector"
        else:
            self.Description = Descript
        # Add the Keywords
        if Keyword == None:
            self.Keywords.append(self.ComponentName)
        else:
            for a in Keyword:
                self.Keywords.append(a)
        # Add the Footprints
        if Footprints != None:
            for a in Footprints:
                self.FootprintList.append(a)
        #}
    ##########################################
    ## Public Function
    def Populate(self):
        #{
        if self.TotalPins != 1:
            self.RectInsert(startx=self.bodyTopLeftX, \
                starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
                endy=self.bodyBottomRightY,thick=0,fill='N')
            self.GenPinFromSpec(self.bodyBottomRightX+150, \
                self.bodyTopLeftY-100,nStartFrom=1, \
                nTotalPins=self.TotalPins,side='R',gentype='N')
        else: # Specific to be 1 Pin Connector
            self.pinNameVisible = False
            self.pinNumberVisible = False
            self.refDesX = -150
            self.refDesY = 0
            self.compNameX = int(-50*(len(self.ComponentName)+2))
            self.compNameY = 0
            self.CircleInsert(0,0,50,thick=0,fill='N')
            self.GenPinFromSpec(200,0,nStartFrom=1, \
                nTotalPins=self.TotalPins,side='R',gentype='N')
        #}    
    ##########################################
    #}
##################################################
class libQUADpack(libComponent):
    #{
    ##########################################
    ## Private Variables
    _name = "QUAD" #Component Type
    _valid = True #if Component is Valid
    ##########################################
    ## Public Variables
    szoffset = 0
    ##########################################
    ## Constructor Functions
    def __init__(self,compName,nPins,refDes='U',Descript="", Keyword=None, \
                 Footprints=None,PinNames=None,PinETypes=None):
        #{
        if nPins%4 != 0:
            raise Exception("Error QUAD package needs even number of Pins")
        self.clear()
        self.ComponentName = compName
        self.RefenceDesignator = refDes
        self.TotalPins = nPins        
        self.compNameX = 0
        self.compNameY = 150
        self.refDesX = 0
        self.refDesY = 50
        sz = 3 + 2 # Default Name Size of 3Chars + 3 space
        # Create Default Pin Set
        for i in range(nPins):
            if PinNames == None:
                self.pinspec.append([str(i+1),'P'])
            else:
                if len(PinNames[i]) > (sz-1):
                    sz = len(PinNames[i])+1
                if PinETypes == None:
                    self.pinspec.append([PinNames[i],'P'])
                else:
                    self.pinspec.append([PinNames[i],PinETypes])
        # Asign Coordinates
        self.bodyTopLeftX = 0 #in Mils
        self.bodyTopLeftY = 0 #in Mils
        # Calcuate the final coordinate
        self.szoffset = int(50*sz)
        mz = int(self.szoffset*2 + (self.TotalPins/4*100)-100)
        print("mz",mz)
        self.bodyBottomRightX = int(mz)#in Mils
        self.bodyBottomRightY = -int(mz)#in Mils (Reverse Y axis)
        # Add Description
        if Descript == "":
            self.Description = "Quad IC"
        else:
            self.Description = Descript
        # Add the Keywords
        if Keyword == None:
            self.Keywords.append(self.ComponentName)
        else:
            for a in Keyword:
                self.Keywords.append(a)
        # Add the Footprints
        if Footprints != None:
            for a in Footprints:
                self.FootprintList.append(a)
        #}
    ##########################################
    ## Public Function
    def Populate(self):
        #{
        self.RectInsert(startx=self.bodyTopLeftX, \
            starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
            endy=self.bodyBottomRightY,thick=0,fill='N')
        #Left
        self.GenPinFromSpec( \
            int(self.bodyTopLeftX-150), \
            int(self.bodyTopLeftY - self.szoffset), \
            nStartFrom=1, \
            nTotalPins=int(self.TotalPins/4), \
            side='L',gentype='N')
        #Bottom
        self.GenPinFromSpec( \
            int(self.bodyTopLeftX+self.szoffset), \
            int(self.bodyBottomRightY-150), \
            nStartFrom=int(self.TotalPins/4)+1, \
            nTotalPins=int(self.TotalPins/4), \
            side='B',gentype='N')
        #Right
        self.GenPinFromSpec( \
            int(self.bodyBottomRightX + 150), \
            int(self.bodyBottomRightY + self.szoffset), \
            nStartFrom=int(self.TotalPins/2)+1, \
            nTotalPins=int(self.TotalPins/4), \
            side='RN',gentype='N')
        #Top
        self.GenPinFromSpec( \
            int(self.bodyBottomRightX - self.szoffset), \
            int(self.bodyTopLeftY + 150), \
            nStartFrom=int(self.TotalPins*3/4)+1, \
            nTotalPins=int(self.TotalPins/4), \
            side='TN',gentype='N')
        #}    
    ##########################################
    #}
##################################################
class libLibrary:
    #{
    ##########################################
    ## Private Variables
    ##########################################
    ## Public Variables
    NumberOfCoponents = 0
    Components = [] #Array of Components
    ComponentText = [] #Array of Component Text
    KicadLibText = ""
    KicadDcmText = ""
    ##########################################
    ## Constructor Functions
    # Empty Constructor
    def __init__(self):
        pass
    ##########################################
    ## Public Function
    def clear(self):
        """ Function to Clear all the Vars """
        #{
        self.KicadLibText =""
        self.KicadDcmText =""
        self.NumberOfCoponents = 0
        if len(self.ComponentText) > 0:
            self.ComponentText = []
        if len(self.Components) > 0:
            for c in self.Components:
                del c
            self.Components = []
        #}
    ############################    
    def AddComponent(self,ptype,compName,refDes,nPins, \
            Descript="", Keyword=None,PinNames=None,PinETypes=None):
        """ Function to Add Components to the List """
        #{
        c = None
        if ptype == 'DIP':
            c = libDIPpack(compName,\
                nPins,refDes,Descript,Keyword,PinNames,PinETypes)
        elif ptype == 'SIP':
            c = libSIPpack(compName,\
                nPins,refDes,Descript,Keyword,PinNames,PinETypes)
        elif ptype == 'CONN12':
            c = libCONN12pack(compName,\
                nPins,refDes,Descript,Keyword,PinNames,PinETypes)
        elif ptype == 'QUAD':
            c = libQUADpack(compName,\
                nPins,refDes,Descript,Keyword,PinNames,PinETypes)
        else:
            raise Exception("Component Type Error")
        self.Components.append(c)
        self.NumberOfCoponents = int(self.NumberOfCoponents + 1)
        #}
    ############################
    def AddHeader(self):
        """ Function to Add Library Header """
        self.KicadLibText = "EESchema-LIBRARY Version 2.3  Date:"
        self.KicadLibText += strftime("%m/%d/%Y %I:%M:%S %p", localtime())
        self.KicadLibText += "\n#encoding utf-8\n"
        self.KicadDcmText = "EESchema-DOCLIB  Version 2.0  Date:"
        self.KicadDcmText += strftime("%m/%d/%Y %I:%M:%S %p", localtime())
        self.KicadDcmText += "\n"
    ############################
    def genDetails(self):
        """ Function to Generate Components and Description """
        for c in self.Components:
            c.Populate()
            c.ToString()
            self.ComponentText.append([c.ComponentText,c.DescriptionText])
    ############################
    def AddDetails(self):
        for a in self.ComponentText:
            self.KicadLibText += a[0]
            self.KicadDcmText += a[1]
    ############################
    def AddFooter(self):
        """ Function to Add the Library Footer """
        self.KicadLibText += "#\n"
        self.KicadLibText += "# End Library\n"
        self.KicadDcmText += "#\n"
        self.KicadDcmText += "# End Doc Library\n"
    ############################
    def Export(self,fname):
        """ Function to Export the Component Data to a Lib & Dcm File """
        #{
        # Check of the File Exist
        if os.path.isfile(fname+".lib"):
            raise Exception("Error Lib File Already Exists, need to use Insert")
        if os.path.isfile(fname+".dcm"):
            raise Exception("Error Dcm File Already Exists, need to use Insert")
        # Add the Header
        self.AddHeader()
        # Generate Component Text
        self.genDetails()
        # Add the Component Text
        self.AddDetails()
        # Add the Footer
        self.AddFooter()
        #print Library File
        print("Library File:")
        print(self.KicadLibText)
        #print Document File
        print("Document File:")
        print(self.KicadDcmText)
        #Ask Confirmation
        #x = input("Test")
        # Write Lib File
        with open(fname+".lib","w") as f:
            f.write(self.KicadLibText)
        # Write Dcm File
        with open(fname+".dcm","w") as f:
            f.write(self.KicadDcmText)
        #}
    ############################
    def InsertToLib(self,fname):
        """ Function to First Import and then insert records"""
        #{
        if not os.path.isfile(fname+".dcm"):
            raise Exception("Error Dcm File Doesnot Exist")
        if not os.path.isfile(fname+".Lib"):
            raise Exception("Error Lib File Doesnot Exist")
        # Clear Old Arrays
        self.KicadLibText =""
        self.KicadDcmText =""
        # Generate Component Text
        if len(self.Components[0].ComponentText) == 0:
            self.genDetails()
        # Add the Component Text
        self.AddDetails()
        # Add the Footer
        self.AddFooter()
        # print Library File
        print("Library File:")
        print(self.KicadLibText)
        # print Document File
        print("Document File:")
        print(self.KicadDcmText)
        # Find Data till end in lib file
        cr = 0
        with open(fname+".lib","r") as fr:
            for k in fr.readlines():
                cr = int(cr + 1)
                if k.strip() == "# End Library":
                    cr = int(cr - 2)
                    break
        # Update the File
        fr = open(fname+".lib","r")
        fw = open(fname+"k.lib","a")
        # Reach to the Write Point
        for i in range(cr):
            k = fr.readline()
            fw.write(k)
        # Load the Data
        fw.write(self.KicadLibText)
        fw.close()
        fr.close()
        # Rename the File
        os.remove(fname+".lib")
        os.rename(fname+"k.lib",fname+".lib")
        # Find Data till end in dcm file
        cr = 0
        with open(fname+".dcm","r") as fr:
            for k in fr.readlines():
                cr = int(cr + 1)
                if k.strip() == "# End Doc Library":
                    cr = int(cr - 2)
                    break
        # Update the File
        fr = open(fname+".dcm","r")
        fw = open(fname+"k.dcm","a")
        # Reach to the Write Point
        for i in range(cr):
            k = fr.readline()
            fw.write(k)
        # Load the Data
        fw.write(self.KicadDcmText)
        fw.close()
        fr.close()
        # Rename the File
        os.remove(fname+".dcm")
        os.rename(fname+"k.dcm",fname+".dcm")
        #}
    ##########################################
    #}
##################################################
############################################################################
# Main FUNCTION>
############################################################################
if __name__ == "__main__" :
    #{
    print(__doc__)
    print("This is a Support Module")
    print()
    print("Testing Library Generation by making Test.lib")
    print()
    if os.path.isfile("Test.dcm"):
        os.remove("Test.dcm")
    if os.path.isfile("Test.lib"):        
        os.remove("Test.lib")
    d = libLibrary()    
    d.AddComponent('SIP',"CONN_1","J",1,"Connector 1Pin")    
    d.AddComponent('CONN12',"CONN_16","J",16,"Connector 16Pin")    
    d.AddComponent('SIP',"CONN_3","J",3,"Connector 3Pin")
    d.AddComponent('DIP',"RES","U",2,"Resistance 2Pin")
    d.AddComponent('QUAD',"chip_12","U",12,"Chip 4Pin")
    d.Export("Test")
    d.clear()
    d.AddComponent('DIP',"DIP_2","U",2,"DIP Holder 2 Pin")
    d.InsertToLib("Test")
    #}
############################################################################

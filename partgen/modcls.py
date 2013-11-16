#!/usr/bin/python
############################################################################
############################################################################
"""
##  modcls - Classes for Generating the PCB Library of Kicad
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
from util import *
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
class modPad:
    """ Class to describe the Pad Details for the Module
        The units supplied can still be in Mills the handling of
        1/10000th Inch is done internally
    """
    #{
    ##########################################
    ## Private Variables
    ##########################################
    ## Public Variables
    PadName = ""
    PadShape = 'C'
    PadType = 'STD'
    posX = 0 #in Mils
    posY = 0 #in Mils
    xsize = 0 #in Mils
    ysize = 0 #in Mils
    xdelta = 0 #in Mils
    ydelta = 0 #in Mils
    OrientAngle = 0 #in Degrees
    Drill = 0 #in Mils
    Drillxoffset = 0 #in Mils
    Drillyoffset = 0 #in Mils
    HoleShape = '' #O-oblong or ''-for None
    Padxdrill = 0 #in Mils for Oblong Drill in Pad
    Padydrill = 0 #in Mils for Oblong Drill in Pad
    NetNumber = 0
    NetName = ""
    LayerMask = "00E0FFFF"
    PadText = "" #Text for the Pad construct
    ##########################################
    ## Constructor Functions
    # Basic Constructor - all asignment in Mills
    def __init__(self,padName,posX,posY,padwidth,padheight, \
                 paddrill,padShape='C',padType='STD',padOrient=0, \
                 padxOffset = 0, padyOffset = 0, \
                 drillOffsetx = 0,drillOffsety = 0, \
                 padDrillShape='',DrillShapeWidth=0,DrillShapeHeight=0, \
                 netNumber=0,netName="",layerMask="00E0FFFF"):
        #{
        self.PadName = padName
        # Shape of Pad
        if padShape in ('C','R','O','T'):
            self.PadShape = padShape
        else:
            raise Exception("Error in Pad Shape")
        # Pad Type and Layer Mask
        if padType in ('STD','SMD','CONN','HOLE','MECA'):
            self.PadType = padType
            if padType == 'STD':
                self.LayerMask = "00E0FFFF"
            elif padType == 'SMD':
                self.LayerMask = "00888000"
            else:
                self.LayerMask = layerMask
        else:
            raise Exception("Error Invalid Pad Type")
        self.posX = posX #in Mils
        self.posY = posY #in Mils
        self.xsize = padwidth #in Mils
        self.ysize = padheight #in Mils
        self.xdelta = padxOffset #in Mils
        self.ydelta = padyOffset #in Mils
        self.OrientAngle = padOrient #in Degrees
        self.Drill = paddrill #in Mils
        self.Drillxoffset = drillOffsetx #in Mils
        self.Drillyoffset = drillOffsety #in Mils
        # Drill Shape
        if padDrillShape == 'O':
            self.HoleShape = padDrillShape #O-oblong or ''-for None
            self.Padxdrill = DrillShapeWidth #in Mils for Oblong Drill in Pad
            self.Padydrill = DrillShapeHeight #in Mils for Oblong Drill in Pad
        else:
            self.HoleShape = ''
            self.Padxdrill = 0
            self.Padydrill = 0
        self.NetNumber = netNumber
        self.NetName = netName
        self.PadText = "" #Text for the Pad construct
        #}
    ##########################################
    ## Public Function
    def ToString(self):
        """ To make the Pad String with 1/10000 inch adjustment """
        #{
        self.PadText += "$PAD\n"
        self.PadText += "Sh \"%s\" %c %d %d %d %d %d\n"%(\
            self.PadName,self.PadShape, \
            int(self.xsize*10),int(self.ysize*10), \
            int(self.xdelta*10),int(self.ydelta*10), \
            int(self.OrientAngle*10))
        # Change in format depending on the Shape of the Hole
        if self.HoleShape == '':
            self.PadText += "Dr %d %d %d\n"%( \
                int(self.Drill*10),int(self.Drillxoffset*10), \
                int(self.Drillyoffset*10))
        else:
            self.PadText += "Dr %d %d %d %c %d %d\n"%( \
                int(self.Drill*10),int(self.Drillxoffset*10), \
                int(self.Drillyoffset*10),self.HoleShape, \
                int(self.Padxdrill*10),int(self.Padydrill*10))
        self.PadText += "At %s N %s\n"%(self.PadType,self.LayerMask)
        self.PadText += "Ne %d \"%s\"\n"%(self.NetNumber,self.NetName)
        self.PadText += "Po %d %d\n"%(int(self.posX*10), \
                                    int(self.posY*10))
        self.PadText += "$EndPAD\n"
        return self.PadText
        #}
    ##########################################
    #}
##################################################
class modModule:
    """ Abstract Base Class to define the Internals of a Module
        Object for of This Class type cant be created
        This would be included into several sub Classes to make custom
        Modules.
    """
    #{
    ##########################################
    ## Private Variables
    _name = "" #Module Type
    _valid = False #if Module is Valid
    ##########################################
    ## Public Variables
    Pads = [] #List of Pads
    Pitch = 0 #in Mils
    UnitsInMM = True #Units Choice
    ModuleName = ""
    RefDes = ""
    PadWidth = 0 #in Mils X
    PadHeight = 0 #in Mils Y
    PadDrill = 0 #in Mils
    PadRowSpacingx = 0 #in Mils
    PadRowSpacingy = 0 #in Mils
    PadSections = 0
    PadShape = "C"
    TotalPads = 0
    Description=""
    DescriptionSpec = {} # Collection containing Generated Description Details
    Keywords = [] # Keyword array
    KeywordsSpec = {} # Collection containing Generated Keyword Details
    bodyTopLeftX = 0
    bodyTopLeftY = 0
    bodyBottomRightX = 0
    bodyBottomRightY = 0
    ModNameX = 0
    ModNameY = 0
    ModNameFontX = 60
    ModNameFontY = 60
    RefDesX = 0
    RefDesY = 0
    RedDesFontX = 50
    RedDesFontY = 50
    ModuleText = ""
    Draws = [] # Array of Drawing objects
    FontWidth = 12 # Pen Width for the Text Drawn
    ##########################################
    ## Constructor Functions
    # Empty Constructor
    def __init__(self):
        #{
        if self.__class__ != modModule:
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
            modModule(self)
        except TypeError as e:
            # We do this for compatibility with py2.3
            raise Error(str(e))
        #}
    ##########################################
    ## Abstract Function
    def Populate(self):
        """ Abstract Function to Add the Pads as per the location
            co-ordinates
            (Must be implemented in Derived Classes)
        """
        self.validate()        
    ############################
    def GenerateDescription(self):
        """ Abstract Function to generate the Description and Keywords
            (Must be implemented in Derived Classes)
        """
        self.validate()
    ##########################################
    ## Public Function
    def validate(self):
        if self._valid == False or self.__class__ == modModule:
            raise TypeError("Error in Component Type")
    ############################
    def clear(self):
        """ Function to Clear the Data from the class """
        #{
        self.validate()
        self.Pads = []
        self.Pitch = 0
        self.UnitsInMM = True
        self.ModuleName = ""
        self.RefDes = ""
        self.PadWidth = 0 #in Mils X
        self.PadHeight = 0 #in Mils Y
        self.PadDrill = 0 #in Mils
        self.PadRowSpacingx = 0 #in Mils
        self.PadRowSpacingy = 0 #in Mils
        self.PadSections = 0
        self.PadShape = "Circular"
        self.TotalPads = 0
        self.Description=""
        self.DescriptionSpec = {} 
        self.Keywords = [] # Keyword array
        self.KeywordsSpec = {}
        self.bodyTopLeftX = 0
        self.bodyTopLeftY = 0
        self.bodyBottomRightX = 0
        self.bodyBottomRightY = 0
        self.ModNameX = 0
        self.ModNameY = 0
        self.ModNameFontX = 60
        self.ModNameFontY = 60
        self.RefDesX = 0
        self.RefDesY = 0
        self.RedDesFontX = 50
        self.RedDesFontY = 50
        self.ModuleText = ""
        self.Draws = [] #Array of Drawing objects
        self.FontWidth = 12
        #}    
    ############################
    def InsertPad(self,padName,posX,posY, \
                 padShape='C',padType='STD',padOrient=0, \
                 padxOffset = 0, padyOffset = 0, \
                 drillOffsetx = 0,drillOffsety = 0, \
                 padDrillShape='',DrillShapeWidth=0,DrillShapeHeight=0, \
                 netNumber=0,netName="",layerMask="00E0FFFF"):
        """ Function to Add pads it to Pad list """
        #{
        self.validate()
        # Create Pad
        p = modPad(padName,posX,posY,self.PadWidth,self.PadHeight, \
                 self.PadDrill,padShape,padType,padOrient, \
                 padxOffset,padyOffset,drillOffsetx,drillOffsety, \
                 padDrillShape,DrillShapeWidth,DrillShapeHeight, \
                 netNumber,netName,layerMask)
        # Add to the Pad List
        self.Pads.append(p)
        #}
    ############################
    def InsertLine(self,startx,starty,endx,endy,width=12,layer=21):
        """ To Insert a Line Segment in the Drawing """
        #{
        self.validate()
        self.Draws.append("DS %d %d %d %d %d %d"%( \
            int(startx*10),int(starty*10),int(endx*10),int(endy*10), \
            int(width*10),layer))
        #}
    ############################
    def InsertCircle(self,posX,posY,pointX,pointY,width=12,layer=21):
        """ To Insert a Circle in the Drawing """
        #{
        self.validate()
        self.Draws.append("DC %d %d %d %d %d %d"%( \
            int(posX*10),int(posY*10),int(pointX*10),int(pointY*10),\
            int(width*10),layer))
        #}
    ############################
    def InsertArc(self,startx,starty,endx,endy,angle,width=12,layer=21):
        """ To Insert a Arc in the Drawing """
        #{
        self.validate()
        self.Draws.append("DC %d %d %d %d %d %d %d"%( \
            int(startx*10),int(starty*10),int(endx*10),int(endy*10),\
            int(angle*10),int(width*10),layer))
        #}
    ############################    
    def AddDescription(self):
        """ Automatically add Description for Module if some info doesnot Exits"""
        #{
        self.validate()
        # Templates
        template_desc_pcb ="""%(name)s %(pin)sPin%(rowx1)s%(fix)s \
%(pitch)s Pitch %(pad)s Pad %(drill)s %(shape)s %(type)s"""
        template_keyw_pcb ="""%(name)s%(pin)s_%(fix)s %(name)s%(pin)s_%(fix)s_\
%(pitch)s %(name)s%(pin)s%(rowx1)s_%(fix)s_%(pitch)s_%(pad)s\
_%(drill)s%(shape)s%(type)s"""
        # Get the Parameters and Format them
        if self.UnitsInMM:
            pich = "%2.2f"%(float(miltomm(self.Pitch)))
            x = "%2.2f"%(float(miltomm(self.PadWidth)))
            y = "%2.2f"%(float(miltomm(self.PadHeight)))
            dril = "%2.2f"%(float(miltomm(self.PadDrill)))
            rox = "%2.2f"%(float(miltomm(self.PadRowSpacingx)))
            roy = "%2.2f"%(float(miltomm(self.PadRowSpacingy)))
        else:
            pich = "%d"%(float(self.Pitch))
            x = ("%d"%(float(self.PadWidth)))
            y = ("%d"%(float(self.PadHeight)))
            dril = ("%d"%(float(self.PadDrill)))
            rox = "%d"%(float(self.PadRowSpacingx))
            roy = "%d"%(float(self.PadRowSpacingy))
        # Add Pins
        self.DescriptionSpec["pin"] = "%d"%self.TotalPads
        self.KeywordsSpec["pin"] = "%d"%self.TotalPads
        # Add Pad Type
        if self.PadDrill != 0: # Holes
            self.DescriptionSpec["fix"]="Through Hole"
            self.KeywordsSpec["fix"]="TH"
        else:
            self.DescriptionSpec["fix"]="SMD"
            self.KeywordsSpec["fix"]="SMD"
        # Add Pitch        
        self.DescriptionSpec["pitch"] = pich
        self.KeywordsSpec["pitch"] = pich
        # Add Pad
        if x != y:
            self.DescriptionSpec["pad"] = x+"X"+y        
            self.KeywordsSpec["pad"] = x+"X"+y
        else:
            self.DescriptionSpec["pad"] = x        
            self.KeywordsSpec["pad"] = x
        # Pad Shape
        if self.PadShape == "C":
            self.DescriptionSpec["shape"] = "Circular"
            self.KeywordsSpec["shape"] = "C"
        elif self.PadShape == "R":
            self.DescriptionSpec["shape"] = "Rectangular"
            self.KeywordsSpec["shape"] = "R"
        elif self.PadShape == "O":
            self.DescriptionSpec["shape"] = "Oblong"
            self.KeywordsSpec["shape"] = "O"           
        else:
            self.DescriptionSpec["shape"] = self.PadShape
            self.KeywordsSpec["shape"] = self.PadShape
        # Add Drill
        if self.PadDrill != 0: # Holes
            self.DescriptionSpec["drill"] = dril+ " Drill"
            self.KeywordsSpec["drill"] = dril + "_"
        else:
            self.DescriptionSpec["drill"] = ""
            self.KeywordsSpec["drill"] = ""
        # Add Row Spacing
        if self.PadRowSpacingx == 0 and self.PadRowSpacingy == 0:
            self.DescriptionSpec["rowx1"] = " "
            self.KeywordsSpec["rowx1"] = ""
        elif self.PadRowSpacingx != 0 and self.PadRowSpacingy == 0:
            self.DescriptionSpec["rowx1"] = " " + rox + " Spacing "
            self.KeywordsSpec["rowx1"] = "_" + rox
            self.DescriptionSpec["pin"] = "%d"%(self.TotalPads/2)
            self.KeywordsSpec["pin"] = "%d"%(self.TotalPads/2)
        elif self.PadRowSpacingx == 0 and self.PadRowSpacingy != 0:
            self.DescriptionSpec["rowx1"] = " " + rox + " Spacing "
            self.KeywordsSpec["rowx1"] = "_" + rox
        elif self.PadRowSpacingx != 0 and self.PadRowSpacingy != 0:
            self.DescriptionSpec["rowx1"] = " " + rox + "X" + roy + " Spacing "
            self.KeywordsSpec["rowx1"] = "_" + rox + "X" + roy
        else:
            raise Exception("Non Implemented Row/Column Spacing")
        # Add Type
        self.DescriptionSpec["type"] = "" # Special for Locking/Normal
        self.KeywordsSpec["type"] = ""
        # Add Name
        self.DescriptionSpec["name"] = self._name
        self.KeywordsSpec["name"] = self._name
        ## Call for Additional Details
        self.GenerateDescription()
        ##
        # Generate the Detail Strings (Remove any Trailing spaces)
        dec = (template_desc_pcb % self.DescriptionSpec).strip()
        key = (template_keyw_pcb % self.KeywordsSpec).strip()
        # Add Defaults if Data is not Present
        if self.ModuleName == "":
            self.ModuleName = key.split(" ")[2]
        if self.Description == "":
            self.Description = dec #Add Default Description
        if self.Keywords == None:
            self.Keywords = key.split(" ")
        #}
    ############################
    def AddModHeader(self):
        """ Function to Generate the header needed for the Module
            defintion in the Lib
        """
        #{
        self.validate()        
        self.ModuleText += "$MODULE %s\n"%(self.ModuleName)
        self.ModuleText += "Po 0 0 0 15 50FE4688 00000000 ~~\n"
        self.ModuleText += "Li %s\n"%(self.ModuleName)        
        self.ModuleText += "Cd %s\n"%(self.Description)
        self.ModuleText += "Kw"
        # Add Keywords        
        for e in self.Keywords:
            self.ModuleText += " " + e
        self.ModuleText += "\n"
        self.ModuleText += "Sc 00000000\n"
        self.ModuleText += "AR %s\n"%(self.ModuleName)
        self.ModuleText += "Op 0 0 0\n"
        # Add the RefDes Name
        self.ModuleText += "T0 %d %d %d %d 0 %d N V 21 \"%s\"\n"%( \
            int(self.RefDesX*10),int(self.RefDesY*10), \
            int(self.RedDesFontX*10),int(self.RedDesFontY*10), \
            int(self.FontWidth*10),self.RefDes)
        self.ModuleText += "T1 %d %d %d %d 0 %d N V 21 \"%s\"\n"%( \
            int(self.ModNameX*10),int(self.ModNameY*10), \
            int(self.ModNameFontX*10),int(self.ModNameFontY*10), \
            int(self.FontWidth*10),self.ModuleName)
        #}
    ############################
    def addDetails(self):
        """ Function to Add Drawing parts and Pads to the Module """
        #{
        self.validate()
        # Add Drawings
        for k in self.Draws:
            self.ModuleText += k + "\n"
        # Generate and Add Pads
        for k in self.Pads:
            k.ToString()
            self.ModuleText += k.PadText
        #}
    ############################
    def addModFooter(self):
        """ Function to generate the Module Footer"""
        #{
        self.validate()
        self.ModuleText += "$EndMODULE  %s\n"%(self.ModuleName)
        #}
    ############################
    def ToString(self):
        """ Generates the Complete Module """
        #{
        self.validate()
        self.AddDescription()
        self.AddModHeader()
        self.addDetails()
        self.addModFooter()
        return self.ModuleText
        #}
    ##########################################
    #}
##################################################
class modDIPpack(modModule):
    """ Class to make DIP through Hole Package """
    #{
    ##########################################
    ## Private Variables
    _name = "DIP" #Module Type
    _valid = True #if Module is Valid
    ##########################################
    ## Public Variables
    
    ##########################################
    ## Constructor Functions
    # Basic Constructor
    def __init__(self,name,refdes,npins,pitch,drill, \
                 rowspacingx,rowspacingy,pinshoriz, \
                 padwidth,padheight,padshape, \
                 descript="",keywords=None):
        #{
        self.clear()
        if npins % 2 != 0:
            raise Exception("Error Number of Pins can only be Even for DIP package")
        self.Pads = []
        self.Pitch = pitch
        self.ModuleName = name
        if refdes == "":
            refdes = "U***"
        self.RefDes = refdes
        self.PadWidth = padwidth #in Mils X
        self.PadHeight = padheight #in Mils Y
        self.PadShape = "O"
        self.PadDrill = drill #in Mils
        self.PadRowSpacingx = rowspacingx #in Mils
        self.PadRowSpacingy = 0 #in Mils - Not Needed as only Vertical rows
        self.PadSections = 2 # Default two rows
        self.TotalPads = npins
        self.Description= descript
        self.Keywords = keywords # Keyword array
        # Make the Boady Drawing
        self.bodyTopLeftX = (self.PadWidth/2) + 50
        self.bodyTopLeftY = -(self.PadHeight/2)
        self.bodyBottomRightX = self.PadRowSpacingx - \
                                self.bodyTopLeftX
        self.bodyBottomRightY = (self.TotalPads/2 - 1)*100 - \
                                self.bodyTopLeftY
        # Name Locations
        self.ModNameX = 10
        self.ModNameY = -200
        self.RefDesX = 10
        self.RefDesY = -100
        #}
    ##########################################
    ## Public Function
    def GenerateDescription(self):
        #{
        self.validate()
        #}
    ############################    
    def Populate(self):
        #{
        self.validate()
        self.InsertLine(startx=self.bodyTopLeftX, \
            starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
            endy=self.bodyTopLeftY)
        self.InsertLine(startx=self.bodyTopLeftX, \
            starty=self.bodyTopLeftY,endx=self.bodyTopLeftX, \
            endy=self.bodyBottomRightY)
        self.InsertLine(startx=self.bodyTopLeftX, \
            starty=self.bodyBottomRightY,endx=self.bodyBottomRightX, \
            endy=self.bodyBottomRightY)
        self.InsertLine(startx=self.bodyBottomRightX, \
            starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
            endy=self.bodyBottomRightY)
        #Add Marking Circle
        m = int((self.PadWidth/2) + 70)
        self.InsertCircle( \
            posX=-m, \
            posY=0, \
            pointX=-m-20, \
            pointY=0)
        #Add the Pads
        y = 0
        for i in range(1,int(self.TotalPads/2 + 1)):
            self.InsertPad(padName=str(i),posX=0,posY=y, \
                 padShape=self.PadShape,padType='STD',padOrient=0, \
                 padxOffset = 0, padyOffset = 0, \
                 drillOffsetx = 0,drillOffsety = 0, \
                 padDrillShape='',DrillShapeWidth=0,DrillShapeHeight=0, \
                 netNumber=0,netName="",layerMask="00E0FFFF")
            y = int(y + 100)
        y = int(y - 100)
        for i in range(int((self.TotalPads/2)+1),int(self.TotalPads+1)):
            self.InsertPad(padName=str(i),posX=self.PadRowSpacingx,posY=y, \
                 padShape=self.PadShape,padType='STD',padOrient=0, \
                 padxOffset = 0, padyOffset = 0, \
                 drillOffsetx = 0,drillOffsety = 0, \
                 padDrillShape='',DrillShapeWidth=0,DrillShapeHeight=0, \
                 netNumber=0,netName="",layerMask="00E0FFFF")
            y = int(y - 100)
        #}
    ##########################################
    #}
##################################################
class modSMDdualpack(modModule):
    """ Class to make SMD Dual Row Packages """
    #{
    ##########################################
    ## Private Variables
    _name = "SMDdual" #Module Type
    _valid = True #if Module is Valid
    ##########################################
    ## Public Variables
    
    ##########################################
    ## Constructor Functions
    # Basic Constructor
    def __init__(self,name,refdes,npins,pitch,drill, \
                 rowspacingx,rowspacingy,pinshoriz, \
                 padwidth,padheight,padshape, \
                 descript="",keywords=None):
        #{
        self.clear()
        if npins % 2 != 0:
            raise Exception("Error Number of Pins can only be Even for DIP package")
        self.Pads = []
        self.Pitch = pitch
        self.ModuleName = name
        if refdes == "":
            refdes = "U***"
        self.RefDes = refdes
        self.PadWidth = padwidth #in Mils X
        self.PadHeight = padheight #in Mils Y
        if padshape == "":
            padshape = "R"
        self.PadShape = padshape
        self.PadDrill = 0 #in Mils For SMD Device
        self.PadRowSpacingx = rowspacingx #in Mils
        self.PadRowSpacingy = 0 #in Mils - Not Needed as only Vertical rows
        self.PadSections = 2 # Default two rows
        self.TotalPads = npins
        self.Description= descript
        self.Keywords = keywords # Keyword array
        # Make the Boady Drawing
        self.bodyTopLeftX = (self.PadWidth/2) + 50
        self.bodyTopLeftY = -(self.PadHeight/2)
        self.bodyBottomRightX = self.PadRowSpacingx - \
                                self.bodyTopLeftX
        self.bodyBottomRightY = (self.TotalPads/2 - 1)*100 - \
                                self.bodyTopLeftY
        # Name Locations
        self.ModNameX = 10
        self.ModNameY = -200
        self.RefDesX = 10
        self.RefDesY = -100
        #}
    ##########################################
    ## Public Function
    def GenerateDescription(self):
        #{
        self.validate()
        #}
    ############################    
    def Populate(self):
        #{
        self.validate()
        self.InsertLine(startx=self.bodyTopLeftX, \
            starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
            endy=self.bodyTopLeftY)
        self.InsertLine(startx=self.bodyTopLeftX, \
            starty=self.bodyTopLeftY,endx=self.bodyTopLeftX, \
            endy=self.bodyBottomRightY)
        self.InsertLine(startx=self.bodyTopLeftX, \
            starty=self.bodyBottomRightY,endx=self.bodyBottomRightX, \
            endy=self.bodyBottomRightY)
        self.InsertLine(startx=self.bodyBottomRightX, \
            starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
            endy=self.bodyBottomRightY)
        #Add Marking Circle
        m = int((self.PadWidth/2) + 70)
        self.InsertCircle( \
            posX=-m, \
            posY=0, \
            pointX=-m-20, \
            pointY=0)
        #Add the Pads
        y = 0
        for i in range(1,int(self.TotalPads/2 + 1)):
            self.InsertPad(padName=str(i),posX=0,posY=y, \
                 padShape=self.PadShape,padType='SMD',padOrient=0, \
                 padxOffset = 0, padyOffset = 0, \
                 drillOffsetx = 0,drillOffsety = 0, \
                 padDrillShape='',DrillShapeWidth=0,DrillShapeHeight=0, \
                 netNumber=0,netName="",layerMask="")#use automatic
            y = int(y + 100)
        y = int(y - 100)
        for i in range(int((self.TotalPads/2)+1),int(self.TotalPads+1)):
            self.InsertPad(padName=str(i),posX=self.PadRowSpacingx,posY=y, \
                 padShape=self.PadShape,padType='SMD',padOrient=0, \
                 padxOffset = 0, padyOffset = 0, \
                 drillOffsetx = 0,drillOffsety = 0, \
                 padDrillShape='',DrillShapeWidth=0,DrillShapeHeight=0, \
                 netNumber=0,netName="",layerMask="")#use automatic
            y = int(y - 100)
        #}
    ##########################################
    #}
##################################################
class modSIPpack(modModule):
    """ Class to make SIP Packages for SMD and Through Hole"""
    #{
    ##########################################
    ## Private Variables
    _name = "SIP" #Module Type
    _valid = True #if Module is Valid
    ##########################################
    ## Public Variables
    FirstPinSquare = False
    LockingPattern = False
    ThroughHole = True
    ##########################################
    ## Constructor Functions
    # Basic Constructor
    def __init__(self,name,refdes,npins,pitch,drill, \
                 rowspacingx,rowspacingy,pinshoriz, \
                 padwidth,padheight,padshape, \
                 descript="",keywords=None,Special=None):
        #{
        self.clear()
        self.Pads = []
        self.Pitch = pitch
        self.ModuleName = name
        if refdes == "":
            refdes = "J***"
        self.RefDes = refdes
        self.PadWidth = padwidth #in Mils X
        self.PadHeight = padheight #in Mils Y
        if padshape == "":
            padshape = "C"
        self.PadShape = padshape
        self.PadDrill = drill #in Mils 
        self.PadRowSpacingx = 0 #in Mils - Not Needed for single line device
        self.PadRowSpacingy = 0 #in Mils - Not Needed as only Vertical rows
        self.PadSections = 1 # Default 1 row only
        self.TotalPads = npins
        self.Description= descript
        self.Keywords = keywords # Keyword array
        # Make the Boady Drawing
        self.bodyTopLeftX = (self.PadWidth/2) + 50
        self.bodyTopLeftY = -(self.PadHeight/2)
        self.bodyBottomRightX = self.PadRowSpacingx - \
                                self.bodyTopLeftX
        self.bodyBottomRightY = (self.TotalPads/2 - 1)*100 - \
                                self.bodyTopLeftY
        # Name Locations
        self.ModNameX = 10
        self.ModNameY = -200
        self.RefDesX = 10
        self.RefDesY = -100
        # Now Load Special Info
        if Special != None:
            if "FirstPinSquare" in Special:
                self.FirstPinSquare = Special["FirstPinSquare"]
                if self.PadWidth != self.PadHeight:# Correction for SMD pads
                    self.FirstPinSquare = False
            if "LockingPattern" in Special:
                self.LockingPattern = Special["LockingPattern"]
            if "ThroughHole" in Special:
                self.ThroughHole = Special["ThroughHole"]
        #}
    ##########################################
    ## Public Function
    def GenerateDescription(self):
        #{
        self.validate()
        #}
    ############################    
    def Populate(self):
        #{
        self.validate()
        self.InsertLine(startx=self.bodyTopLeftX, \
            starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
            endy=self.bodyTopLeftY)
        self.InsertLine(startx=self.bodyTopLeftX, \
            starty=self.bodyTopLeftY,endx=self.bodyTopLeftX, \
            endy=self.bodyBottomRightY)
        self.InsertLine(startx=self.bodyTopLeftX, \
            starty=self.bodyBottomRightY,endx=self.bodyBottomRightX, \
            endy=self.bodyBottomRightY)
        self.InsertLine(startx=self.bodyBottomRightX, \
            starty=self.bodyTopLeftY,endx=self.bodyBottomRightX, \
            endy=self.bodyBottomRightY)
        #Add Marking Circle
        m = int((self.PadWidth/2) + 70)
        self.InsertCircle( \
            posX=-m, \
            posY=0, \
            pointX=-m-20, \
            pointY=0)
        #Add the Pads
        y = 0
        for i in range(1,int(self.TotalPads/2 + 1)):
            self.InsertPad(padName=str(i),posX=0,posY=y, \
                 padShape=self.PadShape,padType='SMD',padOrient=0, \
                 padxOffset = 0, padyOffset = 0, \
                 drillOffsetx = 0,drillOffsety = 0, \
                 padDrillShape='',DrillShapeWidth=0,DrillShapeHeight=0, \
                 netNumber=0,netName="",layerMask="")#use automatic
            y = int(y + 100)
        y = int(y - 100)
        for i in range(int((self.TotalPads/2)+1),int(self.TotalPads+1)):
            self.InsertPad(padName=str(i),posX=self.PadRowSpacingx,posY=y, \
                 padShape=self.PadShape,padType='SMD',padOrient=0, \
                 padxOffset = 0, padyOffset = 0, \
                 drillOffsetx = 0,drillOffsety = 0, \
                 padDrillShape='',DrillShapeWidth=0,DrillShapeHeight=0, \
                 netNumber=0,netName="",layerMask="")#use automatic
            y = int(y - 100)
        #}
    ##########################################
    #}
##################################################
class modLibrary:
    #{
    ##########################################
    ## Private Variables
    ##########################################
    ## Public Variables
    NumberOfModules = 0
    Modules = [] # Array of Module
    ModuleText = [] # Array of Converted modules
    KicadModText = ""
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
        self.NumberOfModules = 0
        self.Modules = [] # Array of Module
        self.ModuleText = [] # Array of Converted modules
        self.KicadModText = ""
        #}
    ############################
    def AddModule(self,chip,name,refdes,npins,pitch,drill, \
                 rowspacingx,rowspacingy,pinshoriz, \
                 padwidth,padheight,padshape, \
                 descript="",keywords=None,special=None):
        #{
        m = None
        if chip == 'DIP':
            m = modDIPpack(name,refdes,npins,pitch,drill, \
                 rowspacingx,rowspacingy,pinshoriz, \
                 padwidth,padheight,padshape, \
                 descript,keywords)
        elif chip in ('SOIC','SSOP','TSSOP','SOP'):
            m = modSMDdualpack(name,refdes,npins,pitch,drill, \
                 rowspacingx,rowspacingy,pinshoriz, \
                 padwidth,padheight,padshape, \
                 descript,keywords)
        else:
            raise Exception("Module Type Error")
        # Automatic population of Description & Keywords
        if len(descript) == 0:
                m.GenerateDescription()
        self.Modules.append(m)
        self.NumberOfModules = int(self.NumberOfModules + 1)
        #}
    ############################
    def AddHeader(self):
        """ Function to Add Module Library Header """
        #{
        self.KicadModText += "PCBNEW-LibModule-V1  "
        self.KicadModText += strftime("%m/%d/%Y %I:%M:%S %p", localtime())
        self.KicadModText += "\n#encoding utf-8\n"
        self.KicadModText += "$INDEX\n"
        # Add Index Details        
        for k in self.Modules:
            if k.ModuleText == "":
                k.Populate()
                k.ToString()
            self.KicadModText += k.ModuleName + "\n"
        self.KicadModText += "$EndINDEX\n"
        #}
    ############################
    def genDetails(self):
        """ Function to Generate Modules and add the Text """
        for k in self.Modules:
            if k.ModuleText == "":
                k.Populate()
                k.ToString()
            self.ModuleText.append(k.ModuleText)
    ############################
    def AddDetails(self):
        #{        
        # Now Add Components
        for k in self.ModuleText:
            self.KicadModText += k
        #}
    ############################
    def AddFooter(self):
        """ Function to Add the Module Library Footer """
        self.KicadModText += "$EndLIBRARY\n"
    ############################
    def Export(self,fname):
        """ Function to Export the Module Data to a Lib """
        #{
        if os.path.isfile(fname+".mod"):
            raise Exception("Error Mod File Already Exists, use Insert")
        # Add the Header
        self.AddHeader()
        # Generate Module Text
        self.genDetails()
        # Add the Module Text
        self.AddDetails()
        # Add the Footer
        self.AddFooter()
        #print Library File
        print("Library File:")
        print(self.KicadModText)
        #Ask Confirmation
        #x = input("Test")
        with open(fname+".mod","w") as f:
            f.write(self.KicadModText)    
        #}
    ############################
    def InsertToLib(self,fname):
        """ Function to First Import and then insert records"""
        #{
        if not os.path.isfile(fname+".mod"):
            raise Exception("Error Mod File Doesnot Exist")
        # Clear Old Arrays
        self.KicadModText =""
        # Generate Component Text
        if len(self.Modules[0].ModuleText) == 0:
            self.genDetails()
        # Add the Component Text
        self.AddDetails()
        # Add the Footer
        self.AddFooter()
        # print Library File
        print("Library File:")
        print(self.KicadModText)
        # Find the End of the Index
        cr = 0
        fr = open(fname+".mod","r")
        fw = open(fname+"k.mod","w")
        # Read the First Line
        rd = fr.readline()
        while rd.strip() != "$EndINDEX":
            fw.write(rd)
            rd = fr.readline()
            cr = int(cr + 1)
        fr.close()        
        # Write the Remaining Entries
        for k in self.Modules:
            fw.write(k.ModuleName + "\n")
        # Write the Index Terminator
        fw.write("$EndINDEX\n")
        # Restore the Read Pointer for the file
        fr = open(fname+".mod","r")
        for i in range(cr):
            rd = fr.readline()
        # Now Start the Copy till Mod Lib end Marker
        rd = fr.readline()
        while rd.strip() != "$EndLIBRARY":
            fw.write(rd)
            rd = fr.readline()
        # Now Write the Remaining Module Entry
        fw.write(self.KicadModText)
        fw.close()
        fr.close()
        # Rename the File
        os.remove(fname+".mod")
        os.rename(fname+"k.mod",fname+".mod")
        #}
    ##########################################
    #}    
############################################################################
# Main FUNCTION>
############################################################################
if __name__ == "__main__" :
    #{
    print(__doc__)
    print("This is a Support Module")
    print()
    if os.path.isfile("Test.mod"):
        os.remove("Test.mod")
    if os.path.isfile("Test.emp"):
        os.remove("Test.emp")
    d = modLibrary()
##    d.AddModule(chip='DIP',name="",refdes="",npins=16,pitch=100, \
##                drill=31,rowspacingx=300,rowspacingy=0,pinshoriz=0, \
##                 padwidth=100,padheight=50,padshape='O')
    d.Exportx("Test")
    os.rename("Test.mod","Test.emp")
    #}
############################################################################

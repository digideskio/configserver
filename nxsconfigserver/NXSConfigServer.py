#    "$Name:  $";
#    "$Header:  $";
#=============================================================================
#
# file :        NXSConfigServer.py
#
# description : Python source for the NXSConfigServer and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                NXSConfigServer are implemented in this file.
#
# project :     TANGO Device Server
#
# $Author:  $
#
# $Revision:  $
#
# $Log:  $
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#          This file is generated by POGO
#    (Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#

""" Configuration Server for Nexus Data Writer """

import PyTango
import sys

from .XMLConfigurator import XMLConfigurator as XMLC


#==================================================================
#   NXSConfigServer Class Description:
#
##         Configuration Server based on MySQL database
#
#==================================================================
#     Device States Description:
#
#   DevState.OPEN :     Open connection to the database
#   DevState.ON :       Server is ON
#   DevState.RUNNING :  Performing a query
#==================================================================


class NXSConfigServer(PyTango.Device_4Impl):

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self, cl, name):
        self.xmlc = None
        PyTango.Device_4Impl.__init__(self, cl, name)
        NXSConfigServer.init_device(self)

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        print >> self.log_info, "[Device delete_device method] for device", \
            self.get_name()
        if hasattr(self,"xmlc") and self.xmlc:
            if hasattr(self.xmlc, "close"):
                self.xmlc.close()
            del self.xmlc
            self.xmlc = None
        self.set_state(PyTango.DevState.OFF)


#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    def init_device(self):
        print >> self.log_info, "In ", self.get_name(), "::init_device()"
        self.xmlc = XMLC(self)
        self.set_state(PyTango.DevState.ON)
        self.get_device_properties(self.get_device_class())
        self.xmlc.versionLabel = self.VersionLabel

#------------------------------------------------------------------
#    Always excuted hook method
#------------------------------------------------------------------
    def always_executed_hook(self):
        print >> self.log_info, "In ", self.get_name(), \
            "::always_excuted_hook()"

#==================================================================
#
#    NXSConfigServer read/write attribute methods
#
#==================================================================
#------------------------------------------------------------------
#    Read Attribute Hardware
#------------------------------------------------------------------
    def read_attr_hardware(self, _):
        print >> self.log_info, "In ", self.get_name(), "::read_attr_hardware()"



#------------------------------------------------------------------
#    Read XMLString attribute
#------------------------------------------------------------------
    def read_XMLString(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_XMLString()"
        
#        attr_XMLString_read = "Hello Tango world"
        attr.set_value(self.xmlc.xmlstring)


#------------------------------------------------------------------
#    Write XMLString attribute
#------------------------------------------------------------------
    def write_XMLString(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_XMLString()"
        
        self.xmlc.xmlstring = attr.get_write_value()
        print >> self.log_info, "Attribute value = ", self.xmlc.xmlstring


#---- XMLString attribute State Machine -----------------
    def is_XMLString_allowed(self, _):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    Read JSONSettings attribute
#------------------------------------------------------------------
    def read_JSONSettings(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_JSONSettings()"
        attr.set_value(self.xmlc.jsonsettings)


#------------------------------------------------------------------
#    Write JSONSettings attribute
#------------------------------------------------------------------
    def write_JSONSettings(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_JSONSettings()"
        if self.is_JSONSettings_write_allowed():
            self.xmlc.jsonsettings = attr.get_write_value()
            print >> self.log_info, "Attribute value = ", self.xmlc.jsonsettings
        else:
            print >> self.log_warn , \
                "To change the settings please close the server."
            raise Exception, \
                "To change the settings please close the server." 

#---- JSONSettings attribute Write State Machine -----------------
    def is_JSONSettings_write_allowed(self):
        if self.get_state() in [PyTango.DevState.OPEN,
                                PyTango.DevState.RUNNING]:
            return False
        return True



#------------------------------------------------------------------
#    Read Version attribute
#------------------------------------------------------------------
    def read_Version(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_Version()"

        self.get_device_properties(self.get_device_class())
        self.xmlc.versionLabel = self.VersionLabel
        attr.set_value(self.xmlc.version)


#---- Version attribute State Machine -----------------
    def is_Version_allowed(self, _):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#    Read Variables attribute
#------------------------------------------------------------------
    def read_Variables(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_Variables()"
        attr.set_value(self.xmlc.variables)


#------------------------------------------------------------------
#    Write Variables attribute
#------------------------------------------------------------------
    def write_Variables(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_Variables()"
        self.xmlc.variables = attr.get_write_value()
        print >> self.log_info, "Attribute value = ", self.xmlc.variables


#---- Variables attribute State Machine -----------------
    def is_Variables_allowed(self, _):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True





#==================================================================
#
#    NXSConfigServer command methods
#
#==================================================================

#------------------------------------------------------------------
#    Open command:
#
#    Description: Opens connection to the database
#                
#------------------------------------------------------------------
    def Open(self):
        print >> self.log_info, "In ", self.get_name(), "::Open()"
        try:
            if self.get_state() == PyTango.DevState.OPEN:
                self.set_state(PyTango.DevState.RUNNING)
                self.xmlc.close()
            self.set_state(PyTango.DevState.RUNNING)
            self.xmlc.open()
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.ON)


#---- Open command State Machine -----------------
    def is_Open_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    Close command:
#
#    Description: Closes connection into the database
#                
#------------------------------------------------------------------
    def Close(self):
        print >> self.log_info, "In ", self.get_name(), "::Close()"

        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.xmlc.close()
            self.set_state(PyTango.DevState.ON)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.ON)


#---- Close command State Machine -----------------
    def is_Close_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    Components command:
#
#    Description: Returns a list of required components
#                
#    argin:  DevVarStringArray    list of component names
#    argout: DevVarStringArray    list of required components
#------------------------------------------------------------------
    def Components(self, argin):
        print >> self.log_info, "In ", self.get_name(), "::Components()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.components(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        
        return argout


#---- Components command State Machine -----------------
    def is_Components_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    DataSources command:
#
#    Description: Return a list of required DataSources
#                
#    argin:  DevVarStringArray    list of DataSource names
#    argout: DevVarStringArray    list of required DataSources
#------------------------------------------------------------------
    def DataSources(self, argin):
        print >> self.log_info, "In ", self.get_name(), "::DataSources()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.dataSources(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        
        return argout


#---- DataSources command State Machine -----------------
    def is_DataSources_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    AvailableComponents command:
#
#    Description: Returns a list of available component names
#                
#    argout: DevVarStringArray    list of available component names
#------------------------------------------------------------------
    def AvailableComponents(self):
        print >> self.log_info, "In ", self.get_name(), \
            "::AvailableComponents()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.availableComponents()
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        
        return argout


#---- AvailableComponents command State Machine -----------------
    def is_AvailableComponents_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    AvailableDataSources command:
#
#    Description: Returns a list of available DataSource names
#                
#    argout: DevVarStringArray    list of available DataSource names
#------------------------------------------------------------------
    def AvailableDataSources(self):
        print >> self.log_info, "In ", self.get_name(), \
            "::AvailableDataSources()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.availableDataSources()
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        
        return argout


#---- AvailableDataSources command State Machine -----------------
    def is_AvailableDataSources_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    StoreComponent command:
#
#    Description: Stores the component from XMLString
#                
#    argin:  DevString    component name
#------------------------------------------------------------------
    def StoreComponent(self, argin):
        print >> self.log_info, "In ", self.get_name(), "::StoreComponent()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.xmlc.storeComponent(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)


#---- StoreComponent command State Machine -----------------
    def is_StoreComponent_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    StoreDataSource command:
#
#    Description: Stores the DataSource from XMLString
#                
#    argin:  DevString    datasource name
#------------------------------------------------------------------
    def StoreDataSource(self, argin):
        print >> self.log_info, "In ", self.get_name(), "::StoreDataSource()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.xmlc.storeDataSource(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)


#---- StoreDataSource command State Machine -----------------
    def is_StoreDataSource_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    CreateConfiguration command:
#
#    Description: Creates the NDTS configuration script from the 
#                 given components. The result is strored in XMLString
#                
#    argin:  DevVarStringArray    list of component names
#------------------------------------------------------------------
    def CreateConfiguration(self, argin):
        print >> self.log_info, "In ", self.get_name(), \
            "::CreateConfiguration()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.xmlc.createConfiguration(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)


#---- CreateConfiguration command State Machine -----------------
    def is_CreateConfiguration_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    DeleteComponent command:
#
#    Description: Deletes the given component
#                
#    argin:  DevString    component name
#------------------------------------------------------------------
    def DeleteComponent(self, argin):
        print >> self.log_info, "In ", self.get_name(), "::DeleteComponent()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.xmlc.deleteComponent(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)


#---- DeleteComponent command State Machine -----------------
    def is_DeleteComponent_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    DeleteDataSource command:
#
#    Description: Deletes the given datasource
#                
#    argin:  DevString    datasource name
#------------------------------------------------------------------
    def DeleteDataSource(self, argin):
        print >> self.log_info, "In ", self.get_name(), "::DeleteDataSource()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.xmlc.deleteDataSource(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)


#---- DeleteDataSource command State Machine -----------------
    def is_DeleteDataSource_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    SetMandatoryComponents command:
#
#    Description: Sets the mandatory components
#                
#    argin:  DevVarStringArray    component names
#------------------------------------------------------------------
    def SetMandatoryComponents(self, argin):
        print >> self.log_info, "In ", self.get_name(), \
            "::SetMandatoryComponents()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.xmlc.setMandatoryComponents(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)


#---- SetMandatoryComponents command State Machine -----------------
    def is_SetMandatoryComponents_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    MandatoryComponents command:
#
#    Description: Sets the mandatory components
#                
#    argout: DevVarStringArray    component names
#------------------------------------------------------------------
    def MandatoryComponents(self):
        print >> self.log_info, "In ", self.get_name(), \
            "::MandatoryComponents()"
        #    Add your own code here
        
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.mandatoryComponents()
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        return argout


#---- MandatoryComponents command State Machine -----------------
    def is_MandatoryComponents_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    UnsetMandatoryComponents command:
#
#    Description: It removes the given components from the mandatory components
#                
#    argin:  DevVarStringArray    list of component names
#------------------------------------------------------------------
    def UnsetMandatoryComponents(self, argin):
        print >> self.log_info, "In ", self.get_name(), \
            "::UnsetMandatoryComponents()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.xmlc.unsetMandatoryComponents(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)


#---- UnsetMandatoryComponents command State Machine -----------------
    def is_UnsetMandatoryComponents_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    ComponentDataSources command:
#
#    Description: returns a list of datasource names for a given component
#                
#    argin:  DevString    component name
#    argout: DevVarStringArray    list of datasource names
#------------------------------------------------------------------
    def ComponentDataSources(self, argin):
        print >> self.log_info, "In ", self.get_name(), \
            "::ComponentDataSources()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.componentDataSources(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        
        return argout


#---- ComponentDataSources command State Machine -----------------
    def is_ComponentDataSources_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    ComponentsDataSources command:
#
#    Description: returns a list of datasource names for a given components
#                
#    argin:  DevVarStringArray    component names
#    argout: DevVarStringArray    list of datasource names
#------------------------------------------------------------------
    def ComponentsDataSources(self, argin):
        print >> self.log_info, "In ", self.get_name(), \
            "::ComponentsDataSources()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.componentsDataSources(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        
        return argout


#---- ComponentsDataSources command State Machine -----------------
    def is_ComponentsDataSources_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#    ComponentsVariables command:
#
#    Description: returns a list of variable names for a given components
#                
#    argin:  DevVarStringArray    component names
#    argout: DevVarStringArray    list of variable names
#------------------------------------------------------------------
    def ComponentsVariables(self, argin):
        print >> self.log_info, "In ", self.get_name(), \
            "::ComponentsVariables()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.componentsVariables(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        
        return argout


#---- ComponentsVariables command State Machine -----------------
    def is_ComponentsVariables_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#    ComponentVariables command:
#
#    Description: returns a list of variable names for a given component
#                
#    argin:  DevString    component name
#    argout: DevVarStringArray    list of variable names
#------------------------------------------------------------------
    def ComponentVariables(self, argin):
        print >> self.log_info, "In ", self.get_name(), "::ComponentVariables()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.componentVariables(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        
        return argout



#---- ComponentVariables command State Machine -----------------
    def is_ComponentVariables_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#    Merge command:
#
#    Description: Merges give components
#                
#    argin:  DevVarStringArray    list of component names
#    argout: DevString    merged components
#------------------------------------------------------------------
    def Merge(self, argin):
        print >> self.log_info, "In ", self.get_name(), "::Merge()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.merge(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        return argout

#---- Merge command State Machine -----------------
    def is_Merge_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True

#------------------------------------------------------------------
#    DependentComponents command:
#
#    Description: returns a list of dependent component names 
#        for a given components
#                
#    argin:  DevVarStringArray    component names
#    argout: DevVarStringArray    list of component names
#------------------------------------------------------------------
    def DependentComponents(self, argin):
        print >> self.log_info, "In ", self.get_name(), \
            "::DependentComponents()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.xmlc.dependentComponents(argin)
            self.set_state(PyTango.DevState.OPEN)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.OPEN)
        
        return argout



#---- DependentComponents command State Machine -----------------
    def is_DependentComponents_allowed(self):
        if self.get_state() in [PyTango.DevState.ON,
                                PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True



#==================================================================
#
##    NXSConfigServerClass class definition
#
#==================================================================
class NXSConfigServerClass(PyTango.DeviceClass):

    ##    Class Properties
    class_property_list = {
        }


    ##    Device Properties
    device_property_list = {
        'VersionLabel':
            [PyTango.DevString,
            "version label",
            [ "XCS" ] ],
        }


    ##    Command definitions
    cmd_list = {
        'Open':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVoid, ""]],
        'Close':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVoid, ""]],
        'Components':
            [[PyTango.DevVarStringArray, "list of component names"],
            [PyTango.DevVarStringArray, "list of required components"]],
        'DataSources':
            [[PyTango.DevVarStringArray, "list of DataSource names"],
            [PyTango.DevVarStringArray, "list of required DataSources"]],
        'AvailableComponents':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVarStringArray, "list of available component names"]],
        'AvailableDataSources':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVarStringArray, "list of available DataSource names"]],
        'StoreComponent':
            [[PyTango.DevString, "component name"],
            [PyTango.DevVoid, ""]],
        'StoreDataSource':
            [[PyTango.DevString, "datasource name"],
            [PyTango.DevVoid, ""]],
        'CreateConfiguration':
            [[PyTango.DevVarStringArray, "list of component names"],
            [PyTango.DevVoid, ""]],
        'DeleteComponent':
            [[PyTango.DevString, "component name"],
            [PyTango.DevVoid, ""]],
        'DeleteDataSource':
            [[PyTango.DevString, "datasource name"],
            [PyTango.DevVoid, ""]],
        'SetMandatoryComponents':
            [[PyTango.DevVarStringArray, "component names"],
            [PyTango.DevVoid, ""]],
        'MandatoryComponents':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVarStringArray, "component names"]],
        'UnsetMandatoryComponents':
            [[PyTango.DevVarStringArray, "list of component names"],
            [PyTango.DevVoid, ""]],
        'ComponentDataSources':
            [[PyTango.DevString, "component name"],
            [PyTango.DevVarStringArray, "list of datasource names"]],
        'ComponentsDataSources':
            [[PyTango.DevVarStringArray, "component names"],
            [PyTango.DevVarStringArray, "list of datasource names"]],
        'ComponentsVariables':
            [[PyTango.DevVarStringArray, "component names"],
            [PyTango.DevVarStringArray, "list of variable names"]],
        'ComponentVariables':
            [[PyTango.DevString, "component name"],
            [PyTango.DevVarStringArray, "list of variable names"]],
        'Merge':
            [[PyTango.DevVarStringArray, "list of component names"],
            [PyTango.DevString, "merged components"]],
        'DependentComponents':
            [[PyTango.DevVarStringArray, "component names"],
            [PyTango.DevVarStringArray, "list of component names"]],
        }


    ##    Attribute definitions
    attr_list = {
        'XMLString':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"XML configuration",
                'description':\
                    "It allows to pass XML strings into database during "\
                    "performing StoreComponent and StoreDataSource."\
                    "\nMoreover, after performing CreateConfiguration "\
                    "it contains the resulting XML configuration.",
                'Display level':PyTango.DispLevel.EXPERT,
            } ],
        'JSONSettings':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Arguments of MySQLdb.connect(...)",
                'description':"The JSON string with parameters of "\
                    "MySQLdb.connect(...).",
                'Memorized':"true",
                'Display level':PyTango.DispLevel.EXPERT,
            } ],
        'Version':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ],
            {
                'label':"configuration version",
                'description':"Configuration version",
            } ],
        'Variables':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"XML configuration variables",
                'description':"The JSON string with "\
                    "XML configuration variables",
            } ],
        }


#------------------------------------------------------------------
##    NXSConfigServerClass Constructor
#
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name)
        print "In NXSConfigServerClass  constructor"

#==================================================================
#
#    NXSConfigServer class main method
#
#==================================================================
if __name__ == '__main__':
    pass

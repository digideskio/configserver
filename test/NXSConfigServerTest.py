#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2016 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
## \package test nexdatas
## \file NXSConfigServerTest.py
# unittests for field Tags running Tango Server
#
import unittest
import os
import sys
import subprocess
import random
import time
import PyTango

import ServerSetUp
import XMLConfiguratorTest
#import XMLConTest as XMLConfiguratorTest
from nxsconfigserver import XMLConfigurator
import nxsconfigserver
## test fixture
class NXSConfigServerTest(XMLConfiguratorTest.XMLConfiguratorTest):

    ## constructor
    # \param methodName name of the test method
    def __init__(self, methodName):
        XMLConfiguratorTest.XMLConfiguratorTest.__init__(self, methodName)

        self._sv = ServerSetUp.ServerSetUp()



    ## test starter
    # \brief Common set up of Tango Server
    def setUp(self):
        self._sv.setUp()
        print "SEED =", self.seed 

    ## test closer
    # \brief Common tear down oif Tango Server
    def tearDown(self): 
        XMLConfiguratorTest.XMLConfiguratorTest.tearDown(self)
        self._sv.tearDown()
        
    ## opens config server
    # \param args connection arguments
    # \returns NXSConfigServer instance   
    def openConfig(self, args):
        
        found = False
        cnt = 0
        while not found and cnt < 1000:
            try:
                print "\b.",
                xmlc = PyTango.DeviceProxy(self._sv.new_device_info_writer.name)
                time.sleep(0.01)
                if xmlc.state() == PyTango.DevState.ON:
                    found = True
                found = True
            except Exception,e:    
                print self._sv.new_device_info_writer.name,e
                found = False
            except:
                found = False
                
            cnt +=1

        if not found:
            raise Exception, "Cannot connect to %s" % self._sv.new_device_info_writer.name


        if xmlc.state()== PyTango.DevState.ON:
            xmlc.JSONSettings = args
            xmlc.Open()
        version = xmlc.version
        vv = version.split('.')
        self.revision = long(vv[-1])
        self.version = ".".join(vv[0:3])
        self.label = ".".join(vv[3:-1])

        self.assertEqual(self.version, nxsconfigserver.__version__ )
        self.assertEqual(self.label, '.'.join(xmlc.Version.split('.')[3:-1]))

        
        self.assertEqual(xmlc.state(), PyTango.DevState.OPEN)
        
        return xmlc


    ## closes opens config server
    # \param xmlc XMLConfigurator instance   
    def closeConfig(self, xmlc):
        self.assertEqual(xmlc.state(), PyTango.DevState.OPEN)

        xmlc.Close()
        self.assertEqual(xmlc.state(), PyTango.DevState.ON)
                
    ## sets xmlconfiguration
    # \param xmlc configuration instance
    # \param xml xml configuration string
    def setXML(self, xmlc, xml):
        xmlc.XMLString = xml


    ## gets xmlconfiguration
    # \param xmlc configuration instance
    # \returns xml configuration string
    def getXML(self, xmlc):
        return xmlc.XMLString 
        



if __name__ == '__main__':
    unittest.main()


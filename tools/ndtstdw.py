#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2013 DESY, Jan Kotanski <jkotan@mail.desy.de>
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
## \package tools nexdatas.configserver
## \file ndtstdw.py
# Command-line tool for ascess to configuration server
#


import sys
import os
import time

from optparse import OptionParser
import PyTango


## configuration server adapter
class NexusServer(object):
    ## constructor
    # \param device device name of configuration server
    def __init__(self, device):
        found = False
        cnt = 0

        try:
            ## configuration server proxy
            self.tdwServer = PyTango.DeviceProxy(device)
        except Exception, e:
#            sys.stderr.write(str(e))
            found = True
            
        if found:
            sys.stderr.write("Error: Cannot connect into configuration server: %s\n"% device)
            sys.stderr.flush()
            sys.exit(255)

        while not found and cnt < 1000:
            if cnt > 1:
                time.sleep(0.01)
            try:
                if self.tdwServer.state() != PyTango.DevState.RUNNING:
                    found = True
            except Exception,e:
#                sys.stderr.write(str(e))
                time.sleep(0.01)
                found = False
            cnt +=1

        if not found:
            sys.stderr.write("Error: Setting up %s takes to long\n"% device)
            sys.stderr.flush()
            sys.exit(255)

            

    def openFile(self, filename):
        self.tdwServer.Init()
        self.tdwServer.FileName = str(filename)
        self.tdwServer.OpenFile()


    def setData(self, jsondata):
        self.tdwServer.TheJSONRecord = str(jsondata)

    def openEntry(self, xmlconfig):
        self.tdwServer.TheXMLSettings = str(xmlconfig)
        self.tdwServer.OpenEntry()

    def record(self, jsondata):
        self.tdwServer.Record(jsondata)

    def closeEntry(self):
        self.tdwServer.CloseEntry()

    def closeFile(self):
        self.tdwServer.CloseFile()
        



    ## perform requested command
    # \param command called command
    # \param args list of item names
    def performCommand(self, command, args):
#    commands = ['openfile','openentry','setdata','record','closeentry','closefile'] 
       if command == 'openfile':
            return self.openFile(args[0]) 
       if command == 'setdata':
            return self.setData(args[0].strip()) 
       if command == 'openentry':
            return self.openEntry(args[0].strip()) 
       if command == 'record':
            return self.record(args[0].strip()) 
       if command == 'closefile':
            return self.closeFile() 
       if command == 'closeentry':
            return self.closeEntry() 
            
## the main function
def main():
    
    
    ## pipe arguments
    pipe = ""
    if not sys.stdin.isatty():
        pp = sys.stdin.readlines()
        ## system pipe 
        pipe = "".join(pp)
        

    commands = ['openfile','openentry','setdata','record','closeentry','closefile']
    ## run options
    options = None
    ## usage example
    usage = "usage: %prog <command> -s <nexus_server> "\
            +" [<arg1> [<arg2>  ...]] \n"\
            +" e.g.: %prog openfile -s p02/tangodataserver/exp.01  $HOME/myfile.h5 \n\n"\
            + "Commands: \n"\
            + "   openfile -s <config_server>  <file_name> \n"\
            + "          open new H5 file\n"\
            + "   setdata -s <config_server> <json_data_string>  \n"\
            + "          assign global JSON data\n"\
            + "   openentry -s <config_server> <xml_config>  \n"\
            + "          create new entry\n"\
            + "   record -s <config_server>  <json_data_string>  \n"\
            + "          record one step with step JSON data \n"\
            + "   closeentry -s <config_server>   \n"\
            + "          close the current entry \n"\
            + "   closefile -s <config_server>  \n"\
            + "          close the current file \n"\
            + " "

    ## option parser
    parser = OptionParser(usage=usage)
    parser.add_option("-s","--server", dest="server", 
                      help="configuration server device name")

    (options, args) = parser.parse_args()

    if not args or args[0] not in commands or not options.server :
        parser.print_help()
        print ""
        sys.exit(255)


    ## configuration server     
    tdwserver = NexusServer(options.server)
    
    ## command-line and pipe arguments
    parg = args[1:]
    if pipe:
        parg.append(pipe)
        
    ## result to print
    result = tdwserver.performCommand(args[0], parg)
    if result and str(result).strip():
        print result



if __name__ == "__main__":
    main()

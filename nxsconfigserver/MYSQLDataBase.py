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
#

""" Providesthe access to MYSQL database with NDTS configuration files """

import MySQLdb

from .Errors import NonregisteredDBRecordError
from . import Streams


class MYSQLDataBase(object):
    """ XML Configurer
    """

    def __init__(self):
        """ constructor

        :brief: It creates the MYSQLDataBase instance
        """
        #: (:class:`MySQLdb.connections.Connection`) db instance
        self.__db = None
        #: (:obj:`dict` <:obj:`str`, any>) connect arguments
        self.__args = None

    def connect(self, args):
        """ connects to the database

        :param args: arguments of the MySQLdb connect method
        :type args: :obj:`dict` <:obj:`str`, any>
        """
        Streams.info("MYSQLDataBase::connect() - connect: %s" % args)
        self.__db = MySQLdb.connect(**args)
        self.__args = args

    def close(self):
        """ closes database connection

        :brief: It closes connection to the open database
        """
        if self.__db:
            try:
                self.__db.ping(True)
                if self.__db.open:
                    self.__db.close()
            except:
                pass

    def version(self):
        """ provides DB configuration version

        :returns: DB configuration version
        :rtype: :obj:`str`
        """
        argout = None
        cursor = None
        if self.__db is not None:
            try:
                try:
                    self.__db.ping(True)
                except:
                    return argout
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select value from properties where name = 'revision';")
                data = cursor.fetchone()
                if not data or not data[0]:
                    raise NonregisteredDBRecordError(
                        "Component %s not registered in the database"
                        % self.__args)
                argout = data[0]
                cursor.close()
            except:
                if cursor:
                    cursor.close()
                raise
        return argout

    @classmethod
    def __escape(cls, string):
        """ adds escape characters to string

        :param string: input string
        :type string: :obj:`str`
        :retruns: string with excape characters
        :rtype: :obj:`str`
        """
        return string.replace("\\", "\\\\").replace("'", "\\\'")

    @classmethod
    def __incRevision(cls, cursor):
        """ increases revision number

        :param cursor: transaction cursor
        :type cursor: :class:`MySQLdb.cursors.Cursor`
        """
        cursor.execute(
            "select value from properties where name = 'revision';")
        data = cursor.fetchone()
        new = str(long(data[0]) + 1)
        cursor.execute(
            "update properties set value = '%s' where name = 'revision';"
            % (cls.__escape(new)))

    def components(self, names):
        """ fetches the required components

        :param names: list of component names
        :type names: :obj:`list` <:obj:`str`>
        :returns: list of given components
        :rtype: :obj:`list` <:obj:`str`>
        """
        argout = []
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                for ar in names:
                    cursor.execute(
                        "select xml from components where name = '%s';"
                        % self.__escape(ar))
                    data = cursor.fetchone()
                    if not data or not data[0]:
                        raise NonregisteredDBRecordError(
                            "Component %s not registered in the database" % ar)
                    argout.append(data[0])
                cursor.close()
            except:
                cursor.close()
                raise
        return argout

    def selections(self, names):
        """ fetches the required selections

        :param names: list of selection names
        :type names: :obj:`list` <:obj:`str`>
        :returns: list of given selections
        :rtype: :obj:`list` <:obj:`str`>
        """
        argout = []
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                for ar in names:
                    cursor.execute(
                        "select selection from selections where name = '%s';"
                        % self.__escape(ar))
                    data = cursor.fetchone()
                    if not data or not data[0]:
                        raise NonregisteredDBRecordError(
                            "Selection %s not registered in the database" % ar)
                    argout.append(data[0])
                cursor.close()
            except:
                cursor.close()
                raise
        return argout

    def dataSources(self, names):
        """ fetches the required datasources

        :param names: list of datasource names
        :type names: :obj:`list` <:obj:`str`>
        :returns: list of given datasources
        :rtype: :obj:`list` <:obj:`str`>
        """
        argout = []
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                for ar in names:
                    cursor.execute(
                        "select xml from datasources where name = '%s';"
                        % self.__escape(ar))
                    data = cursor.fetchone()
                    if not data or not data[0]:
                        raise NonregisteredDBRecordError(
                            "DataSource %s not registered in the database"
                            % ar)
                    argout.append(data[0])
                cursor.close()
            except:
                cursor.close()
                raise
        return argout

    def availableComponents(self):
        """ fetches the names of available components

        :returns: list of available components
        :rtype: :obj:`list` <:obj:`str`>
        """
        argout = []
        if self.__db is not None:
            try:
                self.__db.ping(True)
                cursor = self.__db.cursor()
                cursor.execute("select name from components;")
                data = cursor.fetchall()
                argout = [d[0] for d in data]
                cursor.close()
            except:
                cursor.close()
                raise

        return argout

    def availableSelections(self):
        """ fetches the names of available selections

        :returns: list of available selections
        :rtype: :obj:`list` <:obj:`str`>
        """
        argout = []
        if self.__db is not None:
            try:
                self.__db.ping(True)
                cursor = self.__db.cursor()
                cursor.execute("select name from selections;")
                data = cursor.fetchall()
                argout = [d[0] for d in data]
                cursor.close()
            except:
                cursor.close()
                raise

        return argout

    def availableDataSources(self):
        """ fetches the names of available datasources

        :returns: list of available datasources
        :rtype: :obj:`list` <:obj:`str`>
        """
        argout = []
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute("select name from datasources;")
                data = cursor.fetchall()
                argout = [d[0] for d in data]
                cursor.close()
            except:
                cursor.close()
                raise
        return argout

    def storeComponent(self, name, xml):
        """ stores the given component

        :param name: name of the component to store
        :type name: :obj:`str`
        :param xml: component tree
        :type xml: :obj:`str`
        """
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select xml from components where name = '%s';"
                    % self.__escape(name))
                data = cursor.fetchone()
                if data and len(data) > 0 and data[0]:
                    if data[0] != xml:
                        cursor.execute(
                            "update components set xml"
                            " = '%s' where name = '%s';"
                            % (self.__escape(xml),
                               self.__escape(name)))
                        self.__incRevision(cursor)
                        self.__db.commit()
                    else:
                        self.__db.rollback()
                else:
                    cursor.execute(
                        "insert into components "
                        "values('%s', '%s', 0);"
                        % (self.__escape(name),
                           self.__escape(xml)))
                    self.__incRevision(cursor)
                    self.__db.commit()
                cursor.close()
            except:
                self.__db.rollback()
                cursor.close()
                raise

            Streams.info("MYSQLDataBase::storeComponent()"
                         " - store component %s" % name)

    def storeDataSource(self, name, xml):
        """ stores the given datasource

        :param name: name of the datasource to store
        :type name: :obj:`str`
        :param xml: datasource tree
        :type xml: :obj:`str`
        """
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select xml from datasources where name = '%s';"
                    % self.__escape(name))
                data = cursor.fetchone()
                if data and len(data) > 0 and data[0]:
                    if data[0] != xml:
                        cursor.execute(
                            "update datasources set "
                            "xml = '%s' where name = '%s';"
                            % (self.__escape(xml),
                               self.__escape(name)))
                        self.__incRevision(cursor)
                        self.__db.commit()
                    else:
                        self.__db.rollback()
                else:
                    cursor.execute(
                        "insert into datasources "
                        "values('%s', '%s');"
                        % (self.__escape(name),
                           self.__escape(xml)))

                    self.__incRevision(cursor)
                    self.__db.commit()
                cursor.close()
            except:
                self.__db.rollback()
                cursor.close()
                raise
            Streams.info("MYSQLDataBase::storeDataSource() "
                         "- store datasource %s" % name)

    def storeSelection(self, name, selection):
        """ stores the given selection

        :param name: name of the selection to store
        :type name: :obj:`str`
        :param selection: selection tree
        :type selection: :obj:`str`
        """
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select selection from selections where name = '%s';"
                    % self.__escape(name))
                data = cursor.fetchone()
                if data and len(data) > 0 and data[0]:
                    if data[0] != selection:
                        cursor.execute(
                            "update selections set "
                            "selection = '%s' where name = '%s';"
                            % (self.__escape(selection),
                               self.__escape(name)))
#                        self.__incRevision(cursor)
                        self.__db.commit()
                    else:
                        self.__db.rollback()
                else:
                    cursor.execute(
                        "insert into selections "
                        "values('%s', '%s');"
                        % (self.__escape(name),
                           self.__escape(selection)))

#                    self.__incRevision(cursor)
                    self.__db.commit()
                cursor.close()
            except:
                self.__db.rollback()
                cursor.close()
                raise
            Streams.info("MYSQLDataBase::storeSelection() "
                         "- store selection %s" % name)

    def deleteComponent(self, name):
        """ deletes the given component

        :param name: name of the component to delete
        :type name: :obj:`str`
        """
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select exists(select 1 from components where "
                    "name = '%s');" % self.__escape(name))
                data = cursor.fetchone()
                if data[0]:
                    cursor.execute(
                        "delete from components where name = '%s';"
                        % self.__escape(name))

                    self.__db.commit()
                self.__incRevision(cursor)
                cursor.close()
            except:
                self.__db.rollback()
                cursor.close()
                raise

            Streams.info("MYSQLDataBase::deleteComponent() "
                         "- delete component %s" % name)

    def deleteSelection(self, name):
        """ deletes the given selection

        :param name: name of the selection to delete
        :type name: :obj:`str`
        """
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select exists(select 1 from selections where "
                    "name = '%s');" % self.__escape(name))
                data = cursor.fetchone()
                if data[0]:
                    cursor.execute(
                        "delete from selections where name = '%s';"
                        % self.__escape(name))

                    self.__db.commit()
#                self.__incRevision(cursor)
                cursor.close()
            except:
                self.__db.rollback()
                cursor.close()
                raise

            Streams.info("MYSQLDataBase::deleteSelection() "
                         "- delete selection %s" % name)

    def setMandatory(self, name):
        """ sets components as mandatory

        :param name: name of the component
        :type name: :obj:`str`
        """
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select mandatory from components where name = '%s';"
                    % self.__escape(name))
                data = cursor.fetchone()
                if data and len(data) > 0 and data[0] != 1:
                    cursor.execute(
                        "update components set mandatory = 1 where "
                        "name = '%s';" % self.__escape(name))
                    self.__db.commit()
                    self.__incRevision(cursor)
                else:
                    self.__db.rollback()
                cursor.close()
            except:
                self.__db.rollback()
                cursor.close()
                raise
            Streams.info(
                "MYSQLDataBase::setMandatory() - component %s" % name)

    def unsetMandatory(self, name):
        """sets components as not mandatory

        :param name: name of the component to delete
        :type name: :obj:`str`
        """
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select mandatory from components where name = '%s';"
                    % self.__escape(name))
                data = cursor.fetchone()
                if data and len(data) > 0 and data[0] != 0:
                    cursor.execute(
                        "update components set mandatory = 0 where "
                        "name = '%s';" % self.__escape(name))

                    self.__db.commit()
                    self.__incRevision(cursor)
                else:
                    self.__db.rollback()

                cursor.close()
            except:
                self.__db.rollback()
                cursor.close()
                raise

            Streams.info("MYSQLDataBase::unsetMandatory() "
                         "- component %s" % name)

    def mandatory(self):
        """ provides mandatory components

        :returns: list of mandatory components
        :rtype: :obj:`list` <:obj:`str`>
        """
        argout = []
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select name from components where mandatory = 1")
                data = cursor.fetchall()
                argout = [d[0] for d in data]
                cursor.close()
            except:
                raise

        return argout

    def deleteDataSource(self, name):
        """ deletes the given datasource

        :param name: name of the datasource to delete
        :type name: :obj:`str`
        """
        if self.__db is not None:
            try:
                self.__db.ping(True)
                if not self.__db.open:
                    self.connect(self.__args)
                cursor = self.__db.cursor()
                cursor.execute(
                    "select exists(select 1 from datasources where "
                    "name = '%s');" % self.__escape(name))
                data = cursor.fetchone()
                if data[0]:
                    cursor.execute(
                        "delete from datasources where name = '%s';"
                        % self.__escape(name))

                    self.__db.commit()
                self.__incRevision(cursor)
                cursor.close()
            except:
                self.__db.rollback()
                cursor.close()
                raise
            Streams.info("MYSQLDataBase::deleteDataSource() "
                         "- datasource %s" % name)


if __name__ == "__main__":
    pass

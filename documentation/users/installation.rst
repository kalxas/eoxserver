.. Installation
  #-----------------------------------------------------------------------------
  # $Id$
  #
  # Project: EOxServer <http://eoxserver.org>
  # Authors: Fabian Schindler <fabian.schindler@eox.at>
  #
  #-----------------------------------------------------------------------------
  # Copyright (C) 2020 EOX IT Services GmbH
  #
  # Permission is hereby granted, free of charge, to any person obtaining a
  # copy of this software and associated documentation files (the "Software"),
  # to deal in the Software without restriction, including without limitation
  # the rights to use, copy, modify, merge, publish, distribute, sublicense,
  # and/or sell copies of the Software, and to permit persons to whom the
  # Software is furnished to do so, subject to the following conditions:
  #
  # The above copyright notice and this permission notice shall be included in
  # all copies of this Software or works derived from this Software.
  #
  # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
  # DEALINGS IN THE SOFTWARE.
  #-----------------------------------------------------------------------------

.. _Installation:

Installation
============

This document is a guide to install EOxServer.

Installing from packages
------------------------

EOxServer is packaged and distributed as a Python package. With that in
prerequisite it is easy to define other Python dependencies. Unfortunately
this is not the case for non-Python libraries, as they typically need to
be installed via the operating systems package management system or some
other means. Table: ":ref:`table_eoxserver_dependencies`" below shows
the minimal required software to run EOxServer.

.. _table_eoxserver_dependencies:
.. table:: EOxServer Dependencies

  +-----------+------------------+---------------------------------------------+
  | Software  | Required Version | Description                                 |
  +===========+==================+=============================================+
  | GDAL      | >= 1.7.0         | Geospatial Data Abstraction Library         |
  |           |                  | providing common interfaces for accessing   |
  |           |                  | various kinds of raster and vector data     |
  |           |                  | formats and including a Python binding      |
  |           |                  | which is used by EOxServer                  |
  +-----------+------------------+---------------------------------------------+
  | GEOS      | >= 3.0           | GEOS (Geometry Engine - Open Source) is a   |
  |           |                  | C++ port of the  Java Topology Suite (JTS). |
  +-----------+------------------+---------------------------------------------+
  | libxml2   | >= 2.7           | Libxml2 is the XML C parser and toolkit     |
  |           |                  | developed for the Gnome project.            |
  +-----------+------------------+---------------------------------------------+
  | MapServer | >= 7.0           | Server software implementing various OGC    |
  |           |                  | Web Service interfaces including WCS and    |
  |           |                  | WMS. Includes a Python binding which is     |
  |           |                  | used by EOxServer.                          |
  +-----------+------------------+---------------------------------------------+


When all non-python dependencies are installed, EOxServer can be installed
using the ``pip`` (or sometimes ``pip3``) utility.

::

    # pip3 install -U eoxserver

In the default setting, this also fetches all Python package dependencies. The
``-U`` switch denotes that if EOxServer is already installed, it will be
upgraded to the latest version.

If not otherwise packaged (like with Docker, see below), it is preferred to use
a virtual environment


Using Docker images
-------------------

If Docker is available, the easiest way to set up and use EOxServer
is to use the pre-built and maintained docker images. The images can
be obtained using the ``docker pull`` command like so:
::

    # docker pull eoxa/eoxserver
    Using default tag: latest
    latest: Pulling from eoxa/eoxserver
    93956c6f8d9e: Pull complete
    46bddb84d1c5: Pull complete
    15fa85048576: Pull complete
    8aa40341c4fa: Pull complete
    7a299ef02497: Pull complete
    09229f9ea579: Pull complete
    3163f1230278: Pull complete
    2f90ec943f31: Pull complete
    12b403f83389: Pull complete
    d6c5830b2cc6: Pull complete
    658ea0984fee: Pull complete
    7fbc330a1a79: Pull complete
    Digest: sha256:7ec2310bf28074c34410fadb72c2c1b7dddbd6e381d97ce22ce0d738cd591619
    Status: Downloaded newer image for eoxa/eoxserver:latest
    docker.io/eoxa/eoxserver:latest


.. note:: This will fetch the image with the ``latest`` tag by
          default. Other tags using a different operating system
          or package versions may be available as well.

This image can now be started using the ``docker run`` command.
::

    # docker run --rm -it -p 8000:8000 eoxa/eoxserver


As single docker containers are hard to control by themselves, other
tools like Docker Compose can help to keep static and runtime
configuration manageable.

Consider the following ``docker-compose.yml`` file:

.. code-block:: yaml

    version: "3.6"
    services:
      database:
        image: mdillon/postgis:10
        volumes:
          - database-data:/var/lib/postgresql/data
        environment:
          POSTGRES_USER: "user"
          POSTGRES_PASSWORD: "pw"
          POSTGRES_DB: "dbms"
      eoxserver:
        image: eoxa/eoxserver
        environment:
          DB_USER: "user"
          DB_PW: "pw"
          DB_HOST: database
          DB_PORT: 5432
          DB_NAME: "dbms"
          XML_CATALOG_FILES: /opt/schemas/catalog.xml
        ports:
          - "8800:8000"

    volumes:
      database-data:

This Docker Compose file can now be used to manage the database and EOxServer
in a single step. The following command starts the services in the Compose
file.

::

    docker-compose up

The benefit of this approach is that with Docker Compose the services can
resolve the other services by their names without having to deal with manual
connection or hassling with IP addresses.

For production deployment, Docker Swarm is recommended instead.

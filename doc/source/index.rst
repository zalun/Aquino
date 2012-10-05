.. Aquino documentation master file, created by
   sphinx-quickstart on Thu Oct  4 10:14:31 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Aquino's documentation!
==================================

*Aquino* (which is a development name) is an opensource tool directed to
measure and control freshwater aquariums. `Fork it on github
<https://github.com/zalun/Aquino>`_

.. warning::

   Aquino is currently in very early stage. We are working on measurements and
   web parts (REST API and WebApp client). There is no device which is
   running.

.. note::

   If you'd like to contact us, please do it via IRC. Find ``zalun`` or
   ``dwarder`` on freenode ``#arduino`` or ``#jsfiddle`` channels

Aquino is measuring at least one of the parameters important for
the ecosystem.

One of the major feature of Aquino is alarming the user if any of the
measured parameters will change its value away from defined range.

Aquino is also able to control the tank. Following features are considered:

 * feeder
 * switch the filter onoff while feeding
 * manipulate lights
 * apply chemicals

Contents:

.. toctree::
   :maxdepth: 2

   architecture.rst
   measurements/index.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


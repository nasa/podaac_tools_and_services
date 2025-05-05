podaac_tools_and_services
=========================
This is a meta-repository which lists locations of code related to all tools and services software for `NASA JPL's Physical Oceanography Distributed Active Archive Center (PO.DAAC) <https://podaac.jpl.nasa.gov>`__.

** This repository has been archived as of May 2025.  It is not actively used and is archived for informational and legacy purposes  **

|image7|

What is PO.DAAC?
----------------
The `PO.DAAC <https://podaac.jpl.nasa.gov>`__ is an element of the Earth Observing System Data and Information System (`EOSDIS <https://earthdata.nasa.gov/>`__). The EOSDIS provides science data to a wide community of users for NASA's Science Mission Directorate. `PO.DAAC <https://podaac.jpl.nasa.gov>`__ has become the premier data center for measurements focused on ocean surface topography (OST), sea surface temperature (SST), ocean winds, sea surface salinity (SSS), gravity, ocean circulation and sea ice.

What's in this repository?
--------------------------
This repository reflects an active catalog of all tools and services software pertaining to `PO.DAAC data access <https://podaac.jpl.nasa.gov/dataaccess>`__. If you have a suggestion for a new tool or would like to update the content here, please `open an issue <https://github.com/nasa/podaac_tools_and_services/issues>`__ or `send a pull request <https://github.com/nasa/podaac_tools_and_services/pulls>`__.

Where do I find detailed information on tools and services included in this repository?
---------------------------------------------------------------------------------------
Each repository has it's own README file e.g. `data_animation/README.rst <https://github.com/nasa/podaac_tools_and_services/blob/master/data_animation/README.rst>`__

Keeping Git submodules up-to-date
---------------------------------
In order to keep the submodules as defined in [.gitmodules](https://github.com/nasa/podaac_tools_and_services/blob/master/.gitmodules) up-to-date it is necessary to periodically push updates. You can safely execute this command to do so::


    $ git submodule foreach git pull origin master
    $ git status //you will then see the changes which have been mode
    $ git add -A
    $ git commit -m "Update submodules"
    $ git push origin master


License
-------
| Unless noted explicitly, all code in this repository is licensed permissively under the `Apache License
  v2.0 <http://www.apache.org/licenses/LICENSE-2.0>`__.
| A copy of that license is distributed with each software project.

Copyright and Export Classification
-----------------------------------

::

    Copyright 2019, by the California Institute of Technology. ALL RIGHTS RESERVED. 
    United States Government Sponsorship acknowledged. Any commercial use must be 
    negotiated with the Office of Technology Transfer at the California Institute 
    of Technology.
    This software may be subject to U.S. export control laws. By accepting this software, 
    the user agrees to comply with all applicable U.S. export laws and regulations. 
    User has the responsibility to obtain export licenses, or other export authority 
    as may be required before exporting such information to foreign countries or 
    providing access to foreign persons.

.. |image7| image:: https://podaac.jpl.nasa.gov/sites/default/files/image/custom_thumbs/podaac_logo.png

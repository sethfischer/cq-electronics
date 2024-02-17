============
Contributing
============

Development environment
-----------------------

#. Clone and install:

    .. code:: text

        git clone https://github.com/sethfischer/cq-electronics.git
        cd cq-electronics
        poetry env use python3.11
        poetry install
        poetry shell

#. Install Git hooks:

    .. code:: text

        make install-git-hooks

#. Install CQ-editor:

    .. code:: text

        poetry install --with cq-editor

#. Open examples from the ``examples`` directory with CQ-editor:

    .. code:: text

        cq-editor examples/raspberry_pi_3b.py


Documentation
-------------

Build the documentation:

.. code:: text

    make -C docs/ clean html

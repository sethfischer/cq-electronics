============
Contributing
============

Development environment
-----------------------

#. Clone and install:

    .. code:: text

        git clone https://github.com/sethfischer/cq-electronics.git
        cd cq-electronics
        poetry env use python3.12
        poetry install
        eval $(poetry env activate)

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


Publish release
---------------

.. code-block:: text

    git checkout main
    cz bump --no-verify
    git push origin main && git push --tags
    make poetry-build
    poetry publish

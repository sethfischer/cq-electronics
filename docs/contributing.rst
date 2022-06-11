============
Contributing
============

Development environment
-----------------------

Poetry
~~~~~~

#. Clone and install cq-electronics.

    a. Clone and install:

        .. code:: text

            git clone https://github.com/sethfischer/cq-electronics.git
            cd cq-electronics
            virrtualenv .venv
            . .venv/bin/activate
            python3 -m pip install --upgrade pip
            poetry install

    b. Install Git hooks:

        .. code:: text

            make install-git-hooks

#. Create a new project with cq-electronics installed in editable mode.

    a. Create new project:

        .. code:: text

            mkdir cq-electronics-dev
            cd cq-electronics-dev
            virrtualenv .venv
            . .venv/bin/activate
            python3 -m pip install --upgrade pip
            poetry init

        In ``pyproject.toml`` specify relative path to cq-electronics:

        .. code:: toml

            [tool.poetry]
            name = "cq-electronics-dev"
            version = "0.1.0"
            description = "Development project for cq-electronics"
            authors = ["name <email>"]

            [tool.poetry.dependencies]
            python = ">=3.8,<3.11"
            cq-electronics = {path = "../cq-electronics", develop = true}

            [tool.poetry.dev-dependencies]
            cq-editor = {git = "https://github.com/CadQuery/CQ-editor"}
            PyQt5 = "^5.15.6"
            spyder = "~=5.0"
            path = "^16.4.0"
            pyqtgraph = "^0.12.4"
            Logbook = "^1.5.3"
            requests = "^2.27.1"

            [build-system]
            requires = ["poetry-core>=1.0.0"]
            build-backend = "poetry.core.masonry.api"

    b. Install dependencies, including ``../cq-electronics``:

        .. code:: text

            poetry install

    c. Copy examples from the ``examples`` directory and open with CQ-editor:

        .. code:: text

            cp ../cq-electronics/examples/*.py ./
            cq-editor raspberry_pi_3b.py

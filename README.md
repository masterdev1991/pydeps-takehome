# tc-interview-problem-python-deps

Your primary task will be to implement some Python dependency management features to this codebase. This code
repository has the following structure:

```
tc-interview-problem-python-deps
├── .git
├── .gitignore
├── Dockerfile
├── Makefile
├── README.md
├── apps
│   ├── job-a
│   │   ├── Dockerfile
│   │   └── app.py
│   ├── job-b
│   │   ├── Dockerfile
│   │   └── app.py
│   ├── job-c
│   │   ├── Dockerfile
│   │   └── app.py
│   ├── server-one
│   │   ├── Dockerfile
│   │   └── app.py
│   └── server-two
│       ├── Dockerfile
│       └── app.py
├── lib
│   └── verse
│       └── common.py
├── pyproject.toml
├── scripts
│   └── main.py
├── static_data
│   ├── enron_emails_1702.csv
│   └── LD2011_2014.csv
└── tests
    ├── test_runtime.py
    └── verse
        └── test_common.py
```

To start things off, please complete the following setup steps:


## Python Environment

### Pre-setup

TODO: paste the result of the following command immediately below for your active Python runtime
```
python --version
which python
```

### Python Versions

TODO: please paste all the versions of Python you have installed, e.g. if you have `pyenv` installed you can obtain
this with `pyenv versions`


## Coding Assignment

If you downloaded or cloned this repository for the Live Coding track (Track A), you will be asked to implement the
`align_python_deps()` method in `scripts/main.py`. Please see the `TODO(centerpiece)` in-lined.

And if you have opted into the Take Home track (Track B), please follow the instructions in the
`Case-Study-SWE-DistributedSystems-PythonDeps.pdf` you've been given.

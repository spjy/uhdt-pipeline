# UHDT Pipeline

The script integrating all of the image processing scripts.

## Requirements
1. Python 3.7+
2. pip

## Installation

```bash
$ pip install pipenv virtualenv # install pip
$ virtualenv .venv # Initialize venv environment
$ .venv/Scripts/activate # Start virtualenv environment
$ pip install -r requirements.txt # Install dependencies
```

Duplicate (DO NOT RENAME) the `.env.example` file and rename it to `.env`. Adjust the values as necessary.

## Running

You should be in the virtualenv environment whenever you want to run any scripts internally in the project.

```bash
$ .venv\Scripts\activiate # Start virtualenv environment
```

To run the watcher script (for new files)

```bash
$ py .\src\watcher.py
```

To run the pipeline script:

```bash
$ py .\src\Pipeline.py
```

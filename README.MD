Takes a config file as input from STDIN with the following line format:
MM HH ANY_NAME
With any number of lines, and minute/hour can also be replaced by an '\*'.

Requires current time in HH:MM format as command line argument.

Prints the next execution time for each job in a new line.

## Requirements
- Python with at least version 3.6

## Running
`./cronjob.py HH:MM < config`

Requires the script to be executable:

`chmod +x cronjob.py`

or run

`python cronjob.py HH:MM < config`

## Run Tests
`python tests.py -v`
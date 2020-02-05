Takes a config file as input from STDIN with the following line format:
MM HH ANY_NAME
With any number of lines, and minute/hour can also be replaced by an '\*'.

Requires current time in HH:MM format as command line argument.

Prints the next execution time for each job in a new line.

## Requirements
- Python with at least version 3.6

## Example
With the __test_config.txt__ file as:
```
30 1 /bin/run_me_daily
45 * /bin/run_me_hourly
* * /bin/run_me_every_minute
* 19 /bin/run_me_sixty_times
```
And running the script with:
`./cronjob.py 16:10 < test_config.txt`
Will yield the following result:
```
1:30 tomorrow - /bin/run_me_daily
16:45 today - /bin/run_me_hourly
16:10 today - /bin/run_me_every_minute
19:00 today - /bin/run_me_sixty_times
```

## Running
`./cronjob.py HH:MM < test_config.txt`

Requires the script to be executable:

`chmod +x cronjob.py`

or run

`python cronjob.py HH:MM < test_config.txt`

## Run Tests
`python test_cronjob.py -v`
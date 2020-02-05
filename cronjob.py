#!/usr/bin/env python

"""
Takes a config file as input from STDIN with the following line format:
MM HH ANY_NAME
With any number of lines, and minute/hour can also be replaced by an '*'.

Requires current time in HH:MM format as command line argument.

Prints the next execution time for each job in a new line."""

import sys
import traceback

class Time:
	""" represents a specific time at a day, but can also contain
	wildcard * as hour or/and minute."""
	def __init__(self, hour, minute):
		if not (minute == "*" or int(minute) < 60):
			raise ValueError("Minute doesn't have the right format")
		if not (hour == "*" or int(hour) < 24):
			raise ValueError("Hour doesn't have the right format")
		self.minute = int(minute) if minute != "*" else minute
		self.hour = int(hour) if hour != "*" else hour


class CronJob:
	""" one object represents one job (one line of a config file)"""
	def __init__(self, minute, hour, name):
		self.time = Time(hour, minute)
		self.name = name

	def __str__(self):
		return f"{self.time.minute} {self.time.hour} {self.name}"

	def __repr__(self):
		return f"{self.time.minute} {self.time.hour} {self.name}"

def parse_cron_config(config_lines):
	""" parse input lines to read cron job config file.
	returns a list of CronJobs"""
	cron_lines = []
	for line in config_lines:
		try:
			minute, hour, name = line.strip().split(" ")[0:3]
			cron_new = CronJob(minute, hour, name)
			cron_lines.append(cron_new)
		except ValueError:
			# traceback.print_exc()
			print(f"Error: Invalid config file. Line [{config_lines.index(line)}] does not have the required format:")
			print(f"\t{line.strip()}")
			return []

	return cron_lines

def find_job_runtime(job_t1, t2):
	""" returns the next runtime for job_t1.
	main challenge is to replace wildcards ('*') in job, otherwise
	it's trivial.
	"""
	t1_hour_fixed = job_t1.hour
	t1_minute_fixed = job_t1.minute

	## replace wildcards
	## TWO WILDCARDS
	if job_t1.minute == "*" and job_t1.hour == "*":
		## trivial case with two wildcards
		t1_hour_fixed = t2.hour
		t1_minute_fixed = t2.minute
	## HOUR WILDCARD only
	elif job_t1.hour == "*" and job_t1.minute != "*":
		if t2.minute <= job_t1.minute:
			## still in this hour
			t1_hour_fixed = t2.hour
		else:
			## next hour, mind day change
			t1_hour_fixed = (t2.hour + 1) % 24
	## MINUTE WILDCARD only
	elif job_t1.hour != "*" and job_t1.minute == "*":
		if t2.hour == job_t1.hour:
			## same hour, so now
			t1_minute_fixed = t2.minute
		else:
			## not this hour, so :00
			t1_minute_fixed = 0

	return Time(t1_hour_fixed, t1_minute_fixed)
	

def get_next_runtime(job, current_time):
	""" formats the time when the given job runs next, given the current_time."""
	run_time = find_job_runtime(job.time, current_time)

	day = "today"
	if run_time.hour < current_time.hour or \
		(run_time.hour == current_time.hour and run_time.minute < current_time.minute):
		day = "tomorrow"

	return f"{run_time.hour}:{run_time.minute:0>2} {day} - {job.name}"

def get_upcoming_runtimes(cron_jobs, current_time):
	""" prints the next runtime for each job, given the current_time."""

	assert type(current_time) is Time
	assert all(type(job) is CronJob for job in cron_jobs)

	## get runtime for each single job
	next_runtimes = [get_next_runtime(job, current_time) for job in cron_jobs]

	return next_runtimes

def parse_current_time(time_input):
	try:
		input_arg = time_input
		hour, minute = input_arg.split(":")
		input_time = Time(hour, minute)
		return input_time
	except IndexError:
		print("Error: requires a command line argument")
		return
	except ValueError:
		print("Error: argument has wrong time format (requires HH:MM)")
		return

def main():
	## read from STDIN
	stdin_lines = sys.stdin.readlines()
	## and parse config file
	cron_jobs = parse_cron_config(stdin_lines)

	# print("found the following jobs:")
	# [print(f"\t{c}") for c in cron_jobs]
	# if len(cron_jobs) == 0:
	# 	print("Error: found no cron jobs in config file")
	# 	return

	## read time from command line argument
	input_time = parse_current_time(sys.argv[1])

	## check which jobs run when next
	upcoming = get_upcoming_runtimes(cron_jobs, input_time)

	print("\n".join(upcoming))

if __name__ == '__main__':
	main()
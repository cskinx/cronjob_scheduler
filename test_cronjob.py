#!/usr/bin/env python

import unittest
import cronjob

class TimeParser(unittest.TestCase):
	## test the parser of the current time

	def test_correct(self):
		time_parsed = cronjob.parse_current_time("11:30")
		self.assertTrue(time_parsed.hour == 11)
		self.assertTrue(time_parsed.minute == 30)

	def test_false_hour(self):
		time_parsed = cronjob.parse_current_time("25:30")
		self.assertTrue(time_parsed is None)

	def test_false_minute(self):
		time_parsed = cronjob.parse_current_time("20:60")
		self.assertTrue(time_parsed is None)

	def test_false_chars(self):
		time_parsed = cronjob.parse_current_time("2a:30")
		self.assertTrue(time_parsed is None)

class TestCronParser(unittest.TestCase):
	## test the config file parser

	def test_correct(self):
		config_fine = [
			"30 1 /bin/run_me_daily",
			"45 * /bin/run_me_hourly",
			"* * /bin/run_me_every_minute",
			"* 19 /bin/run_me_sixty_times",
		]

		config_parsed = cronjob.parse_cron_config(config_fine)
		self.assertTrue(len(config_parsed), len(config_fine))

	def test_false_format(self):
		## missing a column
		config = ["* /bin/test",]
		config_parsed = cronjob.parse_cron_config(config)

		self.assertTrue(len(config_parsed) == 0)

	def test_false_hour(self):
		## hour too high
		config = ["* 45 /bin/test",]
		config_parsed = cronjob.parse_cron_config(config)

		self.assertTrue(len(config_parsed) == 0)

	def test_false_minute(self):
		## minute too high
		config = ["80 * /bin/test",]
		config_parsed = cronjob.parse_cron_config(config)

		self.assertTrue(len(config_parsed) == 0)

	def test_false_chars(self):
		## chars shouldn't be accepted
		config = ["AA ?? /bin/test",]
		config_parsed = cronjob.parse_cron_config(config)

		self.assertTrue(len(config_parsed) == 0)

class UpcomingJobsTest(unittest.TestCase):
	## test the correct output of the script

	def test_correct_1610(self):
		## run whole script and verify result
		config_fine = [
			"30 1 /bin/run_me_daily",
			"45 * /bin/run_me_hourly",
			"* * /bin/run_me_every_minute",
			"* 19 /bin/run_me_sixty_times",
			"0 0 /bin/run_me_nightly",
			"* 16 /bin/run_me_sixtyeen_times",
			"00 16 /bin/run_me_afternoonly",
		]
		expected = [
			"1:30 tomorrow - /bin/run_me_daily",
			"16:45 today - /bin/run_me_hourly",
			"16:10 today - /bin/run_me_every_minute",
			"19:00 today - /bin/run_me_sixty_times",
			"0:00 tomorrow - /bin/run_me_nightly",
			"16:10 today - /bin/run_me_sixtyeen_times",
			"16:00 tomorrow - /bin/run_me_afternoonly",
		]
		current_time = "16:10"

		cron_jobs = cronjob.parse_cron_config(config_fine)
		input_time = cronjob.parse_current_time(current_time)
		upcoming = cronjob.get_upcoming_runtimes(cron_jobs, input_time)

		self.assertTrue(len(upcoming) == len(config_fine))
		for i in range(len(config_fine)):
			self.assertTrue(upcoming[i] == expected[i],
			 msg=f"'{upcoming[i]}' does not match {expected[i]}")


	def test_correct_2359(self):
		## run whole script and verify result
		## same as above but with a different time
		config_fine = [
			"30 1 /bin/run_me_daily",
			"45 * /bin/run_me_hourly",
			"* * /bin/run_me_every_minute",
			"* 19 /bin/run_me_sixty_times",
			"0 0 /bin/run_me_nightly",
			"* 16 /bin/run_me_sixtyeen_times",
			"00 16 /bin/run_me_afternoonly",
			"12 12 /bin/run_me_noonly ignore_this",
		]
		expected = [
			"1:30 tomorrow - /bin/run_me_daily",
			"0:45 tomorrow - /bin/run_me_hourly",
			"23:59 today - /bin/run_me_every_minute",
			"19:00 tomorrow - /bin/run_me_sixty_times",
			"0:00 tomorrow - /bin/run_me_nightly",
			"16:00 tomorrow - /bin/run_me_sixtyeen_times",
			"16:00 tomorrow - /bin/run_me_afternoonly",
			"12:12 tomorrow - /bin/run_me_noonly",
		]
		current_time = "23:59"

		cron_jobs = cronjob.parse_cron_config(config_fine)
		input_time = cronjob.parse_current_time(current_time)
		upcoming = cronjob.get_upcoming_runtimes(cron_jobs, input_time)

		self.assertTrue(len(upcoming) == len(config_fine))
		for i in range(len(config_fine)):
			self.assertTrue(upcoming[i] == expected[i],
			 msg=f"'{upcoming[i]}' does not match {expected[i]}")

if __name__ == '__main__':
	unittest.main()
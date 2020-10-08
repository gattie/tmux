#!/usr/bin/env python
"""[summary]

Returns:
    [type]: [description]
"""
import sys
from datetime import date
from calendar import monthrange, isleap
from time import localtime
import argparse

class Progress():
    """[summary]
    """
    def __init__(self):
        self.today = date.today()
        self.localtime = localtime()

    def month_progress(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        total_days_in_month = monthrange(self.today.year, self.today.month)[1]
        percent_of_month = self.today.day/total_days_in_month

        return percent_of_month

    def year_progress(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        day_of_year = self.today.timetuple().tm_yday
        total_days_in_year = 366 if isleap(self.today.year) else 365
        percent_of_year = day_of_year/total_days_in_year

        return percent_of_year

    def day_progress(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        total_sec = self.localtime.tm_hour * 60 * 60 + \
                    self.localtime.tm_min * 60 + \
                    self.localtime.tm_sec
        percent_of_day = total_sec/86400

        return percent_of_day

    def work_progress(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        start_seconds = 9*60*60
        end_seconds = 17*60*60
        total_sec = self.localtime.tm_hour * 60 * 60 + \
                    self.localtime.tm_min * 60 + \
                    self.localtime.tm_sec
        if total_sec < start_seconds:
            total_sec = 0
        elif total_sec > end_seconds:
            total_sec = end_seconds
        else:
            total_sec = total_sec - start_seconds
        percent_of_work = total_sec/end_seconds

        return percent_of_work

def output_progress(progress_percent, time_range):
    """[summary]

    Args:
        progress_percent ([type]): [description]
        time_range ([type]): [description]
    """
    print("{:>5}: [{:<20}] {}%".format(
        time_range,
        '='*round(20*progress_percent),
        round(progress_percent*100)
        ))

def progress_parser():
    """[summary]

    Returns:
        [type]: [description]
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--day", action="store_true",
                        help="return the progress of the current day")
    parser.add_argument("-m", "--month", action="store_true",
                        help="return the progress of the current month")
    parser.add_argument("-y", "--year", action="store_true",
                        help="return the progress of the current year")
    parser.add_argument("-w", "--work", action="store_true",
                        help="return the progress of the work day")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    progress = Progress()

    if args.day:
        day_progress = progress.day_progress()
        output_progress(day_progress, "Day")
    if args.month:
        month_progress = progress.month_progress()
        output_progress(month_progress, "Month")
    if args.year:
        year_progress = progress.year_progress()
        output_progress(year_progress, "Year")
    if args.work:
        work_progress = progress.work_progress()
        output_progress(work_progress, "Work")

if __name__ == '__main__':
    progress_parser()

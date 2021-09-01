#!/usr/bin/env python3
"""[summary]

Returns:
    [type]: [description]
"""
import sys
from datetime import date
from calendar import monthrange, isleap
from time import localtime, sleep
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

    def work_progress(self, start_hour=9, end_hour=17):
        """[summary]

        Returns:
            [type]: [description]
        """
        start_seconds = start_hour*60*60
        end_seconds = end_hour*60*60
        work_seconds = end_seconds - start_seconds
        total_sec = self.localtime.tm_hour * 60 * 60 + \
                    self.localtime.tm_min * 60 + \
                    self.localtime.tm_sec
        if total_sec < start_seconds:
            total_sec = 0
        elif total_sec > end_seconds:
            total_sec = work_seconds
        else:
            total_sec = total_sec - start_seconds
        percent_of_work = total_sec/work_seconds

        return percent_of_work

    def twenty_20_twenty(self):
        next_break = self.localtime.tm_min % 20
        if next_break == 0:
            for i in range(20, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write("{:2d}s - Break time! Look 20 ft away".format(i))
                sys.stdout.flush()
                sleep(1)
        else:
            print("Next break in {} minutes".format(20 - next_break))

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
    parser.add_argument("-20", "--twenty", action="store_true",
                        help="Indicates if you should take a break")
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
    if args.twenty:
        progress.twenty_20_twenty()

if __name__ == '__main__':
    progress_parser()

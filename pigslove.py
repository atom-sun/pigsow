#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
from numpy import exp, log

d0 = datetime.date(2019, 11, 26)
INIT_love = 5


def lin_love(days):
    return INIT_love + days / 100


def calibrate(cal_date):
    cal_days = (cal_date - d0).days
    cal_love = lin_love(cal_days)
    return cal_days, cal_love


def exp_love(days, cal):
    cal_days, cal_love = calibrate(cal)
    return INIT_love * exp(days * (log(cal_love) - log(INIT_love)) / cal_days)


def log_love(days, cal):
    cal_days, cal_love = calibrate(cal)
    return INIT_love + log(1 + days) * (cal_love - INIT_love) / log(1 + cal_days)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--form', choices=['lin', 'exp', 'log'],
                        default='lin', help='the form of the behavior')
    parser.add_argument('-c', '--calibrate', default='20191127',
                        help='calibrate date to match the linear one')
    parser.add_argument('-d', '--date', help='specify the date')
    args = parser.parse_args()
    form, cal, date = args.form, args.calibrate, args.date
    assert len(cal) == 8
    cal = datetime.date(*map(int, (cal[0:4], cal[4:6], cal[6:8])))
    if date is None:
        date = datetime.datetime.now().date()
    else:
        assert len(date) == 8
        date = datetime.date(*map(int, (date[0:4], date[4:6], date[6:8])))
    days = (date - d0).days
    if form == 'lin':
        love = lin_love(days)
    elif form == 'exp':
        love = exp_love(days, cal)
    elif form == 'log':
        love = log_love(days, cal)
    print(f'\nLove level on  {str(date):s} :  {love: 3.4f}\n')

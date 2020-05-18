#!/usr/bin/env python3
import logging
import os
from random import choice, choices, randint
import sched
import sys
import time
import datetime
import calendar

import aws_lambda_logging
from cachetools import TTLCache, cached

log = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

INTERVALS = [1,5,10,15,30,60,90,120,150,180,240,300]
EXCEPTION_TYPES = ['TypeError', 'NameError','ModuleNotFoundError','DatabaseNotFoundError','ZeroDivisionError']
day_cache = TTLCache(maxsize=1000, ttl=3600)

@cached(day_cache)
def find_day():
    day_num = datetime.datetime.today().weekday()
    return (calendar.day_name[day_num])

def make_errors():
    day = find_day()
    for n in range(0,choice(INTERVALS)):
        for exception in choices(EXCEPTION_TYPES,k=randint(1,len(EXCEPTION_TYPES))):
            log.error("{}: Uh oh something is wrong - Today is {}".format(exception,day))
        time.sleep(1/choice(INTERVALS))

def make_warns():
    day = find_day()
    for n in range(0,choice(INTERVALS)):
        for exception in choices(EXCEPTION_TYPES,k=randint(1,len(EXCEPTION_TYPES))):
            log.warn("{}: This is a warn - Today is {}".format(exception,day))
            log.warning("{}: This is a warning - Today is {}".format(exception,day))
        time.sleep(1/choice(INTERVALS))

def make_fatals():
    day = find_day()
    for n in range(0,choice(INTERVALS)):
        for exception in choices(EXCEPTION_TYPES,k=randint(1,len(EXCEPTION_TYPES))):
            log.fatal("{}: This is fatal - Today is {}".format(exception,day))
        time.sleep(1/choice(INTERVALS))

def make_info():
    day = find_day()
    for n in range(0,choice(INTERVALS)):
        log.info("Today is {} and this is fine".format(day))
        time.sleep(0.25)

def main():
    aws_lambda_logging.setup(
        level=os.environ.get('LOGLEVEL', 'INFO'),
        boto_level='CRITICAL'
    )
    methods = [make_errors,make_warns,make_fatals,make_info]
    s = sched.scheduler(time.time, time.sleep)
    while True:
        s.enter(0.5,1,choice(methods))
        s.enter(0.5,1,choice(methods))
        s.run()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import logging
import os
from random import choice, choices
import sched
import sys
import time

import aws_lambda_logging

log = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

INTERVALS = [1,5,10,15,30,60,90,120,150,180,240,300]
EXCEPTION_TYPES = ['TypeError', 'NameError','ModuleNotFoundError']

def make_errors():
    for n in range(0,choice(INTERVALS)):
        for exception in choices(EXCEPTION_TYPES,k=2):
            log.error("{}: Houston, we have a problem".format(exception))
        time.sleep(1/choice(INTERVALS))

def make_info():
    for n in range(0,choice(INTERVALS)):
        log.info("This is fine")
        time.sleep(0.25)

def main():
    aws_lambda_logging.setup(
        level=os.environ.get('LOGLEVEL', 'INFO'),
        boto_level='CRITICAL'
    )
    methods = [make_errors,make_info]
    s = sched.scheduler(time.time, time.sleep)
    while True:
        s.enter(0.5,1,choice(methods))
        s.enter(0.5,1,choice(methods))
        s.run()

if __name__ == "__main__":
    main()
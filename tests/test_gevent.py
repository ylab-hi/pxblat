#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gevent
from gevent.pool import Pool


def work(i):
    gevent.sleep(1)
    return i + 1


pool = Pool(10)

ret = pool.map(work, range(10))


print(ret)

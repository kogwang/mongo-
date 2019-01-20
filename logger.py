# -*- coding:utf-8 -*-
import os
import sys
import logging
import gzip
import time
import gzip
from logging.handlers import TimedRotatingFileHandler

env_dist = os.environ
# 这里用了环境变量。也可以写配置文件。按实际要求来。不过以后一些配置会往环境变量走
log_path = env_dist.get('LOG_PATH', '/var/log/surveyHM/log.log')


class LoggerWriter:
    def __init__(self, level):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.level = level

    def write(self, message):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message != '\n':
            self.level(message)

    def flush(self):
        # create a flush method so things can be flushed when
        # the system wants to. Not sure if simply 'printing'
        # sys.stderr is the correct way to do it, but it seemed
        # to work properly for me.
        self.level(sys.stderr)


logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename=log_path,
                    level=logging.DEBUG
                    )
logger = logging.getLogger('')


# sys.stdout = LoggerWriter(logger.info)
# sys.stderr = LoggerWriter(logger.error)

# class GzTimedRotatingFileHandler(TimedRotatingFileHandler):
#     def __init__(self, filename, when, interval, backupCount):
#         TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount)
#     def doGzip(self, old_log):
#         with open(old_log) as old:
#             with gzip.open(old_log + '.gz', 'wb') as comp_log:
#                 comp_log.writelines(old)
#         os.remove(old_log)
#
#     def doRollover(self):
#         if self.stream:
#             self.stream.close()
#             self.stream = None
#         # get the time that this sequence started at and make it a TimeTuple
#         currentTime = int(time.time())
#         dstNow = time.localtime(currentTime)[-1]
#         t = self.rolloverAt - self.interval
#         if self.utc:
#             timeTuple = time.gmtime(t)
#         else:
#             timeTuple = time.localtime(t)
#             dstThen = timeTuple[-1]
#             if dstNow != dstThen:
#                 if dstNow:
#                     addend = 3600
#                 else:
#                     addend = -3600
#                 timeTuple = time.localtime(t + addend)
#         dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
#         if os.path.exists(dfn):
#             os.remove(dfn)
#         # Issue 18940: A file may not have been created if delay is True.
#         if os.path.exists(self.baseFilename):
#             os.rename(self.baseFilename, dfn)
#             self.doGzip(dfn)
#         if self.backupCount > 0:
#             for s in self.getFilesToDelete():
#                 os.remove(s)
#         if not self.delay:
#             self.stream = self._open()
#         newRolloverAt = self.computeRollover(currentTime)
#         while newRolloverAt <= currentTime:
#             newRolloverAt = newRolloverAt + self.interval
#         if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
#             dstAtRollover = time.localtime(newRolloverAt)[-1]
#             if dstNow != dstAtRollover:
#                 if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
#                     addend = -3600
#                 else:  # DST bows out before next rollover, so we need to add an hour
#                     addend = 3600
#                 newRolloverAt += addend
#         self.rolloverAt = newRolloverAt


# if log_path != '':
#     gz_handler = GzTimedRotatingFileHandler(filename=log_path, when="W6", interval=1, backupCount=30)
#     logger.addHandler(gz_handler)

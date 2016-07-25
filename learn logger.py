#coding:utf-8
import logging

# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('test00.log')
# 再创建一个handler，用于输出到控制台
# ch = logging.StreamHandler()

# 定义handler的输出格式formatter
formatter = logging.Formatter('%(asctime)s%(funcName)s%(module)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
# ch.setFormatter(formatter)


# 给logger添加handler
#logger.addFilter(filter)
logger.addHandler(fh)
# logger.addHandler(ch)


# 记录一条日志
logger.debug('logger debug message')
logger.info('logger info message')
logger.warning('logger warning message')
logger.error('logger error message')
logger.critical('logger critical message')

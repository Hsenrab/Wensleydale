import datetime


class WTime(object):
    """Class that wraps time object so it can be mocked"""
    @staticmethod
    def get_now():
        return datetime.datetime.now()




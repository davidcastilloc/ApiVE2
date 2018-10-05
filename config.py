
class config(object):
    """docstring for config"""
    SECRET_KEY = '84a54fa37b591b64e13e2db2ce2bcd7c9c0c310c92d83e61'


class DevelopmentConfig(object):
    """docstring for DevelopmentConfig"""
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(object):
    """docstring for DevelopmentConfig"""
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False

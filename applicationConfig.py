import configparser


class Config:

    class __Config:
        def __init__(self, configfile):
            config = configparser.ConfigParser()
            config.read(configfile)
            self.config = config

    instance = None

    def __new__(cls, configfile):
        if not Config.instance:
            Config.instance = Config.__Config(configfile)
        return Config.instance

    @classmethod
    def get_mqtt_config(cls):
        return cls.instance.config['MQTT-BROKER']

    @classmethod
    def get_database_config(cls):
        return cls.instance.config['DATABASE-POSTGRES']
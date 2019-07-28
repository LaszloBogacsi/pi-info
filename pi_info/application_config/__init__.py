import configparser

from pi_info.application_config.database_config import DatabaseConfig
from pi_info.application_config.mqtt_config import MqttConfig


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
    def get_mqtt_config(cls) -> MqttConfig:
        mqtt_conf = cls.instance.config['MQTT-BROKER']
        return MqttConfig(mqtt_conf['username'], mqtt_conf['password'], mqtt_conf['host'])

    @classmethod
    def get_database_config(cls) -> DatabaseConfig:
        postgres_config = cls.instance.config['DATABASE-POSTGRES']
        return DatabaseConfig(postgres_config['user'], postgres_config['password'], postgres_config['host'], postgres_config['database'])
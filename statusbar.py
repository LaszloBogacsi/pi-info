from temperature_repository import load_current_temperature


def refresh_statusbar():
    current_temperature = load_current_temperature()
    statusbar_data = {"current_temperature": {"indoor": current_temperature}}
    return statusbar_data
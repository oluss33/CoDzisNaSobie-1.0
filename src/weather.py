class Weather:
    def __init__(self, temperature, wind, hourly_temp):
        self.__temperature = temperature
        self.__wind = wind
        self.__hourly_temp = hourly_temp

    @property
    def temperature(self):
        return self.__temperature

    @property
    def wind(self):
        return self.__wind

    @property
    def hourly_temp(self):
        return self.__hourly_temp
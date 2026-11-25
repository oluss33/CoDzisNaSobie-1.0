class Weather:
    def __init__(self, temperature, wind, pressure, hourly_temp, hourly_pressure, precipitation, precipitation_probability, snowfall, rain, weather_code,):
        self.__temperature = temperature
        self.__wind = wind
        self.__hourly_temp = hourly_temp
        self.__pressure = pressure
        self.__hourly_pressure = hourly_pressure
        self.__precipitation = precipitation
        self.__precipitation_probability = precipitation_probability
        self.__snowfall = snowfall
        self.__rain = rain
        self.__weather_code = weather_code

    @property
    def weather_code(self):
        return self.__weather_code

    @property
    def precipitation(self):
        return self.__precipitation

    @property
    def precipitation_probability(self):
        return self.__precipitation_probability

    @property
    def snowfall(self):
        return self.__snowfall

    @property
    def rain(self):
        return self.__rain

    @property
    def temperature(self):
        return self.__temperature

    @property
    def wind(self):
        return self.__wind

    @property
    def hourly_temp(self):
        return self.__hourly_temp

    @property
    def pressure(self):
        return self.__pressure

    @property
    def hourly_pressure(self):
        return self.__hourly_pressure


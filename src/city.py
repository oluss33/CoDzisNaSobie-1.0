class City:
    def __init__(self, name, country, admin, lat, lon):
        self.__name = name
        self.__country = country
        self.__admin = admin
        self.__lat = lat
        self.__lon = lon

    @property
    def name(self):
        return self.__name
    @property
    def country(self):
        return self.__country
    @property
    def admin(self):
        return self.__admin
    @property
    def lat(self):
        return self.__lat
    @property
    def lon(self):
        return self.__lon

    def __str__(self):
        return f"jestem miastem {self.name}"
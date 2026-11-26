import json_manager


class City:
    def __init__(self, page, name, country, admin, lat, lon, is_favorite = None):
        self.__page = page
        self.__name = name
        self.__country = country
        self.__admin = admin
        self.__lat = lat
        self.__lon = lon
        if not is_favorite:
            self.is_favorite = json_manager.is_city_favorite(page.session.store.get("id"), name, lat, lon)
        else:
            self.is_favorite = is_favorite

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
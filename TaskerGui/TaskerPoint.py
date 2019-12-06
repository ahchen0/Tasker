class Point:
    """
    Object that represents a point on Earth's surface

    :param str name: Name of point
    :param float lat: Latitude
    :param float lon: Longitude
    """
    
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
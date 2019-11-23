from app import db
import random

class Field(db.Model):
    __tablename__ = 'sbvectors2'
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String)
    acres = db.Column(db.Float)
    coordinates = db.Column(db.String)

    def __init__(self, crop, acres, coordinates):
        self.crop = crop
        self.acres = acres
        self.coordinates = coordinates

    def set_mean(self):
        #stub
        self.mean = random.random()*10

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_centroid(self):
        lat_centroid = 0
        lng_centroid = 0
        num_datapoints = len(self.coordinates.get("coordinates"))
        for point in self.coordinates.get("coordinates"):
            lat_centroid += point["lat"]
            lng_centroid += point["lng"]
        lat_centroid = lat_centroid / num_datapoints
        lng_centroid = lng_centroid / num_datapoints
        return (lat_centroid, lng_centroid)

    def set_efficiency(self, score):
        self.efficiency = score

    def serialize(self):
        return {
            'id': self.id,
            'crop': self.crop,
            'acres': self.acres,
            'coordinates': self.coordinates,
            'efficiency': self.efficiency
        }

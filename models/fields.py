from app import db
import random

class Field(db.Model):
    __tablename__ = 'huron_delano_vectors'
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String)
    acres = db.Column(db.Float)
    coordinates = db.Column(db.String)

    def __init__(self, crop, acres, coordinates):
        self.crop = crop
        self.acres = acres
        self.coordinates = coordinates

    def set_mean(self, mean = None):
        #stub
        if mean == None:
            mean = random.random()*10
        self.mean = mean

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def set_centroid(self):
        lat_centroid = 0
        lng_centroid = 0
        num_datapoints = len(self.coordinates.get("coordinates"))
        for point in self.coordinates.get("coordinates"):
            try:
                lat_centroid += point["lat"]
                lng_centroid += point["lng"]
            except TypeError:
                print("lat lng TYPE ERROR!")
                self.centroid = (0,0)
        lat_centroid = lat_centroid / num_datapoints
        lng_centroid = lng_centroid / num_datapoints
        self.centroid = (lat_centroid, lng_centroid)

    def get_centroid(self):
        return self.centroid
    
    def get_id(self):
        return self.id
    
    def get_crop(self):
        return self.crop

    def set_score(self, score):
        self.score = score

    def set_group_id(self, group_id):
        # A group_id is the which group this field belongs to that was used to calculate its efficiency score
        self.group_id = group_id

    def serialize(self):
        
        return {
            'id': self.id,
            'group_id': self.group_id,
            'crop': self.crop,
            'acres': self.acres,
            'coordinates': self.coordinates,
            'eta' : self.mean,
            'score': self.score,
            'centroid': self.centroid
        }

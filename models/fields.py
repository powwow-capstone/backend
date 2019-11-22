from app import db

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

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'crop': self.crop,
            'acres': self.acres,
            'coordinates': self.coordinates
        }

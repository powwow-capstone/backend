from app import db

class ETa(db.Model):
    __tablename__ = 'eta2010_2018'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    dayofyear = db.Column(db.Integer)
    objectid = db.Column(db.Integer)
    crop2014 = db.Column(db.String)
    acres = db.Column(db.Float)
    county = db.Column(db.String)
    shape_leng = db.Column(db.Float)
    shape_area = db.Column(db.Float)
    _count = db.Column(db.Float)
    _sum = db.Column(db.Float)
    _mean = db.Column(db.Float)
    _median = db.Column(db.Float)

    def __init__(self, date, dayofyear, objectid, crop2014, acres, county, shape_leng, shape_area, _count, _sum, _mean, _median):
        self.date = date
        self.dayofyear = dayofyear
        self.objectid = objectid
        self.crop2014 = crop2014
        self.acres = acres
        self.county = county
        self.shape_leng = shape_leng
        self.shape_area = shape_area
        self._count = _count
        self._sum = _sum
        self._mean = _mean
        self._median = _median

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'dayofyear': self.dayofyear,
            'objectid': self.objectid,
            'crop2014': self.crop2014,
            'acres': self.acres,
            'county': self.county,
            'shape_leng': self.shape_leng,
            'shape_area': self.shape_area,
            '_count': self._count,
            '_sum': self._sum,
            '_mean': self._mean,
            '_median': self._median
        }

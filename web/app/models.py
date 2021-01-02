from app import db


class Remote(db.Model):
    __tablename__ = 'remotes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    commands = db.relationship('Command', backref='remote', order_by="asc(Command.position)", lazy=True)

    def __init__(self, name, commands=None):
        self.name = name
        self.commands = commands if commands else []


class Command(db.Model):
    __tablename__ = 'commands'

    id = db.Column(db.Integer, primary_key=True)
    remote_id = db.Column(db.Integer, db.ForeignKey('remotes.id'), nullable=False)
    name = db.Column(db.String)
    decodeType = db.Column(db.Integer)
    value = db.Column(db.Integer)
    raw = db.Column(db.String)  # comma sepereted integer list
    rawLen = db.Column(db.Integer)
    bitLen = db.Column(db.Integer)
    position = db.Column(db.Integer)

    def __init__(self, name, decodeType, value, raw, rawLen, bitLen, position):
        self.name = name
        self.decodeType = decodeType
        self.value = value
        self.raw = raw
        self.rawLen = rawLen
        self.bitLen = bitLen
        self.position = position

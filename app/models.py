from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32), nullable=False)
    user_favourite = db.relationship('Favourite_image', backref='user')

    def __repr__(self):
        return '<User %r>' % self.userName

    def check_pwd(self, pwd):
        return self.pwd == pwd


class Favourite_image(db.Model):
    __tablename__ = 'favourite_image'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    detail_item = db.Column(db.String(255))
    detail_type = db.Column(db.String(255))

    def __repr__(self):
        return '<Favourite_image %r>' % self.user_id


if __name__ == '__main__':
    db.create_all()

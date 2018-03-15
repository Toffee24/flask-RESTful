from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)
db = SQLAlchemy(app)
CORS(app, supports_credentials=True)


# ------------------模型开始------------------
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32), nullable=False)
    user_favourite = db.relationship('Favourite_image', backref='user')

    def __repr__(self):
        return '<User %r>' % self.userName

    def check_pwd(self, password):
        return self.password == password


class Favourite_image(db.Model):
    __tablename__ = 'favourite_image'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    detail_item = db.Column(db.String(255))
    detail_type = db.Column(db.String(255))

    def __repr__(self):
        return '<Favourite_image %r>' % self.user_id


# ------------------模型结束------------------


# ------------------注册功能------------------
class register(Resource):
    def post(self):
        formdata = request.json
        username_count = User.query.filter_by(userName=formdata['userName']).count()
        if username_count > 0:
            return {'message': '相同的用户名已经存在！'}
        if len(formdata['password']) != 6:
            return {'message': '密码应为6位数字！'}
        user = User(
            userName=formdata['userName'],
            password=formdata['password']
        )

        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(userName=formdata['userName']).first()
        userId = user.id
        userName = user.userName

        return {
            'code': 200,
            'userId': userId,
            'userName': userName
        }


# ------------------登陆功能------------------
class login(Resource):
    def post(self):
        formdata = request.json
        user = User.query.filter_by(userName=formdata['userName']).first()
        if not user:
            return {
                'code': '400',
                'message': '不存在该账号！'
            }
        if not user.check_pwd(formdata['password']):
            return {
                'code': '400',
                'message': '密码错误！'
            }
        userId = user.id
        userName = user.userName
        return {
            'code': 200,
            'userId': userId,
            'userName': userName
        }


# ------------------添加收藏------------------
class addCollection(Resource):
    def post(self):
        formdata = request.json
        item = Favourite_image.query.filter_by(detail_item=formdata['imgUrl']).first()
        if not item:
            favouriteItem = Favourite_image(
                user_id=formdata['userId'],
                detail_item=formdata['imgUrl']
            )
            db.session.add(favouriteItem)
            db.session.commit()
            return {
                'code': 200,
                'message': '添加成功',
                'type': 1
            }
        if item:
            db.session.delete(item)
            db.session.commit()
            return {
                'code': 200,
                'message': '删除成功',
                'type': 2
            }


# ------------------查询收藏------------------
class searchCollection(Resource):
    def get(self):
        formdataId = request.args['userId']
        item = Favourite_image.query.filter_by(user_id=formdataId).all()
        itemArr = []
        for i in item:
            itemArr.append(i.detail_item)
        return {
            'code': '200',
            'itemArr': itemArr
        }


api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(addCollection, '/addCollection')
api.add_resource(searchCollection, '/searchCollection')

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run()

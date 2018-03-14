from flask import Flask,request
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from app.models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/some_funny?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)
db=SQLAlchemy(app)

class HelloWorld(Resource):
    def post(self):
        formdata = request.form
        user = User(
            username=formdata.username,
            password=formdata.password
        )
        db.session.add(user)
        db.session.commit()
        return '注册成功'



api.add_resource(HelloWorld, '/register')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

from flask_restx import Namespace, Resource, fields,marshal,Api
import jwt, uuid, os
from flask_cors import CORS
from functools import wraps 
from flask import abort, request, session,Blueprint
from datetime import datetime
from flask import current_app as app
#from sqlalchemy import or_, and_, distinct, func
#from project import cache  #, logging
import requests
from app.models import User
from app import db




authorizations = {
    'KEY': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'API-KEY'
    }
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'API-KEY' in request.headers:
            token = request.headers['API-KEY']
            try:
                data = jwt.decode(token,app.config.get('SECRET_KEY'),algorithms='HS256')
            except:
                return {'message': 'Token is invalid.'}, 403
        if not token:
            return {'message': 'Token is missing or not found.'}, 401
        if data:
            pass
        return f(*args, **kwargs)
    return decorated

api = Blueprint('api',__name__, template_folder='../templates')
utili=Api( app=api, doc='/docs',version='1.4',title='AMS',\
description='', authorizations=authorizations)
#implement cors

CORS(api, resources={r"/api/*": {"origins": "*"}})

user1 = utili.namespace('/api/utili', \
    description= "All routes under this section of the documentation are the open routes bots can perform CRUD action \
    on the application.", \
    path = '/v1/')

modify= user1.model('modify', {
    "id": fields.Integer(required=False,default=" ", description="Users id"),
    "nom": fields.String(required=False,default=" ", description="Users nom"),
    "prenom":fields.String(required=False,default=" ", description="Users prenom"),
    "email":fields.String(required=False,default=" ", description="Users Email"),
    "phone":fields.String(required=False,default=" ", description="Users Phone"),
    "login":fields.String(required=False,default=" ", description="Users login"),
    "role":fields.String(required=False,default=" ", description="Users role"),
   
})
user_all= user1.model('user_all', {
    "id": fields.String(required=False,default=" ", description="Users id"),
    "nom": fields.String(required=False,default=" ", description="Users nom"),
    "prenom":fields.String(required=False,default=" ", description="Users prenom"),
    "email":fields.String(required=False,default=" ", description="Users Email"),
    "phone":fields.String(required=False,default=" ", description="Users Phone"),
    "login":fields.String(required=False,default=" ", description="Users login"),
    "role":fields.String(required=False,default=" ", description="Users role"),
   
})

@user1.doc(
    security='KEY',
    params={'ID': 'Identity of User'
            },
    responses={
        200: 'ok',
        201: 'created',
        204: 'No Content',
        301: 'Resource was moved',
        304: 'Resource was not Modified',
        400: 'Bad Request to server',
        401: 'Unauthorized request from client to server',
        403: 'Forbidden request from client to server',
        404: 'Resource Not found',
        500: 'internal server error, please contact admin and report issue'
    })
@user1.route('/single/user/')
class usersingle(Resource):
    @token_required
    def get(self):
        
        if request.args:
            iD = request.args.get('ID', None)
            token = request.headers['API-KEY']
            data = jwt.decode(token, app.config.get('SECRET_KEY'),algorithms='HS256')
            logger= User.query.filter_by(id=data['id']).first()
            user = User.query.filter_by(id=int(iD)).first()
            if user and logger:
                return {
                   
                    "results": marshal(user,user_all)
                }, 200
            else:
                return {
                   
                    "results": 'user not found'
                }, 400


@user1.doc(
    security='KEY',
    params={'ID': 'Identity of User'
            },
    responses={
        200: 'ok',
        201: 'created',
        204: 'No Content',
        301: 'Resource was moved',
        304: 'Resource was not Modified',
        400: 'Bad Request to server',
        401: 'Unauthorized request from client to server',
        403: 'Forbidden request from client to server',
        404: 'Resource Not found',
        500: 'internal server error, please contact admin and report issue'
    })
@user1.route('/modify/user/')
class usermodify(Resource):
    @token_required
    @user1.expect(modify)
    def post(self):
        req_data = request.json
        
        user = User.query.filter_by(id=req_data['id']).first()
        if user:
            user.nom=req_data["nom"]
            user.prenom=req_data["prenom"]
            user.email=req_data["email"]
            user.phone=req_data["phone"]
            user.login=req_data["login"]
            user.role=req_data["role"]
            db.session.commit()
            return {
                   'res':'success',
                    "results": marshal(user,user_all)
                }, 200
        else:
            return {
                    "res":'user not found'
                }, 400
            
                


@user1.doc(
    security='KEY',
    params={
             'page': 'Number of page'
            },
    responses={
        200: 'ok',
        201: 'created',
        204: 'No Content',
        301: 'Resource was moved',
        304: 'Resource was not Modified',
        400: 'Bad Request to server',
        401: 'Unauthorized request from client to server',
        403: 'Forbidden request from client to server',
        404: 'Resource Not found',
        500: 'internal server error, please contact admin and report issue'
    })
@user1.route('/users/all')
class usera(Resource):
    @token_required
    def get(self):
        if request.args:
            page =int(request.args.get('page', 1))
            
            token = request.headers['API-KEY']
            data = jwt.decode(token, app.config.get('SECRET_KEY'),algorithms='HS256')
            user = User.query.filter_by(id=data['id']).first()
            if user:
                users_all=User.query.paginate(page=page,per_page=10)
                row=User.query.count()
                next_url= page+1 if users_all.has_next else None
                prev_url=page-1 if users_all.has_prev else None
                total = users_all.total
                return {
                    "next":next_url,
                    "prev":prev_url,
                    'totalrow':row,
                    "totalPages": total,
                    "results": marshal(users_all.items,user_all)
                }, 200
            else:
                return {
                    
                    "results":'user not found'
                }, 400

            # Still to fix the next and previous WRT Sqlalchemy


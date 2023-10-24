from flask import Blueprint, url_for
from flask_restx import Api, Resource, fields, reqparse, marshal
from flask import Blueprint, render_template, abort, request, session
from flask_cors import CORS
from functools import wraps
from flask import current_app as app
import requests
from .v1 import router,user1
from app.models import User
import jwt
from datetime import datetime, timedelta
from datetime import datetime
from app import db
# API security
authorizations = {
    'KEY': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'API-KEY'
    }
}


# The token decorator to protect my routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'API-KEY' in request.headers:
            token = request.headers['API-KEY']
            try:
                data = jwt.decode(token, app.config.get('SECRET_KEY'))
            except:
                return {'message': 'Token is invalid.'}, 403
        if not token:
            return {'message': 'Token is missing or not found.'}, 401
        if data:
            pass
        return f(*args, **kwargs)
    return decorated

class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'http' if '8055' in self.base_url else 'https'
        url=url_for(self.endpoint('specs'), _external=True)
        prefix=url.split('/swagger.json')[0]
        prefix=prefix.split('/api')[0]
        url=prefix +'/edlgateway'+'/swagger.json'
        return  url

    
api = Blueprint('api', __name__, template_folder = '../templates')
apisec = Api( app=api, doc='/docs', version='1.9.0', title='MikroticA.', \
    description='This documentation contains all routes to access the Mikrotic. \npip install googletransSome routes require authorization and can only be gotten \
    from the Microtik company', license='../LICENSE', license_url='www.sweep.com', contact='touchone0001@gmail.com', authorizations=authorizations)

CORS(api, resources={r"/api/*": {"origins": "*"}})

apisec.add_namespace(router)
apisec.add_namespace(user1)

login = apisec.namespace('/api/auth', \
    description='This contains routes for core app data access. Authorization is required for each of the calls. \
    To get this authorization, please contact out I.T Team ', \
    path='/v1/')

signup = apisec.namespace('/api/auth', \
    description='This contains routes for core app data access. Authorization is required for each of the calls. \
    To get this authorization, please contact out I.T Team ', \
    path='/v1/')

full_login =  apisec.model('full_login', {
    'login': fields.String(required=True, description="username"),
    'mdp': fields.String(required=True, description="Users Password"),

})

signupdata = apisec.model('Signup', {
    "nom": fields.String(required=False, description="Users nom"),
    "prenom":fields.String(required=False, description="Users prenom"),
    "email":fields.String(required=False, description="Users Email"),
    "login": fields.String(required=True, description="Users login"),
    "mdp": fields.String(required=True, description="Users mdp"),
    "phone": fields.String(required=False, description="Users phone"),
    "role": fields.String(required=False, description="Users role"),
})

@login.doc(
    params={},

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
@login.route('/auth/login')
class Login(Resource):
    @login.expect(full_login)
    def post(self):
        app.logger.info('User login with user_name')
        req_data = request.get_json()
        username=req_data['login']
        password=req_data['mdp']
        if username and password:
            user=User.query.filter_by(login=username).first()
            if user:
                if user.check_password(password):
                    token = jwt.encode({
                        'id': user.id,
                        'user': user.nom,
                        'exp': datetime.utcnow() + timedelta(days=30),
                        'iat': datetime.utcnow()
                    },
                        app.config.get('SECRET_KEY'),
                        algorithm='HS256')
                    data={
                        'id':user.id,
                        'nom':user.nom,
                        'email':user.email,
                        'prenom':user.prenom,
                        'role':user.role,
                        'phone':user.phone,
                        'login':user.login,
                        
                    }
                    return {
                        'status': 1,
                        'res': 'success',
                        'token': str(token),
                        'data':data
                    }, 200

                else:
                    return {
                        'status': 0,
                        'res':'Wrong password'
                        
                    }, 400
            else:
                    return {
                        'status': 0,
                        'res':'Wrong User'
                        
                    }, 400

@signup.doc(
    security='KEY',
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
@signup.route('/auth/signup')
class Signup(Resource):
    #@token_required
    @signup.expect(signupdata)
    def post(self):
        req_data = request.get_json()
        nom=req_data['nom'] or None
        prenom=req_data['prenom'] or None
        email=req_data['email'] or None
        role=req_data['role'] or None
        login=req_data['login'] 
        password=req_data['mdp']
        phone=req_data['phone']
        if login and password:
            user=User(nom=nom,email=email,login=login,prenom=prenom,role=role,phone=phone)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            data={
                'id':user.id,
                'nom':user.nom,
                'email':user.email,
                'prenom':user.prenom,
                'role':user.role,
                'phone':user.phone,
                'login':user.login,
            }
            return {
                'status': 1,
                'res': 'success',
                'data':data
            }, 200

        else:
            return {
                        'status': 0,
                        'res':'Email and password must be there' 
                    }, 400

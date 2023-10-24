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
from app.models import Router,User
from app import db
import paramiko



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
router=Api( app=api, doc='/docs',version='1.4',title='AMS',\
description='', authorizations=authorizations)
#implement cors

CORS(api, resources={r"/api/*": {"origins": "*"}})

router  = router.namespace('/api/router', \
    description= "All routes under this section of the documentation are the open routes bots can perform CRUD action \
    on the application.", \
    path = '/v1/')

create= router.model('create', {
    "nom": fields.String(required=False,default=" ", description="nom"),
    "fabriquant":fields.String(required=False,default=" ", description="Users prenom"),
    "sous_reseau":fields.String(required=False,default=" ", description="Users Email"),
    "mac":fields.String(required=False,default=" ", description="Users Phone"),
    "ip":fields.String(required=False,default=" ", description="Users Phone"),
    'login':fields.String(required=False,default=" ", description="Users Phone"),
    'mdp':fields.String(required=False,default=" ", description="Users Phone"),
   
})
command= router.model('command', {
    "id":fields.Integer(required=False,default=" ", description="id router"),
    'command':fields.String(required=False,default=" ", description="command"),
})
modify= router.model('modify', {
    "nom": fields.String(required=False,default=" ", description="nom"),
    "fabriquant":fields.String(required=False,default=" ", description="Users prenom"),
    "sous_reseau":fields.String(required=False,default=" ", description="Users Email"),
    "mac":fields.String(required=False,default=" ", description="Users Phone"),
    "ip":fields.String(required=False,default=" ", description="ip address"),
    "id":fields.Integer(required=False,default=" ", description="Users id"),
    'login':fields.String(required=False,default=" ", description="User"),
    'mdp':fields.String(required=False,default=" ", description="Users mdp"),
    'update':fields.String(required=False,default=" ", description="Users mdp"),
   
})

@router.doc(
    security='KEY',
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
@router.route('/router/command')
class routercommand(Resource):
    @token_required
    @router.expect(command)
    def post(self):
        req_data = request.json
        token = request.headers['API-KEY']
        data = jwt.decode(token, app.config.get('SECRET_KEY'),algorithms='HS256')
        user = User.query.filter_by(id=data['id']).first()
        if user:
            check=Router.query.filter_by(id=req_data["id"]).first()
            if check:
                try:
                    if req_data["command"] == '1':
                        command='/system package update check-for-updates'
                    if req_data["command"] == '2':
                        command='/system package update install'
                    if req_data["command"] == '3':
                        command='/system routerboard print'
                    if req_data["command"] == '4':
                        command='/system routerboard upgrade'
                    
                    default=datetime.now()
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=check.ip, username=check.login, password=check.mdp)

                    stdin,stdout,stderr=ssh.exec_command(command)
                    response=stdout.readlines()
                    check.update=default
                    db.session.commit()
                except:
                    return {
                        "results":"echec de update"
                    }, 400
                return {
                    "results": response,
                    "res":'success'
                    }, 200
            else:
                return {
                        "results":"router n'existe pas"
                    }, 400
                

@router.doc(
    security='KEY',
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
@router.route('/router/add')
class routeradd(Resource):
    @token_required
    @router.expect(create)
    def post(self):
        req_data = request.json
        token = request.headers['API-KEY']
        data = jwt.decode(token, app.config.get('SECRET_KEY'),algorithms='HS256')
        user = User.query.filter_by(id=data['id']).first()
        if user:
            check=Router.query.filter_by(mac=req_data[ "mac"]).first()
            if check is None:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=req_data[ "ip"], username=req_data['login'], password=req_data['mdp'])
                except:
                    return {
                    "results":"Mauvais login ou l'addresse n'existe pas"
                    }, 400
                route=Router()
                route.nom=req_data["nom"]
                route.fabriquant=req_data["fabriquant"]
                route.sous_reseau=req_data[ "sous_reseau"]
                route.mac=req_data[ "mac"]
                route.ip=req_data[ "ip"]
                route.login=req_data['login']
                route.mdp=req_data['mdp']
                db.session.add(route)
                db.session.commit()
                return {
                    "results": marshal(route,modify)
                    }, 200
            else:
                return {
                    
                    "results":'mac address was taken'
                }, 400
        else:
            return {
                    
                    "results":'user not found'
                }, 400



@router.doc(
    security='KEY',
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
@router.route('/router/modify')
class routermodify(Resource):
    @token_required
    @router.expect(modify)
    def post(self):
        req_data = request.json
        token = request.headers['API-KEY']
        data = jwt.decode(token, app.config.get('SECRET_KEY'),algorithms='HS256')
        user = User.query.filter_by(id=data['id']).first()
        if user:
            route=Router.query.filter_by(id=int(req_data['id'])).first()
            if route:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=req_data[ "ip"], username=req_data['login'], password=req_data['mdp'])
                except:
                    return {
                    "results":"Mauvais login ou l'addresse n'existe pas"
                    }, 400
                
                route.nom=req_data["nom"]
                route.fabriquant=req_data["fabriquant"]
                route.sous_reseau=req_data[ "sous_reseau"]
                route.mac=req_data[ "mac"]
                route.ip=req_data[ "ip"]
                route.login=req_data['login']
                route.mdp=req_data['mdp']
                return {
                    "results": marshal(route,modify)
                    }, 200
            else:
                return {
                    
                    "results":'route not found'
                }, 400
        else:
            return {
                    
                    "results":'user not found'
                }, 400
@router.doc(
    security='KEY',
    params={'ID': 'Identity of Router'
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
@router.route('/single/router/')
class routersingle(Resource):
    def get(self):
        
        if request.args:
            iD = request.args.get('ID', None)
            token = request.headers['API-KEY']
            data = jwt.decode(token, app.config.get('SECRET_KEY'),algorithms='HS256')
            user = User.query.filter_by(id=data['id']).first()
            if user:
                route=Router.query.filter_by(id=int(iD)).first()
                if route:
                    return {
                    "results": marshal(route,modify)
                    }, 200
                return {
                    
                    "results":'route not found'
                }, 400
            return {
                    
                    "results":'user not found'
                }, 400

@router.doc(
    security='KEY',
    params={'page': 'Page Number',
            
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
@router.route('/router/all')
class routera(Resource):
    def get(self):
        if request.args:
            page =int(request.args.get('page', 1))
            
            token = request.headers['API-KEY']
            data = jwt.decode(token, app.config.get('SECRET_KEY'),algorithms='HS256')
            user = User.query.filter_by(id=data['id']).first()
            if user:
                router_all=Router.query.paginate(page=page,per_page=10)
                row=Router.query.count()
                next_url= page+1 if router_all.has_next else None
                prev_url=page-1 if router_all.has_prev else None
               #done
                total = router_all.total
                return {
                    "next":next_url,
                    "prev":prev_url,
                    "totalrow":row,
                    "totalPages": total,
                    "results": marshal(router_all.items,modify)
                }, 200
            else:
                return {
                    
                    "results":'user not found'
                }, 400

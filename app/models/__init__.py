from datetime import datetime
import json
from time import time
from flask import current_app

import jwt
from app import db
from werkzeug.security import generate_password_hash,check_password_hash









class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.String(128),index=True,unique=True)
    prenom=db.Column(db.String(128))
    login=db.Column(db.String(128))
    phone=db.Column(db.String(128))
    role=db.Column(db.String(128))
    email=db.Column(db.String(128),index=True,unique=True)
    password_hash=db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.nom
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    

class Router(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.String(128))
    frabiquant=db.Column(db.String(128))
    sous_reseau=db.Column(db.String(128))
    mac=db.Column(db.String(128))
    ip=db.Column(db.String(128))
    login=db.Column(db.String(128))
    mdp=db.Column(db.String(128))
    update=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    


    def __repr__(self):
        return '<Router %r>' % self.nom

import json
from flask import Blueprint, request

from flaskr.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/heroes', methods = ['GET'])
def get_heroes():
    db = get_db()
    
    name = request.args.get("name")
    if name is None:
        heroes = db.execute("SELECT * FROM hero").fetchall()
    else:
        heroes = db.execute("SELECT * FROM hero WHERE name LIKE '%%%s%%'" % name).fetchall()
   
    return json.dumps([dict(ix) for ix in heroes])


@bp.route('/heroes/<id>', methods = ['GET'])
def get_hero(id):
    db = get_db()
    
    hero = db.execute("SELECT * FROM hero WHERE id=%s" % id).fetchone()
    
    return json.dumps(dict(hero))


@bp.route('/heroes', methods = ['POST'])
def new_hero():
    db = get_db()
    
    hero = request.json
    cursor = db.execute("INSERT INTO hero (name) VALUES ('%s')" % hero['name'])
    db.commit()

    hero["id"] = cursor.lastrowid 
    
    return json.dumps(hero)


@bp.route('/heroes', methods = ['PUT'])
def save_hero():
    db = get_db()
    
    hero = request.json
    db.execute("UPDATE hero SET name='%s' WHERE id=%s" % (hero['name'], hero['id']))
    db.commit()
    
    return json.dumps(hero)


@bp.route('/heroes/<id>', methods = ['DELETE'])
def delete_hero(id):
    db = get_db()
    
    db.execute("DELETE FROM hero WHERE id=%s" % (id))
    db.commit()
    
    return json.dumps([])

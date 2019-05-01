from flask import jsonify, request, redirect
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_claims
import string
from string import ascii_lowercase, ascii_uppercase
from math import floor
from app import app, db, bcrypt, jwt
from app.models import User, Url


host = app.config['HOST']


#
# Join the service
#
@app.route('/api/join', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'err': 2, 'msg': 'Missing JSON in request'})
    username = request.json.get('username')
    password = request.json.get('password')
    if not username:
        return jsonify({'err': 2, "msg": "Missing username"}), 400
    if not password:
        return jsonify({'err': 2, "msg": "Missing password"}), 400
    user = User(
        password=password,
        username=username
    )
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': 'true', 'msg': 'User has been successfully registered'}), 201
    except:
        db.session.rollback()
        return jsonify({'err': 1, 'msg': 'User can not be registered'}), 500


#
# Authorization
#
@app.route('/api/auth', methods=['POST'])
def auth():
    if not request.is_json:
        return jsonify({'err': 2, 'msg': 'Missing JSON in request'}), 400
    username = request.json.get('username')
    password = request.json.get('password')
    if not username:
        return jsonify({'err': 2, 'msg': 'Missing username'}), 400
    if not password:
        return jsonify({'err': 2, 'msg': 'Missing password'}), 400
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({'err': 3, 'msg': 'Wrong username or password'}), 400


#
# Creates new short link
#
@jwt_required
@app.route('/api/short', methods=['POST'])
def get_short():
    if not request.is_json:
        return jsonify({'err': 2, 'msg': 'Missing JSON in request'}), 400
    claims = get_jwt_claims()
    long_url = request.json.get('url', None)
    if not long_url:
        return jsonify({'err': 2, 'msg': 'Missing url in request'}), 400
    url = Url(
        user_id=claims['user_id'],
        url=long_url
    )
    try:
        db.session.add(url)
        db.session.flush()
        short_url = encode(url.id)
        db.session.commit()
        return jsonify({'short': host + short_url, 'long': long_url, 'url_end': short_url}), 201
    except:
        db.session.rollback()
        return jsonify({'err': 1, 'msg': 'Unable to create short link'}), 500



#
# Deletes the the specified short link
#
@jwt_required
@app.route('/api/delete', methods=['POST'])
def delete():
    if not request.is_json:
        return jsonify({'err': 2, 'msg': 'Missing JSON in request'}), 400
    end = request.json.get('url_end', None)
    if not end:
        return jsonify({'err': 2, 'msg': 'Missing url_end in request'}), 400
    id = decode(end)
    deleted = Url.query.filter_by(id=id).delete()
    if deleted:
        db.session.commit()
        return jsonify({'success': 'true', 'msg': 'Link has been successfully deleted'}), 200
    else:
        db.session.rollback()
        return jsonify({'err': 1, 'msg': "Can't delete link"}), 500


#
# Returns information about the specified short link
#
@jwt_required
@app.route('/api/info', methods=['POST'])
def get_info():
    if not request.is_json:
        return jsonify({'err': 2, 'msg': 'Missing JSON in request'}), 400
    end = request.json.get('url_end', None)
    if not end:
        return jsonify({'err': 2, 'msg': 'Missing url_end in request'}), 400
    id = decode(end)
    url_info = Url.query.filter_by(id=id).first()
    if url_info:
        return jsonify({
            'short': host + encode(url_info.id),
            'views': url_info.views,
            'created_at': url_info.created_at,
            'long': url_info.url
        }), 200
    else:
        return jsonify({'err': 4, 'msg': "Link doesn't exist"}), 500


#
# Returns all links belongs to the user
#
@jwt_required
@app.route('/api/all', methods=['POST'])
def get_all():
    claims = get_jwt_claims()
    if not request.is_json:
        return jsonify({'err': 2, 'msg': 'Missing JSON in request'}), 400
    since = request.json.get('since')
    per_page = request.json.get('per_page')
    page = request.json.get('page')
    if not page:
        return jsonify({'err': 2, 'msg': 'Missing page in request'}), 400
    elif not per_page:
        return jsonify({'err': 2, 'msg': 'Missing per_page in request'}), 400
    date_since = since if(since) else ''
    offset = (page-1)*per_page
    user_id = claims['user_id']
    urls = Url.query.filter(Url.created_at >= date_since, user_id == user_id).limit(per_page).offset(offset)
    links = [{
        'short': host + encode(record.id),
        'long': record.url,
        'views': record.views,
        'created_at': record.created_at
    } for record in urls]
    if urls:
        return jsonify({'data': links}), 200
    else:
        return jsonify({'err': 5, 'msg': 'Links not found'}), 404


#
# Redirect
#
@app.route('/<short_url>')
def redirection(short_url):
    if not short_url:
        return jsonify({'err': 2, 'msg': 'Missing short url in request'}), 400
    decoded = decode(short_url)
    url = Url.query.filter_by(id=decoded).first()
    if not url:
        return jsonify({'err': 4, 'msg': "Link doesn't exist"}), 404
    try:
        redirect_url = url.url
        url.views += 1  # Clicks counter
        db.session.commit()
        return redirect(redirect_url)
    except:
        db.session.rollback()
        return jsonify({'err': 1, 'msg': "Cant't redirect"}), 500


#
# From Base10 to Base62
#
def encode(num):
    b = 62
    base = string.digits + ascii_lowercase + ascii_uppercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res


#
# From Base62 to Base10
#
def decode(num):
    b = 62
    base = string.digits + ascii_lowercase + ascii_uppercase
    limit = len(num)
    res = 0
    for i in range(limit):
        res = b * res + base.find(num[i])
    return res


#
# Put user_id into token claims
#
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {'user_id': identity}

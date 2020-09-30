import pymysql
from flask import Flask
from flask_cors import CORS, cross_origin
from db_config import mysql
from flask import jsonify
from flask_restful import reqparse

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/guardList')
@cross_origin(supports_credentials=True)
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM guards_info")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getGuardData', methods=["POST"])
@cross_origin(supports_credentials=True)
def guarddata():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id to get user')
        args = parser.parse_args()
        _userId = args['id']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM guards_info WHERE id=%s", _userId)
        rows = cursor.fetchone()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

@app.route('/getCompanyGuards', methods=["POST"])
@cross_origin(supports_credentials=True)
def companyGuards():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id to get user')
        args = parser.parse_args()
        _userId = args['id']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT m.*, m.id as map_id,g.*, g.id as g_id FROM `mapping_table` as m inner join guards_info as g on m.guard_id=g.id where m.company_id=%s", _userId)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/guard_registration', methods=['POST'])
@cross_origin(supports_credentials=True)
def regst1():
    try:
        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='Email address to create user')
        parser.add_argument('pass1', type=str, help='Password to create user')
        parser.add_argument('fname', type=str, help='first name to create user')
        parser.add_argument('lname', type=str, help='Last name to create user')
        parser.add_argument('phone', type=str, help='phone to create user')
        parser.add_argument('dob', type=str, help='dob to create user')
        parser.add_argument('gender', type=str, help='gender to create user')

        args = parser.parse_args()

        _userEmail = args['email']
        _userPassword = args['pass1']
        _userFname = args['fname']
        _userLname = args['lname']
        _userPhone = args['phone']
        _userDob = args['dob']
        _userGender = args['gender']

        sql = "INSERT INTO guards_info(first_name,last_name,email,phone,dob,gender,password)VALUES(%s,%s,%s,%s,%s,%s,%s)"
        val = (_userFname, _userLname, _userEmail, _userPhone, _userDob, _userGender, _userPassword)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()

        return {'Email': _userEmail, 'Password': _userPassword}

    except Exception as e:
        return {'error': str(e)}


@app.route('/UpdateData', methods=['POST'])
@cross_origin(supports_credentials=True)
def regst2():
    try:
        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='Email address to create user')
        parser.add_argument('email', type=str, help='Email address to create user')
        parser.add_argument('pass1', type=str, help='Password to create user')
        parser.add_argument('fname', type=str, help='first name to create user')
        parser.add_argument('lname', type=str, help='Last name to create user')
        parser.add_argument('phone', type=str, help='phone to create user')
        parser.add_argument('dob', type=str, help='dob to create user')
        parser.add_argument('gender', type=str, help='gender to create user')

        args = parser.parse_args()

        _userId = args['id']
        _userEmail = args['email']
        _userPassword = args['pass1']
        _userFname = args['fname']
        _userLname = args['lname']
        _userPhone = args['phone']
        _userDob = args['dob']
        _userGender = args['gender']

        sql = "UPDATE guards_info SET first_name=%s,last_name=%s,email=%s,phone=%s,dob=%s,gender=%s,password=%s WHERE id=%s"
        val = (_userFname, _userLname, _userEmail, _userPhone, _userDob, _userGender, _userPassword, _userId)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()

        return {'Email': _userEmail, 'Password': _userPassword}

    except Exception as e:
        return {'error': str(e)}


@app.route('/user_login', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('uname', type=str, help='id to get user')
        parser.add_argument('pass', type=str, help='id to get user')
        args = parser.parse_args()
        _uname = args['uname']
        _pass = args['pass']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if _uname == '' and  _pass == '' :
            resp = jsonify("false")
            resp.status_code = 200
            return resp
        sql = 'SELECT * FROM user WHERE username=%s and password=%s'
        val = (_uname, _pass)
        cursor.execute(sql, val)
        print(sql)
        rc=cursor.rowcount
        print(rc)
        if rc>0:
            resp = jsonify("true")
            resp.status_code = 200
            return resp
        else:
            resp = jsonify("false")
            resp.status_code = 200
            return resp
    except Exception as e:
        return {'error': str(e)}

@app.route('/com_registration', methods=["POST"])
@cross_origin(supports_credentials=True)
def comp():
    try:
        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='Email address to create user')
        parser.add_argument('pass1', type=str, help='Password to create user')
        parser.add_argument('cname', type=str, help='first name to create user')
        parser.add_argument('owner', type=str, help='Last name to create user')
        parser.add_argument('phone', type=str, help='phone to create user')
        parser.add_argument('address', type=str, help='dob to create user')
        parser.add_argument('service', type=str, help='gender to create user')

        args = parser.parse_args()

        _comEmail = args['email']
        _comPassword = args['pass1']
        _comCname = args['cname']
        _comOwner = args['owner']
        _comPhone = args['phone']
        _comAdd = args['address']
        _comService = args['service']

        sql = "INSERT INTO company_info(company,owner,email,phone,address,service,password)VALUES(%s,%s,%s,%s,%s,%s,%s)"
        val = (_comCname, _comOwner, _comEmail, _comPhone, _comAdd, _comService, _comPassword)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()

        return {'Email': _comEmail}
    except Exception as e:
        return {'error': str(e)}

    finally:
        cursor.close()
        conn.close()

@app.route('/addMapping', methods=['POST'])
@cross_origin(supports_credentials=True)
def addmapping():
    try:
        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('guard_id', type=str, help='Email address to create user')
        parser.add_argument('company_id', type=str, help='Password to create user')

        args = parser.parse_args()

        _userGuardId = args['guard_id']
        _userCompanyId = args['company_id']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM mapping_table WHERE guard_id=%s ",_userGuardId )
        rows = cursor.fetchone()
        total=rows[0]
        status = 0
        if total==0 :
            sql = "INSERT INTO mapping_table(guard_id,company_id)VALUES(%s,%s)"
            val = (_userGuardId, _userCompanyId)
            cursor.execute(sql, val)
            conn.commit()
            status = 1

        return {'status': status}

    except Exception as e:
        return {'error': str(e)}


@app.route('/comList')
@cross_origin(supports_credentials=True)
def coml():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT company,id FROM company_info")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/deleteMapping', methods=['POST'] )
@cross_origin(supports_credentials=True)
def deletemapping():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='Email address to create user')

        args = parser.parse_args()

        _id = args['id']

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("delete from mapping_table where id=%s",_id)
        conn.commit()

        return {'status': 'true'}
    except Exception as e:
        return {'error': str(e)}
    finally:
        cursor.close()
        conn.close()

"""@app.route('/GetComid', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('cname', type=str, help='id to get user')
        args = parser.parse_args()
        _cname = args['cname']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT id FROM company_info WHERE company=%s'
        val = (_cname)
        cursor.execute(sql, val)
        rows = cursor.fetchone()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

    except Exception as e:
        return {'error': str(e)}"""

if __name__ == '__main__':
    app.run()

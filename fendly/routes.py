import os
from flask import jsonify, request
import cloudinary
import cloudinary.uploader as cloud
from fendly import app
from fendly.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
)

load_dotenv()


from fendly.services import convertToBinaryData, convertToImage

# jwt setup
jwt = JWTManager(app)


@app.route("/api/v1/auth/login", methods=["POST", "GET"])
@cross_origin(supports_credentials=True)
def login():
    try:
        if request.method == "POST":

            data = request.json
            conn = get_db()
            curr = conn.cursor()
            curr.execute('SELECT * FROM "user" WHERE email = %s', (data.get("email"),))
            user = curr.fetchone()
            user = dict(user)
            print(user)
            if user is None:
                return "Invalid credentials", 401
            if user:
                res = check_password_hash(user['password'], data["password"])
                if res:
                    access_token = create_access_token(
                        identity={
                            "email": user['email'],
                            "ID": user['userid'],
                        }
                    )
                    response = {
                        "access_token": access_token,
                        "user_id": user['userid'],
                    }
                    return response, 200
                else:
                    return "Invalid credentials", 401
    except ConnectionError:
        return "Failed to login!", 401
    finally:
        conn.close()


@app.route("/api/v1/auth/logout", methods=["POST", "GET"])
@cross_origin(supports_credentials=True)
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200


@app.route("/api/v1/auth/registration", methods=["POST", "GET"])
@cross_origin(supports_credentials=True)
def registration():
    try:
        if request.method == "POST":
            data = request.json
            conn = get_db()
            curr = conn.cursor()
            curr.execute(
                'INSERT INTO "user" (first_name,last_name,username,email,password) VALUES(%s,%s,%s,%s,%s)',
                [
                    data["first_name"],
                    data["last_name"],
                    data["username"],
                    data["email"],
                    generate_password_hash(data["password"]),
                ],
            )
        conn.commit()
        return "registered successfully", 200
    except ConnectionError:
        conn.rollback()
        return "failed to register user", 501
    finally:
        conn.close()


@app.route("/api/v1/get-user/<int:user_id>", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def get_user_by_id(user_id):
    try:
        conn = get_db()
        curr=conn.cursor()
        curr.execute(
        'SELECT user_details.profile_pic,user_details.job_title,user_details.company,user_details.linkedIn_username,user_details.twitter_username,user_details.github_username,user_details.website, first_name,last_name,username,email FROM "user_details" LEFT JOIN "user"  USING(userID) WHERE user_details.userID = %s',
        (user_id,),
        )
        data = curr.fetchone()
        if data:
            return dict(data),200
        else:
            curr.execute('SELECT first_name, last_name,username,email FROM "user" where userID = %s',(user_id,))
            data = curr.fetchone()
            return dict(data),200
    except:
        return 'could not load user',500
    finally:
        conn.close()


@app.route("/api/v1/delete-account/<int:user_id>", methods=["POST", "GET"])
@cross_origin(supports_credentials=True)
@jwt_required()
def delete_account(user_id):

    try:
        current_user = get_jwt_identity()
        user = current_user.get("ID")
        conn = get_db()
        curr = conn.cursor()
        if user == int(user_id):
            curr.execute('DELETE FROM "user" WHERE userID=%s', (user_id,))
            curr.execute(
                'DELETE FROM "user_details" WHERE userID=%s', (user_id,)
            )
            conn.commit()
            return "User successfully deleted!", 200
    except ConnectionError:
        return "unable to delete user", 500
    finally:
        conn.close()


@app.route("/api/v1/update-user", methods=["POST", "GET"])
@cross_origin(supports_credentials=True)
@jwt_required()
def update_user():
    try:
        if request.method == "POST":
            # cloudinary - get image from request and save it to cloudinary
            # get public url from cloudinary response and save to db
            file = request.files.get("profile_pic")
            cloudinary.config(
                cloud_name=os.getenv("CLOUD_NAME"),
                api_key=os.getenv("API_KEY"),
                api_secret=os.getenv("API_SECRET"),
            )

            # get json data from request and open db connection
            data = dict(request.form)
            conn = get_db()
            curr = conn.cursor()
            # get user identity
            current_user = get_jwt_identity()
            user_id = current_user.get("ID")
            # save data to db
            curr.execute('SELECT userID FROM "user" WHERE userID = %s', (user_id,))
            user = curr.fetchone()
            curr.execute(
                'SELECT * FROM "user_details" WHERE userID = %s',
                (user_id,),
            )
            user_details = curr.fetchone()

            if (user is not None) and (user_details is None):
                if file:
                    upload_result = cloud.upload(file)
                    image = upload_result.get("secure_url")
                else:
                    image = "https://img.icons8.com/ios-filled/344/who.png"
                curr.execute(
                    'INSERT INTO "user_details" (userID,profile_pic,job_title,company,linkedIn_username,twitter_username,github_username,website) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                    [
                        dict(user)['userid'],
                        image,
                        data.get("job_title"),
                        data.get("company"),
                        data.get("linkedIn"),
                        data.get("twitter"),
                        data.get("github"),
                        data.get("website"),
                    ],
                )
                conn.commit()
                return "user details successfully added", 200
            elif (user is not None) and (user_details is not None):
                if file:
                    upload_result = cloud.upload(file)
                    image = upload_result.get("secure_url")
                else:
                    image = dict(user_details)['profile_pic']
                curr.execute(
                    'UPDATE "user_details" SET profile_pic=%s,job_title=%s,company=%s,linkedIn_username=%s,twitter_username=%s,github_username=%s,website=%s WHERE user_details.userID=%s',
                    (
                        image,
                        data.get("job_title"),
                        data.get("company"),
                        data.get("linkedIn"),
                        data.get("twitter"),
                        data.get("github"),
                        data.get("website"),
                        int(data.get("user_id")),
                    ),
                )
                curr.execute(
                    'UPDATE "user" SET first_name=%s,last_name=%s,username=%s,email=%s WHERE userID=%s',
                    (
                        data.get("first_name"),
                        data.get("last_name"),
                        data.get("username"),
                        data.get("email"),
                        int(data.get("user_id")),
                    ),
                )
                conn.commit()
                return "user details successfully updated", 200

            else:
                return "user does not exist", 400
    except ConnectionError:
        conn.rollback()
        return "user update failed", 400
    finally:
        conn.close()

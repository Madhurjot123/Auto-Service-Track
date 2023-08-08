from flask import Flask, render_template, request
from mongoproject3 import MongoDBHelper
import datetime
import hashlib


web_app = Flask('Auto Service Track')


@web_app.route("/")
def index():
    return render_template("index1.html")


@web_app.route("/register")
def register():
    return render_template("register1.html")


@web_app.route("/register-customer", methods=['POST'])
def register_customer():
    customer_data = {
        'name': request.form['name'],
        'shop name': request.form['Shop Name'],
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
        'createdon': datetime.datetime.today()
    }
    print(customer_data)

    db = MongoDBHelper(collection="car customers")
    db.insert(customer_data)

    return render_template('home1.html')


@web_app.route("/login-customer", methods=['POST'])
def login_customer():
    customer_data = {
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
    }
    print(customer_data)

    db = MongoDBHelper(collection="car customers")
    documents = list(db.fetch(customer_data))
    if len(documents) == 1:
        return render_template('home1.html')
    else:
        return render_template('error1.html')





def main():
    web_app.run(port=5001)


if __name__ == "__main__":
    main()

from flask import Flask, render_template, request, session, redirect
from mongoproject3 import MongoDBHelper
import datetime
import hashlib
web_app = Flask('Auto Service Track')
from bson.objectid import ObjectId


@web_app.route("/")
def index():
    return render_template("index1.html")


@web_app.route("/register")
def register():
    return render_template("register1.html")


@web_app.route("/home-Auto Service Track")
def home():
    return render_template("home1.html")


@web_app.route("/register-serviceStation", methods=['POST'])
def register_service_station():
    station_data = {
        'name': request.form['name'],
        'service_station': request.form['service_station'],
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
        'createdOn': datetime.datetime.today()
    }
    print(station_data)

    db = MongoDBHelper(collection="service stations")
    db.insert(station_data)

    return render_template('home1.html')


@web_app.route("/login-serviceStation", methods=['POST'])
def login_service_station():
    service_station_data = {
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
    }
    print(service_station_data)

    db = MongoDBHelper(collection="service stations")
    documents = list(db.fetch(service_station_data))
    if len(documents) == 1:
        session['id'] = str(documents[0]['_id'])
        session['email'] = documents[0]['email']
        session['service_station_id'] = str(documents[0]['_id'])
        session['name'] = documents[0]['name']
        session['service_station_name'] = documents[0]['service_station']  # Set the service_station_name in session
        print(vars(session))
        return render_template('home1.html')
    else:
        return render_template('error1.html')


@web_app.route("/add-customer-service-station", methods=['POST'])
def add_customer_service_station():
    service_station_customer_data = {
        'name': request.form['name'],
        'phone_number': request.form['phone_number'],
        'email': request.form['email'],
        'gender': request.form['gender'],
        'address': request.form['address'],
        'service_station_email': request.form['service_station_email'],
        'service_station_id': request.form['service_station_id'],
        'createdOn': datetime.datetime.today()
    }
    if len(service_station_customer_data['name']) == 0 or len(service_station_customer_data['phone_number']) == 0 or len(
            service_station_customer_data['email']) == 0:
        return render_template('error.html', message="Name, Phone and Email cannot be Empty")
    print(service_station_customer_data)

    db = MongoDBHelper(collection="service station customers")
    db.insert(service_station_customer_data)

    return render_template('success1.html',
                           message="{} added successfully".format(service_station_customer_data['name']))


@web_app.route("/update-customer-service-station", methods=['POST'])
def update_customer_service_station():
    customer_data_to_update = {
        'name': request.form['name'],
        'phone_number': request.form['phone_number'],
        'email': request.form['email'],
        'gender': request.form['gender'],
        'address': request.form['address'],
    }
    if len(customer_data_to_update['name']) == 0 or len(customer_data_to_update['phone_number']) == 0 or len(
            customer_data_to_update['email']) == 0:
        return render_template('error.html', message="Name, Phone and Email cannot be Empty")
    print(customer_data_to_update)
    db = MongoDBHelper(collection="service station customers")
    query = {'email': request.form['email']}
    db.update(customer_data_to_update, query)

    return render_template('success1.html',
                           message="{} updated successfully".format(customer_data_to_update['name']))


@web_app.route("/logout")
def logout():
    session['vet_id'] = ""
    session['email'] = ""
    return redirect("/")


@web_app.route("/fetch-Customers-of-Service-Station")
def fetch_customers_of_service_station():
    db = MongoDBHelper(collection="service station customers")
    query = {'service_station_id': session['service_station_id']}
    documents = db.fetch(query)
    print(documents, type(documents))
    return render_template('customer1.html', documents=documents)


@web_app.route("/delete-customer/<id>")
def delete_customer(id):
    db = MongoDBHelper(collection="service station customers")
    query = {'_id': ObjectId(id)}
    customer = db.fetch(query)[0]
    db.delete(query)
    return render_template("success1.html", message="customer with ID {} and name {} Deleted...".format(id, customer['name']))


@web_app.route("/update-customer/<id>")
def update_customer(id):
    db = MongoDBHelper(collection="service station customers")
    query = {'_id': ObjectId(id)}
    customer = db.fetch(query)[0]
    return render_template("update-customer1.html", customer=customer)



def main():
    web_app.secret_key = 'your_secret_key'
    web_app.run(port=5001)


if __name__ == "__main__":
    main()

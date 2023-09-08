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

    session['service_station_id'] = str(station_data['_id'])  # Corrected the session variable
    session['service_station_name'] = station_data['name']
    session['service_station_email'] = station_data['email']

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
        session['service_station_name'] = documents[0]['service_station']
        session['service_station_email'] = documents[0]['email']
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
        return render_template('error1.html', message="Name, Phone and Email cannot be Empty")
    print(customer_data_to_update)

    db = MongoDBHelper(collection="service station customers")
    query = {'email': request.form['email']}

    print(customer_data_to_update)
    print(query)
    db.update(customer_data_to_update, query)

    return render_template('success1.html',
                           message="{} updated successfully".format(customer_data_to_update['name']))


@web_app.route("/logout")
def logout():
    session['_id'] = ""
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


@web_app.route("/search")
def search():
    return render_template("search1.html")


@web_app.route("/search-customer", methods=["POST"])
def search_customer():
    db = MongoDBHelper(collection="service station customers")
    query = {'email': request.form['email']}
    customers_cursor = db.fetch(query)
    customers = list(customers_cursor)

    if len(customers) == 1:
        customer = customers[0]
        return render_template("customer-profile1.html", customer=customer)
    else:
        return render_template("error1.html", message="customer not found..")

@web_app.route("/add-car/<id>")
def add_car(id):
    db = MongoDBHelper(collection="service station customers")
    query = {'_id': ObjectId(id)}
    customers = db.fetch(query)
    customer = customers[0]
    return render_template("add-car1.html",
                           _id=session['service_station_id'],
                           email=session['service_station_email'],
                           name=session['service_station_name'],
                           customer=customer)





@web_app.route("/save-car", methods=["POST"])
def save_car():
    car_data = {
        'car_name': request.form['car_name'],
        'car_number': request.form['car_number'],
        'car_colour': request.form['car_colour'],
        'car_model': request.form['car_model'],
        'kms_driven': request.form['kms_driven'],
        'service_due': request.form['service_due'],
        'cid': request.form['cid'],
        'customer_email': request.form['customer_email'],
        'service_station_id': session['service_station_id'],
        'createdOn': datetime.datetime.today()
    }

    if len(car_data['car_name']) == 0 or len(car_data['car_number']) == 0:
        return render_template('error1.html', message="Name and colour cannot be Empty")

    print(car_data)
    db = MongoDBHelper(collection="service station cars")
    db.insert(car_data)

    return render_template('success1.html', message="{} added for customer {} successfully.."
                           .format(car_data['car_name'], car_data['customer_email']))

@web_app.route("/fetch-all-cars")
def fetch_all_cars():
    db = MongoDBHelper(collection="service station cars")
    query = {'service_station_id': session['service_station_id']}
    documents = db.fetch(query)
    print(documents, type(documents))
    return render_template('cars1.html',
                           email=session['service_station_email'],
                           name=session['service_station_name'],
                           documents=documents)


@web_app.route("/fetch-cars/<email>")
def fetch_cars_of_customer(email):
    db = MongoDBHelper(collection="service station customers")
    query = {'email': email}
    customer = db.fetch(query)[0]

    db_cars = MongoDBHelper(collection="service station cars")
    query = {'service_station_id': session['service_station_id'], 'customer_email': email}  # Use 'customer_email'
    documents = db_cars.fetch(query)

    return render_template('cars1.html',
                           email=session['service_station_email'],
                           name=session['service_station_name'],
                           customer=customer,
                           documents=documents)


@web_app.route("/delete-car/<id>")
def delete_car(id):
    db = MongoDBHelper(collection="service station cars")
    query = {'_id': ObjectId(id)}
    car = db.fetch(query)[0]
    db.delete(query)
    return render_template("success1.html", message="customer with ID {} and car name {} Deleted...".format(id, car['car_name']))


@web_app.route("/update-car-service-station/<customer_email>", methods=['POST'])
def update_car_service_station(customer_email):
    car_data_to_update = {
        'car_name': request.form['car_name'],
        'car_number': request.form['car_number'],
        'car_colour': request.form['car_colour'],
        'car_model': request.form['car_model'],
        'kms_driven': request.form['kms_driven'],
        'car_id': request.form['car_id'],
        'service_due': request.form['service_due'],
        'customer_email': customer_email,
        'service_station_id': session['service_station_id'],
        'createdOn': datetime.datetime.today()
    }

    db = MongoDBHelper(collection="service station cars")
    query = {'_id': ObjectId(request.form['car_id'])}

    print(car_data_to_update)
    print(query)
    db.update(car_data_to_update, query)

    if len(car_data_to_update['car_name']) == 0 or len(car_data_to_update['car_number']) == 0 or len(
            car_data_to_update['service_due']) == 0:
        return render_template('error1.html', message="car name, car number, and service due cannot be Empty")

    return render_template('success1.html',
                           message="{} updated successfully".format(car_data_to_update['car_name']))


@web_app.route("/update-car/<id>")
def update_car(id):
    db = MongoDBHelper(collection="service station cars")
    query = {'_id': ObjectId(id)}
    car = db.fetch(query)[0]
    return render_template("update-cars1.html", car=car, customer_email=car['customer_email'])


@web_app.route("/add-service/<id>")
def add_service(id):
    db = MongoDBHelper(collection="service station cars")
    query = {'_id': ObjectId(id)}
    cars = db.fetch(query)
    car = cars[0]

    db_customer = MongoDBHelper(collection="service station customers")
    query_customer = {'email': car['customer_email']}
    customer = db_customer.fetch(query_customer)[0]

    return render_template("add-services1.html",
                           _id=session['service_station_id'],
                           email=session['service_station_email'],
                           name=session['service_station_name'],
                           car=car,
                           customer=customer)


@web_app.route("/save-service", methods=["POST"])
def save_service():
    service_data = {
        'problem': request.form['problem'],
        'Repaired Parts': request.form['Repaired Parts'],
        'replaced parts': request.form['replaced parts'],
        'car type': request.form['car type'],
        'price': request.form['price'],
        'service_due': request.form['service_due'],
        'cid': request.form['cid'],
        'customer_email': request.form['customer_email'],
        'car_id': request.form['car_id'],
        'car_number': request.form['car_number'],
        'service_station_name': session['service_station_name'],
        'service_station_email': session['service_station_email'],
        'createdOn': datetime.datetime.today()
    }

    if len(service_data['problem']) == 0 or len(service_data['service_due']) == 0:
        return render_template('error1.html', message="problem and service due cannot be Empty")

    print(service_data)
    db = MongoDBHelper(collection="service-station-services")
    db.insert(service_data)

    return render_template('success1.html', message="service added successfully..")


@web_app.route("/fetch-services-cars/<car_number>")
def fetch_services_of_car(car_number):
    print("car_number:", car_number)

    db_services = MongoDBHelper(collection="service-station-services")
    query_services = {
        'car_number': car_number,
    }
    documents = db_services.fetch(query_services)
    print(documents, type(documents))

    return render_template('services-cars.html',
                           documents=documents,
                           car_number=car_number)




def main():
    web_app.secret_key = 'your_secret_key'
    web_app.run(port=12121)


if __name__ == "__main__":
    main()
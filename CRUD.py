from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder = ".")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///WarehouseDB.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Warehouse(db.Model):
	__tablename__ = "table"
	location = db.Column(db.String, primary_key = True)
	inventory = db.Column(db.Integer, nullable = False, default = 0)

	def __init__(self, location, inventory):
		self.location = location
		self.inventory = inventory

def readWarehouses():
	return db.session.query(Warehouse).all()

def createWarehouse(location, inventory):
	
	try:
		warehouse = Warehouse(location, inventory)
		db.session.add(warehouse)
		db.session.commit()
		db.session.refresh(warehouse)

	except: # im sorry
		db.session.rollback()

@app.route("/", methods = ["GET", "POST"])
def MainPage():
	if request.method == "POST":
		
		location = request.form["location1"]
		if(location.isspace() or location in [warehouse.location for warehouse in db.session.query(Warehouse).all()]):
			flash("Invalid entry :)", "error")

		createWarehouse(location, request.form["inventory"])

	return render_template("index.html", warehouses = readWarehouses())

@app.route("/update/", methods = ["POST"])
def updateWarehouse():
	
	if request.method == "POST":
		db.session.query(Warehouse).filter_by(location = request.form["location2"]).update({"inventory": request.form["newInventory"]})
		db.session.commit()

	return redirect("/", code = 302)

@app.route("/delete/", methods = ["POST"])
def deleteWarehouse():
	
	if request.method == "POST":
		db.session.query(Warehouse).filter_by(location = request.form["location3"]).delete()
		db.session.commit()

	return redirect("/", code = 302)

if(__name__ == "__main__"):
	db.create_all()
	app.run(debug = True)

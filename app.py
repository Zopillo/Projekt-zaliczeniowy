from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ksiazka.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#inicjacja
db = SQLAlchemy(app)

#budowanie bazy
class Ksiazka(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	#funkcja do zwracania wartości
	def __repr__(self):
		return '<Name %r>' % self.id

@app.route('/')
def index():
	title = "Moja aplikacja webowa"
	return render_template("index.html", title = title)


@app.route('/delete/<int:id>')
def delete(id):
	friend_to_delete = Ksiazka.query.get_or_404(id)
	try:
		db.session.delete(friend_to_delete)
		db.session.commit()
		return redirect('/ksiazka')
	except:
		return "Wyskoczyl blad przy usuwaniu"


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
 	title = "UPDATE"
 	friend_to_update = Ksiazka.query.get_or_404(id)
 	if request.method == "POST":
 		friend_to_update.name = request.form['name']
 		try:
 			db.session.commit()
 			return redirect('/ksiazka')
 		except:
 			return "Wyskoczyl blad..."
 	else: 
 		return render_template("update.html", title = title, friend_to_update = friend_to_update)






@app.route('/ksiazka', methods=['POST','GET'])
def ksiazka():
	title = "Ksiazka telefoniczna"

	if request.method == "POST":

		friend_name = request.form['name']
		new_friend = Ksiazka(name=friend_name)

		#dodanie do bazy

		try:
			db.session.add(new_friend)
			db.session.commit()
			return redirect('/ksiazka')
		except:
			return "Wyskoczyl blad..."

	else:
		ksiazkatel = Ksiazka.query.order_by(Ksiazka.date_created)
		return render_template("ksiazka.html", title = title, ksiazka = ksiazkatel)

	return render_template("ksiazka.html", title = title)
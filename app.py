from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SISTEMAS_UPEA_2026_GOLD_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products_v3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'tbl_productos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Product {self.name}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    query = request.args.get('search')
    if query:
        dataset = Product.query.filter(Product.name.contains(query)).all()
    else:
        dataset = Product.query.order_by(Product.id.desc()).all()
    return render_template('index.html', products=dataset)

@app.route('/inventory/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            price = float(request.form.get('price'))
            stock = int(request.form.get('stock'))
            
            new_item = Product(name=name, price=price, stock=stock)
            db.session.add(new_item)
            db.session.commit()
            flash('Registro exitoso en el sistema.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error en los datos ingresados.', 'danger')
            
    return render_template('add.html')

@app.route('/inventory/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Product.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.price = float(request.form.get('price'))
        item.stock = int(request.form.get('stock'))
        db.session.commit()
        flash('Información actualizada correctamente.', 'info')
        return redirect(url_for('index'))
    return render_template('edit.html', product=item)

@app.route('/inventory/delete/<int:id>')
def delete(id):
    item = Product.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Producto eliminado de la base de datos.', 'warning')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
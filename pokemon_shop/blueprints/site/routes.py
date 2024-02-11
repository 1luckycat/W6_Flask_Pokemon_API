from flask import Blueprint, flash, redirect, render_template, request

# internal imports
from pokemon_shop.models import Product, Customer, Order, db
from pokemon_shop.forms import ProductForm


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def shop():
    allprods = Product.query.all()
    allcustomers = Customer.query.all()
    allorders = Order.query.all()

    shop_stats = {
        'products': len(allprods),
        'sales': sum([order.order_total for order in allorders]),
        'customers': len(allcustomers)
    }

    return render_template('shop.html', shop=allprods, stats=shop_stats)


@site.route('/shop/create', methods=['GET', 'POST'])
def create():
    createform = ProductForm()

    if request.method == 'POST' and createform.validate_on_submit():
        name = createform.name.data
        image = createform.image.data
        types = createform.types.data
        ability = createform.ability.data
        height = createform.height.data
        weight = createform.weight.data
        price = createform.price.data
        quantity = createform.quantity.data

        pokemon = Product(name, price, quantity, image, types, ability, height, weight)

        db.session.add(pokemon)
        db.session.commit()

        flash(f"You have successfully added {name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("Unable to process your request.  Please try again.", category='warning')
        return redirect('/shop/create')
    
    return render_template('create.html', form=createform)


@site.route('/shop/update/<id>', methods=['GET', 'POST'])
def update(id):
    pokemon = Product.query.get(id) 
    updateform = ProductForm()

    if request.method == 'POST' and updateform.validate_on_submit():

        pokemon.name = updateform.name.data 
        pokemon.image = pokemon.set_image(updateform.image.data, updateform.name.data)
        pokemon.types = pokemon.set_types(updateform.types.data, updateform.name.data)
        pokemon.ability = pokemon.set_ability(updateform.ability.data, updateform.name.data)
        pokemon.height = pokemon.set_height(updateform.height.data, updateform.name.data)
        pokemon.weight = pokemon.set_weight(updateform.weight.data, updateform.name.data)
        pokemon.price = updateform.price.data 
        pokemon.quantity = updateform.quantity.data 

        #commit our changes
        db.session.commit()

        flash(f"You have successfully updated {pokemon.name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("Unable to process your request.  Please try again.", category='warning')
        return redirect('/')
    
    return render_template('update.html', form=updateform, product=pokemon )


@site.route('/shop/delete/<id>')
def delete(id):
    pokemon = Product.query.get(id)

    db.session.delete(pokemon)
    db.session.commit()

    return redirect('/')


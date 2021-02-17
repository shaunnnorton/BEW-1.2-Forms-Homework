from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm,GroceryItemForm,SignUpForm,LoginForm
from grocery_app import bcrypt
# Import app and db from events_app package so that we can run app
from grocery_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    """Routre to render homepage with all stores."""
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    '''Route for adding a new_store to the database. '''
    form = GroceryStoreForm()
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user,
            created_by_id=current_user.id
        )
        db.session.add(new_store)
        db.session.commit()
        flash("New Store Was Created!")
        return redirect(url_for('main.store_detail',store_id=new_store.id))
    return render_template('new_store.html',form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    '''Route for adding a new item to the Database'''
    form = GroceryItemForm()
    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=current_user,
            created_by_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        flash("New Item was Created!")
        return redirect(url_for('main.item_detail',item_id=new_item.id))
    return render_template('new_item.html',form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    '''Route for displaying and modifying a store's information in the database.'''
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)

    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.commit()
        flash("Store Infromation Was Updated")
        return redirect(url_for('main.store_detail',store_id=store_id))
    
    return render_template('store_detail.html', store=store,form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    '''Route for displaying and modifying a items information in the database.'''
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)
    if form.validate_on_submit():
        item.name=form.name.data
        item.price=form.price.data
        item.category=form.category.data
        item.photo_url=form.photo_url.data
        item.store=form.store.data
        db.session.commit()
        flash("Item information was Updated!")
        return redirect(url_for('main.item_detail',item_id=item_id))
    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', item=item,form=form)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_items.append(item)
    db.session.commit()
    flash(f'{item.name} added to Shopping list')
    return redirect(url_for('main.item_detail',item_id=item_id))

@main.route('/shopping_list')
@login_required
def shopping_list():
    items = current_user.shopping_list_items
    context = {'items':items}
    return render_template('shopping_list.html',**context)


# routes.py

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))


import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy # Changed: Imported SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import random


app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'devraj.patel247@gmail.com' # Your Gmail address
app.config['MAIL_PASSWORD'] = 'kyyi dcvz ofvr bjbz' # Your App Password here

mail = Mail(app)

app.secret_key = 'your_secret_key' # Make sure to change this to a strong, random key in production!

# Removed MySQL Config specific to Flask_MySQLdb
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Mohit@0007'
# app.config['MYSQL_DB'] = 'shopping_app'

# SQLAlchemy (PostgreSQL) Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
print(f"DEBUG: SQLALCHEMY_DATABASE_URI is: {app.config['SQLALCHEMY_DATABASE_URI']}") # ADD THIS LINE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Good practice for SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

# Define User model for SQLAlchemy (This is how you interact with your 'users' table)
class User(db.Model):
    __tablename__ = 'users' # Ensure this matches your table name in shopping_app.sql
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Store hashed password

    def __repr__(self):
        return f'<User {self.username}>'

# IMPORTANT: You need to create the table if it doesn't exist.
# For initial deployment on Render, the 'db.create_all()' will typically run if the table doesn't exist,
# but usually, you'd run this locally once, or use migrations.
# Since you have shopping_app.sql, you'll import that to Render's Postgres.
# So, you don't need to run this on every app start, but it's here for context.
# with app.app_context():
# db = SQLAlchemy(app)
with app.app_context(): # ADD THIS LINE
    db.create_all()  


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

ALL_PRODUCTS = [
    {
        'id': 1,
        'name': 'KRISH DUTT',
        'price': 69,
        'image': 'krish.jpg',
        'personality': 'Pookie',
        'color': 'White (Russian)',
        'details': 'Super funny and always cracking jokes!',
        'category': 'chill',
        'catchphrase': '"Eee chalneee!!"',
        'hobbies': ['video editing', 'watching movies and webseries', 'applying proposals', 'Gymfreak'],
        'best_feature': 'Content creator',
    },

    {
        'id': 2,
        'name': 'MAHARSHI PATEL',
        'price': 69,
        'image': 'maharshi.jpg',
        'personality': 'Badmosh',
        'color': 'White',
        'details': 'Big contacts, anywhere, anytime',
        'category': 'Badmosh',
        'catchphrase': '"Maare ketla.."',
        'hobbies': ['Cricket', 'To keep exploring','photography', 'Aalu Sev LOVER!'],
        'best_feature': 'ATTRACTIVE',
    },
    {
        'id': 3,
        'name': 'DEEP PATEL',
        'price': 69,
        'image': 'deep.jpg',
        'personality': 'BATMAN',
        'color': 'NATURAL WHITE',
        'details': 'Bakchodi on TOP',
        'category': 'chill',
        'catchphrase': '"Rano rana ni rite!"',
        'hobbies': ['LCN', 'Valorant'],
        'best_feature': 'GAMER + Introvert',
    },
    {
        'id': 4,
        'name': 'DEVRAJ PATEL',
        'price': 69,
        'image': 'devraj.jpg',
        'personality': 'Calm & Controlled',
        'color': 'Brown',
        'details': 'Problem solver',
        'category': 'Toppers',
        'catchphrase': '"TMKC!"',
        'hobbies': ['Coding', 'Part time singer', 'Bike riding', "Wicket keeper"],
        'best_feature': 'Always ready to help',
    },
    {
        'id': 5,
        'name': 'MOHIT SAHU',
        'price': 69,
        'image': 'mohit.jpg',
        'personality': 'Multitasker',
        'color': 'Indian',
        'details': 'Can buy anyone',
        'category': 'chill',
        'catchphrase': '"G@nd marave.."',
        'hobbies': ['Andha paisa', 'Gamer', 'One sided Lover', 'Gymfreak'],
        'best_feature': 'Down to earth',
    },
    {
        'id': 6,
        'name': 'MEET PANCHAL',
        'price': 69,
        'image': 'meet.jpg',
        'personality': 'Straight',
        'color': 'White asian',
        'details': 'Chill guy',
        'category': 'chill',
        'catchphrase': '"Maaro @@ le"',
        'hobbies': ['Trend setter', 'Music Lover', 'Gym Boy'],
        'best_feature': 'Acheived Calmness',
    },
    {
        'id': 7,
        'name': 'KAVY VAGADIYA',
        'price': 69,
        'image': 'kavy.png',
        'personality': 'FIGMA',
        'color': 'Indian',
        'details': 'Thala Lover',
        'category': 'Baaj',
        'catchphrase': '"Chaklaa Koi Di Baaj no Bane"',
        'hobbies': ['FF Lover', 'Idli lover', "Thala's six"],
        'best_feature': 'Easygoer',
    },

    {
        'id': 8,
        'name': 'JENISH PATEL',
        'price': 69,
        'image': 'jenish.png',
        'personality': 'Open',
        'color': 'North indian',
        'details': 'Koi farak nai padta',
        'category': 'Badmosh',
        'catchphrase': '"Maare baar javanu chee.."',
        'hobbies': ['Gaamdu lover', 'Rakhadvu', "Clg thi ghare javu"],
        'best_feature': "The man with 0 haters",
    },
    {
        'id': 9,
        'name': 'DEV CHAUHAN',
        'price': 30,
        'image': 'devc.jpg',
        'personality': 'Topper',
        'color': 'White indian',
        'details': 'Tensed for results (10spi)',
        'category': 'Toppers',
        'catchphrase': '"Are yaaarrr"',
        'hobbies': ['Garba Lover', 'Eating tasty', "IPDC Lover"],
        'best_feature': "Loading..",
    },
    {
        'id': 10,
        'name': 'DEV PANDYA',
        'price': 69,
        'image': 'devp.png',
        'personality': 'Pandit',
        'color': 'Brown Indian',
        'details': 'GRC MEMBER',
        'category': 'Badmosh',
        'catchphrase': '"Moree moro"',
        'hobbies': ['LCN', 'Choraafadi lover', "Pro at Soldering"],
        'best_feature': "Confident",
    },
    {
        'id': 11,
        'name': 'KRISH BHRAMBHATT',
        'price': 69,
        'image': 'krishB.jpg',
        'personality': 'Aesthetic',
        'color': 'White',
        'details': '404 Not found',
        'category': 'baaj',
        'catchphrase': '"😄"',
        'hobbies': ['Chess player', "Pro Dancer", 'Setting hairs', 'Gymfreak'],
        'best_feature': "Living to the fullest",
    },
    {
        'id': 12,
        'name': 'MAHIL PARMAR',
        'price': 69,
        'image': 'mahil.png',
        'personality': 'Don',
        'color': 'Pure indian',
        'details': 'Bapunagar under control!',
        'category': 'Badmosh',
        'catchphrase': '"Pachaas baap!!"',
        'hobbies': ['pepsi lover', "Programming ", 'Driving'],
        'best_feature': "yaaro pe jaan luta du"
    },
    {
        'id': 13,
        'name': 'PREET RUPARELIYA',
        'price': 69,
        'image': 'preet.jpg',
        'personality': 'Classy',
        'color': 'Natural White',
        'details': 'Rarely college goer',
        'category': 'chill',
        'catchphrase': '"Aavana-aava...."',
        'hobbies': ["Gymrat", 'Driving', 'Study from home'],
        'best_feature': "Extrovert"
    },
    {
        'id': 14,
        'name': 'HARSHVARDHAN GANGURDE',
        'price': 69,
        'image': 'harshvardhan.jpg',
        'personality': 'Pookie',
        'color': 'Pure indian',
        'details': 'most famous guy of clg',
        'category': 'chill',
        'catchphrase': '"Jane L*da"',
        'hobbies': ['Volleyball', 'Influencing'],
        'best_feature': "Socially Extrovert"
    },
    {
        'id': 15,
        'name': 'YASH PRAJAPATI',
        'price': 69,
        'image': 'yash.jpg',
        'personality': 'Heart hacker',
        'color': 'Dark, Darker, Darkest',
        'details': 'Jhon banega don.',
        'category': 'Badmosh',
        'catchphrase': '"Maar Khais"',
        'hobbies': ['Cricket','Java', 'VGG Lover'],
        'best_feature': "Ready to help"
    },
    {
        'id': 16,
        'name': 'JIMIT PATEL',
        'price': 69,
        'image': 'jimit.jpg',
        'personality': 'Smart',
        'color': 'Pure indian',
        'details': 'AMTS under control',
        'category': 'baaj',
        'catchphrase': '"Manit ne Phone kar!!"',
        'hobbies': ['Amts ka BAAP', 'Always chill'],
        'best_feature': "Gatti ka step-father"
    },
    {
        'id': 17,
        'name': 'DEEP PATEL',
        'price': 69,
        'image': 'deepj.jpg',
        'personality': 'Kiddo',
        'color': 'Milk White',
        'details': 'Enough to generate a tornado',
        'category': 'Badmosh',
        'catchphrase': '"Maa Ch*di"',
        'hobbies': ["Food lover", "BGMI"],
        'best_feature': "Hot and Sweet"
    },
    {
        'id': 18,
        'name': 'MANIT PATEL',
        'price': 69,
        'image': 'manit.jpg',
        'personality': 'Friendly',
        'color': 'indian',
        'details': 'Maa ka laadla',
        'category': 'chill',
        'catchphrase': '"Jovu Padse.."',
        'hobbies': ["Staying at home", "Listening music"],
        'best_feature': "Even I don't know"
    },
    {
        'id': 19,
        'name': 'NIRAV SOLANKI',
        'price': 69,
        'image': 'nirav.jpg',
        'personality' : 'Pure Kathiyavadi',
        'color': 'Pure indian',
        'details': "Web Developer",
        'category': 'baaj',
        'catchphrase': '"Haaltino thaa"',
        'hobbies': ["Body building", "Sports Cars"],
        'best_feature': "Can create a quick friendly environment"
    },
    {
        'id': 20,
        'name': 'PARSHV SHAH',
        'price': 69,
        'image': 'parshv.jpg',
        'personality': 'Badmosh fr',
        'color': 'indian',
        'category': 'Badmosh',
        'catchphrase': '"Yaarr"',
        'hobbies': ['Adventure', 'Gaming'],
        'best_feature': "Always ready for help"
    }
]


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    flip = False # False = Login, True = Register

    if request.method == 'POST':
        if 'login_submit' in request.form:
            username = request.form['login_username']
            password = request.form['login_password']
            
            # --- SQLAlchemy Change ---
            user = User.query.filter_by(username=username).first()
            # --- End SQLAlchemy Change ---

            if user and check_password_hash(user.password, password): # Changed: user.password
                session['username'] = username
                flash('Logged in successfully!')
                return redirect(url_for('products'))
            else:
                message = "Invalid username or password."
                flip = False

        elif 'register_submit' in request.form:
            flip = True
            username = request.form['register_username']
            email = request.form['register_email']
            password = request.form['register_password']
            confirm_password = request.form['register_confirm_password']

            if password != confirm_password:
                message = "Passwords don't match."
            else:
                # --- SQLAlchemy Change ---
                existing_user_username = User.query.filter_by(username=username).first()
                existing_user_email = User.query.filter_by(email=email).first()
                # --- End SQLAlchemy Change ---

                if existing_user_username or existing_user_email:
                    message = "Username or email already exists."
                else:
                    hashed_password = generate_password_hash(password)
                    # --- SQLAlchemy Change ---
                    new_user = User(username=username, email=email, password=hashed_password)
                    db.session.add(new_user)
                    db.session.commit()
                    # --- End SQLAlchemy Change ---

                    flash('Registration successful! Please log in.')
                    return redirect(url_for('index'))

    return render_template('index.html', message=message, flip=flip, username=session.get('username'))

@app.route('/products')
def products():
    if 'username' not in session:
        flash('Please log in first.')
        return redirect(url_for('index'))

    selected_category = request.args.get('category')

    if selected_category and selected_category != "":
        filtered_products = [p for p in ALL_PRODUCTS if p['category'] == selected_category]
    else:
        filtered_products = ALL_PRODUCTS

    cart = session.get('cart', {})
    cart_count = sum(cart.values())

    return render_template('main.html', username=session['username'], products=filtered_products, cart_count=cart_count, selected_category=selected_category)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    if 'username' not in session:
        flash('Please log in first.')
        return redirect(url_for('index'))

    cart = session.get('cart', {})

    cart_items = []
    total_price = 0.0

    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = next((p for p in ALL_PRODUCTS if p['id'] == product_id), None)
        if product:
            item_total = product['price'] * quantity
            item = product.copy()
            item['quantity'] = quantity
            item['total'] = item_total
            item['id'] = product['id']
            cart_items.append(item)
            total_price += item_total
        else:
            print(f"Warning: Product with ID {product_id} not found in ALL_PRODUCTS list.")

    total_price = float(total_price)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price, username=session['username'])

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Item added to cart!')
    return redirect(url_for('products'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'username' not in session:
        flash('Please log in first.')
        return redirect(url_for('index'))

    cart = session.get('cart', {})

    product_id_str = str(product_id)
    if product_id_str in cart:
        cart.pop(product_id_str)
        session['cart'] = cart
        flash('Item removed from cart.')

    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'username' not in session:
        flash('Please log in first.')
        return redirect(url_for('index'))

    username = session['username']

    # --- SQLAlchemy Change ---
    user_data = User.query.filter_by(username=username).first()
    # --- End SQLAlchemy Change ---

    if not user_data:
        flash('User email not found.')
        return redirect(url_for('cart'))

    user_email = user_data.email # Changed: Access email via .email on the User object
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('products'))

    all_products = ALL_PRODUCTS

    cart_items = []
    total_price = 0
    for product_id_str, qty in cart.items():
        product_id = int(product_id_str)
        product = next((p for p in all_products if p['id'] == product_id), None)
        if product:
            item_total = float(product['price'] * qty)
            total_price += item_total
            cart_items.append({
                'name': product['name'],
                'price': product['price'],
                'quantity': qty,
                'total': item_total
            })
        else:
            print(f"Product with id {product_id} not found!")

    if request.method == 'POST':
        try:
            msg = Message("Payment Confirmation - HoomanMart",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[user_email])
            msg.body = f"Hi {username},\n\nThank you for your purchase!\n\nOrder details:\n"
            for item in cart_items:
                msg.body += f"- {item['name']} x {item['quantity']} = ${item['total']:.2f}\n"
            msg.body += f"\nTotal Paid: ${total_price:.2f}\n\nThanks!"
            mail.send(msg)
            flash('Payment successful! Confirmation email sent.')
        except Exception as e:
            flash(f"Payment processed but email failed: {str(e)}")

        session['cart'] = {} # Clear cart after successful checkout/email attempt
        return redirect(url_for('products'))

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

# The corrected and completed /mock-payment route
@app.route('/initiate-mock-payment', methods=['POST'])
def initiate_mock_payment():
    if 'username' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('index'))

    # Get total_price from the form submitted by checkout.html
    total_price_str = request.form.get('total_price')
    try:
        total_price = float(total_price_str)
        if total_price <= 0 and not session.get('cart'): # Check if cart is empty after float conversion
            flash('Your cart is empty or total price is zero.', 'error')
            return redirect(url_for('products'))
    except (ValueError, TypeError):
        flash('Invalid total price for payment.', 'error')
        return redirect(url_for('checkout'))

    # Render the new scanner payment page, passing the total price
    return render_template('mock_scanner_payment.html', total_price=total_price)

# This route completes the scanner payment after UTR submission
@app.route('/complete-mock-payment', methods=['POST'])
def complete_mock_payment():
    if 'username' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('index'))

    utr = request.form.get('utr')
    total_price_str = request.form.get('total_price') # Get total_price passed from scanner page

    try:
        total_price = float(total_price_str)
    except (ValueError, TypeError):
        flash('Payment validation failed: Invalid total price.', 'error')
        return redirect(url_for('checkout')) # Redirect back to checkout if price is invalid

    # Basic UTR validation: must be 12 digits and numeric
    if utr and len(utr) == 12 and utr.isdigit():
        # Payment successful simulation
        customer_name = session.get('username', 'Customer')
        print(f"Mock Scanner Payment successful for {customer_name} with UTR: {utr} - Amount: ${total_price_str}")

        # Clear cart
        session['cart'] = {}
        flash(f"Payment successful! Thank you, {customer_name}. Your purchase is complete.", 'success')
        return redirect(url_for('products')) # Redirect to products page on success
    else:
        flash("Invalid UTR. Please enter a 12-digit number.", 'error')
        # If UTR is invalid, redirect back to the scanner page, passing total_price again
        return render_template('mock_scanner_payment.html', total_price=total_price)

# The single, correct /paypal-payment-complete route
@app.route('/paypal-payment-complete', methods=['POST'])
def paypal_payment_complete():
    data = request.get_json(force=True) # force=True to ensure JSON parsing
    print("Payment success:", data)

    # Clear cart safely
    session['cart'] = {}

    # Extract customer name or default to 'Customer'
    customer_name = data.get('name') if data else 'Customer'

    # Flash a success message
    flash(f"Payment successful! Thank you, {customer_name}.", 'success') # Added 'success' category

    # Return HTTP 200 OK with empty body
    return '', 200

@app.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    if 'username' not in session:
        flash('Please log in first.')
        return redirect(url_for('index'))

    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        try:
            new_quantity = int(request.form['quantity'])
            if new_quantity > 0:
                cart[product_id_str] = new_quantity
                flash(f"Quantity for item updated to {new_quantity}.")
            else:
                cart.pop(product_id_str)
                flash("Item removed from cart (quantity set to 0 or less).")
        except (ValueError, KeyError):
            flash("Invalid quantity provided.")
        session['cart'] = cart
    else:
        flash("Product not found in cart.")

    return redirect(url_for('cart'))

@app.route('/payment-success')
def payment_success():
    return render_template('payment_success.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
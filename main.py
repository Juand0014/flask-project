from flask import Flask
from flask import render_template, request, make_response, session, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
import json
import forms
from config import DevelopmentConfig
from helper import date_format

from models import db, User, Comment

from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

csrf = CSRFProtect()
mail = Mail()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['comment']:
        return redirect(url_for('login'))

    elif 'username' in session and request.endpoint in ['login', 'create']:
        return redirect(url_for('index'))


@app.after_request
def after_request(response):
    return response


@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        username = session['username']
        print(username)
    # custom_cookie = request.cookies.get('custom_cookie', "Undefined")
    comment_form = forms.CommentForm(request.form)
    return render_template('index.html', title="Curso de flask", form=comment_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            success_message = 'Bienvenido {}'.format(username)
            flash(success_message)
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error_message = "Usuario o contraseña no valida!"
            flash(error_message)

        session['username'] = login_form.username.data
    return render_template('login.html', form=login_form)


@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('user_id', '1')
    return response


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    session['user_id'] = 1
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():
        user_id = session['user_id']
        comment = Comment(user_id=user_id, text=comment_form.comment.data)

        db.session.add(comment)
        db.session.commit()

        success_message = 'Nuevo Comentario Creado!'
        flash(success_message)
    else:
        print("Error en el Formulario")

    return render_template('comment.html', title='Curso de flask', form=comment_form)


@app.route('/ajax-login', methods=['POST'])
def ajax_login():
    username = request.form['username']
    response = {
        'status': 200,
        'username': username,
        'id': 1
    }
    return json.dumps(response)


@app.route('/create', methods=['GET', 'POST'])
def create():
    create_form = forms.CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():
        user = User(
            create_form.username.data,
            create_form.password.data,
            create_form.email.data
        )

        db.session.add(user)
        db.session.commit()
        
        msg = Message('Gracias por tu registro', sender= app.config['MAIL_USERNAME'], recipients = [user.email])
        msg.html = render_template('email.html', user=user.username)
        mail.send(msg)

        success_message = 'Usuario registrado en la base de datos'
        flash(success_message)
        return redirect(url_for('login'))

    return render_template('create.html', form=create_form)


@app.route('/reviews/', methods=['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def reviews(page = 1):
    per_page = 2
    
    comment_list = Comment.query.join(User).add_columns(
        User.username,
        Comment.text,
        Comment.created_date
    ).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('reviews.html', comments=comment_list, date_format=date_format)


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8000)

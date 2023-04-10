from flask import Flask
from flask import render_template, request, make_response, session, redirect, url_for
from flask_wtf.csrf import CSRFProtect

import forms

app = Flask(__name__)
app.secret_key = 'super secret key'
csrf = CSRFProtect(app)
app.jinja_env.globals["csrf_token"] = 

@app.route("/", methods=['GET' ,'POST'])
def index():
	custom_cookie = request.cookies.get('custom_cookie')
	comment_form = forms.CommentForm(request.form)
	print(custom_cookie)
	return render_template('index.html', title = "Curso de flask", form = comment_form);

@app.route('/login', methods=['GET' ,'POST'])
def login():
  login_form = forms.LoginForm(request.form)
  if request.method == 'POST' and login_form.validate():
    session['username'] = login_form.username.data
  return render_template('login.html', form= login_form)


@app.route('/cookie')
def cookie():
  response = make_response( render_template('cookie.html') )
  response.set_cookie('custom_cookie', 'Juan')
  return response

@app.route('/logout')
def logout():
  if 'username' in session:
    pass
  return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True, port=8000)
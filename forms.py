from wtforms import Form
from wtforms import StringField, validators, HiddenField, PasswordField
from wtforms.fields import EmailField
from models import User

def length_honetpot(form, field):
  if len(field.data) > 0:
    raise validators.ValidationError('El campo debe estar vacio')

class CommentForm(Form):
  comment = StringField('Comentario')
  honeypot = HiddenField('', [length_honetpot])
  
class LoginForm(Form):
  username = StringField('Username', [
    validators.Length(min=4, max=25, message="Ingrese un username valido")
  ])
  password = PasswordField('Password', [validators.Length(min=1, message="El password es requerido")])
  

class CreateForm(Form):
  username = StringField('Username', 
                         [
                           validators.length(min=7, max=25, message="Ingrese un username valido!."),
                         ])
  email = EmailField("Correo Electronico", 
                        [
                          validators.Email(message="Ingrese un email valido")
                        ])
  password = PasswordField('Password', [validators.Length(min=1, message="El password es requerido")])
  
  def validate_username(form, field):
    username = field.data
    user = User.query.filter_by(username=username).first()
    if user is not None:
      raise validators.ValidationError('El username ya se encuentra registrado!')
      
    
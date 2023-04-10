from wtforms import Form
from wtforms import StringField, validators, HiddenField, PasswordField
from wtforms.fields import EmailField

def length_honetpot(form, field):
  if len(field.data) > 0:
    raise validators.ValidationError('El campo debe estar vacio')

class CommentForm(Form):
  username = StringField('Username', 
                         [
                           validators.length(min=7, max=25, message="Ingrese un username valido!."),
                         ])
  email = EmailField("Correo Electronico", 
                        [
                          validators.Email(message="Ingrese un email valido")
                        ])
  comment = StringField('Comentario')
  honeypot = HiddenField('', [length_honetpot])
  
class LoginForm(Form):
  username = StringField('Username', [
    validators.Length(min=4, max=25, message="Ingrese un username valido")
  ])
  password = PasswordField('Password', [validators.Length(min=1, message="El password es requerido")])
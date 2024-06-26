from flask import Flask, render_template
from flask_login import LoginManager
from saleapp.models import *
from flask_admin import Admin
from flask_login import LoginManager, login_required, UserMixin
app=Flask(__name__)
app.secret_key="@345whejwelkfneoisjdi*widwe23751@#%$&*"

app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:1234567@localhost:5432/webhaisan"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config['PAGE_SIZE']=12
db.init_app(app)

login=LoginManager(app=app)
admin =Admin(app=app, name='Hải Sản Food', template_mode='bootstrap4')
def main():
    db.create_all()

if __name__=="__main__":
    with app.app_context():
        main()
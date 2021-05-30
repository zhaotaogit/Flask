from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import Config
from forms import RegisterForm

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        pass
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Подключение к базе данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Определение модели данных
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)

# Главная страница с кнопкой перехода на страницу отчёта
@app.route('/')
def index():
    return render_template('index.html')

# Страница с кнопками для формирования отчётов
@app.route('/report')
def report():
    reports = Report.query.all()  # Получаем данные из базы
    return render_template('report.html', reports=reports)

# Функция для добавления тестовых данных (можно запустить один раз)
@app.route('/add_sample_data')
def add_sample_data():
    sample_report = Report(name="Отчёт 1", data="Данные отчёта 1")
    db.session.add(sample_report)
    db.session.commit()
    return "Данные добавлены!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаём таблицу, если её нет
    app.run(debug=True)


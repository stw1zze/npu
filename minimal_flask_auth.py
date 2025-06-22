from flask import Flask, render_template_string, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'секретный_ключ_для_сессий'

# Простейшая "база данных" в памяти
users = {}

# HTML шаблон (упрощённый)
template = '''
<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8" />
<title>НПУ GTA</title>
<style>
  body { font-family: Arial; background: linear-gradient(135deg, #001f4d, #0057b7); color: white; text-align: center; padding: 2rem; }
  input, button { border-radius: 10px; padding: 10px; margin: 5px; }
  .error { color: #ffb3b3; }
</style>
</head>
<body>
  {% if 'user' in session %}
    <h2>Вітаємо, {{ session['user'] }}!</h2>
    <form action="{{ url_for('logout') }}" method="post">
      <button type="submit">Вийти</button>
    </form>
  {% else %}
    <h2>Реєстрація</h2>
    <form method="post" action="{{ url_for('register') }}">
      <input name="username" placeholder="Ім'я" required />
      <input type="password" name="password" placeholder="Пароль" required />
      <button type="submit">Зареєструватися</button>
    </form>
    <h2>Вхід</h2>
    <form method="post" action="{{ url_for('login') }}">
      <input name="username" placeholder="Ім'я" required />
      <input type="password" name="password" placeholder="Пароль" required />
      <button type="submit">Увійти</button>
    </form>
    {% if error %}
      <p class="error">{{ error }}</p>
    {% endif %}
  {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(template)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    if username in users:
        return render_template_string(template, error='Користувач вже існує')
    users[username] = generate_password_hash(password)
    session['user'] = username
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username not in users or not check_password_hash(users[username], password):
        return render_template_string(template, error='Невірний логін або пароль')
    session['user'] = username
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

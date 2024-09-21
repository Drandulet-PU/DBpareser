from flask import Flask
import os
from views import register_routes
from db import get_db

def create_app():
    DATABASE = 'diplom.db'
    #DEBUG = True
    SECRET_KEY = 'development key'

    # обновляет конфиг
    app = Flask(__name__)
    app.config.from_object(__name__)

    # явно указывает путь к бд
    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, DATABASE),
    ))

    # загружаем vies
    register_routes(app)

    return app
    
# создает пустую бд
def init_db():
    app = create_app()
    with app.app_context():
        db, cur = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            cur.executescript(f.read())
        db.commit()
            
if __name__ == '__main__':
    app = create_app()
    app.run()
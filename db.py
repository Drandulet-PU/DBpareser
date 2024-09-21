import sqlite3
from flask import Flask, current_app, g

# Соединяет с указанной бд.
def connect_db():
    db = sqlite3.connect(current_app.config['DATABASE'])
    cur = db.cursor()
    return db, cur
    
# Открывает соединение с бд если его еще нет в этом контексте
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.db, g.cur = connect_db()
    return g.db, g.cur
    
    # создает пустую бд
    def init_db(app):
        with app.app_context():
            db = get_db()
            with current_app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
    
# безопасное исполнение комманд
def sexecute(s, param=(), commit=0):
    db, cur = get_db()
    try:
        cur.execute(s, param)
        if commit:
            db.commit()
            
    except sqlite3.Error as ex:
        g.error = ex
        if commit:
            db.rollback()
            
    finally:
        return cur
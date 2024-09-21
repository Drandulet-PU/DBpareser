from flask import Blueprint, request, g, redirect, url_for, render_template, abort
from models import *

def register_routes(app):
        
    # Главная страница
    @app.route('/')
    def layout():
        return render_template('layout.html', \
                               groups=Group.gets())
    
    # Страница создания/изменения группы
    @app.route('/create_group/<int:id_3>', methods=['GET', 'POST'])
    def create_group(id_3):
        if request.method == "POST":
            if id_3 == 0:
                id_3 = Group.add(request.form['name'])
            else:
                Group.change(id_3, request.form['name'])
                
            if not g.get('error'):
                return redirect(url_for('show_table', \
                                        id_3=id_3))
            
            if str(g.error) == "UNIQUE constraint failed: groups.name":
                g.error = "Группа с таким именем уже есть"

        return render_template('create_group.html', \
                               groups=Group.gets())

    # Страница таблиц
    @app.route('/show_table/<int:id_3>', methods=['GET', 'POST'])
    def show_table(id_3):
        if Group.get(id_3) == None:
            abort(404)
            
        delete = request.args.get('delete', default=0, type=int)
        if delete:
            Group.delete(id_3)
            
            if not g.get('error'):
                return redirect(url_for('layout'))
                
        teachers = request.args.get('teachers', default=0, type=int)
        students = request.args.get('students', default=0, type=int)
        if (teachers or students) < 0 or (teachers or students) > 2:
            abort(404)
        
        ansr = ('', "ORDER BY avg_mark", "ORDER BY avg_mark DESC")
        head, body = get_table(id_3, ansr[teachers], ansr[students])
        teachers_table = Teacher.gets(id_3)
        students_table = Student.gets(id_3)
        
        return render_template('show_table.html', 
                               id_3=id_3, \
                               groups=Group.gets(), \
                               group=Group.get(id_3), \
                               head=head, body=body, \
                               teachers_table = teachers_table, \
                               students_table = students_table, \
                               teachers=teachers, students=students)


    # Страница изменения учителя
    @app.route('/change_teachers/<int:id_3>/<int:id_2>', methods=['GET', 'POST'])
    def change_teachers(id_3, id_2):
        if Group.get(id_3) == None:
            abort(404)
            
        if request.method == "POST":
            data = request.form
            delete = request.args.get('delete', default=0, type=int)
            if delete:
                Teacher.delete(id_2)
            elif id_2 == 0:
                id_2 = Teacher.add(data, id_3)
                change_marks([[key, id_2, value] for key, value in data.items()][4:])
            else:
                print(1)
                Teacher.change(data, id_2)
                print(2)
                change_marks([[key, id_2, value] for key, value in data.items()][4:])
                print(3)
                
            if not g.get('error'):
                return redirect(url_for('show_table', \
                                        id_3=id_3))
            
        head, body = Teacher.get(id_2, id_3)
        
        if id_2 and head == None:
            abort(404)

        return render_template('change_teachers.html', \
                               id_3=id_3, id_2=id_2, \
                               groups=Group.gets(), \
                               head=head, body=body) 
                               

    # Страница изменения ученика
    @app.route('/change_students/<int:id_3>/<int:id_1>', methods=['GET', 'POST'])
    def change_students(id_3, id_1):
        if Group.get(id_3) == None:
                abort(404)
                
        if request.method == "POST":
            data = request.form
            delete = request.args.get('delete', default=0, type=int)
            if delete:
                Student.delete(id_1)
            elif id_1 == 0:
                id_1 = Student.add(data, id_3)
                change_marks([[id_1, key, value] for key, value in data.items()][2:])
            else:
                Student.change(data, id_1)
                change_marks([[id_1, key, value] for key, value in data.items()][2:])
                
            if not g.get('error'):
                return redirect(url_for('show_table', \
                                        id_3=id_3))
            
        head, body = Student.get(id_1, id_3)
        
        if id_1 and head == None:
            abort(404)


        return render_template('change_students.html',
                               id_3=id_3, id_1=id_1, \
                               groups=Group.gets(), \
                               head=head, body=body, \
                               )

    # Разрывает соединение с бд при смене контекса
    @app.teardown_appcontext
    def close_db(error):
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()
            
    # 404
    @app.errorhandler(404)
    def error404(error):
        return render_template('404.html', \
                               groups=Group.gets())
                           
                 
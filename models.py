import sqlite3
from db import sexecute
from flask import Flask, current_app, g

class Group:
    # получение групп
    @staticmethod
    def gets():
        return sexecute("""
            SELECT * 
            FROM groups
            """).fetchall()
        
    # получение группы
    @staticmethod
    def get(id_3):
        cur = sexecute("""SELECT name 
            FROM groups 
            WHERE id_3 = ?
            """, (id_3,)).fetchone()
        if cur:
            return cur[0]
            
    
    # изменение группы
    @staticmethod
    def change(id_3, name):
        sexecute("""
            UPDATE groups
            SET name = ?
            WHERE id_3 == ?
            """, (name, id_3,), commit=1)
    
    # добавление группы
    @staticmethod
    def add(name):
        cur = sexecute("""
            INSERT INTO groups (name)
            SELECT ?
            """, (name,), commit=1)
            
        id_3 = cur.lastrowid
        
        return id_3
    
    # удаление группы
    @staticmethod
    def delete(id_3):
        sexecute("""
            DELETE FROM marks
            WHERE id_1 IN
            (SELECT id_1 
            FROM students
            WHERE id_3 = ?) 
            OR id_2 IN
            (SELECT id_2
            FROM teachers
            WHERE id_3 = ?)
            """, (id_3,id_3,), commit=1)
            
        sexecute("""
            DELETE FROM groups 
            WHERE id_3 = ?
            """, (id_3,), commit=1)
            
        sexecute("""
            DELETE FROM teachers
            WHERE id_3 = ?
            """, (id_3,), commit=1)
            
        sexecute("""
            DELETE FROM students
            WHERE id_3 = ?
            """, (id_3,), commit=1)
         
class Teacher:
    # получение учителей
    @staticmethod
    def gets(id_3):
        return sexecute("""
            SELECT id_2, name, work_place, job_title, gak
            FROM teachers
            WHERE id_3 = ?
        """, (id_3,)).fetchall()
    
    # получение учителя
    @staticmethod
    def get(id_2, id_3):
        head = sexecute("""
            SELECT name, work_place, job_title, gak
            FROM teachers
            WHERE id_2 = ?
        """, (id_2,)).fetchone()
     
        body = sexecute("""
            SELECT s.id_1, s.name, m.mark
            FROM students s
            LEFT JOIN marks m ON s.id_1 = m.id_1 AND m.id_2 = ?
            WHERE s.id_3 = ?;
        """, (id_2, id_3,)).fetchall()
            
        return head, body
    
    # изменение учителя
    @staticmethod
    def change(data, id_2):
        print("start")
        cur = sexecute("""
            UPDATE teachers
            SET name = ?, work_place = ?, job_title = ?, gak = ?
            WHERE id_2 == ?
            """, (data["name"], data["work_place"], data["job_title"], data["gak"], id_2,), commit=1)
        print("done")
    
    # добавление учителя
    @staticmethod
    def add(data, id_3):
        cur = sexecute("""
            INSERT INTO teachers (id_3, name, work_place, job_title, gak)
            SELECT ?, ?, ?, ?, ?
            """, (id_3, data["name"], data["work_place"], data["job_title"], data["gak"],), commit=1)
        
        id_2 = cur.lastrowid
        
        return id_2
    
    # удаление учителя
    @staticmethod
    def delete(id_2):
        sexecute("""
            DELETE FROM teachers 
            WHERE id_2 = ?
            """, (id_2,), commit=1)
            
        sexecute("""
            DELETE FROM marks 
            WHERE id_2 = ?
            """, (id_2,), commit=1)

class Student:
    # получение учеников
    @staticmethod
    def gets(id_3):
        return sexecute("""
            SELECT id_1, name, topic
            FROM students
            WHERE id_3 = ?
        """, (id_3,)).fetchall()
    
    # получение ученика
    @staticmethod
    def get(id_1, id_3):
        head = sexecute("""
            SELECT name, topic
            FROM students
            WHERE id_1 = ?
        """, (id_1,)).fetchone()
     
        body = sexecute("""
            SELECT t.id_2, t.name, m.mark
            FROM teachers t
            LEFT JOIN marks m ON t.id_2 = m.id_2 AND m.id_1 = ?
            WHERE t.id_3 = ?;
        """, (id_1, id_3,)).fetchall()
            
        return head, body
    
    # изменение ученика
    @staticmethod
    def change(data, id_1):
        sexecute("""
            UPDATE students
            SET name = ?, topic = ?
            WHERE id_1 == ?
            """, (data["name"], data["topic"], id_1,), commit=1)
    
    # добавление ученика
    @staticmethod
    def add(data, id_3):
        cur = sexecute("""
            INSERT INTO students (id_3, name, topic)
            SELECT ?, ?, ?
            """, (id_3, data["name"], data["topic"],), commit=1)
        
        id_1 = cur.lastrowid
        
        return id_1
        
    # удаление ученика
    @staticmethod
    def delete(id_1):
        sexecute("""
            DELETE FROM students 
            WHERE id_1 = ?
            """, (id_1,), commit=1)
            
        sexecute("""
            DELETE FROM marks 
            WHERE id_1 = ?
            """, (id_1,), commit=1)

# получение отсортированной таблицы
def get_table(id_3, teachers, students):
    head = sexecute("""
        SELECT t.id_2, t.name,
        COALESCE(AVG(m.mark), 0) AS avg_mark
        FROM teachers t
        LEFT JOIN marks m ON t.id_2 = m.id_2
        WHERE t.id_3 = ?
        GROUP BY t.id_2
    """ + teachers, (id_3,)).fetchall()

    body = sexecute(f"""
        SELECT s.id_1, s.name,
        {' '.join([f'MAX(CASE WHEN m.id_2 == {i[0]} THEN m.mark END),' for i in head])}
        COALESCE(AVG(m.mark), 0) AS avg_mark
        FROM students s
        LEFT JOIN marks m ON s.id_1 = m.id_1
        WHERE s.id_3 = ?
        GROUP BY s.id_1
    """ + students, (id_3,)).fetchall()
    
    return head, body

# изменение/добавление оценок
def change_marks(data):
    for i in data:
        if i[2] == '':
            i[2] = None
        print(i[0], i[1], i[2],)
        cur = sexecute("""
            UPDATE marks 
            SET mark = ? 
            WHERE id_1 = ? AND id_2 = ?
            """, (i[2], i[0], i[1],), commit=1)
        
        if cur.rowcount == 0:
            sexecute("""
            INSERT INTO marks (id_1, id_2, mark)
            SELECT ?, ?, ?
            """, (i[0], i[1], i[2],), commit=1)
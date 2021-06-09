import sqlite3
conn = sqlite3.connect('project.db')
cur = conn.cursor()


def test():
    cur.execute("SELECT * FROM student;")
    all_results = cur.fetchall()
    return all_results


def search_id(user_id):
    cur.execute(f'''SELECT student_name FROM student
                    WHERE student_id = {user_id};''')
    one_result = cur.fetchone()
    return one_result


def writing_student(user_list):
    cur.execute('''INSERT INTO student(student_id, surname, student_name, group_id) 
                    VALUES(?, ?, ?, ?);''', user_list)
    conn.commit()


# запрос на выдачу расписания по номеру группы
def give_schedule(id_group):
    cur.execute(f'''SELECT schedule.start_time, schedule.end_time, subjects.subjects_name 
                FROM group_schedule, schedule, subjects
                WHERE  group_schedule.group_id = {id_group}  
                AND group_schedule.schedule_id = schedule.schedule_id
                AND schedule.subjects_id = subjects.subjects_id
                ;''')
    all_results = cur.fetchall()
    return all_results


# запрос для выдачи заданий по номеру группы (создала новую таблицу)
def give_tasks(id_group):
    cur.execute(f'''SELECT  subjects.subjects_name, topic, description, date_deadline, time_deadline
                FROM tasks, subjects, tasks_for_group
                WHERE tasks.subject_id = subjects.subjects_id
                AND tasks_for_group.task_id = tasks.task_id
                AND tasks_for_group.group_id = {id_group}
                ;''')
    all_results = cur.fetchall()
    return all_results


def student_group(id_student):
    cur.execute(f'''SELECT group_id FROM student
                    WHERE student_id = {id_student};''')
    one_result = cur.fetchone()
    return one_result



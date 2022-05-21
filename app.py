from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/roopa-db'

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    score = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, fname, lname, score):
        self.fname = fname
        self.lname = lname
        self.score = score


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        score = request.form['score']
        student = Student(fname, lname, score)

        try:
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("Error while saving to DB." + str(e))
    else:
        students = Student.query.order_by(Student.date_created).all()
        return render_template('index.html', students=students)
    return render_template('index.html')


@app.route('/delete/<int:student_id>')
def delete(student_id):
    record_to_delete = Student.query.get_or_404(student_id)

    try:
        db.session.delete(record_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print("Error while delete from DB." + str(e))
        return 'There was a problem deleting the student.'


@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.id = request.form['id']
        student.fname = request.form['fname']
        student.lname = request.form['lname']
        student.score = request.form['score']
        student = Student(student.fname, student.lname, student.score)

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("Error while update on DB." + str(e))
            return 'There was a problem updating the student.'

    else:
        return render_template('update.html', student=student)


if __name__ == '__main__':  # python interpreter assigns "__main__" to the file you run
    app.run(debug=True)

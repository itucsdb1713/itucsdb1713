from handlers import site
from database import database
from user import *
import psycopg2 as dbapi2
import datetime
from passlib.apps import custom_app_context as pwd_context
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import login_user, current_user, login_required, logout_user
import urllib


@site.route('/training', methods=['GET', 'POST'])
@login_required
def training_page():
    if current_user.userType == 'admin' or current_user.userType == 'Trainer':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            if request.method == 'GET':
                query = """ SELECT x.ID, y.Name, x.TrainingName, x.Location, x.TrainingDate FROM TrainingInfo As x JOIN Parameters as y ON x.TypeId = y.Id ORDER BY x.TrainingDate DESC"""
                cursor.execute(query)
                trainings = cursor.fetchall()
                connection.commit()
                return render_template('training.html',trainings=trainings)
            else:
                deletes = request.form.getlist('training_to_delete')

                for delete in deletes:
                    query = "DELETE FROM TrainingInfo WHERE ID='%d'" % int(delete)
                    cursor.execute(query)


                return redirect(url_for('site.training_page'))
    else:
        return render_template('error.html')


@site.route('/training/add', methods=['GET', 'POST'])
@login_required
def training_add():
    if current_user.userType == 'admin' or current_user.userType == 'Trainer':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if request.method == 'GET':
                query = """ SELECT * FROM PARAMETERS WHERE TYPEID=4"""  #typeid 4 for training
                cursor.execute(query)
                training_data = cursor.fetchall()
                return render_template('training_add.html',training_data=training_data)
            else:
                trainingType = request.form['trainingType']
                trainingName = request.form['trainingName']
                trainingLoc = request.form['trainingLoc']
                trainingDate = request.form['trainingDate']

                query = "INSERT INTO TrainingInfo(TYPEID,TrainingName,Location,TrainingDate,CreateUserId,CreateDate) VALUES('%d', '%s', '%s', '%s','%d','%s')" % (int(trainingType), trainingName, trainingLoc, trainingDate,current_user.id,datetime.datetime.now())
                cursor.execute(query)

                connection.commit()

                return redirect(url_for('site.training_page'))
    else:
        return render_template('error.html')

@site.route('/training/update/<int:trainingID>', methods=['GET', 'POST'])
@login_required
def training_update(trainingID):
    if current_user.userType == 'admin' or current_user.userType == 'Trainer':
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if request.method == 'GET':

                query = """ SELECT x.ID, y.Name, x.TrainingName, x.Location, x.TrainingDate FROM TrainingInfo As x JOIN Parameters as y ON x.TypeId = y.Id WHERE x.ID=%d""" %(trainingID)
                cursor.execute(query)
                training = cursor.fetchone()
                query = """ SELECT * FROM PARAMETERS WHERE TYPEID=4"""  # typeid 4 for training
                cursor.execute(query)
                training_data = cursor.fetchall()
                connection.commit()
                print(training)
                return render_template('training_update.html', training=training,training_data=training_data)
            else:

                new_trainingType = request.form['trainingType']
                new_trainingName = request.form['trainingName']
                new_trainingLoc = request.form['trainingLoc']
                new_trainingDate = request.form['trainingDate']

                if new_trainingType != '':
                    query = """UPDATE TrainingInfo SET TypeID = '%s' WHERE ID = %d""" % (new_trainingType, int(trainingID))
                    cursor.execute(query)
                if new_trainingName != '':
                    query = """UPDATE TrainingInfo SET TrainingName = '%s' WHERE ID = %d""" % (new_trainingName, int(trainingID))
                    cursor.execute(query)
                if new_trainingLoc != '':
                    query = """UPDATE TrainingInfo SET Location = '%s' WHERE ID = %d""" % (new_trainingLoc, int(trainingID))
                    cursor.execute(query)
                if new_trainingDate != '':
                    query = """UPDATE TrainingInfo SET TrainingDate = '%s' WHERE ID = %d""" % (new_trainingDate, int(trainingID))
                    cursor.execute(query)


                connection.commit()
                return redirect(url_for('site.training_page'))
    else:
        return render_template('error.html')

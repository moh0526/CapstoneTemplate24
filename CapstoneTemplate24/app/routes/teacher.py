# These routes are an example of how to use data, forms and routes to create
# a forum where a blogs and comments on those blogs can be
# Created, Read, Updated or Deleted (CRUD)

# Teacher part

from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Teacher, Review
from app.classes.forms import TeacherForm, TeacherReviewForm
from flask_login import login_required
import datetime as dt

# This is the route to list all blogs
@app.route('/teacher/list')
@app.route('/teachers')
# This means the user must be logged in to see this page
@login_required
def teacherList():
    # This retrieves all of the 'blogs' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'blogs'.
    teachers = Teacher.objects().order_by("teacher_lname")
    # This renders (shows to the user) the blogs.html template. it also sends the blogs object 
    # to the template as a variable named blogs.  The template uses a for loop to display
    # each blog.
    return render_template('teachers.html',teachers=teachers)

# This route will get one specific blog and any comments associated with that blog.  
# The blogID is a variable that must be passsed as a parameter to the function and 
# can then be used in the query to retrieve that blog from the database. This route 
# is called when the user clicks a link on bloglist.html template.
# The angle brackets (<>) indicate a variable. 
@app.route('/teacher/<teacherID>')
# This route will only run if the user is logged in.
@login_required
def teacher(teacherID):
    # retrieve the blog using the blogID
    thisTeacher = Teacher.objects.get(id=teacherID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to blogs meaning that every comment contains a reference to a blog. In this case
    # there is a field on the comment collection called 'blog' that is a reference the Blog
    # document it is related to.  You can use the blogID to get the blog and then you can use
    # the blog object (thisBlog in this case) to get all the comments.
    theseReviews = Review.objects(teacher=thisTeacher)
    # Send the blog object and the comments object to the 'blog.html' template.
    return render_template('teacher.html',teacher=thisTeacher, reviews=theseReviews)

# This route will delete a specific blog.  You can only delete the blog if you are the author.
# <blogID> is a variable sent to this route by the user who clicked on the trash can in the 
# template 'blog.html'. 
# TODO add the ability for an administrator to delete blogs. 
@app.route('/teacher/delete/<teacherID>')
# Only run this route if the user is logged in.
@login_required
def teacherDelete(teacherID):
    # retrieve the blog to be deleted using the blogID
    deleteTeacher = Teacher.objects.get(id=teacherID)
    # check to see if the user that is making this request is the author of the blog.
    # current_user is a variable provided by the 'flask_login' library.
    if current_user == deleteTeacher.author:
        # delete the blog using the delete() method from Mongoengine
        deleteTeacher.delete()
        # send a message to the user that the blog was deleted.
        flash('The Teacher was deleted.')
    else:
        # if the user is not the author tell them they were denied.
        flash("You can't delete a teacher you don't own.")
    # Retrieve all of the remaining blogs so that they can be listed.
    teachers = Teacher.objects()  
    # Send the user to the list of remaining blogs.
    return render_template('teachers.html',teachers=teachers)

# This route actually does two things depending on the state of the if statement 
# 'if form.validate_on_submit()'. When the route is first called, the form has not 
# been submitted yet so the if statement is False and the route renders the form.
# If the user has filled out and succesfully submited the form then the if statement
# is True and this route creates the new blog based on what the user put in the form.
# Because this route includes a form that both gets and blogs data it needs the 'methods'
# in the route decorator.
@app.route('/teacher/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def teacherNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = TeacherForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        for teacher in Teacher.objects():
            if teacher.teacher_fname==form.teacher_fname.data and teacher.teacher_fname==form.teacher_fname.data:
                flash("This teacher already exists. You can't add them again.")
                return render_template('teacherform.html',form=form)

        # This stores all the values that the user entered into the new blog form. 
        # Blog() is a mongoengine method for creating a new blog. 'newBlog' is the variable 
        # that stores the object that is the result of the Blog() method.  
        
        newTeacher = Teacher(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            teacher_fname = form.teacher_fname.data,
            teacher_lname = form.teacher_lname.data,
            teacher_email = form.teacher_email.data,
            teacher_pronouns = form.teacher_pronouns.data,
            teacher_room = form.teacher_room.data,
            subject_taught = form.subject_taught.data,
            teacher_academy = form.teacher_academy.data,
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
            
        )
        # This is a method that saves the data to the mongoDB database.
        newTeacher.save()

        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('teacher',teacherID=newTeacher.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('teacherform.html',form=form)


# This route enables a user to edit a blog.  This functions very similar to creating a new 
# blog except you don't give the user a blank form.  You have to present the user with a form
# that includes all the values of the original blog. Read and understand the new blog route 
# before this one. 
@app.route('/teacher/edit/<teacherID>', methods=['GET', 'POST'])
@login_required
def teacherEdit(teacherID):
    editTeacher = Teacher.objects.get(id=teacherID)
    # if the user that requested to edit this blog is not the author then deny them and
    # send them back to the blog. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editTeacher.author:
        flash("You can't edit a teacher you don't own.")
        return redirect(url_for('teacher',teacherID=teacherID))
    # get the form object
    form = TeacherForm()
    # If the user has submitted the form then update the blog.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editTeacher.update(
            teacher_fname = form.teacher_fname.data,
            teacher_lname = form.teacher_lname.data,
            teacher_email = form.teacher_email.data,
            teacher_pronouns = form.teacher_pronouns.data,
            teacher_room = form.teacher_room.data,
            subject_taught = form.subject_taught.data,
            teacher_academy = form.teacher_academy.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow
        )
        # After updating the document, send the user to the updated blog using a redirect.
        return redirect(url_for('teacher',teacherID=teacherID))

    # if the form has NOT been submitted then take the data from the editBlog object
    # and place it in the form object so it will be displayed to the user on the template.
    form.teacher_lname.data = editTeacher.teacher_lname
    form.teacher_email.data = editTeacher.teacher_email
    form.teacher_pronouns.data = editTeacher.teacher_pronouns
    form.teacher_room.data = editTeacher.teacher_room
    form.subject_taught.data = editTeacher.subject_taught
    form.teacher_academy.data = editTeacher.teacher_academy



    # Send the user to the blog form that is now filled out with the current information
    # from the form.
    return render_template('teacherform.html',form=form)


# Teacher Review Part
# @app.route('/teacher/<teacherID>')
# def reviewList(teacherID):
#     reviews = [Review.objects.get(id=teacherID)]
#     for review in reviews:
#         average_five_star_rating += review.form.five_star_rating.data
#     average_five_star_rating /= len(reviews)
#     average_five_star_rating.save()
#     return render_template('teacher.html',reviews=reviews)
    

@app.route('/review/new/<teacherID>', methods=['GET', 'POST'])
@login_required
def reviewNew(teacherID):
    teacher = Teacher.objects.get(id=teacherID)
    form = TeacherReviewForm()
    if form.validate_on_submit():
        newReview = Review(
            author = current_user.id,
            teacher = teacherID,
            five_star_rating = form.five_star_rating.data,
            stress_rating = form.stress_rating.data,
            difficulty_rating = form.difficulty_rating.data,
            listen_to_music = form.listen_to_music.data,
            breaks_during_class = form.breaks_during_class.data,
            games_in_lesson = form.games_in_lesson.data

        )
        newReview.save()
        return redirect(url_for('teacher',teacherID=teacherID))
    return render_template('reviewform.html',form=form,teacher=teacher)

@app.route('/review/edit/<reviewID>', methods=['GET', 'POST'])
@login_required
def reviewEdit(reviewID):
    editReview = Review.objects.get(id=reviewID)
    if current_user != editReview.author:
        flash("You can't edit a review you didn't write.")
        return redirect(url_for('teacher',teacherID=editReview.teacher.id))
    teacher = Teacher.objects.get(id=editReview.teacher.id)
    form = TeacherReviewForm()
    if form.validate_on_submit():
        editReview.update(
            five_star_rating = form.five_star_rating.data,
            stress_rating = form.stress_rating.data,
            difficulty_rating = form.difficulty_rating.data,
            listen_to_music = form.listen_to_music.data,
            breaks_during_class = form.breaks_during_class.data,
            games_in_lesson = form.games_in_lesson.data,
            modifydate = dt.datetime.utcnow
        )

        return redirect(url_for('teacher',teacherID=editReview.teacher.id))

    form.five_star_rating.data = editReview.five_star_rating
    form.stress_rating.data = editReview.stress_rating
    form.difficulty_rating.data = editReview.difficulty_rating
    form.listen_to_music.data = editReview.listen_to_music
    form.breaks_during_class.data = editReview.breaks_during_class
    form.games_in_lesson.data = editReview.games_in_lesson


    return render_template('reviewform.html',form=form,teacher=teacher)   

@app.route('/review/delete/<reviewID>')
@login_required
def reviewDelete(reviewID): 
    deleteReview = Review.objects.get(id=reviewID)
    deleteReview.delete()
    flash('The reviews was deleted.')
    return redirect(url_for('teacher',teacherID=deleteReview.teacher.id)) 

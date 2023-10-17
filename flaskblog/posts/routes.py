from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Posts
from flaskblog.posts.forms import Postform
posts=Blueprint('posts',__name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
   formm=Postform()
   if formm.validate_on_submit():
   
        post=Posts(title=formm.title.data,content=formm.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("posted",'success')
        return redirect(url_for('main.home'))
   return render_template('create_post.html',title='create post',form=formm,legend="New post")
   
   
@posts.route("/post/int:<Posts_id>")
def post(Posts_id):
   post=Posts.query.get_or_404(Posts_id)
   return render_template('post.html',title=post.title,post=post)
   

  

@posts.route("/post/int:<Posts_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(Posts_id):
   post=Posts.query.get_or_404(Posts_id)
   if post.author!=current_user:
      abort(403)
   formm=Postform()
   if formm.validate_on_submit():
     post.title=formm.title.data
     post.content=formm.content.data
     db.session.commit()
     flash("updated","success")
     return redirect(url_for('posts.post',Posts_id=post.id))
   elif request.method=='GET':
    formm.title.data=post.title
    formm.content.data=post.content
   return render_template('create_post.html',title='upadte post',form=formm,legend="update post")

@posts.route("/post/int:<Posts_id>/delete", methods=[ 'POST'])
@login_required
def delete_post(Posts_id):
 post=Posts.query.get_or_404(Posts_id)
 if post.author!=current_user:
      abort(403)
 db.session.delete(post)
 db.session.commit()
 flash('your post has been deleted','success')
 return redirect(url_for('main.home'))




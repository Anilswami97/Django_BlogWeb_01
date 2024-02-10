from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from .models import Blog, BlogComment
from django.contrib import messages
from Blog.templatetags import extras

# Create your views here.

def blogHome(request):
    blog = Blog.objects.all()
    return render(request, "blog/blogHome.html", {"blogs": blog})

def blogPost(request, slug):
    post = Blog.objects.filter(sno = slug).first()
    comments = BlogComment.objects.filter(post = post, parent=None)
    replies = BlogComment.objects.filter(post = post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply];
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post':post, 'comments':comments, 'replyDict':replyDict, 'user':request.user}
    return render(request, "blog/blogPost.html", context)


def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSo = request.POST.get("postSno")
        replySno = request.POST.get("replySno")
        post = Blog.objects.get(sno = postSo)

        if replySno == "":
            blogcomment =  BlogComment(Comment = comment, user = user, post = post)
        
        else:
            parent = BlogComment.objects.get(sno = replySno)
            blogcomment =  BlogComment(Comment = comment, user = user, post = post, parent=parent)

        blogcomment.save()
        messages.success(request, "Your reply has been posted successfully!")
    return redirect(f"/blog/{post.sno}/")


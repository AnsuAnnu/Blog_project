from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.template.defaultfilters import title
from django.urls import reverse_lazy

from .models import Post,Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


# posts=[
# 	{
# 		'author':'Shem Franz',
# 		'title':'Blog Post 1',
# 		'content':'this is my first common post',
# 		'date_posted':'2nd February, 2022',
# 	},
# 	{
# 		'author':'Shem Franz',
# 		'title':'Blog Post 1',
# 		'content':'this is my first common post',
# 		'date_posted':'2nd February, 2022',
# 	}
#
# ]
# def Home(request):
# 	context=	{
# 		'posts':Post.objects.all()
#
# 	}
#
# 	return render(request,'blog/home.html',context)
def About(request):


	return render(request,'blog/about.html',{'title':'About Page'})

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]
    paginate_by = 4
    def get_queryset(self):
        query=self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ). order_by('date_posted')
        return Post.objects.all().order_by('date_posted')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'





class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('blog-detail',kwargs={'pk':self.object.pk})



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'users/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = post
            comment.user = request.user
            comment.save()
            return redirect("blog-detail", pk=post.id)
    else:
        form = CommentForm()
    return render(request, "blog/add_comment.html", {"form": form, "post": post})


@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)  # Ensure the user owns the comment
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog-detail", pk=comment.blog.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, "blog/update_comment.html", {"form": form, "comment": comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_superuser:  # Only owner or admin can delete
        comment.delete()
    return redirect("blog-detail", pk=comment.blog.id)
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, View
from django.utils import timezone
from django.utils.decorators import method_decorator

from .forms import NewTopicForm, EditTopicForm, PostForm
from .models import Board, Post, Topic
# 
# 
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
# from django.db.models import Count
# from django.views.generic import View
# from .forms import NewTopicForm, EditTopicForm, PostForm
# from .models import Board, Topic, Post

def home(request):
    boards = Board.objects.all()
    return render(request, 'boards/home.html', {'boards': boards})

def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'boards/topics.html', {'board': board, 'topics': topics})

@login_required
def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('boards:topic_posts', board_id=board.pk, topic_id=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})

def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    topic.views += 1
    topic.save()    
    return render(request, 'boards/topic_posts.html', {'topic': topic})

@login_required
def edit_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    if request.method == 'POST':
        form = EditTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.save()
            return redirect('boards:reply_topic', board_id=board_id, topic_id=topic_id)
    else:
        form = EditTopicForm()
    return render(request, 'boards/edit_topic.html', {'topic': topic, 'form': form})

@login_required
def reply_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('boards:topic_posts', board_id=board_id, topic_id=topic_id)
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})

class NewPostView(View):
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boards:post_list')
        return render(request, 'boards/new_post.html', {'form': form})

    def get(self, request):
        form = PostForm()
        return render(request, 'boards/new_post.html', {'form': form})
    
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)    

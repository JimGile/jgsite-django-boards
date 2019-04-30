from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTopicForm
from .models import Board, Topic, Post

def home(request):
    boards = Board.objects.all()
    return render(request, 'boards/home.html', {'boards': boards})

def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    return render(request, 'boards/topics.html', {'board': board})

def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('boards:board_topics', board_id=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    return render(request, 'my_notes_app/index.html')


def check_topic_owner(user, topic):
    if topic.owner != user:
        raise Http404


@login_required
def topics(request):
    topics_ = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics_}
    return render(request, 'my_notes_app/topics.html', context)


@login_required
def topic(request, topic_id):
    topic_ = Topic.objects.get(id=topic_id)
    check_topic_owner(request.user, topic_)
    entries = topic_.entry_set.order_by('-date_added')
    context = {'topic': topic_, 'entries': entries}
    return render(request, 'my_notes_app/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic_ = form.save(commit=False)
            new_topic_.owner = request.user
            new_topic_.save()
            return HttpResponseRedirect(reverse('my_notes_app:topics'))
        else:
            print("\033[31m[ERROR]\033[0m Not valid form data")

    context = {'form': form}
    return render(request, 'my_notes_app/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request.user, topic)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_ = form.save(commit=False)
            new_entry_.topic = topic
            new_entry_.save()
            return HttpResponseRedirect(reverse('my_notes_app:topic', args=[topic_id]))
        else:
            print("\033[31m[ERROR]\033[0m Not valid form data")
    context = {'topic': topic, 'form': form}
    return render(request, 'my_notes_app/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request.user, topic)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_notes_app:topic', args=[topic.id]))
        else:
            print("\033[31m[ERROR]\033[0m Not valid form data")
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'my_notes_app/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    print(
        "\033[32m[INFO]\033[0m Received a delete entry request, id = " + str(entry_id))
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    entry.delete()
    return HttpResponseRedirect(reverse('my_notes_app:topic', args=[topic.id]))


@login_required
def delete_topic(request, topic_id):
    print(
        "\033[32m[INFO]\033[0m Received a delete topic request, id = " + str(topic_id))
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request.user, topic)
    topic.delete()
    return HttpResponseRedirect(reverse('my_notes_app:topics'))


@login_required
def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request.user, topic)

    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_notes_app:topic', args=[topic_id]))
        else:
            print("\033[31m[ERROR]\033[0m Not valid form data")
    context = {'topic': topic, 'form': form}
    return render(request, 'my_notes_app/edit_topic.html', context)

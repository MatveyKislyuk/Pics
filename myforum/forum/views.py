# forum/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Image, Tag
from .forms import ImageForm, TagForm, AddTagForm
from django.http import JsonResponse

def index(request):
    return render(request,'forum/index.html')
def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = ImageForm()
    return render(request, 'forum/add_image.html', {'form': form})

def image_list(request):
    all_tags = Tag.objects.all()
    selected_tag1 = request.GET.get('tag1', '')
    selected_tag2 = request.GET.get('tag2', '')

    if selected_tag1 and selected_tag2:
        images = Image.objects.filter(tags__name=selected_tag1).filter(tags__name=selected_tag2)
    elif selected_tag1:
        images = Image.objects.filter(tags__name=selected_tag1)
    elif selected_tag2:
        images = Image.objects.filter(tags__name=selected_tag2)
    else:
        images = Image.objects.all()

    return render(request, 'forum/image_list.html', {'images': images, 'all_tags': all_tags, 'selected_tags': [selected_tag1, selected_tag2]})

def delete_image(request):
    images = Image.objects.all()
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        if image_id:
            image = Image.objects.get(pk=image_id)
            image.delete()
            return redirect('image_list')
    return render(request, 'forum/delete_image.html', {'images': images})


def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = TagForm()
    return render(request, 'forum/add_tag.html', {'form': form})


def add_tag_to_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(Image, id=image_id)
        new_tag_name = request.POST.get('new_tag', '')
        remove_tag_name = request.POST.get('remove_tag', '')

        if new_tag_name:
            tag, created = Tag.objects.get_or_create(name=new_tag_name)
            image.tags.add(tag)
            return JsonResponse({'success': True, 'tag_name': tag.name})

        elif remove_tag_name:
            try:
                tag_to_remove = Tag.objects.get(name=remove_tag_name)
                image.tags.remove(tag_to_remove)
                return JsonResponse({'success': True})
            except Tag.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Tag not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def delete_tag(request):
    if request.method == 'POST':
        tag_to_delete = request.POST.get('tagToDelete')

        if tag_to_delete:
            try:
                tag = Tag.objects.get(name=tag_to_delete)
                tag.delete()
                # Успешное удаление
                return redirect('delete_tag')  # Перенаправление на страницу после удаления
            except Tag.DoesNotExist:
                # Тег не найден
                pass

    # Получение списка всех тегов
    all_tags = Tag.objects.all()

    context = {'all_tags': all_tags}
    return render(request, 'forum/delete_tag.html', context)
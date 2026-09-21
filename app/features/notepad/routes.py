from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from splent_framework.utils.form_helpers import form_error, form_success

from app.features.notepad import notepad_bp
from app.features.notepad.forms import NotepadForm
from app.features.notepad.services import NotepadService

notepad_service = NotepadService()



@notepad_bp.route('/notepad', methods=['GET'])
@login_required
def index():
    form = NotepadForm()
    notepads = notepad_service.get_all_by_user(current_user.id)
    return render_template('notepad/index.html', notepads=notepads, form=form)



@notepad_bp.route('/notepad/create', methods=['GET', 'POST'])
@login_required
def create_notepad():
    form = NotepadForm()
    if form.validate_on_submit():
        result = notepad_service.create(
            title=form.title.data,
            body=form.body.data,
            user_id=current_user.id
        )
        return form_success('notepad.index', 'Notepad created successfully!')
    return form_error('notepad/create.html', form)



@notepad_bp.route('/notepad/<int:notepad_id>', methods=['GET'])
@login_required
def get_notepad(notepad_id):
    notepad = notepad_service.get_or_404(notepad_id)
    return render_template('notepad/show.html', notepad=notepad)


@notepad_bp.route('/notepad/edit/<int:notepad_id>', methods=['GET', 'POST'])
@login_required
def edit_notepad(notepad_id):
    notepad = notepad_service.get_or_404(notepad_id)
    form = NotepadForm(obj=notepad)
    if form.validate_on_submit():
        result = notepad_service.update(
            notepad_id,
            title=form.title.data,
            body=form.body.data
        )
        return form_success('notepad.index', 'Notepad updated successfully!')
    return form_error('notepad/edit.html', form, notepad=notepad)


@notepad_bp.route('/notepad/delete/<int:notepad_id>', methods=['POST'])
@login_required
def delete_notepad(notepad_id):
    notepad_service.delete(notepad_id)
    return form_success('notepad.index', 'Notepad deleted successfully!')
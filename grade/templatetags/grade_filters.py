from django import template

register = template.Library()

@register.filter
def get_grade(grades, exam_type):
    for grade in grades:
        if grade.exam_type == exam_type:
            return grade.grade
    return ''

@register.filter
def get_form_grade(forms, exam_type):
    for form in forms:
        if form.initial.get('exam_type') == exam_type:
            return form['grade']
    return ''

@register.filter
def get_form_notes(forms, exam_type):
    for form in forms:
        if form.initial.get('exam_type') == exam_type:
            return form['notes']
    return ''


@register.filter
def get_grade_for_exam_type(grades, exam_type):
    return grades.filter(exam_type=exam_type).first()

@register.filter
def find_form(forms, student_id):
    return [form for form in forms if form.initial.get('student') == student_id]

@register.filter
def find_exam_type(forms, exam_type):
    for form in forms:
        if form.initial.get('exam_type') == exam_type:
            return form
    return None
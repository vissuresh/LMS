from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from application.models import Section, Book
from application.schemas import SectionSchema, BookSchema
from application.validation import check_librarian
from application import db
from sqlalchemy.exc import IntegrityError
import json

section_bp = Blueprint(
    'sections',
    __name__
)


@section_bp.get('/all')
@jwt_required()
def get_all_sections():    
    
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    search_by = request.args.get('search_by', 'section_name')
    search_query = request.args.get('query')

    section_query = Section.query

    if search_query not in [None, '']:
        if search_by == 'section_name':
            section_query = section_query.filter(Section.name.ilike(f"%{search_query}%"))
        elif search_by == 'section_id':
            section_query = section_query.filter(Section.id == search_query)

    section_query = section_query.order_by(Section.date_created.desc())

    if page is None:
        sections = section_query.all()
        result = SectionSchema().dump(sections, many=True)
        return jsonify({"sections": result}), 200
    

    try:
        sections = section_query.paginate(
            page = page,
            per_page = per_page
        )
    except:
        return jsonify({
            "error": "page or per-page out of bounds"
        }), 400

    result = SectionSchema().dump(sections, many=True)    

    return jsonify({
        "sections" : result,

        "pagination": {
            "page": sections.page,
            "per_page": sections.per_page,
            "total": sections.total,
            "pages": sections.pages
        }
    }), 200



@section_bp.get('/<int:section_id>')
@jwt_required()
def get_section(section_id):
    section = Section.query.get_or_404(section_id)
    return (SectionSchema().dump(section), 200)


@section_bp.get('/<int:section_id>/books')
@jwt_required()
def get_section_books(section_id):
    section = Section.query.get_or_404(section_id)
    section_data =  SectionSchema().dump(section)

    popular_books = section.books.order_by(db.func.avg(Book.feedback.any().rating).desc()).limit(10).all()
    popular_books_data = BookSchema().dump(popular_books, many=True)


    return jsonify({"section":section_data, "popular_books": popular_books_data}), 200



@section_bp.post('/')
@check_librarian
def create_section():
    data = json.loads(request.form.get('data'))
    section_name = data.get('name').strip().lower()
    section_desc = data.get('desc')
    if not section_name or section_desc == '':
        return jsonify({"message": "Incomplete form data"}), 400

    data['name'] = section_name 
    new_section = SectionSchema().load(data, session=db.session)
    try:
        new_section.save()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred"}), 400
    
    return jsonify({"message": "success"}), 201


@section_bp.patch('/<int:section_id>')
@check_librarian
def update_section(section_id):
    section = Section.query.get_or_404(section_id)
    data = json.loads(request.form.get('data'))
    
    SectionSchema().load(data, instance=section, session=db.session, partial=True)

    try:
        section.save()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred"}), 400
    
    return jsonify({"message":"success"}), 200



@section_bp.delete('/<int:section_id>')
@check_librarian
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)

    try:
        section.delete()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred"}), 400

    return jsonify({"message":"success"}), 200
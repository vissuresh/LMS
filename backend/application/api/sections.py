from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from application.models import Section, Book
from application.schemas import SectionSchema, BookSchema
from application.validation import check_librarian
from application import db

section_bp = Blueprint(
    'sections',
    __name__
)


@section_bp.get('/all')
@jwt_required()
def get_all_sections():    
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    try:
        sections = Section.query.paginate(
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
    section_data = SectionSchema().dump(section)


    books = Book.query.filter_by(section_id=section_id).all()
    books_data = BookSchema().dump(books, many=True)

    return jsonify({"section":section_data, "books" : books_data}), 200



@section_bp.post('/')
@check_librarian
def create_section():
    new_section = SectionSchema().load(request.json, session=db.session)
    new_section.save()
    return jsonify({"message": "success"}), 201


@section_bp.patch('/<int:section_id>')
@check_librarian
def update_section(section_id):
    section = Section.query.get_or_404(section_id)
    SectionSchema().load(request.json, instance=section, session=db.session, partial=True)
    section.save()
    
    return jsonify({"message":"success"}), 200



@section_bp.delete('/<int:section_id>')
@check_librarian
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)
    section.delete()

    return jsonify({"message":"success"}), 200
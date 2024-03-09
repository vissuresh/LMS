from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Section
from schemas import SectionSchema

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
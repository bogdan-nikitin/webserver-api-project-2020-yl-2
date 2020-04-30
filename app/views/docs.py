from flask import Blueprint, render_template
from modules.constants import ROOT_DIR

blueprint = Blueprint('docs', __name__,
                      template_folder=ROOT_DIR + '/app/docs/cached')


@blueprint.route('/docs/v1/api_docs')
def api_docs():
    return render_template('api_docs.jinja2')

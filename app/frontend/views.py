from flask import (Blueprint, render_template)

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def media_stats():
    return render_template('media-stats.html')

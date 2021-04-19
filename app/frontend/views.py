from flask import (Blueprint, render_template)
from typing import Any

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def media_stats() -> Any:
    return render_template('media-stats.html')

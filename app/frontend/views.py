from flask import (Blueprint, render_template)
from typing import Any
import datetime

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def media_stats() -> Any:
    today = datetime.datetime.today()
    month = today.month
    if int(month) < 10:
        month = f'0{month}'
    current_month = f'{today.year}-{month}'
    export_url = '/static/export'
    charts_url = f'{export_url}/{current_month}_'

    return render_template('media-stats.html', charts_url=charts_url)

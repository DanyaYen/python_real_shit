from flask import Flask, render_template, request, jsonify, send_from_directory
from report_gen.celery_worker import make_report
from celery.result import AsyncResult
from report_gen.celery_worker import celery

app = Flask(__name__)

@app.route('/task-status/<task_id>')
def task_status(task_id):
    task = AsyncResult(task_id, app=celery)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'В очереди...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'status': task.info.get('status', '')}
        if 'filename' in task.info:
            response['result'] = f"/reports/{task.info['filename']}"
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)

@app.route('/')
def index():
    """Отображает главную страницу с формой."""
    return render_template('index.html')

@app.route('/generate-report', methods=['POST'])
def generate_report():
    user_data = request.form.get('user_data')
    task = make_report.delay(user_data)
    return jsonify({'task_id': task.id}), 202

@app.route('/reports/<filename>')
def download_report(filename):
    return send_from_directory('reports', filename)

if __name__ == '__main__':
    app.run(debug=True)
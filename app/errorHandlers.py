from flask import jsonify, render_template, current_app

def handle_bad_request(error):
    current_app.logger.error(f"An error occurred: {str(error)}")
    return jsonify({'error': 'Bad Request'}), 400

def not_found_error(error):
    current_app.logger.error(f"An error occurred: {str(error)}")
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

def handle_internal_server_error(error):
    current_app.logger.error(f"An error occurred: {str(error)}")
    return render_template('error.html', error_code=500, error_message="Problem with server or with your token for Typless connection."), 500

def handle_generic_exception(error):
    current_app.logger.error(f"An error occurred: {str(error)}")
    return jsonify({'error': str(error)}), 500
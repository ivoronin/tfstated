# pylint: disable=C0114
import errno
import os
import os.path
import sys
import tempfile
from flask import Blueprint, abort, request, send_file
from flask import current_app as app
from flask_httpauth import HTTPBasicAuth

bp = Blueprint("state", __name__) # pylint: disable=C0103
auth = HTTPBasicAuth() # pylint: disable=C0103

@auth.verify_password
def verify_password(username, password):
    """Called by flask_httpauth"""
    if username == app.config['USERNAME']:
        return password == app.config['PASSWORD']
    return False

@bp.before_app_first_request
def init(): # pylint: disable=C0116
    try:
        os.mkdir(app.config['DATA_DIR'])
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise sys.exc_info()
    try:
        os.remove(app.config['LOCK_FILE'])
    except OSError as exc:
        if exc.errno != errno.ENOENT:
            raise sys.exc_info()

@bp.route('/state', methods=['GET'])
@auth.login_required
def state_fetch(): # pylint: disable=C0116
    try:
        return send_file(app.config['STATE_FILE'])
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            return ('Not Found\n', 404)
        bp.logger.error('Error sending %s: %s', app.config['STATE_FILE'], exc) # pylint: disable=E1101
        abort(500)

@bp.route('/state', methods=['POST'])
@auth.login_required
def state_update(): # pylint: disable=C0116
    try:
        tmp_dir = os.path.dirname(app.config['STATE_FILE'])
        tmp_prefix = "%s." % os.path.basename(app.config['STATE_FILE'])
        (tmp_fd, tmp_name) = tempfile.mkstemp(prefix=tmp_prefix, dir=tmp_dir)
        os.write(tmp_fd, request.data)
        os.fsync(tmp_fd)
        os.close(tmp_fd)
        os.rename(tmp_name, app.config['STATE_FILE'])
    except OSError as exc:
        bp.logger.error('Error saving data to state file %s: %s', app.config['STATE_FILE'], exc) # pylint: disable=E1101
        abort(500)

    return ('Created\n', 200)

@bp.route('/state', methods=['DELETE'])
@auth.login_required
def state_purge(): # pylint: disable=C0116
    try:
        os.remove(app.config['STATE_FILE'])
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            return('Not Found\n', 404)
        bp.logger.error('Error deleting %s: %s', app.config['STATE_FILE'], exc) # pylint: disable=E1101
        abort(500)

    return ('Deleted\n', 200)

@bp.route('/state', methods=['LOCK'])
@auth.login_required
def state_lock(): # pylint: disable=C0116
    try:
        lock_fd = os.open(app.config['LOCK_FILE'], os.O_WRONLY|os.O_CREAT|os.O_EXCL)
        os.write(lock_fd, request.data)
        os.close(lock_fd)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            return('Conflict\n', 409)
        bp.logger.error('Error locking file %s: %s', app.config['LOCK_FILE'], exc) # pylint: disable=E1101
        abort(500)

    return ('Locked\n', 200)

@bp.route('/state', methods=['UNLOCK'])
@auth.login_required
def state_unlock(): # pylint: disable=C0116
    try:
        os.remove(app.config['LOCK_FILE'])
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            return('Not Found\n', 404)
        bp.logger.error('Error unlocking file %s: %s', app.config['LOCK_FILE'], exc) # pylint: disable=E1101
        abort(500)

    return ('Unlocked\n', 200)

# pylint: disable=C0114
import os
import os.path
from flask import Flask
from tfstated import state

def create_app(): # pylint: disable=C0116
    app = Flask(__name__)

    username = os.getenv('TFSTATED_USERNAME', 'terraform')
    password = os.getenv('TFSTATED_PASSWORD', 'terraform')
    data_dir = os.getenv('TFSTATED_DATA_DIR', '/tfstate')

    app.config.from_mapping(
        USERNAME=username,
        PASSWORD=password,
        DATA_DIR=data_dir,
        STATE_FILE=os.path.join(data_dir, 'terraform.tfstate'),
        LOCK_FILE=os.path.join(data_dir, 'terraform.lock')
    )

    app.register_blueprint(state.bp)
    return app

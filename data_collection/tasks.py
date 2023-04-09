import os

from celery import shared_task
from celery_progress.backend import ProgressRecorder

from config.settings import ENV
from config.settings import S3_SCRATCH_DIR
from config.settings import S3_STUDIES_PATH
from . import utils


@shared_task(bind=True)
def fetch_fastq(self, run_id):
    """
    Celery task to fetch fastq files from SRA.
    """
    print(f'Executing fetch_fastq function.')
    # Create a progress recorder.
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(5, 100, description=f'Process started.')

    # Create the output directory
    output_dir = os.path.join(S3_STUDIES_PATH, run_id)
    utils.create_dir(output_dir)

    # Fetch the fastq file(s)
    command = f'fasterq-dump {run_id} -O {output_dir} -t {S3_SCRATCH_DIR}'
    print(command)
    return_code = utils.run_conda_command(cmd=command, env=ENV)

    if return_code != 0:
        error_desc = f'Error in downloading {run_id}. Return code: {return_code}.'
        print(error_desc)
        utils.create_txt(file_path=os.path.join(output_dir, 'error.txt'), contents=error_desc)
        progress_recorder.set_progress(100, 100, description=error_desc)
        return

    print('Creating complete.txt')
    utils.create_txt(file_path=os.path.join(output_dir, 'complete.txt'))
    progress_recorder.set_progress(100, 100, description=f'Process completed.')

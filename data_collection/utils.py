import os
import shutil
import subprocess


def run_conda_command(cmd, env):
    """
    Run the shell command in the given conda environment.
    """
    cmd = f'conda run --no-capture-output -n {env} ' + cmd
    process = subprocess.run(cmd, shell=True)

    return process.returncode


def create_dir(directory):
    """
    Create a new directory. Overwrite if it already exists.
    """
    print(f'Creating dir: {directory}')
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def create_txt(file_path, contents=''):
    """
    Create an empty text file.
    """
    with open(file_path, 'w') as f:
        if contents:
            f.write(contents)
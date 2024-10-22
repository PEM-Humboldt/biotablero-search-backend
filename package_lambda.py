#!/usr/bin/env python3
import os
import shutil
import subprocess
from typing import Set


def get_dependencies() -> Set[str]:
    """Get all required dependencies from requirements.txt"""
    with open('requirements.txt', 'r') as f:
        return {line.strip() for line in f if line.strip() and not line.startswith('#')}



def create_lambda_layer(layer_name, requirements_file):
    """Creates a Lambda Layer package based on a requirements file"""
    layer_dir = f'{layer_name}/python'

    if os.path.exists(layer_name):
        shutil.rmtree(layer_name)
    os.makedirs(layer_dir)

    subprocess.check_call([
        'pip', 'install',
        '-r', requirements_file,
        '-t', layer_dir,
        '--no-cache-dir'
    ])

    shutil.make_archive(layer_name, 'zip', layer_name)
    shutil.rmtree(layer_name)
    print(f'Layer package created: {layer_name}.zip')


def create_lambda_package():
    """Create Lambda deployment package with application code only"""
    # Create temporary directory for the code
    if os.path.exists('lambda_package'):
        shutil.rmtree('lambda_package')
    os.makedirs('lambda_package')

    # Copy application code to the package
    shutil.copytree('app', 'lambda_package/app')

    # Create the ZIP file of the Lambda code
    shutil.make_archive('lambda_package', 'zip', 'lambda_package')

    # Clear the temporary directory
    shutil.rmtree('lambda_package')

    print("Lambda code package created: lambda_package.zip")


if __name__ == "__main__":
    # Lightweight layer for critical dependencies
    create_lambda_layer('lambda_layer_light', 'requirements-light.txt')

    # Layer heavy part 1 for large dependencies
    create_lambda_layer('lambda_layer_heavy_part1', 'requirements-heavy-part1.txt')

    # Layer heavy part 2 for other large dependencies
    create_lambda_layer('lambda_layer_heavy_part2', 'requirements-heavy-part2.txt')

    # Layer heavy part 3 for other large dependencies
    create_lambda_layer('lambda_layer_heavy_part3', 'requirements-heavy-part3.txt')

    # Layer heavy part 4 for other large dependencies
    create_lambda_layer('lambda_layer_heavy_part4', 'requirements-heavy-part4.txt')

    # Create Lambda deployment package with application code
    create_lambda_package()

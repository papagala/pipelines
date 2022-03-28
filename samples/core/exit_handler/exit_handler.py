#!/usr/bin/env python3
# Copyright 2019-2021 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kfp.deprecated import compiler
from kfp.deprecated import components
from kfp.deprecated import dsl
from kfp.deprecated.components import Fin
from kfp.deprecated.components import InputPath
from kfp.deprecated.components import load_component_from_url

gcs_download_op = load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/961b17fa6844e1d79e5d3686bb557d830d7b5a95/components/google-cloud/storage/download_blob/component.yaml'
)


@components.create_component_from_func
def print_file(file_path: InputPath('Any')):
    """Print a file."""
    with open(file_path) as f:
        print(f.read())


@components.create_component_from_func
def echo_msg(msg: str):
    """Echo a message by parameter."""
    print(msg)


@components.create_component_from_func
def exit_op(msg: str):
    """Echo a message by parameter."""
    print(msg)


@dsl.pipeline(
    name='exit-handler',
    description='Downloads a message and prints it. The exit handler will run after the pipeline finishes (successfully or not).'
)
def pipeline_exit_handler(url: str = 'gs://ml-pipeline/shakespeare1.txt'):
    """A sample pipeline showing exit handler."""

    exit_task = exit_op('exit!')

    with dsl.ExitHandler(exit_task):
        download_task = gcs_download_op(url)
        echo_task = print_file(download_task.output)


ir_file = __file__.replace('.py', '.yaml')

if __name__ == '__main__':
    import datetime

    from google.cloud import aiplatform  # import aiplatform[pipelines]
    compiler.Compiler().compile(
        pipeline_func=pipeline_exit_handler, package_path=ir_file)

    from kfp.deprecated import Client

    client = Client(
        host="15c9762d0a39d30a-dot-us-central1.pipelines.googleusercontent.com")
    client.create_run_from_pipeline_func(pipeline_exit_handler, arguments={})
    # aiplatform.PipelineJob(
    #     template_path=ir_file,
    #     pipeline_root='gs://cjmccarthy-kfp-default-bucket',
    #     display_name=str(datetime.datetime.now())).submit()

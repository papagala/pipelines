# Copyright 2022 The Kubeflow Authors
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

from typing import Dict
import unittest

import kfp.deprecated as kfp
from kfp.samples.test.utils import KfpTask
from kfp.samples.test.utils import run_pipeline_func
from kfp.samples.test.utils import TestCase
import kfp_server_api

from .pipeline_with_named_tuples import pipeline_with_named_tuples


def verify(t: unittest.TestCase, run: kfp_server_api.ApiRun,
           tasks: Dict[str, KfpTask], **kwargs):
    t.assertEqual(run.status, 'Succeeded')


if __name__ == '__main__':
    run_pipeline_func([
        TestCase(
            pipeline_func=pipeline_with_named_tuples,
            verify_func=verify,
            mode=kfp.dsl.PipelineExecutionMode.V2_ENGINE,
        ),
    ])

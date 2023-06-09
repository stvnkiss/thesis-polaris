import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import suite as test

subdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'manifests'))
decision_yamls = [f'{subdir}/workload_test.yaml', f'{subdir}/slo-mapping_test.yaml']
horizontal_yamls = [f'{subdir}/workload_reference.yaml', f'{subdir}/slo-mapping_reference.yaml']

decision_l = test.SloTest('Threshold', 'test-pause-deployment', decision_yamls)
horizontal = test.SloTest('Horizontal', 'reference-pause-deployment', horizontal_yamls)

data = [73, 74, 73, 74, 73, 74, 73, 74, 73, 74, 73, 74, 73, 74, 73, 74, 73, 74, 73, 74, 73, 74, 72]

test.run_test(decision_l, horizontal, data)

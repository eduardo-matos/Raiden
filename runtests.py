#!/usr/bin/env python

import os
import sys
import pytest


args = ['-rsxX', '--tb=native', '--cov', 'raiden', '--cov-config', '.coveragerc',
        '--cov-report', 'html', '--cov-report', 'term-missing'] + sys.argv[1:]

sys.exit(pytest.main(args + ['tests/']))

# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork
"""Here we watch the ``PYTHON_UPWORK_BASE_URL``
variable and if it is defined, use it as ``BASE_URL``.

"""

import os

BASE_URL = os.environ.get('PYTHON_UPWORK_BASE_URL',
                          'https://www.upwork.com')

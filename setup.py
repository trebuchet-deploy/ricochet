# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

setup(name="TrebuchetRicochet",
      version="0.2",
      packages=find_packages(),
      install_requires=['Flask>=0.8', 'redis>=2.4.9'],

      author="Ryan Lane",
      author_email="ryan@ryandlane.com",
      description="A web interface to trebuchet.",
      license="apache2",
      url="https://github.com/trebuchet-deploy/ricochet",

      entry_points={
          'console_scripts': [
              'ricochet = ricochet.runserver:main',
          ],
      })

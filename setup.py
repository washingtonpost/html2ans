import sys
import os
from codecs import open
from setuptools import setup, find_packages
from setuptools.command.install import install


THIS_FILE_DIR = os.path.dirname(__file__)

try:
    # pip 9
    from pip.req import parse_requirements
    from pip.download import PipSession
except ImportError:
    # pip 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession


def load_reqs(fn):
    reqs = []
    reqs_extras = {}
    parsed_reqs = parse_requirements(fn, session=PipSession())

    for req in parsed_reqs:
        markers = req.markers
        if markers:
            reqs_extras[":" + str(markers)] = str(req.req)
        else:
            reqs.append(str(req.req))

    return reqs, reqs_extras


NEEDS_DOCS = 'build_sphinx' in sys.argv
NEEDS_PYTEST = {'pytest', 'test', 'ptr'}.intersection(sys.argv)

DOCS_REQUIRE, DOCS_EXTRAS = load_reqs('reqs/doc.txt') if NEEDS_DOCS else ([], {})
INSTALL_REQUIRES, EXTRAS_REQUIRE = load_reqs('reqs/default.in')
TESTS_REQUIRE, TESTS_EXTRAS = load_reqs('reqs/test.txt')
SETUP_REQUIRES = []

if NEEDS_DOCS:
    EXTRAS_REQUIRE.update(DOCS_EXTRAS)
    SETUP_REQUIRES.extend(DOCS_REQUIRE)
if NEEDS_PYTEST:
    EXTRAS_REQUIRE.update(TESTS_EXTRAS)
    SETUP_REQUIRES.append('pytest-runner')

# Get the long description from the README file
with open(os.path.join(THIS_FILE_DIR, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# The full version, including alpha/beta/rc tags
RELEASE = '3.0.0'
# The short X.Y version
VERSION = '.'.join(RELEASE.split('.')[:2])

PROJECT = 'html2ans'
AUTHOR = 'Arc Professional Services Team'
COPYRIGHT = '2019, {}'.format(AUTHOR)


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != RELEASE:
            info = "Git tag: {tag} does not match the version of this app: {release}".format(tag=tag, release=RELEASE)
            sys.exit(info)


setup(
    name=PROJECT,
    version=RELEASE,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    description='Convert HTML to ANS',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/washingtonpost/html2ans',
    author=AUTHOR,
    author_email='arc.professional.services@gmail.com',
    license='MIT',
    packages=find_packages('src', exclude=['docs', 'tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require=EXTRAS_REQUIRE,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', PROJECT),
            'version': ('setup.py', VERSION),
            'release': ('setup.py', RELEASE)
        }
    },
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)

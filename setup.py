from codecs import open
import os
from setuptools import find_packages, setup
from setuptools.command.install import install
import sys


NEEDS_DOCS = 'build_sphinx' in sys.argv
NEEDS_PYTEST = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
DOCS_REQUIRE = ('sphinx',)
INSTALL_REQUIRES = (
    'BeautifulSoup4<5',
    'ftfy<5;python_version<"3"',
    'ftfy<6;python_version>="3"',
    'html5lib<2',
    'lxml<5',
    'six<2',
    'furl>=2.0.0,<3',
)
TESTS_REQUIRE = ('pytest<5',)
SETUP_REQUIRES = (('pytest-runner',) if NEEDS_PYTEST else ()) + (DOCS_REQUIRE if NEEDS_DOCS else ())
EXTRAS_REQUIRE = {
    'dev': DOCS_REQUIRE + TESTS_REQUIRE,
    'tests': TESTS_REQUIRE
}
THIS_FILE_DIR = os.path.dirname(__file__)

# Get the long description from the README file
with open(os.path.join(THIS_FILE_DIR, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# The full version, including alpha/beta/rc tags
RELEASE = '3.0.4'
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
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

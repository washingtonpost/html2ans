import sys
import os
from codecs import open
from setuptools import setup, find_packages
from setuptools.command.install import install


THIS_FILE_DIR = os.path.dirname(__file__)

try:
    # pip 9
    from pip.req.req_install import InstallRequirement
except ImportError:
    # pip 10
    from pip._internal.req.req_install import InstallRequirement


def load_reqs(fn):
    reqs = []
    with open(fn) as reqs_file:
        for line in reqs_file:
            try:
                InstallRequirement.from_line(line)
            except Exception:
                # not a line containing a dependency
                pass
            else:
                reqs.insert(0, line.strip())  # reverse the order for setuptools
    return reqs


NEEDS_DOCS = 'build_sphinx' in sys.argv
NEEDS_PYTEST = {'pytest', 'test', 'ptr'}.intersection(sys.argv)

DOCS_REQUIRE = load_reqs('reqs/doc.txt') if NEEDS_DOCS else []
INSTALL_REQUIRES = load_reqs('reqs/default.in')
TESTS_REQUIRE = load_reqs('reqs/test.txt')


# Get the long description from the README file
with open(os.path.join(THIS_FILE_DIR, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# The full version, including alpha/beta/rc tags
RELEASE = '3.0.0dev0'
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
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name=PROJECT,
    version=RELEASE,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    description='Convert HTML to ANS',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/washingtonpost/html2ans',
    author=AUTHOR,
    author_email='arc.professional.services@gmail.com',
    license='MIT',
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    setup_requires=['pytest-runner'] if NEEDS_PYTEST else [],
    tests_require=TESTS_REQUIRE,
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

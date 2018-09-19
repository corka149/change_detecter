from setuptools import setup

setup(
    name='change_detector',
    version='0.6',
    packages=['change_detector', 'change_detector.client_server', 'change_detector.file_syncer'],
    url='https://github.com/corka149/change_detector',
    license='MIT',
    author='Corka149',
    author_email='corka149@mailbox.org',
    include_package_data=True,
    description='A library to perform different actions, performed when files changed.'
)

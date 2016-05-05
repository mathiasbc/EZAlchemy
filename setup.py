import setuptools


setup_params = dict(
    name='ezalchemy',
    version='1.1.2',
    description='Thin wrapper around sqlalchemy for quick database integration',
    author="Mathias Bustamante",
    author_email="mathiasbc@gmail.com",
    url="https://github.com/mathiasbc/EZAlchemy",
    download_url="https://github.com/mathiasbc/EZAlchemy/tarball/1.1.2",
    packages=['ezalchemy'],
    install_requires=[
        'SQLAlchemy>=1.0.9,<2',
    ]
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)

from setuptools import setup

import rcon_py
def long_description():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(
    name='rcon_py',
    version=rcon_py.__version__,
    description=str(rcon_py.__doc__).strip(),
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/notseanray/rcon-py',
    download_url=f'https://github.com/notseanray/rcon-py/{rcon_py.__version__}.tar.gz',
    author=rcon_py.__author__,
    author_email='seanray410@gmail.com',
    license=rcon_py.__license__,
    python_requires='>=3.1',
    project_urls={
        'GitHub': 'https://github.com/httpie/httpie',
    },
)

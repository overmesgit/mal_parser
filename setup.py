from setuptools import setup

setup(name='mal_parser',
      version='0.1',
      description='Tool for parsing MyAnimeList anime, manga and top pages',
      url='http://github.com/overmes/mal_parser',
      author='Artem Bezu',
      author_email='overmes@gmail.com',
      license='MIT',
      packages=['mal_parser'],
      install_requires=[
          'requests',
          'lxml',
          'pyquery',
          'python-dateutil',
          'aiohttp'
      ],
      zip_safe=False)
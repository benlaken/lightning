from setuptools import setup

setup(
    name='stormstats',
    version='0.2',
    description='Used for GIS investigation into lightning statistics',
    scripts=[],
    author_email='jcalogovic@geof.hr',
    author=['Jasa Čalogović', 'Benjamin A. Laken'],
    url='https://github.com/jcalogovic/lightning',
    download_url="https://github.com/jcalogovic/lightning/tarball/0.1",
    packages=['stormstats'],
    package_dir={'stormstats': 'stormstats'},
    package_data={'stormstats': ['egdata/*', 'examples/*']},
    license='MIT',
    install_requires=['bokeh', 'pandas', 'folium', 'tqdm', 'geopandas'],
    keywords=['lightning', 'geoscience', 'statistics', 'science'],
    zip_safe=False,
)

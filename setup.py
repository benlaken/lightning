from setuptools import setup, find_packages

setup(
    name='stormstats',
    version='0.1',
    description='Analysis software for investigation into lightning',
    packages=find_packages(exclude=['*test']),
    scripts=[],
    author_email='jcalogovic@geof.hr',
    author=['Jasa Čalogović', 'Benjamin A. Laken'],
    url='https://github.com/jcalogovic/lightning',
    download_url="https://github.com/jcalogovic/lightning/tarball/0.1",
    license='MIT',
    install_requires=['bokeh', 'pandas'],
    keywords=['lightning', 'geoscience', 'statistics','science'],
    zip_safe=False,
)

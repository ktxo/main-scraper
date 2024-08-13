from os.path import abspath, dirname, join
import setuptools

aboutpath = join(abspath(dirname(__file__)),'ktxo','scraper', '_about.py')
_about = {}
with open(aboutpath) as fp:
    exec(fp.read(), _about)

setuptools.setup(
    name=_about["__name__"],
    version=_about["__version__"],
    author=_about["__author__"],
    author_email=_about["__author_email__"],
    description=_about["__description_message__"],
    url=_about["__url__"],
    #entry_points={'console_scripts': ['main_template = ktxo.scraper.main_scraper:main']},
    include_package_data=True,
    packages=setuptools.find_packages(include=["ktxo.scraper"]),
    python_requires='>=3.10',
    install_requires=['selenium', 'beautifulsoup4', 'fake-useragent', 'undetected_chromedriver'],
    classifiers=['Programming Language :: Python :: 3.10'],
    keywords='scraper rpa selenium'
)

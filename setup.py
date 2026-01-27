from setuptools import setup, find_packages

# Baca requirements dari requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Baca README untuk deskripsi panjang
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='panen-tweet',
    version='1.0.0',
    author='Ramadhani',
    author_email='your.email@example.com',
    description='Powerful Twitter/X scraping tool dengan Selenium',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Dhaniaaa/Scrapping-X',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'scrape-x=scrape_x.cli:main',
        ],
    },
    keywords='twitter scraping selenium web-scraping x-scraper',
    project_urls={
        'Bug Reports': 'https://github.com/Dhaniaaa/Scrapping-X/issues',
        'Source': 'https://github.com/Dhaniaaa/Scrapping-X',
    },
)

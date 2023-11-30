import setuptools

with open("README.md", 'r', encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='pydayada',
    version='1.0.0',
    author='Marco R. Gazzetta',
    author_email='dev@mrgazz.com',
    description='Distribute a file into shards, shares that can be recombined into the original file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mansxu/pydayada',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['pydayada = pydayada:main']},
    install_requires=['pycryptodome', 'simplecrypto'],
)

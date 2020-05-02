from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pirateplayer',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'rpi.gpio',
        'gpiozero',
        'spidev',
        'numpy',
        'st7789',
        'pillow',
        'mutagen',
        'pygobject',
        'autopep8'
    ],
    entry_points='''
            [console_scripts]
            pirateplayer=player:main
        ''',
    description='Play offline music on PirateAudio',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/TestDotCom/pirateplayer',
    license='MIT License',
    author='TestDotCom',
    author_email=''
)

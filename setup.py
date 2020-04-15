from setuptools import setup, find_packages

setup(
    name='pirateplayer',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'rpi.gpio',
        'gpiozero',
        'spidev',
        'numpy',
        'st7789',
        'pillow',
        'vext',
        'vext.gi',
        'pylint',
        'autopep8'
    ],
    entry_points='''
            [console_scripts]
            pirateplayer=player:main
        ''',
    url='https://github.com/TestDotCom/pirateplayer',
    license='MIT',
    author='TestDotCom',
    author_email='',
    description='Play offline music on PirateAudio'
)

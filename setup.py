from setuptools import setup, find_packages

setup(
    name='pirateplayer',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyalsaaudio',
        'miniaudio',
        'gpiozero',
        'pigpio',
        'spidev',
        'numpy',
        'st7789',
        'pillow'
    ],
    entry_points='''
            [console_scripts]
            pirateplayer=player:main
        ''',
    url='',
    license='',
    author='TestDotCom',
    author_email='',
    description='Play offline music on PirateAudio'
)

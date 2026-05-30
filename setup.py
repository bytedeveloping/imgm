from setuptools import setup

setup(
    name='imgm',
    version='1.0.0',
    description='Professional Image Processing CLI Tool',
    author='Benjamin',
    py_modules=['imgm', 'processor', 'filters', 'presets', 'plugins_system', 'gui'],
    install_requires=[
        'Pillow==10.0.0',
        'tqdm==4.65.0',
        'rich==13.5.2',
        'colorama==0.4.6',
    ],
    entry_points={
        'console_scripts': [
            'imgm=imgm:main',
        ],
    },
    python_requires='>=3.8',
)

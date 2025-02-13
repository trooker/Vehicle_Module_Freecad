from setuptools import find_packages, setup

VERSION ='1.0.0'
DESCRIPTION = 'AAP first Python library'

setup(
    name='aap_lib',  
    #packages=find_packages(),
    #
    packages=find_packages(include=['aap_lib']),
    version=VERSION,
    description=DESCRIPTION,
    author='lu',
    author_email = "<luzzo@abbottanp.com>",
    url="https://abbottanp.com/",
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    keywords=['gm-mobile','ev','abiriba_rg','speed-bump', 'FreeCAD'],
    classifiers=[
		"Development Status :: 3 - Detail CAD",
		"Programming Language :: Python 3",
		"Operating System :: Ubuntu"
    ]

)

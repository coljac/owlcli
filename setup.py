from setuptools import setup

setup(
         name='owlcli',  
         version='0.1', 
         scripts=['owlcli'],
         install_requires=[
            'beautifulsoup4',
            'lxml'
          ]
      )

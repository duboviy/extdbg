from distutils.core import setup
setup(
  name = 'extdbg',
  packages = ['extdbg'], # this must be the same as the name above
  version = '0.0.1',
  description = 'An extended debugging python utilities.',
  author = 'Eugene Duboviy',
  author_email = 'eugene.dubovoy@gmail.com',
  url = 'https://github.com/duboviy/extdbg', # use the URL to the github repo
  download_url = 'https://github.com/duboviy/extdbg/tarball/0.0.1', # I'll explain this in a second
  keywords = ['debug', 'utility', 'testing'], # arbitrary keywords
  classifiers=[
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
  ],
  long_description="""
extdbg extends existing debugging utilities and provides a simple and pythonic way to debug.
""",
  install_requires=[
    'psutil',
    'gevent',
  ],
)

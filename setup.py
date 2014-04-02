from setuptools import setup, find_packages

setup(name='sneeze-pocket',
      version='0.0.1',
      author='Silas Ray',
      author_email='silas.ray@nytimes.com',
      license='Apache2.0',
      url='http://pocket.readthedocs.org/',
      description='A Sneeze plugin for logging logging',
      long_description='A plugin for Sneeze that shunts logging messages to the reporting DB.',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Information Technology',
                   'Topic :: Software Development :: Quality Assurance',
                   'Topic :: Software Development :: Testing'],
      packages=find_packages(),
      install_requires=['nose-sneeze'],
      entry_points={'nose.plugins.sneeze.plugins.add_models' : ['pocket_models = pocket.database:add_models'],
                    'nose.plugins.sneeze.plugins.add_options' : ['pocket_options = pocket.log_lib:add_options'],
                    'nose.plugins.sneeze.plugins.managers' : ['pocket_manager = pocket.log_lib:TissueHandler']})

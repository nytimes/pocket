from setuptools import setup, find_packages

setup(name='pocket',
      version='0.0.0',
      packages=find_packages(),
      install_requires=['sneeze'],
      entry_points={'nose.plugins.sneeze.plugins.add_models' : ['pocket_models = pocket.database:add_models'],
                    'nose.plugins.sneeze.plugins.add_options' : ['pocket_options = pocket.log_lib:add_options'],
                    'nose.plugins.sneeze.plugins.managers' : ['pocket_manager = pocket.log_lib:TissueHandler']})
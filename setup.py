from setuptools import find_packages, setup
from typing import List
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements.
    '''
    HYPEN_DOT_E = '-e .'
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        
        if HYPEN_DOT_E in requirements:
            requirements.remove(HYPEN_DOT_E)
    return requirements
setup(
    name='mlproject',
    version='0.0.1',
    author='Sahil Sawant',
    author_email='smsawant17@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)
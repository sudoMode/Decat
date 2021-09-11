from setuptools import setup
from setuptools import find_packages
from pathlib import Path

BASE = Path(__file__).parent.resolve()
_README = (BASE / 'README.md').read_text(encoding='utf-8')


setup(
            name='decat',
            version='0.0.1',
            description='De-concatenate strings that do not have white-spaces.',
            long_description=_README,
            long_description_content_type='text/markdown',
            author='Mandeep Singh',
            author_email='singh.mandeep2207@gmail.com',
            url='https://github.com/sudoMode/Decat',
            license='MIT',
            classifiers=[
                            'Development Status :: 3 - Alpha',
                            'Intended Audience :: Developers',
                            'License :: OSI Approved :: MIT License',
                            'Programming Language :: Python :: 3.6',
                            'Programming Language :: Python :: 3.7',
                            'Programming Language :: Python :: 3.8',
                            'Programming Language :: Python :: 3.9',
                        ],
            keywords='nlp, text mining',
            package_dir={'': 'decat'},
            packages=find_packages(where='decat'),
            py_modules=['__init__', '__main__', '__settings__'],
            include_package_data=True,
            python_requires='>=3.6',
            install_requires=[],
            entry_points={
                            'console_scripts': [
                                                    'decat=decat.__main__:main'
                                               ]
                         },
            project_urls={'Source': 'https://github.com/sudoMode/Decat',
                          'Bug Reports': 'https://github.com/sudoMode/Decat/issues'}
      )

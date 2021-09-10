from distutils.core import setup
from decat.__settings__ import join
from decat.__settings__ import VERSION as _VERSION
from decat.__settings__ import BASE as _BASE


_README = join(_BASE, 'README.md')


setup(
            name='decat',
            version=_VERSION,
            description='De-concatenate strings that do not have white-spaces.',
            long_description=_README,
            long_description_content_type='text/markdown',
            author='Mandeep Singh',
            author_email='singh.mandeep2207@gmail.com',
            url='https://github.com/sudoMode/Decat',
            license='MIT',
            classifiers=[
                            'License :: OSI Approved :: MIT License',
                            'Programming Language :: Python :: 3.6',
                            'Programming Language :: Python :: 3.7',
                            'Programming Language :: Python :: 3.8',
                            'Programming Language :: Python :: 3.9',
                        ],
            packages=['decat'],
            include_package_data=True,
            install_requires=[],
            entry_points={
                            'console_scripts': [
                                                    'decat=decat.__main__:main'
                                               ]
                         }
      )

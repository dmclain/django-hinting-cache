from distutils.core import setup

setup(
    name='django-hinting-cache',
    version='0.1',
    description='Cache wrapper that turns many gets into get_manys',
    author='Dave McLain',
    author_email='python@davemclain.com',
    url='https://github.com/dmclain/django-hinting-cache',
    license='MIT',
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=['django_hinting_cache'],
)

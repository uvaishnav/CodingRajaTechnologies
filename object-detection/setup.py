import setuptools

setuptools.setup(
    name = 'wasteDetection',
    version= '0.0.0',
    author= 'Vaishnav Uppalapati',
    author_email= 'vaishnavut@gmail.com',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires = []
)

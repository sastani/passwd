from setuptools import setup, find_packages

setup(name="passwd_as_a_service",
      version="0.1",
      python_requires=">=3.6",
      install_requires=["toml", "django", "djangorestframework"],
      packages=find_packages(exclude=("tests",)),
      author="Sina Astani"
      )
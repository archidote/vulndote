from setuptools import setup, find_packages

setup(
    name="vulndote",
    version="0.0.1",
    author="archidote",
    author_email="archidote.contact@gmail.com",
    url="https://github.com/archidote/vulndote",
    description="Coming Soon",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["beautifulsoup4", "httpx", "PyGithub", "pyTelegramBotAPI", "requests", "schedule", "urllib3"],
    entry_points={"console_scripts": ["timechecker = src.main:main"]},
)

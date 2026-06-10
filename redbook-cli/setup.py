from setuptools import setup, find_packages

setup(
    name='redbook-cli',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['requests', 'rich'],
    entry_points={
        'console_scripts': [
            'redbook=src.cli:main',
        ],
    },
    author='LLyhy',
    description='红宝书 CLI - 用矛盾分析法分析算法问题',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LLyhy/redbook',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

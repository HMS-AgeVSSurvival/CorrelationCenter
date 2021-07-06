from setuptools import setup

setup(
    name="correlation_center",
    version="0.1",
    description="Compute the correlations of some trained algorithms from NHANES dataset.",
    packages=["residual"],
    requires=["setuptools", "wheel"],
    install_requires=[
        "numpy",
        "pandas==1.2.5",
        "pyarrow",
        "scikit-survival",
        "gspread",
        "matplotlib", 
        "openpyxl"
    ],
    extras_require={
        "dev": ["tqdm", "jupyter", "ipympl", "black"]
    },
    entry_points={
        "console_scripts": [
            "residual=residual.compute_residual:residual_cli",
        ]
    },
)
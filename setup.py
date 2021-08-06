from setuptools import setup

setup(
    name="correlation_center",
    version="0.1",
    description="Compute the correlations of some trained algorithms from NHANES dataset.",
    packages=["residual", "log_hazard_ratio", "correlation"],
    requires=["setuptools", "wheel"],
    install_requires=[
        "numpy",
        "pandas==1.2.5",
        "pyarrow",
        "scikit-survival",
        "gspread",
        "matplotlib", 
        "openpyxl",
        "lifelines"
    ],
    extras_require={
        "dev": ["tqdm", "jupyter", "ipympl", "black"]
    },
    entry_points={
        "console_scripts": [
            "residual=residual.compute_residual:residual_cli",
            "log_hazard_ratio=log_hazard_ratio.compute_log_hazard_ratio:log_hazard_ratio_cli",
            "residual_correlation=correlation.compute_residual_correlation:compute_residual_correlation_cli",
            "feature_importances_correlation=correlation.compute_feature_importances_correlation:compute_feature_importances_correlation_cli",
        ]
    },
)
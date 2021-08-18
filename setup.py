from setuptools import setup

setup(
    name="correlation_center",
    version="0.1",
    description="Compute the correlations of some trained algorithms from NHANES dataset.",
    packages=["residual", "log_hazard_ratio", "correlation"],
    requires=["setuptools", "wheel"],
    install_requires=[
        "numpy==1.16.6",
        "pandas==1.2.5",
        "pyarrow==4.0.1",
        "scikit-survival==0.15.0.post0",
        "gspread==3.7.0",
        "openpyxl==3.0.7",
        "lifelines==0.26.0"
    ],
    extras_require={
        "dev": ["tqdm==4.61.2", "jupyter==1.0.0", "ipympl==0.7.0", "black==21.6b0"]
    },
    entry_points={
        "console_scripts": [
            "residual=residual.compute_residual:residual_cli",
            "log_hazard_ratio=log_hazard_ratio.compute_log_hazard_ratio:log_hazard_ratio_cli",
            "residual_correlation=correlation.compute_residual_correlation:compute_residual_correlation_cli",
            "feature_importances_correlation=correlation.compute_feature_importances_correlation:compute_feature_importances_correlation_cli",
            "feature_importances=feature_importances.store_feature_importances:feature_importances_cli",
        ]
    },
)
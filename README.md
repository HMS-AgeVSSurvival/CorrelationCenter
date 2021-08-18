# CorrelationCenter
Compute the correlations between the outputs of the TrainingCenter. 

Feel free to start a discussion to ask anything [here](https://github.com/HMS-Internship/CorrelationCenter/discussions)

To setup the virtual environment:
```Bash
pip install -e .
```

## [I Residual](./residual)

It fetches the data from TrainingCenter, adds to it the predictions and the feature importances from the dumps and compute the residuals. The outcoming data is stored at _data/main_category/category.feather_.

To launch this step:
```Bash
./residual/shell_script/run_residual.sh
```


## [II Log hazard ratio](./log_hazard_ratio)

It uses the residuals from age prediction computed in the last [step](#I-Residual) as a predictor for survival along with the age, the sex and the ethnicities. It outputs the results on a [google sheet](https://docs.google.com/spreadsheets/d/1IZDQmitlE5fU_5wbu2T8jF2_4i7I7Q_VTTjv6buVFwc/edit#gid=750005196).

To launch this step:
```Bash
./log_hazard_ratio/shell_script/run_log_hazard_ratio.sh
```

## [III Feature importances](./feature_importances)

It stores the feature importances, that were gathered in the first [step](#I-Residual), at _data/feature_importances/main_category/category.feather_.

To launch this step:
```Bash
./feature_importances/run_feature_importances.sh
```

## [IV Correlation](./correlation)

It computes the correlations between the residuals and between the feature importances from the data that has been stored in the first [step](#I-Residual). The outcoming correlations are stored at _data/correlation/residual/_ and _data/correlation/feature_importances/_.

To launch this step:
```Bash
./correlation/run_residual_correlation.sh
./correlation/run_feature_importances_correlation.sh
```


## Structure to have before launching the jobs
```
┣ 📦TrainingCenter
┃  ┗ 📂data
┃     ┣ 📂examination
┃     ┃ ┗ 📜[category].feather
┃     ┣ 📂laboratory
┃     ┃ ┗ 📜[category].feather
┃     ┗ 📂questionnaire
┃       ┗ 📜[category].feather
┣ 📦CorrelationCenter
   ┗ 📂[...]
```

## Structure of the data folder when the jobs are finished
```
 📂data
 ┣ 📂correlation
 ┃ ┣ 📂feature_importances
 ┃ ┃ ┣ 📜pearson_[...].feather
 ┃ ┃ ┣ 📜spearman_[...].feather
 ┃ ┗ 📂residual
 ┃   ┣ 📜number_participants_[...].feather
 ┃   ┣ 📜pearson_[...].feather
 ┃   ┗ 📜spearman_[...].feather
 ┣ 📂examination
 ┃ ┗ 📜[category].feather
 ┣ 📂feature_importances
 ┃ ┣ 📂examination
 ┃ ┃ ┗ 📜[category].feather
 ┃ ┣ 📂laboratory
 ┃ ┃ ┗ 📜[category].feather
 ┃ ┗ 📂questionnaire
 ┃ ┃ ┗ 📜[category].feather
 ┣ 📂laboratory
 ┃ ┗ 📜[category].feather
 ┗ 📂questionnaire
   ┗ 📜[category].feather
```
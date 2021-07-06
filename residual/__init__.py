AGE_COLUMN = "RIDAGEEX_extended; Best age in months at date of examination for individuals under 85 years of age at screening."
GENDER_COLUMN = 'RIAGENDR; Gender of the sample person'
ETHNICITIES = ['RIDRETH1_Non-Hispanic Black; Recode of reported race and ethnicity information.', 'RIDRETH1_Non-Hispanic White; Recode of reported race and ethnicity information.', 'RIDRETH1_Other Hispanic; Recode of reported race and ethnicity information.', 'RIDRETH1_Other Race - Including Multi-Racial; Recode of reported race and ethnicity information.']

DEATH_COLUMN = "mortstat"
FOLLOW_UP_TIME_COLUMN = "follow_up_time"

# Concerning log_hazard_ratio
COLUMNS_TO_DROP_FOR_SCALE = [
    DEATH_COLUMN,
    FOLLOW_UP_TIME_COLUMN,
    "survival_type_alive"
]
COLUMNS_TO_ADD_AFTER_SCALE = [DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN]
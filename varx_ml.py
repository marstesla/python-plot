import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.api import VAR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from xgboost import XGBRegressor


# =========================
# CONFIG
# =========================

DATE_COL = "date"
ENDOG = ["cpi", "unemployment", "gdp"]
EXOG = ["policy_rate", "oil_price"]

MAX_LAGS = 4        # VAR lag order
TEST_SIZE = 24      # last N obs as test


# =========================
# 1. LOAD & PREP DATA
# =========================

def load_data(path):
    df = pd.read_csv(path)
    df[DATE_COL] = pd.to_datetime(df[DATE_COL])
    df = df.sort_values(DATE_COL).set_index(DATE_COL)
    df = df.asfreq("M")
    return df


df = load_data("macro_data.csv")

endog = df[ENDOG]
exog = df[EXOG]


# =========================
# 2. TRAIN / TEST SPLIT
# =========================

train_endog = endog.iloc[:-TEST_SIZE]
test_endog  = endog.iloc[-TEST_SIZE:]

train_exog = exog.iloc[:-TEST_SIZE]
test_exog  = exog.iloc[-TEST_SIZE:]


# =========================
# 3. FIT VAR-X ON TRAIN
# =========================

model_var = VAR(endog=train_endog, exog=train_exog)
res_var = model_var.fit(MAX_LAGS)

print(res_var.summary())


# =========================
# 4. VAR-X FORECAST ON TEST
# =========================

# We forecast dynamically over the test window
var_forecasts = res_var.forecast(
    y=train_endog.values[-MAX_LAGS:],
    steps=TEST_SIZE,
    exog_future=test_exog.values
)

var_forecasts_df = pd.DataFrame(
    var_forecasts,
    index=test_endog.index,
    columns=ENDOG
)

# CPI baseline forecast from VAR-X
cpi_var_pred = var_forecasts_df["cpi"]
cpi_actual   = test_endog["cpi"]

rmse_var = mean_squared_error(cpi_actual, cpi_var_pred, squared=False)
mae_var  = mean_absolute_error(cpi_actual, cpi_var_pred)

print(f"VAR-X CPI RMSE: {rmse_var:.4f}")
print(f"VAR-X CPI MAE : {mae_var:.4f}")


# =========================
# 5. BUILD RESIDUAL SERIES FOR CPI
# =========================

# In-sample fitted values for CPI
fitted_in_sample = res_var.fittedvalues["cpi"]
actual_in_sample = train_endog["cpi"].iloc[MAX_LAGS:]  # align with fitted

cpi_resid = actual_in_sample - fitted_in_sample
cpi_resid.name = "cpi_resid"

resid_df = pd.concat([cpi_resid, train_endog.iloc[MAX_LAGS:], train_exog.iloc[MAX_LAGS:]], axis=1)


# =========================
# 6. FEATURE ENGINEERING FOR ML ON RESIDUALS
# =========================

def make_lagged_features(df, cols, n_lags=6):
    out = df.copy()
    for col in cols:
        for lag in range(1, n_lags + 1):
            out[f"{col}_lag_{lag}"] = out[col].shift(lag)
    return out

# We'll use lags of CPI, unemployment, gdp, policy_rate, oil_price
ml_feat_cols = ENDOG + EXOG

ml_df = make_lagged_features(resid_df, ml_feat_cols, n_lags=6)
ml_df = ml_df.dropna()

X_ml = ml_df.drop(columns=["cpi_resid"])
y_ml = ml_df["cpi_resid"]


# =========================
# 7. TRAIN ML MODEL ON RESIDUALS
# =========================

split_idx = int(len(ml_df) * 0.8)
X_ml_train, X_ml_val = X_ml.iloc[:split_idx], X_ml.iloc[split_idx:]
y_ml_train, y_ml_val = y_ml.iloc[:split_idx], y_ml.iloc[split_idx:]

ml_model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)

ml_model.fit(X_ml_train, y_ml_train)

y_val_pred = ml_model.predict(X_ml_val)
rmse_ml = mean_squared_error(y_ml_val, y_val_pred, squared=False)
mae_ml  = mean_absolute_error(y_ml_val, y_val_pred)

print(f"Residual ML RMSE (val): {rmse_ml:.4f}")
print(f"Residual ML MAE  (val): {mae_ml:.4f}")


# =========================
# 8. HYBRID FORECAST ON TEST SET
# =========================

# We need ML features aligned with the test period.
# Strategy:
# - Rebuild a combined df including full sample
# - Generate lagged features
# - Extract rows corresponding to test period

full_resid_like = pd.concat(
    [endog, exog],
    axis=1
)

full_resid_like = make_lagged_features(full_resid_like, ml_feat_cols, n_lags=6)
full_resid_like = full_resid_like.dropna()

# Align index with full_resid_like and test period
test_index = test_endog.index
ml_test_feat = full_resid_like.loc[test_index]

# Predict residual correction for CPI
cpi_resid_pred_test = ml_model.predict(ml_test_feat)

# Hybrid CPI forecast = VAR-X CPI forecast + ML residual correction
cpi_hybrid_pred = cpi_var_pred + cpi_resid_pred_test

rmse_hybrid = mean_squared_error(cpi_actual, cpi_hybrid_pred, squared=False)
mae_hybrid  = mean_absolute_error(cpi_actual, cpi_hybrid_pred)

print(f"HYBRID CPI RMSE: {rmse_hybrid:.4f}")
print(f"HYBRID CPI MAE : {mae_hybrid:.4f}")


# =========================
# 9. PLOTS
# =========================

plt.figure(figsize=(10, 5))
plt.plot(cpi_actual.index, cpi_actual.values, label="Actual CPI", color="black")
plt.plot(cpi_var_pred.index, cpi_var_pred.values, label="VAR-X CPI", color="blue")
plt.plot(cpi_hybrid_pred.index, cpi_hybrid_pred, label="Hybrid CPI (VAR-X + ML)", color="red")
plt.title("CPI Forecast: VAR-X vs Hybrid")
plt.legend()
plt.tight_layout()
plt.show()

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Tuple

from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor
import matplotlib.pyplot as plt


# =========================
# 1. Config
# =========================

@dataclass
class Config:
    date_col: str = "date"
    target_col: str = "inflation"   # change to your target
    freq: str = "M"                 # 'M' for monthly, 'Q' for quarterly, etc.
    lags: int = 12                  # number of lag features
    rolling_windows: List[int] = None
    test_size: int = 24             # last N observations as test
    n_splits: int = 5               # for time-series CV

    def __post_init__(self):
        if self.rolling_windows is None:
            self.rolling_windows = [3, 6, 12]


CONFIG = Config()


# =========================
# 2. Data loading & basic cleaning
# =========================

def load_data(path: str, config: Config) -> pd.DataFrame:
    df = pd.read_csv(path)
    df[config.date_col] = pd.to_datetime(df[config.date_col])
    df = df.sort_values(config.date_col).set_index(config.date_col)
    # Optional: enforce regular frequency
    df = df.asfreq(config.freq)
    return df


# =========================
# 3. Feature engineering
# =========================

def add_lag_features(df: pd.DataFrame, col: str, n_lags: int) -> pd.DataFrame:
    for lag in range(1, n_lags + 1):
        df[f"{col}_lag_{lag}"] = df[col].shift(lag)
    return df


def add_rolling_features(df: pd.DataFrame, col: str, windows: List[int]) -> pd.DataFrame:
    for w in windows:
        df[f"{col}_roll_mean_{w}"] = df[col].shift(1).rolling(window=w).mean()
        df[f"{col}_roll_std_{w}"] = df[col].shift(1).rolling(window=w).std()
    return df


def build_feature_matrix(df: pd.DataFrame, config: Config) -> pd.DataFrame:
    df = df.copy()
    # Lag features for target
    df = add_lag_features(df, config.target_col, config.lags)
    # Rolling stats for target
    df = add_rolling_features(df, config.target_col, config.rolling_windows)

    # You can add macro covariates here:
    # for col in ["unemployment", "gdp", "oil_price"]:
    #     df = add_lag_features(df, col, 3)

    # Drop rows with NaNs created by lags/rolling
    df = df.dropna()
    return df


# =========================
# 4. Train-test split (time series)
# =========================

def train_test_split_ts(df: pd.DataFrame, config: Config) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return df.iloc[:-config.test_size], df.iloc[-config.test_size:]


def get_X_y(df: pd.DataFrame, config: Config) -> Tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=[config.target_col])
    y = df[config.target_col]
    return X, y


# =========================
# 5. Time-series cross-validation (optional but recommended)
# =========================

def time_series_cv(
    X: pd.DataFrame,
    y: pd.Series,
    config: Config,
    model_params: dict = None
):
    if model_params is None:
        model_params = {}

    tscv = TimeSeriesSplit(n_splits=config.n_splits)
    rmses = []

    for fold, (train_idx, val_idx) in enumerate(tscv.split(X), start=1):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model = XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            random_state=42,
            **model_params
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_val)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        rmses.append(rmse)
        print(f"Fold {fold}: RMSE = {rmse:.4f}")

    print(f"Average CV RMSE: {np.mean(rmses):.4f} ± {np.std(rmses):.4f}")


# =========================
# 6. Final training and static test evaluation
# =========================

def train_and_evaluate(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_params: dict = None
) -> XGBRegressor:
    if model_params is None:
        model_params = {}

    model = XGBRegressor(
        n_estimators=800,
        learning_rate=0.03,
        max_depth=4,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="reg:squarederror",
        random_state=42,
        **model_params
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Test RMSE: {rmse:.4f}")
    print(f"Test MAE : {mae:.4f}")

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(y_test.index, y_test.values, label="Actual")
    plt.plot(y_test.index, y_pred, label="Predicted")
    plt.title("Test set: actual vs predicted")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return model


# =========================
# 7. Rolling-origin forecast (true time-series evaluation)
# =========================

def rolling_forecast(
    df: pd.DataFrame,
    config: Config,
    model_params: dict = None
) -> pd.DataFrame:
    """
    Expanding-window rolling forecast:
    - Start with minimal training window
    - At each step, refit model and predict next point
    """
    if model_params is None:
        model_params = {}

    df = df.copy()
    X, y = get_X_y(df, config)

    preds = []
    dates = []

    # start rolling from the point where we have at least some history
    start_idx = len(X) - config.test_size

    for i in range(start_idx, len(X)):
        train_X = X.iloc[:i]
        train_y = y.iloc[:i]
        test_X = X.iloc[i:i+1]

        model = XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            random_state=42,
            **model_params
        )
        model.fit(train_X, train_y)
        pred = model.predict(test_X)[0]

        preds.append(pred)
        dates.append(test_X.index[0])

    y_true = y.iloc[start_idx:]
    results = pd.DataFrame(
        {"y_true": y_true.values, "y_pred": preds},
        index=dates
    )

    rmse = mean_squared_error(results["y_true"], results["y_pred"], squared=False)
    mae = mean_absolute_error(results["y_true"], results["y_pred"])
    print(f"Rolling forecast RMSE: {rmse:.4f}")
    print(f"Rolling forecast MAE : {mae:.4f}")

    plt.figure(figsize=(10, 4))
    plt.plot(results.index, results["y_true"], label="Actual")
    plt.plot(results.index, results["y_pred"], label="Rolling forecast")
    plt.title("Rolling-origin forecast")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return results


# =========================
# 8. Main
# =========================

if __name__ == "__main__":
    DATA_CSV_PATH = "your_data.csv"  # <-- change this

    # 1) Load
    df_raw = load_data(DATA_CSV_PATH, CONFIG)

    # 2) Build features
    df_feat = build_feature_matrix(df_raw, CONFIG)

    # 3) Split
    train_df, test_df = train_test_split_ts(df_feat, CONFIG)
    X_train, y_train = get_X_y(train_df, CONFIG)
    X_test, y_test = get_X_y(test_df, CONFIG)

    # 4) Time-series CV
    print("=== Time-series cross-validation ===")
    time_series_cv(X_train, y_train, CONFIG)

    # 5) Final train & evaluate
    print("\n=== Final train & static test evaluation ===")
    model = train_and_evaluate(X_train, y_train, X_test, y_test)

    # 6) Rolling forecast
    print("\n=== Rolling-origin forecast ===")
    rolling_results = rolling_forecast(df_feat, CONFIG)

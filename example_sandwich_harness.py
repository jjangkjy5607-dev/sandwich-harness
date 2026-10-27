import ast
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def check_source(source: str) -> None:
    functions = [n for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if any((len(source.splitlines()) > 200, any(n.end_lineno - n.lineno + 1 > 35 for n in functions))):
        raise ValueError("AST gate: file > 200 lines or function > 35 lines")

def check_frame(frame: pd.DataFrame) -> None:
    if tuple(frame.columns) != ("x", "y") or frame.shape != (5, 2):
        raise ValueError("Input gate: expected five rows with x and y columns")
    if not np.isfinite(frame.to_numpy(dtype=float)).all():
        raise ValueError("Input gate: missing or non-finite values")

def features(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[["x"]].copy()

def run_demo() -> list[float]:
    check_source(Path(__file__).read_text(encoding="utf-8"))
    frame = pd.DataFrame({"x": [0., 1., 2., 3., 4.], "y": [1., 3., 5., 7., 9.]})
    check_frame(frame)
    scores = []
    for train, valid in KFold(5, shuffle=True, random_state=42).split(frame):
        model = make_pipeline(StandardScaler(), LinearRegression())
        model.fit(features(frame.iloc[train]), frame["y"].iloc[train])
        predictions = model.predict(features(frame.iloc[valid]))
        if predictions.shape != (len(valid),) or not np.isfinite(predictions).all():
            raise ValueError("Output gate: invalid predictions")
        scores.append(float(np.mean((predictions - frame["y"].iloc[valid]) ** 2)))
    return scores
if __name__ == "__main__":
    print("5-fold MSE:", run_demo())

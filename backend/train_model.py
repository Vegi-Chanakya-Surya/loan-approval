# """

#working model (ultimate simple model)
# Train a simple DecisionTree pipeline on synthetic loan data and save as model.pkl

# Run:
#     python train_model.py
#

# This will write `model.pkl` next to this file.
# """
# import os
# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.pipeline import Pipeline
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# from sklearn.metrics import classification_report


# def make_synthetic(n=2000, random_state=42):
#     rng = np.random.RandomState(random_state)
#     applicant_income = rng.uniform(2000, 20000, size=n)
#     loan_amount = rng.uniform(500, 50000, size=n)
#     credit_history = rng.choice(["good", "bad"], size=n, p=[0.7, 0.3])
#     employment_type = rng.choice(["salaried", "self-employed", "unemployed"], size=n, p=[0.6, 0.3, 0.1])

#     # deceptively simple rule + noise to decide approval
#     # base score
#     score = (applicant_income / (loan_amount + 1))
#     score += (credit_history == "good") * 1.0
#     score += (employment_type == "salaried") * 0.3
#     prob = 1 / (1 + np.exp(- (score - 0.5)))
#     y = (prob + rng.normal(scale=0.2, size=n)) > 0.6
#     df = pd.DataFrame({
#         "applicant_income": applicant_income,
#         "loan_amount": loan_amount,
#         "credit_history": credit_history,
#         "employment_type": employment_type,
#         "approved": y.astype(int)
#     })
#     return df


# def build_and_save_model(out_path="model.pkl"):
#     df = make_synthetic()
#     X = df[["applicant_income", "loan_amount", "credit_history", "employment_type"]]
#     y = df["approved"]

#     num_features = ["applicant_income", "loan_amount"]
#     cat_features = ["credit_history", "employment_type"]

#     pre = ColumnTransformer(
#         transformers=[
#             ("num", StandardScaler(), num_features),
#             ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
#         ]
#     )

#     pipe = Pipeline([
#         ("pre", pre),
#         ("clf", DecisionTreeClassifier(max_depth=6, random_state=42))
#     ])

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#     pipe.fit(X_train, y_train)

#     preds = pipe.predict(X_test)
#     print("Classification report on held-out test set:")
#     print(classification_report(y_test, preds))

#     joblib.dump(pipe, out_path)
#     print(f"Saved model pipeline to {out_path}")


# if __name__ == "__main__":
#     here = os.path.dirname(__file__)
#     out = os.path.join(here, "model.pkl")
#     build_and_save_model(out)


"""
Train a realistic DecisionTree model on rule-based synthetic loan data.
Run:
    python train_model.py
"""
# import os
# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.pipeline import Pipeline
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# from sklearn.metrics import classification_report


# def make_synthetic(n=2000, random_state=42):
#     rng = np.random.RandomState(random_state)
#     applicant_income = rng.uniform(5000, 150000, size=n)  # more realistic range
#     loan_amount = rng.uniform(10000, 500000, size=n)
#     credit_history = rng.choice(["good", "bad"], size=n, p=[0.7, 0.3])
#     employment_type = rng.choice(["salaried", "self-employed", "unemployed"], size=n, p=[0.6, 0.3, 0.1])

#     approved = []
#     for inc, loan, ch, emp in zip(applicant_income, loan_amount, credit_history, employment_type):
#         ratio = loan / inc

#         # realistic approval rules
#         if emp == "unemployed":
#             approved.append(0)
#         elif ch == "bad" and ratio > 2:
#             approved.append(0)
#         elif ratio < 3 and ch == "good" and emp != "unemployed":
#             approved.append(1)
#         elif ratio < 1.5:
#             approved.append(1)
#         else:
#             approved.append(int(rng.rand() > 0.6))  # random chance zone

#     df = pd.DataFrame({
#         "applicant_income": applicant_income,
#         "loan_amount": loan_amount,
#         "credit_history": credit_history,
#         "employment_type": employment_type,
#         "approved": approved
#     })
#     return df


# def build_and_save_model(out_path="model.pkl"):
#     df = make_synthetic()
#     X = df[["applicant_income", "loan_amount", "credit_history", "employment_type"]]
#     y = df["approved"]

#     num_features = ["applicant_income", "loan_amount"]
#     cat_features = ["credit_history", "employment_type"]

#     pre = ColumnTransformer([
#         ("num", StandardScaler(), num_features),
#         ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
#     ])

#     pipe = Pipeline([
#         ("pre", pre),
#         ("clf", DecisionTreeClassifier(max_depth=6, random_state=42))
#     ])

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#     pipe.fit(X_train, y_train)

#     preds = pipe.predict(X_test)
#     print("Classification report on test data:\n")
#     print(classification_report(y_test, preds))

#     joblib.dump(pipe, out_path)
#     print(f"\n✅ Saved improved model pipeline to {out_path}")


# if __name__ == "__main__":
#     here = os.path.dirname(__file__)
#     out = os.path.join(here, "model.pkl")
#     build_and_save_model(out)

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import classification_report


def make_synthetic(n=2000, random_state=42):
    rng = np.random.RandomState(random_state)
    applicant_income = rng.uniform(5000, 150000, size=n)     # realistic income range
    loan_amount = rng.uniform(10000, 500000, size=n)         # realistic loan range
    credit_history = rng.choice(["good", "bad"], size=n, p=[0.7, 0.3])
    employment_type = rng.choice(["salaried", "self-employed", "unemployed"],
                                 size=n, p=[0.6, 0.3, 0.1])

    approved = []
    for inc, loan_amt, ch, emp in zip(applicant_income, loan_amount, credit_history, employment_type):
        ratio = loan_amt / (inc + 1e-9)

        # Reject absurd loan-to-income ratios before even generating approval
        if ratio > 50:
            approved.append(0)
            continue

        # realistic approval rules
        if emp == "unemployed":
            approved.append(0)
        elif ch == "bad" and ratio > 2:
            approved.append(0)
        elif ratio < 3 and ch == "good" and emp != "unemployed":
            approved.append(1)
        elif ratio < 1.5:
            approved.append(1)
        else:
            approved.append(int(rng.rand() > 0.6))  # some randomness to avoid perfect rules

    df = pd.DataFrame({
        "applicant_income": applicant_income,
        "loan_amount": loan_amount,
        "credit_history": credit_history,
        "employment_type": employment_type,
        "approved": approved
    })

    # Drop any still-extreme rows (safety guard)
    df = df[df["loan_amount"] / (df["applicant_income"] + 1e-9) < 100]
    df = df.reset_index(drop=True)
    return df


def build_and_save_model(out_path="model.pkl"):
    df = make_synthetic()

    # Warn if extreme data still exists
    extreme_cases = df[df["loan_amount"] / (df["applicant_income"] + 1e-9) > 20]
    if not extreme_cases.empty:
        print(f"⚠️ Warning: {len(extreme_cases)} extreme loan-to-income cases remain in synthetic data.")

    X = df[["applicant_income", "loan_amount", "credit_history", "employment_type"]]
    y = df["approved"]

    num_features = ["applicant_income", "loan_amount"]
    cat_features = ["credit_history", "employment_type"]

    pre = ColumnTransformer([
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
    ])

    pipe = Pipeline([
        ("pre", pre),
        ("clf", DecisionTreeClassifier(max_depth=6, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)
    print("\nClassification report on test data:\n")
    print(classification_report(y_test, preds))

    joblib.dump(pipe, out_path)
    print(f"\n✅ Saved improved model pipeline to {out_path}")


def sanity_check_input(applicant_income, loan_amount):
    """
    Runtime sanity checker using consistent names.
    Returns a tuple (message, level) where level is "ok", "suspicious", or "unrealistic".
    """
    ratio = loan_amount / (applicant_income + 1e-9)
    if ratio > 100:
        msg = f"⚠️ Unrealistic input: loan is {ratio:.1f}× income — auto-reject likely."
        return msg, "unrealistic"
    if ratio > 20:
        msg = f"⚠️ Suspicious input: loan is {ratio:.1f}× income — model may be unreliable."
        return msg, "suspicious"
    return f"✅ Input looks reasonable (Loan-to-income ratio = {ratio:.2f}).", "ok"


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    out = os.path.join(here, "model.pkl")
    build_and_save_model(out)

    # Example sanity checks (for quick manual testing; remove or ignore in production)
    print(sanity_check_input(30000, 2_000_000_000_000))   # huge loan example
    print(sanity_check_input(200000, 100000000000000000)) # another extreme example

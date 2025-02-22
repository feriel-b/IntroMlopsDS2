import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
import mlflow
import mlflow.sklearn

#warnings.filterwarnings("ignore")

def prepare_data(train_path="churn_80.csv", test_path="churn_20.csv"):
    """Loads, cleans, and prepares data for training and evaluation using original ordinal encoding for categorical features."""
    df_80 = pd.read_csv(train_path)
    df_20 = pd.read_csv(test_path)

    # Fill missing values with mean for numeric columns
    for col in df_80.select_dtypes(include=["float64", "int64"]).columns:
        df_80[col].fillna(df_80[col].mean(), inplace=True)
        df_20[col].fillna(df_20[col].mean(), inplace=True)

    # Identify categorical features (including 'State')
    categorical_features = ['International plan', 'Voice mail plan']
    
    # Initialize the OrdinalEncoder and apply it to both datasets
    encoder = OrdinalEncoder()
    df_80[categorical_features] = encoder.fit_transform(df_80[categorical_features])
    df_20[categorical_features] = encoder.transform(df_20[categorical_features])

    # One-hot encode the "State" feature (to generate multiple columns, e.g., state_0 to state_6).
    df_80 = pd.get_dummies(df_80, columns=["State"], prefix="state")
    df_20 = pd.get_dummies(df_20, columns=["State"], prefix="state")
    
    
    # Convert the Churn feature to int (if necessary)
    df_80['Churn'] = df_80['Churn'].astype(int)
    df_20['Churn'] = df_20['Churn'].astype(int)
    
   

    # Normalize data using MinMaxScaler
    scaler = MinMaxScaler()
    df_80_scaled = pd.DataFrame(scaler.fit_transform(df_80), columns=df_80.columns)
    df_20_scaled = pd.DataFrame(scaler.transform(df_20), columns=df_20.columns)

    # Drop redundant features if needed
    drop_cols = ["Total day charge", "Total eve charge", "Total night charge", "Total intl charge"]
    df_80_scaled.drop(columns=drop_cols, inplace=True, errors="ignore")
    df_20_scaled.drop(columns=drop_cols, inplace=True, errors="ignore")

    # Separate features and labels
    X_train = df_80_scaled.drop(columns=["Churn"])
    y_train = df_80_scaled["Churn"]
    X_test = df_20_scaled.drop(columns=["Churn"])
    y_test = df_20_scaled["Churn"]
    
    pd.set_option('display.max_columns', None)

    print(" Data preparation !")
    print(X_train.head())

    return X_train, y_train, X_test, y_test

def train_model(X_train, y_train, X_test, y_test, C=1.0, kernel='rbf', gamma='scale'):
    """Trains an SVM model and logs with MLflow, returns (model, test_accuracy)."""
    
    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")

    with mlflow.start_run():
        model = SVC(C=C, kernel=kernel, gamma=gamma, random_state=42)
        model.fit(X_train, y_train)

        # Log hyperparameters for SVM
        mlflow.log_param("C", C)
        mlflow.log_param("kernel", kernel)
        mlflow.log_param("gamma", gamma)

        # Log metrics
        train_acc = accuracy_score(y_train, model.predict(X_train))
        test_acc = accuracy_score(y_test, model.predict(X_test))
        mlflow.log_metric("train_accuracy", train_acc)
        mlflow.log_metric("test_accuracy", test_acc)

        # Log the model with MLflow
        mlflow.sklearn.log_model(model, "svm_model")

        # Save locally with a filename based on hyperparameters
        joblib.dump(model, f"churn_model_{C}_{kernel}_{gamma}.joblib")
        print(f"✅ Model trained and logged with MLflow (C={C}, kernel={kernel}, gamma={gamma})")

    return model,test_acc

def save_model(model, filename="churn_model.joblib"):
    """Saves the given model to a file."""
    joblib.dump(model, filename)
    print(f"💾 Model saved as {filename}")

def load_model(model_path="churn_model.joblib"):
    """Loads the trained model."""
    try:
        return joblib.load(model_path)
    except FileNotFoundError:
        raise ValueError("Aucun modèle trouvé. Exécutez d'abord l'entraînement!")

def retrain_model(C=1.0, kernel='rbf', gamma='scale'):
    """Retrains the SVM model with new hyperparameters."""
    X_train, y_train, _, _ = prepare_data()
    model = SVC(C=C, kernel=kernel, gamma=gamma, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, "churn_model.joblib")
    print("✅ Model retrained and saved!")
   
def evaluate_model(model, X_test, y_test):
    """Evaluates the model on test data and prints metrics."""
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {acc:.2f}")
    print("\n🔍 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["No Churn", "Churn"]))
    return acc
    

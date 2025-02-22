import argparse
from pipeline import (
    prepare_data,
    train_model,
    evaluate_model,
    save_model,
    load_model,
)

def main(args):
    if args.prepare:
        print("\n🔄 Préparation des données...")
        prepare_data("churn_80.csv", "churn_20.csv")
        print("✅ Données préparées et enregistrées !")

    elif args.train:
        print("\n🚀 Chargement et préparation des données...")
        X_train, y_train, X_test, y_test = prepare_data("churn_80.csv", "churn_20.csv")

        print("\n🎯 Entraînement du modèle avec hyperparameter tuning...")

        # Define hyperparameter grid for SVM
        C_list = [0.1, 1.0, 10.0]
        gamma_list = ['scale', 'auto']
        kernel_list = ['rbf']  # You can add more kernels if needed

        # Grid search: train models with different hyperparameters
        for C in C_list:
            for gamma in gamma_list:
                for kernel in kernel_list:
                    print(f"\n🚀 Training with C={C}, gamma={gamma}, kernel={kernel}")
                    model = train_model(
                        X_train, y_train, X_test, y_test,
                        C=C,
                        kernel=kernel,
                        gamma=gamma
                    )

                    # Save each trained model
                    filename = f"churn_model_{C}_{kernel}_{gamma}.joblib"
                    save_model(model, filename)

        print("\n✅ Hyperparameter tuning completed and models saved!")

    elif args.evaluate:
        print("\n📂 Chargement du modèle...")
        model = load_model()

        print("\n📊 Chargement et préparation des données de test...")
        X_train, y_train, X_test, y_test = prepare_data("churn_80.csv", "churn_20.csv")

        print("\n🔍 Évaluation du modèle...")
        evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de prédiction du Churn")

    parser.add_argument("--prepare", action="store_true", help="Préparer les données")
    parser.add_argument("--train", action="store_true", help="Entraîner le modèle")
    parser.add_argument("--evaluate", action="store_true", help="Évaluer le modèle")

    args = parser.parse_args()
    main(args)

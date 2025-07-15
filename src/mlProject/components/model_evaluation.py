import os
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, average_precision_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from pathlib import Path
from mlProject.utils.common import save_json
from mlProject.entity.config_entity import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred, proba):
        f1 = f1_score(actual, pred)
        precision = precision_score(actual, pred)
        recall = recall_score(actual, pred)
        roc_auc = roc_auc_score(actual, proba)
        avg_precision = average_precision_score(actual, proba)

        return f1, precision, recall, roc_auc, avg_precision


    def log_into_mlflow(self):

        data = pd.read_csv(self.config.data_path)
        data['Tenure'] = 2025 - data['JoiningYear']
        X = data.drop(self.config.target_column,axis =1)
        y = data[self.config.target_column]

        model = joblib.load(self.config.model_path) # loading the model

        # Define stratified k-fold
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        # Initialize metrics
        f1_scores, precisions, recalls, auc_roc_scores, auc_pr_scores = [], [], [], [], []


        mlflow.set_registry_uri(self.config.mlflow_uri) # doing everything inside a remote server
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme


        with mlflow.start_run():
            # Cross-validation
            for fold, (train_index, test_index) in enumerate(skf.split(X, y), 1):
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                y_train, y_test = y.iloc[train_index], y.iloc[test_index]
                
                # Fit model on training fold
                model.fit(X_train, y_train)
                
                # Predict on test fold
                y_pred = model.predict(X_test)
                y_proba = model.predict_proba(X_test)[:, 1]
                
                # Compute metrics
                f1, precision, recall, roc_auc, avg_precision = self.eval_metrics(y_test, y_pred, y_proba)
                
                # Store metrics
                f1_scores.append(f1)
                precisions.append(precision)
                recalls.append(recall)
                auc_roc_scores.append(roc_auc)
                auc_pr_scores.append(avg_precision)
                
                # Log per-fold metrics
                mlflow.log_metric(f"f1_score_fold_{fold}", f1)
                mlflow.log_metric(f"precision_fold_{fold}", precision)
                mlflow.log_metric(f"recall_fold_{fold}", recall)
                mlflow.log_metric(f"auc_roc_fold_{fold}", roc_auc)
                mlflow.log_metric(f"auc_pr_fold_{fold}", avg_precision)
                print(f"Fold {fold}: F1={f1:.4f}, Precision={precision:.4f}, Recall={recall:.4f}, AUC-ROC={roc_auc:.4f}, AUC-PR={avg_precision:.4f}")

            # Compute average and std
            avg_f1 = np.mean(f1_scores)
            std_f1 = np.std(f1_scores)
            avg_precision = np.mean(precisions)
            avg_recall = np.mean(recalls)
            avg_auc_roc = np.mean(auc_roc_scores)
            avg_auc_pr = np.mean(auc_pr_scores)

            # Log average metrics
            mlflow.log_metric("avg_f1_score", avg_f1)
            mlflow.log_metric("std_f1_score", std_f1)
            mlflow.log_metric("avg_precision", avg_precision)
            mlflow.log_metric("avg_recall", avg_recall)
            mlflow.log_metric("avg_auc_roc", avg_auc_roc)
            mlflow.log_metric("avg_auc_pr", avg_auc_pr)

            # Save metrics locally using save_json
            scores = {
                "avg_f1_score": avg_f1,
                "std_f1_score": std_f1,
                "avg_precision": avg_precision,
                "avg_recall": avg_recall,
                "avg_auc_roc": avg_auc_roc,
                "avg_auc_pr": avg_auc_pr,
                "f1_scores": f1_scores,
                "precisions": precisions,
                "recalls": recalls,
                "auc_roc_scores": auc_roc_scores,
                "auc_pr_scores": auc_pr_scores
            }
            save_json(path=Path(self.config.metric_file_name), data=scores)

            # Log model parameters
            mlflow.log_params(self.config.all_params)

            # Log model
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name="GradientBoostingClassifier")
            else:
                mlflow.sklearn.log_model(model, "model")

            print(f"Average F1-score: {avg_f1:.4f}, Std: {std_f1:.4f}")
            print(f"Average Precision: {avg_precision:.4f}")
            print(f"Average Recall: {avg_recall:.4f}")
            print(f"Average AUC-ROC: {avg_auc_roc:.4f}")
            print(f"Average AUC-PR: {avg_auc_pr:.4f}")
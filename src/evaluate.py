import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, roc_curve, auc
from sklearn.preprocessing import label_binarize

MODEL_DIR = "models"
REPORT_DIR = "reports"
TEST_DATA_PATH = os.path.join(MODEL_DIR, "test_set.csv")

def evaluate_models():
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    print("Loading test data...")
    if not os.path.exists(TEST_DATA_PATH):
        print("Test data not found. Run src/train.py first.")
        return

    df_test = pd.read_csv(TEST_DATA_PATH)
    X_test = df_test.drop(columns=['Label_Encoded'])
    y_test = df_test['Label_Encoded']
    
    # Load Models
    rf = joblib.load(os.path.join(MODEL_DIR, "rf_model.pkl"))
    xgb = joblib.load(os.path.join(MODEL_DIR, "xgb_model.pkl"))
    # IsoForest requires boolean conversion, omitting from standard comparison for simplicity in this script
    
    models = {"Random Forest": rf, "XGBoost": xgb}
    
    with open(os.path.join(REPORT_DIR, "evaluation_metrics.txt"), "w") as f:
        f.write("AI-NIDS Model Evaluation Report\n")
        f.write("================================\n\n")

        for name, model in models.items():
            print(f"Evaluating {name}...")
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)
            
            # Metrics
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            # Confusion Matrix for FPR calculation
            cm = confusion_matrix(y_test, y_pred)
            # FP / (FP + TN) - simplified for multi-class macro average manually or via library
            # Here we just dump the CM
            
            # Confusion Matrix Plot
            if name == "Random Forest":
                plt.figure(figsize=(6, 5))
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['BENIGN', 'DDoS', 'PortScan'], yticklabels=['BENIGN', 'DDoS', 'PortScan'])
                plt.title('Confusion Matrix - Random Forest')
                plt.ylabel('True Label')
                plt.xlabel('Predicted Label')
                plt.tight_layout()
                plt.savefig(os.path.join(REPORT_DIR, "confusion_matrix.png"))
                plt.close()

            # ROC AUC (One vs Rest)
            n_classes = len(np.unique(y_test))
            if n_classes > 2:
                y_test_bin = label_binarize(y_test, classes=sorted(np.unique(y_test)))
                try:
                    roc = roc_auc_score(y_test_bin, y_prob, average='weighted', multi_class='ovr')
                    
                    # Plot ROC for RF
                    if name == "Random Forest":
                         fpr = dict()
                         tpr = dict()
                         roc_auc = dict()
                         for i in range(n_classes):
                             fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_prob[:, i])
                             roc_auc[i] = auc(fpr[i], tpr[i])

                         plt.figure(figsize=(8, 6))
                         colors = ['blue', 'red', 'green']
                         classes = ['BENIGN', 'DDoS', 'PortScan']
                         for i, color in zip(range(n_classes), colors):
                             plt.plot(fpr[i], tpr[i], color=color, lw=2,
                                      label='ROC curve of class {0} (area = {1:0.2f})'
                                      ''.format(classes[i], roc_auc[i]))
                         plt.plot([0, 1], [0, 1], 'k--', lw=2)
                         plt.xlim([0.0, 1.0])
                         plt.ylim([0.0, 1.05])
                         plt.xlabel('False Positive Rate')
                         plt.ylabel('True Positive Rate')
                         plt.title('Receiver Operating Characteristic (RF)')
                         plt.legend(loc="lower right")
                         plt.savefig(os.path.join(REPORT_DIR, "roc_curve.png"))
                         plt.close()

                except Exception as e:
                    print(f"ROC Error: {e}")
                    roc = "N/A"
            else:
                 roc = roc_auc_score(y_test, y_prob[:, 1])

            # Report Writing
            f.write(f"--- {name} ---\n")
            f.write(f"Accuracy:  {acc:.4f}\n")
            f.write(f"Precision: {prec:.4f}\n")
            f.write(f"Recall:    {rec:.4f}\n")
            f.write(f"F1 Score:  {f1:.4f}\n")
            f.write(f"ROC-AUC:   {roc}\n")
            f.write(f"Confusion Matrix:\n{cm}\n\n")
            
            # Feature Importance
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                indices = np.argsort(importances)[::-1]
                cols = X_test.columns
                
                f.write("Top 5 Features:\n")
                for i in range(5):
                    f.write(f"{i+1}. {cols[indices[i]]} ({importances[indices[i]]:.4f})\n")
                f.write("\n")

    print(f"Evaluation complete. Report saved to {REPORT_DIR}/evaluation_metrics.txt")

if __name__ == "__main__":
    evaluate_models()

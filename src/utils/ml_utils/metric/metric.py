from src.entity.artifact_entity import ClassificationMetricArtifact
from src.exceptions.exceptions import NetworkSecurityException
from sklearn.metrics import f1_score, precision_score, recall_score
import sys

def classification_metric(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true,y_pred)
        model_recall_score = recall_score(y_true,y_pred)
        model_precission_score = precision_score(y_true,y_pred)
        classification_metric = ClassificationMetricArtifact(model_f1_score,model_precission_score,model_recall_score)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)
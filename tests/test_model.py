import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from train import train_models

def test_train_models():
    output = train_models()

    assert "log_reg_model" in output
    assert "random_forest_model" in output
    assert "comparison_table" in output

    table = output["comparison_table"]
    assert "accuracy" in table.columns

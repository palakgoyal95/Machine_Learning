import sys
import os
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    import ml_model.predict as predict
except Exception:
    print('IMPORT_ERROR')
    traceback.print_exc()
    sys.exit(1)

sample = "Experienced Python developer with SQL, Pandas, NumPy, AWS and Docker. Built ETL pipelines and models."

try:
    out = predict.predict_resume(sample)
    print('PREDICTION_OUTPUT:')
    import json
    print(json.dumps(out, indent=2))
except Exception:
    print('PREDICT_ERROR')
    traceback.print_exc()
    sys.exit(1)

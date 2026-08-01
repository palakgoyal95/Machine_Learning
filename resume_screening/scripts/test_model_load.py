import traceback
import sys

import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    import ml_model.predict as predict
except Exception as e:
    print('IMPORT_ERROR')
    traceback.print_exc()
    sys.exit(1)

try:
    print('MODEL_TYPE:', type(predict.model))
    print('HAS_PREDICT_PROBA:', hasattr(predict.model, 'predict_proba'))
    print('CLASSES:', getattr(predict.model, 'classes_', None))
    print('VECT_TYPE:', type(predict.vectorizer))
except Exception:
    print('LOAD_ERROR')
    traceback.print_exc()
    sys.exit(1)

print('OK')

import json
import os
from functools import wraps
from datetime import datetime

class DbCContract:
    def __init__(self, log_file="contract_violations.json"):
        self.log_file = log_file
        self.violations = []
        self._load_existing()
    
    def _load_existing(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.violations = json.load(f)
            except:
                self.violations = []
    
    def _save_violations(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.violations, f, indent=2)
    
    def _serialize_args(self, obj):
        if hasattr(obj, '__dict__'):
            return str({k: v for k, v in obj.__dict__.items() if not k.startswith('_')})
        return str(obj)
    
    def _log_violation(self, contract_type, function_name, message, details=None):
        safe_details = {}
        if details:
            for k, v in details.items():
                if isinstance(v, (list, tuple)):
                    safe_details[k] = [self._serialize_args(x) for x in v]
                else:
                    safe_details[k] = self._serialize_args(v)
        
        violation = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": contract_type,
            "function": function_name,
            "message": message,
            "details": safe_details
        }
        self.violations.append(violation)
        self._save_violations()
    
    def requires(self, condition, error_msg="Precondition failed"):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not condition(*args, **kwargs):
                    self._log_violation(
                        "PRECONDITION", 
                        func.__name__, 
                        error_msg,
                        {"args": args, "kwargs": kwargs}
                    )
                    raise ValueError(error_msg)
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def ensures(self, condition, error_msg="Postcondition failed"):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not condition(result, *args, **kwargs):
                    self._log_violation(
                        "POSTCONDITION",
                        func.__name__,
                        error_msg,
                        {"result": result, "args": args, "kwargs": kwargs}
                    )
                    raise ValueError(error_msg)
                return result
            return wrapper
        return decorator

dbc = DbCContract()
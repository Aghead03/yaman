import sys
import importlib
import os
import traceback

# 👇 حدد ملف الإعدادات تبع مشروعك (غير yaman.settings إذا اسمك مختلف)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yaman.settings")

loaded_modules = set()

def trace_imports(frame, event, arg):
    if event == "call":
        code = frame.f_code
        filename = code.co_filename
        if filename.endswith(".py"):
            module_name = frame.f_globals.get("name")
            if module_name not in loaded_modules:
                loaded_modules.add(module_name)
                print(f"📦 Importing: {module_name} from {filename}")
    return trace_imports

sys.settrace(trace_imports)

try:
    importlib.import_module("yaman.urls")  # غير yaman.urls لو اسم ملف urls مختلف
except Exception:
    print("\n❌ حصل خطأ أثناء الاستيراد:\n")
    traceback.print_exc()

sys.settrace(None)
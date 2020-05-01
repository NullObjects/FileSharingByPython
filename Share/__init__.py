import sys
import os
#引用Model模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == "__main__":
    print("===== ===== Path ===== =====")
    for item in sys.path:
        print(item)
    print("===== ===== Path ===== =====")
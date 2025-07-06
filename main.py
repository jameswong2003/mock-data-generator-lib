import importlib.util
import inspect
import os
import sys
from typing import List, Type, Dict, Any

import helper.random_helper as random_helper

def extract_class(file_path: str) -> List[Type]:
    """
    Given a file path, extract classes within the file
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f'Cannot import module from {file_path}')

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    classes = [
        obj for name, obj in vars(module).items()
        if inspect.isclass(obj) and obj.__module__ == module.__name__
    ]

    return classes


def extract_attributes(clazz: Type) -> Dict[str, tuple[Any, str]]:
    """
    Extracts non-callable, non-special class attributes and their types.
    Returns a dictionary of attribute name -> (value, type name).
    """
    attrs = {
        name: (value, type(value).__name__)
        for name, value in vars(clazz).items()
        if not name.startswith('__') and not callable(value)
    }
    return attrs


def randomize_attributes(attr: Dict[str, tuple[Any, str]], known_classes: Dict[str, Type]) -> Dict[str, Any]:
    mock_data = {}
    for key, (value, type_name) in attr.items():
        if type_name == 'int':
            mock_data[key] = random_helper.random_n_int(3)
        elif type_name == 'float':
            mock_data[key] = random_helper.random_float_num(0, 999, 2)
        elif type_name == 'str':
            mock_data[key] = random_helper.random_n_chars(5, set(['a', 'b', 'c', 'd']))
        elif type_name == 'bool':
            mock_data[key] = random_helper.random_bool()
        elif type_name in known_classes:
            # If type is of classes instead of primitive
            nested_class = known_classes[type_name]
            nested_attrs = extract_attributes(nested_class)
            mock_data[key] = randomize_attributes(nested_attrs, known_classes)
        else:
            # Doesn't exist within known_classes
            mock_data[key] = f"<unsupported type: {type_name}>"
    return mock_data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_classes.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        class_objs = extract_class(file_path)
        class_map = {cls.__name__: cls for cls in class_objs}

        print(f"Found {len(class_objs)} class(es):")
        for cls in class_objs:
            print(f"\nClass: {cls.__name__}")
            attrs = extract_attributes(cls)
            print("  Attributes:", attrs)
            randomized = randomize_attributes(attrs, class_map)
            print("  Randomized:", randomized)

    except Exception as e:
        print(f"Error: {e}")

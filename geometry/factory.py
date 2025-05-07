from typing import Any, Dict, Type
from .shapes import Shape, Circle, Triangle, Square


class ShapeFactory:
    _registry: Dict[str, Type[Shape]] = {
        'circle': Circle,
        'triangle': Triangle,
        'square': Square,
    }

    @classmethod
    def create(cls, shape_type: str, *args, **kwargs) -> Shape:
        if shape_type not in cls._registry:
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")
        return cls._registry[shape_type](*args, **kwargs)

    @classmethod
    def register_shape(cls, name: str, shape_cls: Type[Shape]):
        if not issubclass(shape_cls, Shape):
            raise TypeError("Класс должен наследовать Shape")
        cls._registry[name] = shape_cls

import unittest
from geometry.shapes import Circle, Triangle
from geometry.factory import ShapeFactory
import math


class TestShapes(unittest.TestCase):

    def test_circle_area(self):
        c = Circle(1)
        self.assertAlmostEqual(c.area(), math.pi)

    def test_triangle_area(self):
        t = Triangle(3, 4, 5)
        self.assertAlmostEqual(t.area(), 6.0)

    def test_invalid_triangle(self):
        with self.assertRaises(ValueError):
            Triangle(1, 2, 10)

    def test_right_triangle(self):
        t = Triangle(3, 4, 5)
        self.assertTrue(t.is_right_triangle())

    def test_not_right_triangle(self):
        t = Triangle(3, 4, 6)
        self.assertFalse(t.is_right_triangle())

    def test_factory_circle(self):
        shape = ShapeFactory.create('circle', 2)
        self.assertIsInstance(shape, Circle)
        self.assertAlmostEqual(shape.area(), math.pi * 4)

    def test_factory_triangle(self):
        shape = ShapeFactory.create('triangle', 3, 4, 5)
        self.assertIsInstance(shape, Triangle)
        self.assertAlmostEqual(shape.area(), 6.0)

    def test_factory_invalid(self):
        with self.assertRaises(ValueError):
            ShapeFactory.create('square', 2)

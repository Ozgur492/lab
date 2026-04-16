import unittest
from cart import ShoppingCart

class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item(self):
        self.cart.add_item("Laptop", 999.99, 1)
        self.assertEqual(self.cart._items["Laptop"]["quantity"], 1)

    def test_remove_item(self):
        self.cart.add_item("Mouse", 25.0, 1)
        self.cart.remove_item("Mouse")
        self.assertNotIn("Mouse", self.cart._items)

    def test_get_total(self):
        self.cart.add_item("Keyboard", 75.0, 1)
        self.cart.add_item("Monitor", 300.0, 2)
        self.assertEqual(self.cart.get_total(), 675.0)

    def test_fixed_discount(self):
        self.cart.add_item("Headphones", 40.0, 1)
        self.cart.apply_discount("FLAT5")
        self.assertEqual(self.cart.get_total(), 35.0)

    def test_clear(self):
        self.cart.add_item("Webcam", 60.0, 1)
        self.cart.clear()
        self.assertEqual(self.cart._items, {})

    def test_zero_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("SSD", 120.0, 0)

    def test_remove_nonexistent_raises(self):
        with self.assertRaises(KeyError):
            self.cart.remove_item("GPU")

    def test_invalid_discount_code(self):
        self.cart.add_item("RAM", 50.0, 1)
        with self.assertRaises(ValueError):
            self.cart.apply_discount("FAKE")

    def test_below_minimum_order(self):
        self.cart.add_item("USB Cable", 10.0, 1)
        with self.assertRaises(ValueError):
            self.cart.apply_discount("FLAT5")

    # bug var burada, > yerine >= olmasi lazim ama > kullanmis
    # 30 dolarin ustu istiyosa 30 da gecmeli ama gecmiyo
    def test_exact_threshold_bug(self):
        self.cart.add_item("Mousepad", 30.0, 1)
        with self.assertRaises(ValueError):
            self.cart.apply_discount("FLAT5")

    # yuzde indirimi calismıyo cunku // kullanmis / yerine
    # 10 // 100 = 0 oluyo yani indirim hic uygulanmiyo
    def test_percent_discount_bug(self):
        self.cart.add_item("Tablet", 100.0, 1)
        self.cart.apply_discount("SAVE10")
        self.assertEqual(self.cart.get_total(), 100.0)  # 90 olmasi lazimdi

    # ayni itemi ekliyince quantity ustune eklemesi lazim += ile
    # ama = ile yazmis yani 3+2=5 yerine sadece 2 oluyo
    def test_add_same_item_twice_bug(self):
        self.cart.add_item("Pen", 5.0, 3)
        self.cart.add_item("Pen", 5.0, 2)
        self.assertEqual(self.cart._items["Pen"]["quantity"], 2)  # 5 olmasi lazim

    # clear yapinca discount sifirlanmiyo, _discount = None yapmamis
    def test_clear_no_discount_reset_bug(self):
        self.cart.add_item("Monitor", 200.0, 1)
        self.cart.apply_discount("SAVE10")
        self.cart.clear()
        self.assertIsNotNone(self.cart._discount)  # None olmasi lazimdi aslinda

# tdd kismi - once testleri yazdim sonra implement ettim
class TestGetItemCount(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_empty(self):
        self.assertEqual(self.cart.get_item_count(), 0)

    def test_multiple_items(self):
        self.cart.add_item("Keyboard", 75.0, 2)
        self.cart.add_item("Mouse", 25.0, 3)
        self.assertEqual(self.cart.get_item_count(), 5)

    def test_after_remove(self):
        self.cart.add_item("Keyboard", 75.0, 2)
        self.cart.add_item("Mouse", 25.0, 3)
        self.cart.remove_item("Keyboard")
        self.assertEqual(self.cart.get_item_count(), 3)

if __name__ == "__main__":
    unittest.main()

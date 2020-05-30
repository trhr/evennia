"""
Unit tests for typeclass base system

"""
from django.test import override_settings
from evennia.utils.test_resources import EvenniaTest
from mock import patch

# ------------------------------------------------------------
# Manager tests
# ------------------------------------------------------------


class TestAttributes(EvenniaTest):
    def test_attrhandler(self):
        key = "testattr"
        value = "test attr value "
        self.obj1.attributes.add(key, value)
        self.assertEqual(self.obj1.attributes.get(key), value)
        self.obj1.db.testattr = value
        self.assertEqual(self.obj1.db.testattr, value)

    @override_settings(TYPECLASS_AGGRESSIVE_CACHE=False)
    @patch("evennia.typeclasses.attributes._TYPECLASS_AGGRESSIVE_CACHE", False)
    def test_attrhandler_nocache(self):
        key = "testattr"
        value = "test attr value "
        self.obj1.attributes.add(key, value)
        self.assertFalse(self.obj1.attributes._cache)

        self.assertEqual(self.obj1.attributes.get(key), value)
        self.obj1.db.testattr = value
        self.assertEqual(self.obj1.db.testattr, value)
        self.assertFalse(self.obj1.attributes._cache)

    def test_weird_text_save(self):
        "test 'weird' text type (different in py2 vs py3)"
        from django.utils.safestring import SafeText

        key = "test attr 2"
        value = SafeText("test attr value 2")
        self.obj1.attributes.add(key, value)
        self.assertEqual(self.obj1.attributes.get(key), value)


class TestTypedObjectManager(EvenniaTest):
    def _manager(self, methodname, *args, **kwargs):
        return list(getattr(self.obj1.__class__.objects, methodname)(*args, **kwargs))

    def test_get_by_tag_no_category(self):
        self.obj1.tags.add("tag1")
        self.obj1.tags.add("tag2")
        self.obj1.tags.add("tag2c")
        self.obj2.tags.add("tag2")
        self.obj2.tags.add("tag2a")
        self.obj2.tags.add("tag2b")
        self.obj2.tags.add("tag3 with spaces")
        self.obj2.tags.add("tag4")
        self.obj2.tags.add("tag2c")
        self.assertEqual(self._manager("get_by_tag", "tag1"), [self.obj1])
        self.assertEqual(
            set(self._manager("get_by_tag", "tag2")), set([self.obj1, self.obj2])
        )
        self.assertEqual(self._manager("get_by_tag", "tag2a"), [self.obj2])
        self.assertEqual(self._manager("get_by_tag", "tag3 with spaces"), [self.obj2])
        self.assertEqual(self._manager("get_by_tag", ["tag2a", "tag2b"]), [self.obj2])
        self.assertEqual(self._manager("get_by_tag", ["tag2a", "tag1"]), [])
        self.assertEqual(
            self._manager("get_by_tag", ["tag2a", "tag4", "tag2c"]), [self.obj2]
        )

    def test_get_by_tag_and_category(self):
        self.obj1.tags.add("tag5", "category1")
        self.obj1.tags.add("tag6")
        self.obj1.tags.add("tag7", "category1")
        self.obj1.tags.add("tag6", "category3")
        self.obj1.tags.add("tag7", "category4")
        self.obj2.tags.add("tag5", "category1")
        self.obj2.tags.add("tag5", "category2")
        self.obj2.tags.add("tag6", "category3")
        self.obj2.tags.add("tag7", "category1")
        self.obj2.tags.add("tag7", "category5")
        self.obj1.tags.add("tag8", "category6")
        self.obj2.tags.add("tag9", "category6")

        self.assertEqual(
            self._manager("get_by_tag", "tag5", "category1"), [self.obj1, self.obj2]
        )
        self.assertEqual(self._manager("get_by_tag", "tag6", "category1"), [])
        self.assertEqual(
            self._manager("get_by_tag", "tag6", "category3"), [self.obj1, self.obj2]
        )
        self.assertEqual(
            self._manager("get_by_tag", ["tag5", "tag6"], ["category1", "category3"]),
            [self.obj1, self.obj2],
        )
        self.assertEqual(
            self._manager("get_by_tag", ["tag5", "tag7"], "category1"),
            [self.obj1, self.obj2],
        )
        self.assertEqual(
            self._manager("get_by_tag", category="category1"), [self.obj1, self.obj2]
        )
        self.assertEqual(self._manager("get_by_tag", category="category2"), [self.obj2])
        self.assertEqual(
            self._manager("get_by_tag", category=["category1", "category3"]),
            [self.obj1, self.obj2],
        )
        self.assertEqual(
            self._manager("get_by_tag", category=["category1", "category2"]),
            [self.obj1, self.obj2],
        )
        self.assertEqual(
            self._manager("get_by_tag", category=["category5", "category4"]), []
        )
        self.assertEqual(
            self._manager("get_by_tag", category="category1"), [self.obj1, self.obj2]
        )
        self.assertEqual(
            self._manager("get_by_tag", category="category6"), [self.obj1, self.obj2]
        )

    def test_get_tag_with_all(self):
        self.obj1.tags.add("tagA", "categoryA")
        self.assertEqual(
            self._manager(
                "get_by_tag", ["tagA", "tagB"], ["categoryA", "categoryB"], match="all"
            ),
            [],
        )

    def test_get_tag_with_any(self):
        self.obj1.tags.add("tagA", "categoryA")
        self.assertEqual(
            self._manager(
                "get_by_tag", ["tagA", "tagB"], ["categoryA", "categoryB"], match="any"
            ),
            [self.obj1],
        )

    def test_get_tag_withnomatch(self):
        self.obj1.tags.add("tagC", "categoryC")
        self.assertEqual(
            self._manager(
                "get_by_tag", ["tagA", "tagB"], ["categoryA", "categoryB"], match="any"
            ),
            [],
        )

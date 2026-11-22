import unittest
import pandas as pd

from app.transformations.dataframe_transformations import DataframeTransformations


class TestTimestampOrder(unittest.TestCase):

    def get_events(self, timestamps, activities):
        df = pd.DataFrame({
            "case": ["Case 1"] * len(timestamps),
            "timestamp": timestamps,
            "event": activities,
        })

        transformation = DataframeTransformations()
        transformation.set_dataframe(df)
        return transformation.dataframe_to_cases_list()

    def test_dates_are_sorted(self):
        result = self.get_events(
            ["10.3.10", "9.3.10", "11.3.10"],
            ["B", "A", "C"],
        )
        self.assertEqual(result, [["A", "B", "C"]])

    def test_times_are_sorted(self):
        result = self.get_events(
            ["9.3.10 10:15", "9.3.10 8:05", "9.3.10 9:30"],
            ["C", "A", "B"],
        )
        self.assertEqual(result, [["A", "B", "C"]])

    def test_equal_timestamps_keep_order(self):
        result = self.get_events(
            ["9.3.10 9:00", "9.3.10 9:00", "9.3.10 8:00"],
            ["B", "C", "A"],
        )
        self.assertEqual(result, [["A", "B", "C"]])

    def test_original_dataframe_is_not_changed(self):
        df = pd.DataFrame({
            "case": ["Case 1", "Case 1"],
            "timestamp": ["10.3.10", "9.3.10"],
            "event": ["B", "A"],
        })
        original = df.copy(deep=True)

        transformation = DataframeTransformations()
        transformation.set_dataframe(df)
        transformation.dataframe_to_cases_list()

        pd.testing.assert_frame_equal(df, original)

    def test_legacy_timestamp_format(self):
        result = self.get_events(
            ["09-3-2004:15.01", "09-3-2004:8.05"],
            ["B", "A"],
        )
        self.assertEqual(result, [["A", "B"]])


if __name__ == "__main__":
    unittest.main()

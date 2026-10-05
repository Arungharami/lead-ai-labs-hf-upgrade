import unittest

import pandas as pd

from lead_ai_bench.data import prepare_frame


def fixture():
    return pd.DataFrame({
        "transaction_id": [str(i) for i in range(40)],
        "amount": list(range(40)),
        "is_fraud": [0] * 20 + [1] * 20,
    })


class TestDataContractRegressions(unittest.TestCase):
    def test_different_ids_do_not_hide_duplicate_features(self):
        frame = fixture()
        duplicate = frame.iloc[[0]].assign(transaction_id="another-id")
        x, y, _ = prepare_frame(pd.concat([frame, duplicate]))
        self.assertEqual(len(x), 40)
        self.assertEqual(len(y), 40)
        self.assertFalse(x.duplicated().any())

    def test_conflicting_labels_fail_before_splitting(self):
        frame = fixture()
        conflict = frame.iloc[[0]].assign(transaction_id="another-id", is_fraud=1)
        with self.assertRaisesRegex(ValueError, "conflicting"):
            prepare_frame(pd.concat([frame, conflict]))

    def test_fractional_labels_are_not_truncated(self):
        frame = fixture()
        frame["is_fraud"] = frame["is_fraud"].astype(float)
        frame.loc[0, "is_fraud"] = 0.7
        with self.assertRaisesRegex(ValueError, "binary classes"):
            prepare_frame(frame)

    def test_reserved_feature_name_remains_a_feature(self):
        frame = fixture().rename(columns={"amount": "__target__"})
        x, _, names = prepare_frame(frame)
        self.assertEqual(names, ["__target__"])
        self.assertEqual(x.iloc[-1, 0], 39)

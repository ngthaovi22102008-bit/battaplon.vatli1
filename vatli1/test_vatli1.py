import os
import tempfile
import unittest
from pathlib import Path

import vatli1


class TestVatLi1(unittest.TestCase):
    def setUp(self):
        self.danh_sach = [
            {'q': 2e-6, 'x': 0.0, 'y': 0.0},
            {'q': -4e-6, 'x': 3.0, 'y': 0.0},
            {'q': 3e-6, 'x': 1.5, 'y': 2.0},
        ]
        self.ket_qua = vatli1.tinh_luc_he_dien_tich(self.danh_sach)

    def test_tinh_luc_he_dien_tich_q1(self):
        q1 = self.ket_qua[1]
        self.assertAlmostEqual(q1['Fx_val'], 0.002816, places=6)
        self.assertAlmostEqual(q1['Fy_val'], -0.006912, places=6)
        self.assertAlmostEqual(q1['F_total'], 0.007463618425401984, places=6)

    def test_tinh_luc_he_dien_tich_q2(self):
        q2 = self.ket_qua[2]
        self.assertAlmostEqual(q2['Fx_val'], -0.018368, places=6)
        self.assertAlmostEqual(q2['Fy_val'], 0.013824, places=6)
        self.assertAlmostEqual(q2['F_total'], 0.02298883207124712, places=6)

    def test_ve_so_do_dien_tich_creates_png(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'test_plot.png'
            saved_path = vatli1.ve_so_do_dien_tich(
                self.danh_sach,
                self.ket_qua,
                str(output_path),
                show=False,
            )
            self.assertTrue(os.path.exists(saved_path))
            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)


if __name__ == '__main__':
    unittest.main()

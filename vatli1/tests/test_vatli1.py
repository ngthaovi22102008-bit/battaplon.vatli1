import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import vatli1


class TestVatLi1(unittest.TestCase):
    def setUp(self):
        self.danh_sach = [
            {'q': 2e-6, 'x': 0.0, 'y': 0.0},
            {'q': -4e-6, 'x': 3.0, 'y': 0.0},
            {'q': 3e-6, 'x': 1.5, 'y': 2.0},
        ]
        self.ket_qua = vatli1.tinh_luc_he_dien_tich(self.danh_sach)

    def test_q1_force_components(self):
        q1 = self.ket_qua[1]
        self.assertAlmostEqual(q1['Fx_val'], 0.002816, places=6)
        self.assertAlmostEqual(q1['Fy_val'], -0.006912, places=6)
        self.assertAlmostEqual(q1['F_total'], 0.007463618425401984, places=6)

    def test_q2_force_components(self):
        q2 = self.ket_qua[2]
        self.assertAlmostEqual(q2['Fx_val'], -0.018368, places=6)
        self.assertAlmostEqual(q2['Fy_val'], 0.013824, places=6)
        self.assertAlmostEqual(q2['F_total'], 0.02298883207124712, places=6)

    def test_q3_force_components(self):
        q3 = self.ket_qua[3]
        self.assertAlmostEqual(q3['Fx_val'], 0.015552, places=6)
        self.assertAlmostEqual(q3['Fy_val'], -0.006912, places=6)
        self.assertAlmostEqual(q3['F_total'], 0.017018826281503672, places=6)

    def test_two_charge_system_runs_without_error(self):
        danh_sach = [
            {'q': 1e-6, 'x': 0.0, 'y': 0.0},
            {'q': -2e-6, 'x': 2.0, 'y': 0.0},
        ]
        ket_qua = vatli1.tinh_luc_he_dien_tich(danh_sach)
        self.assertEqual(len(ket_qua), 2)
        self.assertGreater(ket_qua[1]['F_total'], 0.0)
        self.assertGreater(ket_qua[2]['F_total'], 0.0)

    def test_plot_export_creates_png(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'test_plot.png'
            saved_path = vatli1.ve_so_do_dien_tich(
                self.danh_sach,
                self.ket_qua,
                str(output_path),
                show=False,
            )
            self.assertTrue(Path(saved_path).exists())
            self.assertGreater(Path(saved_path).stat().st_size, 0)


if __name__ == '__main__':
    unittest.main()

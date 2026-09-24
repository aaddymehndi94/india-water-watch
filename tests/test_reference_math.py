"""Invented arithmetic fixtures only. No fixture represents observed India data."""
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import math
import unittest
from tools.reference_math import (finite, rainfall_departure, precipitation_volume_m3,
    aggregate_rainfall_departure, aggregate_storage_fill, ComparisonContext,
    comparison_problems, count_at_or_below, is_stale, forecast_active)

class ReferenceMathTests(unittest.TestCase):
    def test_rain_departure(self):
        self.assertAlmostEqual(rainfall_departure(80, 100), -20)
    def test_normal_and_zero_actual(self):
        self.assertEqual(rainfall_departure(30,30), 0)
        self.assertEqual(rainfall_departure(0,30), -100)
    def test_missing_and_zero_normal(self):
        for a,n in [(None,30),(30,None),(30,0),(0,0)]: self.assertIsNone(rainfall_departure(a,n))
    def test_negative_rain_rejected(self):
        for a,n in [(-1,30),(30,-1)]:
            with self.assertRaises(ValueError): rainfall_departure(a,n)
    def test_nonfinite_and_nonnumber_rejected(self):
        for v in [True,False,'5',None,float('nan'),float('inf'),-float('inf')]:
            with self.assertRaises(ValueError): finite(v,'fixture')
    def test_precipitation_volume_units(self):
        self.assertEqual(precipitation_volume_m3(2,3), 6000)
    def test_invalid_precipitation_area(self):
        for r,a in [(2,0),(2,-1),(-1,3)]:
            with self.assertRaises(ValueError): precipitation_volume_m3(r,a)
    def test_area_weighted_ratio_not_mean_percentage(self):
        rows=[(10,100,1),(190,200,2)]
        self.assertAlmostEqual(aggregate_rainfall_departure(rows),-22)
        self.assertNotAlmostEqual(aggregate_rainfall_departure(rows),(-90-5)/2)
    def test_empty_rainfall_rows_rejected(self):
        with self.assertRaises(ValueError): aggregate_rainfall_departure([])
    def test_partial_rainfall_coverage_rejected(self):
        with self.assertRaises(ValueError): aggregate_rainfall_departure([(5,10,1),(None,10,1)])
    def test_zero_aggregate_normal_is_unavailable(self):
        self.assertIsNone(aggregate_rainfall_departure([(0,0,1),(0,0,2)]))
    def test_invalid_aggregate_area(self):
        with self.assertRaises(ValueError): aggregate_rainfall_departure([(5,10,0)])
    def test_storage_ratio_of_sums(self):
        self.assertEqual(aggregate_storage_fill([(1,10),(90,100)]),100*91/110)
    def test_storage_above_capacity_not_clipped(self):
        self.assertEqual(aggregate_storage_fill([(11,10)]),110)
    def test_invalid_storage_rejected(self):
        for rows in [[],[(1,0)],[(-1,10)]]:
            with self.assertRaises(ValueError): aggregate_storage_fill(rows)
    def context(self):
        return ComparisonContext('rainfall','v1','mm','area-id','b1','series-id','normal-period','JJAS','season_to_date','09-23')
    def test_comparable_context_passes(self):
        c=self.context(); self.assertEqual(comparison_problems(c,c),[])
    def test_each_core_context_mismatch_rejected(self):
        c=self.context()
        for field in ('metric','definition_version','unit','geography','boundary_version','series','baseline','season','period_kind','cutoff_month_day'):
            with self.subTest(field=field):
                self.assertIn(f'{field}: mismatch',comparison_problems(c,replace(c,**{field:'different'})))
    def test_unknown_context_rejected(self):
        c=self.context(); self.assertIn('baseline: unknown',comparison_problems(c,replace(c,baseline='')))
    def test_cohort_and_population_mismatch(self):
        c=self.context()
        for field in ['cohort','population_basis']:
            self.assertIn(f'{field}: mismatch',comparison_problems(c,replace(c,**{field:'new'})))
    def test_historical_count_includes_ties(self):
        self.assertEqual(count_at_or_below([3,1,2,2,5],2),(3,5))
    def test_history_requires_eligible_values(self):
        with self.assertRaises(ValueError): count_at_or_below([],2)
        with self.assertRaises(ValueError): count_at_or_below([float('nan')],2)
    def test_stale_at_exact_boundary(self):
        t=datetime(2020,1,1,tzinfo=timezone.utc)
        self.assertFalse(is_stale(t,t+timedelta(days=1),timedelta(days=1)))
        self.assertTrue(is_stale(t,t+timedelta(days=1,seconds=1),timedelta(days=1)))
    def test_stale_rejects_future_and_negative_age(self):
        t=datetime(2020,1,1,tzinfo=timezone.utc)
        with self.assertRaises(ValueError): is_stale(t+timedelta(seconds=1),t,timedelta(days=1))
        with self.assertRaises(ValueError): is_stale(t,t,timedelta(days=-1))
    def test_naive_datetime_rejected(self):
        t=datetime(2020,1,1)
        with self.assertRaises(ValueError): is_stale(t,t,timedelta(days=1))
    def test_forecast_valid_and_expired(self):
        t=datetime(2020,1,1,tzinfo=timezone.utc); end=t+timedelta(days=1)
        self.assertTrue(forecast_active(t,t,end,t))
        self.assertFalse(forecast_active(t,t,end,end))
    def test_forecast_not_issued_or_not_yet_valid(self):
        t=datetime(2020,1,1,tzinfo=timezone.utc)
        self.assertFalse(forecast_active(t,t,t+timedelta(days=1),t-timedelta(seconds=1)))
        self.assertFalse(forecast_active(t,t+timedelta(hours=1),t+timedelta(days=1),t))
    def test_invalid_forecast_window(self):
        t=datetime(2020,1,1,tzinfo=timezone.utc)
        with self.assertRaises(ValueError): forecast_active(t,t,t,t)

if __name__=='__main__': unittest.main()

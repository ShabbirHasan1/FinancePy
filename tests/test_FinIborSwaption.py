###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

from financepy.products.rates.ibor_single_curve import IborSingleCurve
from financepy.models.bk_tree import BKTree
from financepy.models.hw_tree import HWTree
from financepy.models.sabr_shifted import SABRShifted
from financepy.models.sabr import SABR
from financepy.models.black_shifted import BlackShifted
from financepy.models.black import Black
from financepy.products.rates.ibor_swaption import SwapTypes
from financepy.products.rates.ibor_swaption import IborSwaption
from financepy.products.rates.ibor_swap import IborSwap
from financepy.products.rates.ibor_deposit import IborDeposit
from financepy.utils.frequency import FrequencyTypes
from financepy.utils.day_count import DayCountTypes
from financepy.utils.date import Date
import numpy as np


def build_curve(valuation_date):
    depoBasis = DayCountTypes.THIRTY_E_360_ISDA
    depos = []

    spot_days = 0
    settlement_date = valuation_date.add_weekdays(spot_days)
    deposit_rate = 0.05

    depo1 = IborDeposit(settlement_date, "1M", deposit_rate, depoBasis)
    depo2 = IborDeposit(settlement_date, "3M", deposit_rate, depoBasis)
    depo3 = IborDeposit(settlement_date, "6M", deposit_rate, depoBasis)

    depos.append(depo1)
    depos.append(depo2)
    depos.append(depo3)

    fras = []

    swaps = []
    fixedBasis = DayCountTypes.ACT_365F
    fixedFreq = FrequencyTypes.SEMI_ANNUAL
    fixed_leg_type = SwapTypes.PAY

    swap_rate = 0.05
    swap1 = IborSwap(settlement_date, "1Y", fixed_leg_type,
                     swap_rate, fixedFreq, fixedBasis)
    swap2 = IborSwap(settlement_date, "3Y", fixed_leg_type,
                     swap_rate, fixedFreq, fixedBasis)
    swap3 = IborSwap(settlement_date, "5Y", fixed_leg_type,
                     swap_rate, fixedFreq, fixedBasis)

    swaps.append(swap1)
    swaps.append(swap2)
    swaps.append(swap3)

    libor_curve = IborSingleCurve(valuation_date, depos, fras, swaps)

    return libor_curve


valuation_date = Date(1, 1, 2011)


exercise_date = Date(1, 1, 2012)
swapMaturityDate = Date(1, 1, 2017)

swapFixedFrequencyType = FrequencyTypes.SEMI_ANNUAL
swapFixedDayCountType = DayCountTypes.ACT_365F

model1 = Black(0.00001)
model2 = BlackShifted(0.00001, 0.0)
model3 = SABR(0.013, 0.5, 0.5, 0.5)
model4 = SABRShifted(0.013, 0.5, 0.5, 0.5, -0.008)
model5 = HWTree(0.00001, 0.00001)
model6 = BKTree(0.01, 0.01)

settlement_date = valuation_date.add_weekdays(2)

libor_curve = build_curve(valuation_date)


def test_pay():
    libor_curve = build_curve(valuation_date)
    swaptionType = SwapTypes.PAY

    k = 0.02
    swaption = IborSwaption(settlement_date,
                            exercise_date,
                            swapMaturityDate,
                            swaptionType,
                            k,
                            swapFixedFrequencyType,
                            swapFixedDayCountType)

    swap1 = swaption.value(valuation_date, libor_curve, model1)
    swap2 = swaption.value(valuation_date, libor_curve, model2)
    swap3 = swaption.value(valuation_date, libor_curve, model3)
    swap4 = swaption.value(valuation_date, libor_curve, model4)
    swap5 = swaption.value(valuation_date, libor_curve, model5)
    swap6 = swaption.value(valuation_date, libor_curve, model6)
    assert round(swap1, 1) == 125086.9
    assert round(swap2, 1) == 125086.9
    assert round(swap3, 1) == 125086.9
    assert round(swap4, 1) == 125086.9
    assert round(swap5, 1) == 125683.7
    assert round(swap6, 1) == 124501.2

    k = 0.035
    swaption = IborSwaption(settlement_date,
                            exercise_date,
                            swapMaturityDate,
                            swaptionType,
                            k,
                            swapFixedFrequencyType,
                            swapFixedDayCountType)

    swap1 = swaption.value(valuation_date, libor_curve, model1)
    swap2 = swaption.value(valuation_date, libor_curve, model2)
    swap3 = swaption.value(valuation_date, libor_curve, model3)
    swap4 = swaption.value(valuation_date, libor_curve, model4)
    swap5 = swaption.value(valuation_date, libor_curve, model5)
    swap6 = swaption.value(valuation_date, libor_curve, model6)
    assert round(swap1, 4) == 62492.5528
    assert round(swap2, 4) == 62492.5528
    assert round(swap3, 4) == 62492.5645
    assert round(swap4, 4) == 62492.8429
    assert round(swap5, 4) == 63098.4538
    assert round(swap6, 4) == 62307.1897

    k = 0.065
    swaption = IborSwaption(settlement_date,
                            exercise_date,
                            swapMaturityDate,
                            swaptionType,
                            k,
                            swapFixedFrequencyType,
                            swapFixedDayCountType)

    swap1 = swaption.value(valuation_date, libor_curve, model1)
    swap2 = swaption.value(valuation_date, libor_curve, model2)
    swap3 = swaption.value(valuation_date, libor_curve, model3)
    swap4 = swaption.value(valuation_date, libor_curve, model4)
    swap5 = swaption.value(valuation_date, libor_curve, model5)
    swap6 = swaption.value(valuation_date, libor_curve, model6)
    assert round(swap1, 4) == 0.0
    assert round(swap2, 4) == 0.0
    assert round(swap3, 4) == 22.1029
    assert round(swap4, 4) == 60.3266
    assert round(swap5, 4) == 0.0
    assert round(swap6, 4) == 0.0


def test_receive():
    swaptionType = SwapTypes.RECEIVE

    k = 0.02
    swaption = IborSwaption(settlement_date,
                            exercise_date,
                            swapMaturityDate,
                            swaptionType,
                            k,
                            swapFixedFrequencyType,
                            swapFixedDayCountType)

    swap1 = swaption.value(valuation_date, libor_curve, model1)
    swap2 = swaption.value(valuation_date, libor_curve, model2)
    swap3 = swaption.value(valuation_date, libor_curve, model3)
    swap4 = swaption.value(valuation_date, libor_curve, model4)
    swap5 = swaption.value(valuation_date, libor_curve, model5)
    swap6 = swaption.value(valuation_date, libor_curve, model6)
    assert round(swap1, 4) == 0.0
    assert round(swap2, 4) == 0.0
    assert round(swap3, 4) == 0.0
    assert round(swap4, 4) == 0.0046
    assert round(swap5, 4) == 0.0
    assert round(swap6, 4) == 0.0

    k = 0.05
    swaption = IborSwaption(settlement_date,
                            exercise_date,
                            swapMaturityDate,
                            swaptionType,
                            k,
                            swapFixedFrequencyType,
                            swapFixedDayCountType)

    swap1 = swaption.value(valuation_date, libor_curve, model1)
    swap2 = swaption.value(valuation_date, libor_curve, model2)
    swap3 = swaption.value(valuation_date, libor_curve, model3)
    swap4 = swaption.value(valuation_date, libor_curve, model4)
    swap5 = swaption.value(valuation_date, libor_curve, model5)
    swap6 = swaption.value(valuation_date, libor_curve, model6)
    assert round(swap1, 4) == 101.7984
    assert round(swap2, 4) == 101.7984
    assert round(swap3, 4) == 4945.3846
    assert round(swap4, 4) == 5392.5785
    assert round(swap5, 4) == 0.0
    assert round(swap6, 4) == 762.5307

    k = 0.08
    swaption = IborSwaption(settlement_date,
                            exercise_date,
                            swapMaturityDate,
                            swaptionType,
                            k,
                            swapFixedFrequencyType,
                            swapFixedDayCountType)

    swap1 = swaption.value(valuation_date, libor_curve, model1)
    swap2 = swaption.value(valuation_date, libor_curve, model2)
    swap3 = swaption.value(valuation_date, libor_curve, model3)
    swap4 = swaption.value(valuation_date, libor_curve, model4)
    swap5 = swaption.value(valuation_date, libor_curve, model5)
    swap6 = swaption.value(valuation_date, libor_curve, model6)
    assert round(swap1, 4) == 125290.5007
    assert round(swap2, 4) == 125290.5007
    assert round(swap3, 4) == 125291.0815
    assert round(swap4, 4) == 125293.5617
    assert round(swap5, 4) == 124657.1389
    assert round(swap6, 4) == 124274.9037

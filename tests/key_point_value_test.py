import os
import numpy as np
import sys
import unittest

from mock import Mock, patch

from utilities.geometry import midpoint

from analysis_engine.derived_parameters import Flap
from analysis_engine.library import align
from analysis_engine.node import (
    A, KTI, P, KeyPointValue, KeyTimeInstance, Section,
)

from analysis_engine.key_point_values import (
    AccelerationLateralAtTouchdown,
    AccelerationLateralDuringLanding,
    AccelerationLateralMax,
    AccelerationLateralTakeoffMax,
    AccelerationLateralTaxiingStraightMax,
    AccelerationLateralTaxiingTurnsMax,
    AccelerationLongitudinalPeakTakeoff,
    AccelerationLongitudinalPeakLanding,
    AccelerationNormal20FtToFlareMax,
    AccelerationNormalAirborneFlapsDownMax,
    AccelerationNormalAirborneFlapsDownMin,
    AccelerationNormalAirborneFlapsUpMax,
    AccelerationNormalAirborneFlapsUpMin,
    AccelerationNormalAtLiftoff,
    AccelerationNormalAtTouchdown,
    AccelerationNormalLiftoffTo35FtMax,
    AccelerationNormalMax,
    AccelerationNormalOffset,
    Airspeed10000To8000FtMax,
    Airspeed10000ToLandMax,
    Airspeed1000To500FtMax,
    Airspeed1000To500FtMin,
    Airspeed1000To8000FtMax,
    Airspeed3000To1000FtMax,
    Airspeed35To1000FtMax,
    Airspeed35To1000FtMin,
    Airspeed5000To3000FtMax,
    Airspeed500To20FtMax,
    Airspeed500To20FtMin,
    Airspeed8000To10000FtMax,
    Airspeed8000To5000FtMax,
    AirspeedAsGearExtendingMax,
    AirspeedAsGearRetractingMax,
    AirspeedAt35FtInTakeoff,
    AirspeedAtGearDownSelection,
    AirspeedAtGearUpSelection,
    AirspeedAtLiftoff,
    AirspeedAtTouchdown,
    AirspeedBelowAltitudeMax,
    AirspeedBetween90SecToTouchdownAndTouchdownMax,
    AirspeedCruiseMax,
    AirspeedCruiseMin,
    AirspeedGustsDuringFinalApproach,
    AirspeedLevelFlightMax,
    AirspeedMax,
    AirspeedMax3Sec,
    AirspeedMinusV235To1000FtMax,
    AirspeedMinusV235To1000FtMin,
    AirspeedMinusV2At35Ft,
    AirspeedMinusV2AtLiftoff,
    AirspeedRTOMax,
    AirspeedRelative1000To500FtMax,
    AirspeedRelative1000To500FtMin,
    AirspeedRelative20FtToTouchdownMax,
    AirspeedRelative20FtToTouchdownMin,
    AirspeedRelative500To20FtMax,
    AirspeedRelative500To20FtMin,        
    AirspeedRelativeAtTouchdown,
    AirspeedRelativeFor3Sec1000To500FtMax,
    AirspeedRelativeFor3Sec1000To500FtMin,
    AirspeedRelativeFor3Sec20FtToTouchdownMax,
    AirspeedRelativeFor3Sec20FtToTouchdownMin,
    AirspeedRelativeFor3Sec500To20FtMax,
    AirspeedRelativeFor3Sec500To20FtMin,    
    AirspeedRelativeFor5Sec1000To500FtMax,
    AirspeedRelativeFor5Sec1000To500FtMin,
    AirspeedRelativeFor5Sec20FtToTouchdownMax,
    AirspeedRelativeFor5Sec20FtToTouchdownMin,
    AirspeedRelativeFor5Sec500To20FtMax,
    AirspeedRelativeFor5Sec500To20FtMin,
    AirspeedRelativeWithFlapDescentMin,
    AirspeedTODTo10000Max,
    AirspeedThrustReverseDeployedMin,
    AirspeedTrueAtTouchdown,
    AirspeedVacatingRunway,
    AirspeedWithFlapClimbMax,
    AirspeedWithFlapClimbMin,
    AirspeedWithFlapDescentMax,
    AirspeedWithFlapDescentMin,
    AirspeedWithFlapMax,
    AirspeedWithFlapMin,
    AirspeedWithGearDownMax,
    AltitudeAtFirstFlapChangeAfterLiftoff,
    AltitudeAtGoAroundGearUpSelection,
    AltitudeAtGoAroundMin,
    AltitudeAtLastFlapChangeBeforeLanding,
    AltitudeAtLiftoff,
    AltitudeAtMachMax,
    AltitudeOvershootAtSuspectedLevelBust,
    AltitudeAtGearDownSelection,
    AltitudeAtGearUpSelection,
    AltitudeAtTouchdown,
    AltitudeAutopilotDisengaged,
    AltitudeAutopilotEngaged,
    AltitudeAutothrottleDisengaged,
    AltitudeAutothrottleEngaged,    
    AltitudeFlapExtensionMax,
    AltitudeGoAroundFlapRetracted,
    AltitudeMax,
    AltitudeMinsToTouchdown,
    AltitudeWithFlapsMax,
    AOAInGoAroundMax,
    AOAWithFlapMax,
    BrakePressureInTakeoffRollMax,
    ControlColumnStiffness,
    DecelerationFromTouchdownToStopOnRunway,
    DelayedBrakingAfterTouchdown,
    EngEPR500FtToTouchdownMin,
    EngGasTempTakeoffMax,
    EngN1500To20FtMin,
    EngN1TakeoffMax,
    EngOilTempMax,
    EngOilTemp15MinuteMax,
    EngVibN1Max,
    EngVibN2Max,
    Eng_N1MaxDurationUnder60PercentAfterTouchdown,
    FlapAtLiftoff,
    FlapAtTouchdown,
    FuelQtyAtLiftoff,
    FuelQtyAtTouchdown,
    GroundspeedOnGroundMax,
    GrossWeightAtLiftoff,
    GrossWeightAtTouchdown,
    HeadingAtLanding,
    HeadingAtTakeoff,
    ILSFrequencyOnApproach,
    ILSGlideslopeDeviation1500To1000FtMax,
    ILSGlideslopeDeviation1000To250FtMax,
    ILSLocalizerDeviation1500To1000FtMax,
    ILSLocalizerDeviation1000To250FtMax,    
    LatitudeAtLanding,
    LatitudeAtLiftoff,
    LatitudeAtTakeoff,
    LatitudeAtTouchdown,
    LongitudeAtLanding,
    LongitudeAtLiftoff,
    LongitudeAtTakeoff,
    LongitudeAtTouchdown,
    MachAsGearExtendingMax,
    MachAsGearRetractingMax,
    MachMax,
    MachWithGearDownMax,
    Pitch35To400FtMax,
    Pitch35To400FtMin,
    PitchAtLiftoff,
    PitchAtTouchdown,
    PitchInGoAroundMax,
    RateOfDescent10000To5000FtMax,
    RateOfDescent5000To3000FtMax,
    RateOfDescent3000To2000FtMax,
    RateOfDescent2000To1000FtMax,
    RateOfDescent1000To500FtMax,
    RateOfDescent500To20FtMax,
    RateOfDescent500FtToTouchdownMax,
    RateOfDescentAtTouchdown,
    RateOfDescentBelow10000FtMax,
    RateOfDescentMax,
    RateOfDescentTopOfDescentTo10000FtMax,
    RollTakeoffTo20FtMax,
    Roll20To400FtMax,
    Roll400To1000FtMax,
    RollAbove1000FtMax,
    Roll1000To300FtMax,
    Roll300To20FtMax,
    Roll20FtToLandingMax,
    RollCyclesInFinalApproach,
    RollCyclesNotInFinalApproach,
    RudderExcursionDuringTakeoff,
    RudderReversalAbove50Ft,
    SpeedbrakesDeployedInGoAroundDuration,
    SpeedbrakesDeployed1000To20FtDuration,
    SpeedbrakesDeployedWithPowerOnDuration,
    SpeedbrakesDeployedWithConfDuration,
    SpeedbrakesDeployedWithPowerOnInHeightBandsDuration,
    TailClearanceOnApproach,
    TailClearanceOnLandingMin,
    TailClearanceOnTakeoffMin,
    TailwindLiftoffTo100FtMax,
    Tailwind100FtToTouchdownMax,
    TCASRAWarningDuration,
    TCASRAReactionDelay,
    TCASRAInitialReaction,
    TCASRAToAPDisengageDuration,
    TerrainClearanceAbove3000FtMin,
    ThrottleCyclesInFinalApproach,
    ThrustAsymmetryInFlight,
    ThrustAsymmetryInGoAround,
    ThrustAsymmetryOnApproachDuration,
    ThrustAsymmetryOnApproachMax,
    ThrustAsymmetryOnTakeoff,
    ThrustAsymmetryWithReverseThrustMax,
    ThrustAsymmetryWithReverseThrustDuration,
    TouchdownTo60KtsDuration,
    TouchdownToElevatorDownDuration,
    TurbulenceInApproachMax,
    TurbulenceInCruiseMax,
    TurbulenceInFlightMax,
    VerticalSpeedInGoAroundMax,
    WindAcrossLandingRunwayAt50Ft,
    WindDirectionInDescent,
    WindSpeedInDescent,
    ZeroFuelWeight,
)
from analysis_engine.key_time_instances import Eng_Stop
from analysis_engine.library import (max_abs_value, max_value, min_value)
from analysis_engine.flight_phase import Fast
from flight_phase_test import buildsection

debug = sys.gettrace() is not None


test_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'test_data')


################################################################################
# Superclasses


class NodeTest(object):
    def test_can_operate(self):
        self.assertEqual(
            self.node_class.get_operational_combinations(),
            self.operational_combinations,
        )


class CreateKPVsAtKPVsTest(NodeTest):
    '''
    Example of subclass inheriting tests:
    
class TestAltitudeAtLiftoff(unittest.TestCase, CreateKPVsAtKPVsTest):
    def setUp(self):
        self.node_class = AltitudeAtLiftoff
        self.operational_combinations = [('Altitude STD', 'Liftoff')]
    '''
    def test_derive(self):
        mock1, mock2 = Mock(), Mock()
        mock1.array = Mock()
        node = self.node_class()
        node.create_kpvs_at_kpvs = Mock()
        node.derive(mock1, mock2)
        node.create_kpvs_at_kpvs.assert_called_once_with(mock1.array, mock2)


class CreateKPVsAtKTIsTest(NodeTest):
    '''
    Example of subclass inheriting tests:
    
class TestAltitudeAtLiftoff(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeAtLiftoff
        self.operational_combinations = [('Altitude STD', 'Liftoff')]
    '''
    def test_derive_mocked(self):
        mock1, mock2 = Mock(), Mock()
        mock1.array = Mock()
        node = self.node_class()
        node.create_kpvs_at_ktis = Mock()
        node.derive(mock1, mock2)
        node.create_kpvs_at_ktis.assert_called_once_with(mock1.array, mock2)


class CreateKPVsWithinSlicesTest(NodeTest):
    '''
    Example of subclass inheriting tests:
    
class TestRollAbove1500FtMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RollAbove1500FtMax
        self.operational_combinations = [('Roll', 'Altitude AAL For Flight Phases')]
        # Function passed to create_kpvs_within_slices
        self.function = max_abs_value
        # second_param_method_calls are method calls made on the second
        # parameter argument, for example calling slices_above on a Parameter.
        # It is optional.
        self.second_param_method_calls = [('slices_above', (1500,), {})]
    
    TODO: Implement in a neater way?
    '''
    def test_derive_mocked(self):
        mock1, mock2, mock3 = Mock(), Mock(), Mock()
        mock1.array = Mock()
        if hasattr(self, 'second_param_method_calls'):
            mock3 = Mock()
            setattr(mock2, self.second_param_method_calls[0][0], mock3)
            mock3.return_value = Mock()
        node = self.node_class()
        node.create_kpvs_within_slices = Mock()
        node.derive(mock1, mock2)
        if hasattr(self, 'second_param_method_calls'):
            mock3.assert_called_once_with(*self.second_param_method_calls[0][1])
            node.create_kpvs_within_slices.assert_called_once_with(\
                mock1.array, mock3.return_value, self.function)
        else:
            self.assertEqual(mock2.method_calls, [])
            node.create_kpvs_within_slices.assert_called_once_with(\
                mock1.array, mock2, self.function)


class CreateKPVFromSlicesTest(NodeTest):
    '''
    Example of subclass inheriting tests:
    
class TestRollAbove1500FtMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RollAbove1500FtMax
        self.operational_combinations = [('Roll', 'Altitude AAL For Flight Phases')]
        # Function passed to create_kpvs_within_slices
        self.function = max_abs_value
        # second_param_method_calls are method calls made on the second
        # parameter argument, for example calling slices_above on a Parameter.
        # It is optional.
        self.second_param_method_calls = [('slices_above', (1500,), {})]
    
    TODO: Implement in a neater way?
    '''
    def test_derive_mocked(self):
        mock1, mock2, mock3 = Mock(), Mock(), Mock()
        mock1.array = Mock()
        if hasattr(self, 'second_param_method_calls'):
            mock3 = Mock()
            setattr(mock2, self.second_param_method_calls[0][0], mock3)
            mock3.return_value = Mock()
        node = self.node_class()
        node.create_kpv_from_slices = Mock()
        node.derive(mock1, mock2)
        if hasattr(self, 'second_param_method_calls'):
            mock3.assert_called_once_with(*self.second_param_method_calls[0][1])
            node.create_kpv_from_slices.assert_called_once_with(\
                mock1.array, mock3.return_value, self.function)
        else:
            self.assertEqual(mock2.method_calls, [])
            node.create_kpv_from_slices.assert_called_once_with(\
                mock1.array, mock2, self.function)

            
################################################################################
# Test Classes


################################################################################
# Acceleration


class TestAccelerationLateralAtTouchdown(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationLateralAtTouchdown.get_operational_combinations(),
            [('Acceleration Lateral Offset Removed', 'Touchdown',)])
        
    @patch('analysis_engine.key_point_values.bump')
    def test_derive(self, bump):
        values = [(1, 2,), (3, 4,)]
        bump.side_effect = lambda *args, **kwargs: values.pop()
        node = AccelerationLateralAtTouchdown()
        acc = Mock()
        tdwn = [Section('Touchdown', slice(10, 20), 10, 20),
                Section('Touchdown', slice(30, 40), 30, 40),]
        node.derive(acc, tdwn)
        self.assertEqual(bump.call_args_list[0][0], (acc, tdwn[0]))
        self.assertEqual(bump.call_args_list[1][0], (acc, tdwn[1]))
        self.assertEqual(
            node,
            [KeyPointValue(3, 4.0, 'Acceleration Lateral At Touchdown',
                           slice(None, None)),
             KeyPointValue(1, 2.0, 'Acceleration Lateral At Touchdown',
                           slice(None, None))])


class TestAccelerationLateralDuringLanding(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationLateralDuringLanding.get_operational_combinations(),
            [('Acceleration Lateral Offset Removed', 'Landing Roll',
              'FDR Landing Runway',)])

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAccelerationLateralMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationLateralMax.get_operational_combinations(),
            [('Acceleration Lateral Offset Removed',),
             ('Acceleration Lateral Offset Removed', 'Groundspeed',),])        
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAccelerationLateralTakeoffMax(unittest.TestCase,
                                        CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AccelerationLateralTakeoffMax
        self.operational_combinations = [
            ('Acceleration Lateral Offset Removed', 'Takeoff Roll')]
        self.function = max_abs_value
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAccelerationLateralTaxiingStraightMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationLateralTaxiingStraightMax.get_operational_combinations(),
            [('Acceleration Lateral Offset Removed', 'Taxiing',
              'Turning On Ground',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAccelerationLateralTaxiingTurnsMax(unittest.TestCase,
                                             CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AccelerationLateralTaxiingTurnsMax
        self.operational_combinations = [('Acceleration Lateral Offset Removed',
                                          'Turning On Ground',)]
        self.function = max_abs_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAccelerationLongitudinalPeakTakeoff(unittest.TestCase,
                                              CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = AccelerationLongitudinalPeakTakeoff
        self.operational_combinations = [('Acceleration Longitudinal',
                                          'Takeoff',)]
        self.function = max_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAccelerationLongitudinalPeakLanding(unittest.TestCase,
                                              CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = AccelerationLongitudinalPeakLanding
        self.operational_combinations = [('Acceleration Longitudinal',
                                          'Landing',)]
        self.function = max_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAccelerationNormalMax(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = AccelerationNormalMax
        self.operational_combinations = [('Acceleration Normal Offset Removed',
                                          'Mobile')]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAccelerationNormal20FtToFlareMax(unittest.TestCase,
                                           CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AccelerationNormal20FtToFlareMax
        self.operational_combinations = [('Acceleration Normal Offset Removed',
                                          'Altitude AAL For Flight Phases')]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (20, 5,), {})]
    
    def test_derive(self):
        '''
        Depends upon DerivedParameterNode.slices_from_to and library.max_value.
        '''
        # Test height range limit
        alt_aal = P('Altitude AAL For Flight Phases', np.ma.arange(48, 0, -3))
        acceleration_normal = \
            P('Acceleration Normal',
              np.ma.array(range(10,18) + range(18, 10, -1)) / 10.0)
        node = AccelerationNormal20FtToFlareMax()
        node.derive(acceleration_normal, alt_aal)
        self.assertEqual(node,
                [KeyPointValue(index=10, value=1.6,
                               name='Acceleration Normal 20 Ft To Flare Max')])
        # Test peak acceleration
        alt_aal = P('Altitude AAL For Flight Phases', np.ma.arange(32, 0, -2))
        node = AccelerationNormal20FtToFlareMax()
        node.derive(acceleration_normal, alt_aal)
        self.assertEqual(node,
                [KeyPointValue(index=8, value=1.8,
                               name='Acceleration Normal 20 Ft To Flare Max')])


class TestAccelerationNormalAirborneFlapsUpMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationNormalAirborneFlapsUpMax.get_operational_combinations(),
            [('Acceleration Normal Offset Removed', 'Flap', 
              'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAccelerationNormalAirborneFlapsUpMin(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationNormalAirborneFlapsUpMin.get_operational_combinations(),
            [('Acceleration Normal Offset Removed', 'Flap', 
              'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAccelerationNormalAirborneFlapsDownMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationNormalAirborneFlapsDownMax.get_operational_combinations(),
            [('Acceleration Normal Offset Removed', 'Flap', 
              'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAccelerationNormalAirborneFlapsDownMin(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationNormalAirborneFlapsDownMin.get_operational_combinations(),
            [('Acceleration Normal Offset Removed', 'Flap', 
              'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAccelerationNormalAtLiftoff(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationNormalAtLiftoff.get_operational_combinations(),
            [('Acceleration Normal Offset Removed', 'Liftoff',)])
        
    @patch('analysis_engine.key_point_values.bump')
    def test_derive(self, bump):
        values = [(1, 2,), (3, 4,)]
        bump.side_effect = lambda *args, **kwargs: values.pop()
        node = AccelerationNormalAtLiftoff()
        acc = Mock()
        tdwn = [Section('Liftoff', slice(10, 20), 10, 20),
                Section('Liftoff', slice(30, 40), 30, 40),]
        node.derive(acc, tdwn)
        self.assertEqual(bump.call_args_list[0][0], (acc, tdwn[0]))
        self.assertEqual(bump.call_args_list[1][0], (acc, tdwn[1]))
        self.assertEqual(
            node,
            [KeyPointValue(3, 4.0, 'Acceleration Normal At Liftoff',
                           slice(None, None)),
             KeyPointValue(1, 2.0, 'Acceleration Normal At Liftoff',
                           slice(None, None))])


class TestAccelerationNormalAtTouchdown(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationNormalAtTouchdown.get_operational_combinations(),
            [('Acceleration Normal Offset Removed', 'Touchdown',)])
        
    @patch('analysis_engine.key_point_values.bump')
    def test_derive(self, bump):
        values = [(1, 2,), (3, 4,)]
        bump.side_effect = lambda *args, **kwargs: values.pop()
        node = AccelerationNormalAtTouchdown()
        acc = Mock()
        tdwn = [Section('Touchdown', slice(10, 20), 10, 20),
                Section('Touchdown', slice(30, 40), 30, 40),]
        node.derive(acc, tdwn)
        self.assertEqual(bump.call_args_list[0][0], (acc, tdwn[0]))
        self.assertEqual(bump.call_args_list[1][0], (acc, tdwn[1]))
        self.assertEqual(
            node,
            [KeyPointValue(3, 4.0, 'Acceleration Normal At Touchdown',
                           slice(None, None)),
             KeyPointValue(1, 2.0, 'Acceleration Normal At Touchdown',
                           slice(None, None))])                


class TestAccelerationNormalLiftoffTo35FtMax(unittest.TestCase,
                                             CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AccelerationNormalLiftoffTo35FtMax
        self.operational_combinations = [('Acceleration Normal Offset Removed',
                                          'Takeoff',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAccelerationLateralOffset(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAccelerationNormalOffset(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AccelerationNormalOffset.get_operational_combinations(),
            [('Acceleration Normal', 'Taxiing',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Airspeed


########################################
# Airspeed: General


class TestAirspeedMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedMax
        self.operational_combinations = [('Airspeed', 'Airborne')]
        self.function = max_value
        
    def test_derive_basic(self):
        testline = np.arange(0,12.6,0.1)
        testwave = (np.cos(testline)*(-100))+100
        spd = P('Airspeed', np.ma.array(testwave))
        waves=np.ma.clump_unmasked(np.ma.masked_less(testwave,80))
        airs=[]
        for wave in waves:
            airs.append(Section('Airborne',wave, wave.start, wave.stop))
        kpv = AirspeedMax()
        kpv.derive(spd, airs)
        self.assertEqual(len(kpv), 2)
        self.assertEqual(kpv[0].index, 31)
        self.assertGreater(kpv[0].value, 199.9)
        self.assertLess(kpv[0].value, 200)
        self.assertEqual(kpv[1].index, 94)
        self.assertGreater(kpv[1].value, 199.9)
        self.assertLess(kpv[1].value, 200)


class TestAirspeedMax3Sec(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedMax3Sec.get_operational_combinations(),
            [('Airspeed', 'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedCruiseMax(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = AirspeedCruiseMax
        self.operational_combinations = [('Airspeed', 'Cruise',)]
        self.function = max_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedCruiseMin(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = AirspeedCruiseMin
        self.operational_combinations = [('Airspeed', 'Cruise',)]
        self.function = min_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedGustsDuringFinalApproach(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test Not Implemented')
    
    # This function interpolates twice, hence the more complex test case.
    def test_derive_basic(self):
        spd = P('Airspeed', np.ma.array([180,140,100]), frequency=0.5,
                offset=0.0)
        alt = P('Altitude Radio', np.ma.array([45,35,25,15,5,0]), frequency=1.0,
                offset=0.0)
        kpv=AirspeedGustsDuringFinalApproach()
        kpv.get_derived([spd,alt])
        self.assertEqual(kpv[0].value, 40)
        self.assertEqual(kpv[0].index, 1.25)


########################################
# Airspeed: Climbing


class TestAirspeedAtLiftoff(unittest.TestCase,
                            CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AirspeedAtLiftoff
        self.operational_combinations = [('Airspeed', 'Liftoff',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')   


class TestAirspeedAt35FtInTakeoff(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedAt35FtInTakeoff.get_operational_combinations(),
            [('Airspeed', 'Takeoff',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeed35To1000FtMax(unittest.TestCase,
                                CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Airspeed35To1000FtMax
        self.operational_combinations = [('Airspeed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (35, 1000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeed35To1000FtMin(unittest.TestCase,
                                CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Airspeed35To1000FtMin
        self.operational_combinations = [('Airspeed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (35, 1000), {})]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeed1000To8000FtMax(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = Airspeed1000To8000FtMax
        self.operational_combinations = [('Airspeed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (1000, 8000), {})]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeed8000To10000FtMax(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = Airspeed8000To10000FtMax
        self.operational_combinations = [('Airspeed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (8000, 10000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')  


########################################
# Airspeed: Descending


class TestAirspeed10000To8000FtMax(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = Airspeed10000To8000FtMax
        self.operational_combinations = [('Airspeed', 'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (10000, 8000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeed8000To5000FtMax(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = Airspeed8000To5000FtMax
        self.operational_combinations = [('Airspeed', 'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (8000, 5000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeed5000To3000FtMax(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = Airspeed5000To3000FtMax
        self.operational_combinations = [('Airspeed', 'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (5000, 3000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeed3000To1000FtMax(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = Airspeed3000To1000FtMax
        self.operational_combinations = [('Airspeed', 'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (3000, 1000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeed1000To500FtMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Airspeed1000To500FtMax
        self.operational_combinations = [('Airspeed',
                                          'Altitude AAL For Flight Phases')]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (1000, 500,), {})]
        
    def test_derive_basic(self):
        testline = np.arange(0, 12.6, 0.1)
        testwave = (np.cos(testline) * -100) + 100
        spd = P('Airspeed', np.ma.array(testwave))
        alt_ph = P('Altitude AAL For Flight Phases', 
                           np.ma.array(testwave) * 10)
        kpv = Airspeed1000To500FtMax()
        kpv.derive(spd, alt_ph)
        self.assertEqual(len(kpv), 2)
        self.assertEqual(kpv[0].index, 48)
        self.assertEqual(kpv[0].value, 91.250101656055278)
        self.assertEqual(kpv[1].index, 110)
        self.assertEqual(kpv[1].value, 99.557430201194919)


class TestAirspeed1000To500FtMin(unittest.TestCase,
                                 CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Airspeed1000To500FtMin
        self.operational_combinations = [('Airspeed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (1000, 500), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeed500To20FtMax(unittest.TestCase,
                                CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Airspeed500To20FtMax
        self.operational_combinations = [('Airspeed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (500, 20), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeed500To20FtMin(unittest.TestCase,
                                CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Airspeed500To20FtMin
        self.operational_combinations = [('Airspeed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (500, 20), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedAtTouchdown(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AirspeedAtTouchdown
        self.operational_combinations = [('Airspeed', 'Touchdown')]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeedTrueAtTouchdown(unittest.TestCase,
                                  CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AirspeedTrueAtTouchdown
        self.operational_combinations = [('Airspeed True', 'Touchdown',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


########################################
# Airspeed: Minus V2


class TestAirspeedMinusV2AtLiftoff(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AirspeedMinusV2AtLiftoff
        self.operational_combinations = [('Airspeed Minus V2', 'Liftoff')]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeedMinusV2At35Ft(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedMinusV2At35Ft.get_operational_combinations(),
            [('Airspeed Minus V2', 'Takeoff',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedMinusV235To1000FtMax(unittest.TestCase,
                                       CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedMinusV235To1000FtMax
        self.operational_combinations = [('Airspeed Minus V2',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (35, 1000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedMinusV235To1000FtMin(unittest.TestCase,
                                       CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedMinusV235To1000FtMin
        self.operational_combinations = [('Airspeed Minus V2',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (35, 1000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


########################################
# Airspeed: Relative

class TestAirspeedRelativeAtTouchdown(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AirspeedRelativeAtTouchdown
        self.operational_combinations = [('Airspeed Relative', 'Touchdown')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeedRelative1000To500FtMax(unittest.TestCase,
                                         CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelative1000To500FtMax
        self.operational_combinations = [('Airspeed Relative',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (1000, 500), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelative1000To500FtMin(unittest.TestCase,
                                         CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelative1000To500FtMin
        self.operational_combinations = [('Airspeed Relative',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (1000, 500), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeedRelative500To20FtMax(unittest.TestCase,
                                       CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelative500To20FtMax
        self.operational_combinations = [('Airspeed Relative',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (500, 20), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelative500To20FtMin(unittest.TestCase,
                                       CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelative500To20FtMin
        self.operational_combinations = [('Airspeed Relative',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (500, 20), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')
        

class TestAirspeedRelative20FtToTouchdownMax(unittest.TestCase,
                                             CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelative20FtToTouchdownMax
        self.operational_combinations = [('Airspeed Relative',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (20, 0), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelative20FtToTouchdownMin(unittest.TestCase,
                                             CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelative20FtToTouchdownMin
        self.operational_combinations = [('Airspeed Relative',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (20, 0), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeedRelativeFor3Sec1000To500FtMax(unittest.TestCase,
                                                CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor3Sec1000To500FtMax
        self.operational_combinations = [('Airspeed Relative For 3 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (1000, 500), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor3Sec1000To500FtMin(unittest.TestCase,
                                                CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor3Sec1000To500FtMin
        self.operational_combinations = [('Airspeed Relative For 3 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (1000, 500), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor3Sec20FtToTouchdownMax(unittest.TestCase,
                                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor3Sec20FtToTouchdownMax
        self.operational_combinations = [('Airspeed Relative For 3 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (20, 0), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor3Sec20FtToTouchdownMin(unittest.TestCase,
                                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor3Sec20FtToTouchdownMin
        self.operational_combinations = [('Airspeed Relative For 3 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (20, 0), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor3Sec500To20FtMax(unittest.TestCase,
                                              CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor3Sec500To20FtMax
        self.operational_combinations = [('Airspeed Relative For 3 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (500, 20), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor3Sec500To20FtMin(unittest.TestCase,
                                              CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor3Sec500To20FtMin
        self.operational_combinations = [('Airspeed Relative For 3 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (500, 20), {})]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor5Sec1000To500FtMax(unittest.TestCase,
                                                CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor5Sec1000To500FtMax
        self.operational_combinations = [('Airspeed Relative For 5 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (1000, 500), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor5Sec1000To500FtMin(unittest.TestCase,
                                                CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor5Sec1000To500FtMin
        self.operational_combinations = [('Airspeed Relative For 5 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (1000, 500), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor5Sec500To20FtMax(unittest.TestCase,
                                              CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor5Sec500To20FtMax
        self.operational_combinations = [('Airspeed Relative For 5 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (500, 20), {})]
        
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor5Sec500To20FtMin(unittest.TestCase,
                                              CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor5Sec500To20FtMin
        self.operational_combinations = [('Airspeed Relative For 5 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (500, 20), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor5Sec20FtToTouchdownMax(unittest.TestCase,
                                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor5Sec20FtToTouchdownMax
        self.operational_combinations = [('Airspeed Relative For 5 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (20, 0), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAirspeedRelativeFor5Sec20FtToTouchdownMin(unittest.TestCase,
                                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRelativeFor5Sec20FtToTouchdownMin
        self.operational_combinations = [('Airspeed Relative For 5 Sec',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (20, 0), {})]
        
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


########################################
# Airspeed: (Other)

class TestAirspeedVacatingRunway(unittest.TestCase,
                                 CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AirspeedVacatingRunway
        self.operational_combinations = [('Airspeed True',
                                          'Landing Turn Off Runway',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeedRTOMax(unittest.TestCase,
                         CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedRTOMax
        self.operational_combinations = [('Airspeed', 'Rejected Takeoff',)]
        self.function = max_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeed10000ToLandMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            Airspeed10000ToLandMax.get_operational_combinations(),
            [('Airspeed', 'Altitude STD Smoothed', 'Altitude QNH',
              'FDR Landing Airport', 'Descent')])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedTODTo10000Max(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedTODTo10000Max.get_operational_combinations(),
            [('Airspeed', 'Altitude STD Smoothed', 'Altitude QNH', 'FDR Landing Airport',
              'Descent')])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedBetween90SecToTouchdownAndTouchdownMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedBetween90SecToTouchdownAndTouchdownMax.get_operational_combinations(),
            [('Airspeed', 'Secs To Touchdown',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedLevelFlightMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedLevelFlightMax.get_operational_combinations(),
            [('Airspeed', 'Level Flight',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedBelowAltitudeMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedBelowAltitudeMax.get_operational_combinations(),
            [('Airspeed', 'Altitude AAL For Flight Phases'),])
    
    def test_derive(self):
        airspeed = P(array=np.ma.arange(20))
        alt_aal = P(array=np.ma.arange(0, 10000, 500))
        param = AirspeedBelowAltitudeMax()
        param.derive(airspeed, alt_aal)
        self.assertEqual(param,
            [KeyPointValue(index=19, value=19.0, 
                           name='Airspeed Below 10000 Ft Max',
                           slice=slice(None, None, None), datetime=None), 
             KeyPointValue(index=15, value=15.0, 
                           name='Airspeed Below 8000 Ft Max',
                           slice=slice(None, None, None), datetime=None), 
             KeyPointValue(index=13, value=13.0, 
                           name='Airspeed Below 7000 Ft Max',
                           slice=slice(None, None, None), datetime=None), 
             KeyPointValue(index=9, value=9.0, 
                           name='Airspeed Below 5000 Ft Max',
                           slice=slice(None, None, None), datetime=None), 
             KeyPointValue(index=5, value=5.0, 
                           name='Airspeed Below 3000 Ft Max',
                           slice=slice(None, None, None), datetime=None)])


################################################################################
# Angle of Attack

class TestAOAWithFlapMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(AOAWithFlapMax.get_operational_combinations(),
                         [('Flap', 'AOA', 'Fast',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Airspeed With Flap

class TestAirspeedWithFlapMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(\
            AirspeedWithFlapMax.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Fast')])
        
    def test_derive(self):
        spd = P('Airspeed', np.ma.array(range(30)))
        flap = P('Flap', np.ma.array([0]*10 + [5]*10 + [10]*10))
        fast = buildsection('Fast',0,30)
        flap.array[19] = np.ma.masked # mask the max val
        spd_flap = AirspeedWithFlapMax()
        spd_flap.derive(flap, spd, fast)
        self.assertEqual(len(spd_flap), 2)
        self.assertEqual(spd_flap[0].name, 'Airspeed With Flap 5 Max')
        self.assertEqual(spd_flap[0].index, 18) # 19 was masked
        self.assertEqual(spd_flap[0].value, 18)
        self.assertEqual(spd_flap[1].name, 'Airspeed With Flap 10 Max')
        self.assertEqual(spd_flap[1].index, 29)
        self.assertEqual(spd_flap[1].value, 29)

    def test_derive_alternative_method(self):
        # This test will produce a warning "No flap settings - rounding to nearest 5"
        airspeed = P('Airspeed', np.ma.arange(20))
        flap = P('Flap',
                 np.ma.masked_array([0] * 2 + [1] * 2 + [2] * 2 + [5] * 2 +
                                    [10] * 2 +  [15] * 2 + [25] * 2 +
                                    [30] * 2 + [40] * 2 + [0] * 2))
        fast = buildsection('Fast',0,20)
        step = Flap()
        step.derive(flap)
        
        airspeed_with_flap_max = AirspeedWithFlapMax()
        airspeed_with_flap_max.derive(step, airspeed, fast)
        self.assertEqual(airspeed_with_flap_max,
          [KeyPointValue(index=7, value=7, name='Airspeed With Flap 5 Max'),
           KeyPointValue(index=9, value=9, name='Airspeed With Flap 10 Max'),
           KeyPointValue(index=11, value=11, name='Airspeed With Flap 15 Max'),
           KeyPointValue(index=13, value=13, name='Airspeed With Flap 25 Max'),
           KeyPointValue(index=15, value=15, name='Airspeed With Flap 30 Max'),
           KeyPointValue(index=17, value=17, name='Airspeed With Flap 40 Max')])


class TestAirspeedWithFlapMin(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithFlapMin.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedWithFlapClimbMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithFlapClimbMax.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Climb',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedWithFlapClimbMin(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithFlapClimbMin.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Climb',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedWithFlapDescentMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithFlapDescentMax.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Descent',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedWithFlapDescentMin(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithFlapDescentMin.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Descent To Flare',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedRelativeWithFlapDescentMin(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedRelativeWithFlapDescentMin.get_operational_combinations(),
            [('Flap', 'Airspeed Relative', 'Descent To Flare',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Thrust Reversers

class TestAirspeedThrustReverseDeployedMin(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedThrustReverseDeployedMin.get_operational_combinations(),
            [('Airspeed True', 'Thrust Reversers', 'Eng (*) N1 Avg',
              'Landing',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGroundspeedThrustReverseDeployedMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedThrustReverseSelected(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestThrustAsymetryWithThrustReverse(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestThrustWithThrustReverseInTransit(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTouchdownToThrustReverseDeployedDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TouchdownToSpoilersDeployedDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Takeoff and Use of TOGA


class TestGroundspeedAtTOGA(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTOGASelectedInFlightNotGoAroundDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestLiftoffToClimbPitchDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')    


################################################################################
# Landing Gear
        
        
########################################
# 'Gear Down' Multistate


class TestAirspeedWithGearDownMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithGearDownMax.get_operational_combinations(),
            [('Airspeed', 'Gear Down', 'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestMachWithGearDownMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            MachWithGearDownMax.get_operational_combinations(),
            [('Mach', 'Gear Down', 'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


########################################
# Gear Retracting/Extending Section


class TestAirspeedAsGearRetractingMax(unittest.TestCase,
                                      CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedAsGearRetractingMax
        self.operational_combinations = [('Airspeed', 'Gear Retracting',)]
        self.function = max_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeedAsGearExtendingMax(unittest.TestCase,
                                     CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AirspeedAsGearExtendingMax
        self.operational_combinations = [('Airspeed', 'Gear Extending',)]
        self.function = max_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestMachAsGearRetractingMax(unittest.TestCase,
                                  CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = MachAsGearRetractingMax
        self.operational_combinations = [('Airspeed', 'Gear Retracting',)]
        self.function = max_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestMachAsGearExtendingMax(unittest.TestCase,
                                     CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = MachAsGearExtendingMax
        self.operational_combinations = [('Airspeed', 'Gear Extending',)]
        self.function = max_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


########################################
# Gear Up/Down Selection KTI


class TestAirspeedAtGearUpSelection(unittest.TestCase,
                                    CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AirspeedAtGearUpSelection
        self.operational_combinations = [('Airspeed', 'Gear Up Selection',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAirspeedAtGearDownSelection(unittest.TestCase,
                                      CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AirspeedAtGearDownSelection
        self.operational_combinations = [('Airspeed', 'Gear Down Selection',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


##################################
# Braking


class TestBrakePressureInTakeoffRollMax(unittest.TestCase,
                                        CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = BrakePressureInTakeoffRollMax
        self.operational_combinations = [('Brake Pressure', 'Takeoff Roll',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestDelayedBrakingAfterTouchdown(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            DelayedBrakingAfterTouchdown.get_operational_combinations(),
            [('Landing', 'Groundspeed', 'Touchdown',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################


class TestGenericDescent(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedWithFlapClimbMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithFlapClimbMax.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Climb',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedWithFlapClimbMin(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithFlapClimbMin.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Climb',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedWithFlapDescentMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithFlapDescentMax.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Descent',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAirspeedWithFlapDescentMin(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AirspeedWithFlapDescentMin.get_operational_combinations(),
            [('Flap', 'Airspeed', 'Descent To Flare',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeAtTouchdown(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeAtTouchdown
        self.operational_combinations = [('Altitude STD Smoothed', 'Touchdown')]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')    


class TestAltitudeAtMachMax(unittest.TestCase, CreateKPVsAtKPVsTest):
    def setUp(self):
        self.node_class = AltitudeAtMachMax
        self.operational_combinations = [('Altitude STD Smoothed', 'Mach Max')]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')      


class TestAltitudeMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AltitudeMax
        self.operational_combinations = [('Altitude STD Smoothed', 'Airborne')]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestControlColumnStiffness(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(ControlColumnStiffness.get_operational_combinations(),
                         [('Control Column Force','Control Column','Fast')])

    def test_derive_too_few_samples(self):
        cc_disp = P('Control Column', 
                            np.ma.array([0,.3,1,2,2.5,1.4,0,0]))
        cc_force = P('Control Column Force',
                             np.ma.array([0,2,4,7,8,5,2,1]))
        phase_fast = Fast()
        phase_fast.derive(P('Airspeed', np.ma.array([100]*10)))
        stiff = ControlColumnStiffness()
        stiff.derive(cc_force,cc_disp,phase_fast)
        self.assertEqual(stiff, [])
        
    def test_derive_max(self):
        testwave = np.ma.array((1.0 - np.cos(np.arange(0,6.3,0.1)))/2.0)
        cc_disp = P('Control Column', testwave * 10.0)
        cc_force = P('Control Column Force', testwave * 27.0)
        phase_fast = buildsection('Fast',0,63)
        stiff = ControlColumnStiffness()
        stiff.derive(cc_force,cc_disp,phase_fast)
        self.assertEqual(stiff.get_first().index, 31) 
        self.assertAlmostEqual(stiff.get_first().value, 2.7) # lb/deg 
        

class TestEngEPR500FtToTouchdownMin(unittest.TestCase,
                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = EngEPR500FtToTouchdownMin
        self.operational_combinations = [('Eng (*) EPR Min',
                                          'Altitude AAL For Flight Phases')]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (500, 0,), {})]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')  


class TestEngN1500To20FtMin(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = EngN1500To20FtMin
        self.operational_combinations = [('Eng (*) N1 Min',
                                          'Altitude AAL For Flight Phases')]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (500, 20,), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')      


class TestEngGasTempTakeoffMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = EngGasTempTakeoffMax
        self.operational_combinations = [('Eng (*) Gas Temp Max',
                                          'Takeoff 5 Min Rating')]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')      


class TestEngN1TakeoffMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = EngN1TakeoffMax
        self.function = max_value
        self.operational_combinations = [('Eng (*) N1 Max',
                                          'Takeoff 5 Min Rating')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')     


class TestEngOilTempMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = EngOilTempMax
        self.function = max_value
        self.operational_combinations = [('Eng (*) Oil Temp Max', 'Airborne')]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')     


class TestEngOilTemp15MinuteMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(EngOilTempMax.get_operational_combinations(),
                         [('Eng (*) Oil Temp Max', 'Airborne')])
        
    def test_derive_all_oil_data_masked(self):
        # This has been a specific problem, hence this test.
        oil_temp=np.ma.array(data=[123,124,125,126,127], dtype=float,
                             mask=[1,1,1,1,1])
        kpv = EngOilTemp15MinuteMax()
        kpv.derive(P('Eng (*) Oil Temp Max', oil_temp))


class TestEngVibN1Max(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = EngVibN1Max
        self.function = max_value
        self.operational_combinations = [('Eng (*) Vib N1 Max', 'Airborne')]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestEngVibN2Max(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = EngVibN2Max
        self.function = max_value
        self.operational_combinations = [('Eng (*) Vib N2 Max', 'Airborne')]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestEng_N1MaxDurationUnder60PercentAfterTouchdown(unittest.TestCase):
    def test_can_operate(self):
        opts = Eng_N1MaxDurationUnder60PercentAfterTouchdown.get_operational_combinations()
        self.assertEqual(
            ('Eng (*) Stop', 'Eng (1) N1', 'Touchdown'), opts[0]) 
        self.assertEqual(
            ('Eng (*) Stop', 'Eng (2) N1', 'Touchdown'), opts[1]) 
        self.assertEqual(
            ('Eng (*) Stop', 'Eng (3) N1', 'Touchdown'), opts[2])
        self.assertEqual(
            ('Eng (*) Stop', 'Eng (4) N1', 'Touchdown'), opts[3])
        self.assertTrue(
            ('Eng (*) Stop', 'Eng (1) N1', 'Eng (2) N1', 'Touchdown') in opts) 
        self.assertTrue(all(['Touchdown' in avail for avail in opts]))
        self.assertTrue(all(['Eng (*) Stop' in avail for avail in opts]))
        
    def test_derive_eng_n1_cooldown(self):
        #TODO: Add later if required
        #gnd = S(items=[Section('', slice(10,100))]) 
        eng_stop = Eng_Stop(items=[KeyTimeInstance(90, 'Eng (1) Stop'),])
        eng = P(array=np.ma.array([100] * 60 + [40] * 40)) # idle for 40        
        tdwn = KTI(items=[KeyTimeInstance(30), KeyTimeInstance(50)])
        max_dur = Eng_N1MaxDurationUnder60PercentAfterTouchdown()
        max_dur.derive(eng_stop, eng, eng, None, None, tdwn)
        self.assertEqual(max_dur[0].index, 60) # starts at drop below 60
        self.assertEqual(max_dur[0].value, 30) # stops at 90
        self.assertTrue('Eng (1)' in max_dur[0].name)
        # Eng (2) should not be in the results as it did not have an Eng Stop KTI
        ##self.assertTrue('Eng (2)' in max_dur[1].name)
        self.assertEqual(len(max_dur), 1)

        
class TestILSGlideslopeDeviation1500To1000FtMax(unittest.TestCase):
        
    def test_derive_basic(self):
        testline = np.ma.array((75 - np.arange(63))*25) # 1875 to 325 ft in 63 steps.
        alt_ph = P('Altitude AAL For Flight Phases', testline)
        
        testwave = np.ma.array(1.0 - np.cos(np.arange(0,6.3,0.1)))
        ils_gs = P('ILS Glideslope', testwave)
        
        gs_estab = buildsection('ILS Glideslope Established', 2,63)
        
        kpv = ILSGlideslopeDeviation1500To1000FtMax()
        kpv.derive(ils_gs, alt_ph, gs_estab)
        # 'KeyPointValue', 'index' 'value' 'name'
        self.assertEqual(len(kpv), 1)
        self.assertEqual(kpv[0].index, 31)
        self.assertAlmostEqual(kpv[0].value, 1.99913515027)

    def test_derive_four_peaks(self):
        testline = np.ma.array((75 - np.arange(63))*25) # 1875 to 325 ft in 63 steps.
        alt_ph = P('Altitude AAL For Flight Phases', testline)
        testwave = np.ma.array(-0.2-np.sin(np.arange(0,12.6,0.1)))
        ils_gs = P('ILS Glideslope', testwave)
        gs_estab = buildsection('ILS Glideslope Established', 2,56)
        kpv = ILSGlideslopeDeviation1500To1000FtMax()
        kpv.derive(ils_gs, alt_ph, gs_estab)
        # 'KeyPointValue', 'index' 'value' 'name'
        self.assertAlmostEqual(kpv[0].value, -1.1995736)


class TestILSGlideslopeDeviation1000To250FtMax(unittest.TestCase):
        
    def test_derive_basic(self):
        testline = np.ma.array((75 - np.arange(63))*25) # 1875 to 325 ft in 63 steps.
        alt_ph = P('Altitude AAL For Flight Phases', testline)
        
        testwave = np.ma.array(1.0 - np.cos(np.arange(0,6.3,0.1)))
        ils_gs = P('ILS Glideslope', testwave)
        
        gs_estab = buildsection('ILS Glideslope Established', 2,63)
        
        kpv = ILSGlideslopeDeviation1000To250FtMax()
        kpv.derive(ils_gs, alt_ph, gs_estab)
        # 'KeyPointValue', 'index' 'value' 'name'
        self.assertEqual(len(kpv), 1)
        self.assertEqual(kpv[0].index, 36)
        self.assertAlmostEqual(kpv[0].value, 1.89675842)

    def test_derive_four_peaks(self):
        testline = np.ma.array((75 - np.arange(63))*25) # 1875 to 325 ft in 63 steps.
        alt_ph = P('Altitude AAL For Flight Phases', testline)
        testwave = np.ma.array(-0.2-np.sin(np.arange(0,12.6,0.1)))
        ils_gs = P('ILS Glideslope', testwave)
        gs_estab = buildsection('ILS Glideslope Established', 2,56)
        kpv = ILSGlideslopeDeviation1000To250FtMax()
        kpv.derive(ils_gs, alt_ph, gs_estab)
        # 'KeyPointValue', 'index' 'value' 'name'
        self.assertAlmostEqual(kpv[0].value, 0.79992326)


class TestHeadingAtTakeoff(unittest.TestCase):
    def test_can_operate(self):
        expected = [('Heading Continuous', 'Takeoff')]
        opts = HeadingAtTakeoff.get_operational_combinations()
        self.assertEqual(opts, expected) 
        
    def test_derive_basic(self):
        head = P('Heading Continuous',np.ma.array([0,2,4,7,9,8,6,3]))
        toff = buildsection('Takeoff', 2,6)
        kpv = HeadingAtTakeoff()
        kpv.derive(head, toff)
        expected = [KeyPointValue(index=4, value=7.5,
                                  name='Heading At Takeoff')]
        self.assertEqual(kpv, expected)
        
    def test_derive_modulus(self):
        head = P('Heading Continuous',np.ma.array([0,2,4,7,9,8,6,3])*-1.0)
        toff = buildsection('Takeoff', 2,6)
        kpv = HeadingAtTakeoff()
        kpv.derive(head, toff)
        expected = [KeyPointValue(index=4, value=360-7.5,
                                  name='Heading At Takeoff')]
        self.assertEqual(kpv, expected)

class TestHeadingAtLanding(unittest.TestCase):
    def test_can_operate(self):
        expected = [('Heading Continuous', 'Landing')]
        opts = HeadingAtLanding.get_operational_combinations()
        self.assertEqual(opts, expected) 
        
    def test_derive_basic(self):
        head = P('Heading Continuous',np.ma.array([0,1,2,3,4,5,6,7,8,9,10,-1,-1,
                                                   7,-1,-1,-1,-1,-1,-1,-1,-10]))
        landing = buildsection('Landing',5,15)
        head.array[13] = np.ma.masked
        kpv = HeadingAtLanding()
        kpv.derive(head, landing)
        expected = [KeyPointValue(index=10, value=6.0,
                                  name='Heading At Landing')]
        self.assertEqual(kpv, expected)


class TestILSFrequencyOnApproach(unittest.TestCase):
    def test_can_operate(self):
        expected = [('ILS Frequency', 'ILS Localizer Established',)]
        opts = ILSFrequencyOnApproach.get_operational_combinations()
        self.assertEqual(opts, expected) 
        
    def test_derive_basic(self):
        # Let's give this a really hard time with alternate samples invalid and
        # the final signal only tuned just at the end of the data.
        frq = P('ILS Frequency',np.ma.array([108.5]*6+[114.05]*4))
        frq.array[0:10:2] = np.ma.masked
        ils = buildsection('ILS Localizer Established', 2, 9)
        kpv = ILSFrequencyOnApproach()
        kpv.derive(frq, ils)
        expected = [KeyPointValue(index=2, value=108.5, 
                                  name='ILS Frequency On Approach')]
        self.assertEqual(kpv, expected)


class TestILSLocalizerDeviation1500To1000FtMax(unittest.TestCase):
    def test_can_operate(self):
        expected = [('ILS Localizer','Altitude AAL For Flight Phases',
                     'ILS Localizer Established')]
        opts = ILSLocalizerDeviation1500To1000FtMax.get_operational_combinations()
        self.assertEqual(opts, expected) 
        
    def test_derive_basic(self):
        testline = np.arange(0,12.6,0.1)
        testwave = (np.cos(testline)*(-1000))+1000
        alt_ph = P('Altitude AAL For Flight Phases',
                           np.ma.array(testwave))
        ils_loc = P('ILS Localizer', np.ma.array(testline))
        loc_est = buildsection('ILS Localizer Established', 30,115)
        kpv = ILSLocalizerDeviation1500To1000FtMax()
        kpv.derive(ils_loc, alt_ph, loc_est)
        # 'KeyPointValue', 'index value name'
        self.assertEqual(len(kpv), 2)
        self.assertEqual(kpv[0].index, 47)
        self.assertEqual(kpv[1].index, 109)
        
        
class TestILSLocalizerDeviation1000To250FtMax(unittest.TestCase):
    def test_can_operate(self):
        expected = [('ILS Localizer','Altitude AAL For Flight Phases',
                     'ILS Localizer Established')]
        opts = ILSLocalizerDeviation1000To250FtMax.get_operational_combinations()
        self.assertEqual(opts, expected) 
        
    def test_ils_loc_1000_250_basic(self):
        testline = np.arange(0,12.6,0.1)
        testwave = (np.cos(testline)*(-1000))+1000
        alt_ph = P('Altitude AAL For Flight Phases',
                           np.ma.array(testwave))
        ils_loc = P('ILS Localizer', np.ma.array(testline))
        loc_est = buildsection('ILS Localizer Established', 30,115)
        kpv = ILSLocalizerDeviation1000To250FtMax()
        kpv.derive(ils_loc, alt_ph, loc_est)
        # 'KeyPointValue', 'index value name'
        self.assertEqual(len(kpv), 2)
        self.assertEqual(kpv[0].index, 55)
        self.assertEqual(kpv[0].value, 5.5)
        self.assertEqual(kpv[1].index, 114)
        self.assertEqual(kpv[1].value, 11.4)


class TestMachMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = MachMax
        self.operational_combinations = [('Mach', 'Airborne')]
        self.function = max_value

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestAltitudeAtFirstFlapChangeAfterLiftoff(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AltitudeAtFirstFlapChangeAfterLiftoff.get_operational_combinations(),
            [('Flap', 'Altitude AAL', 'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeAtGearDownSelection(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AltitudeAtGearDownSelection.get_operational_combinations(),
            [('Altitude AAL', 'Gear Down Selection',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeAtGearUpSelection(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AltitudeAtGearUpSelection.get_operational_combinations(),
            [('Altitude AAL', 'Gear Up Selection',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeAtLastFlapChangeBeforeLanding(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AltitudeAtLastFlapChangeBeforeLanding.get_operational_combinations(),
            [('Flap', 'Altitude AAL', 'Touchdown',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeAtLiftoff(unittest.TestCase,
                            CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeAtLiftoff
        self.operational_combinations = [('Altitude STD Smoothed', 'Liftoff',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAltitudeAutopilotDisengaged(unittest.TestCase,
                                      CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeAutopilotDisengaged
        self.operational_combinations = [('Altitude AAL',
                                          'AP Disengaged Selection',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAltitudeAutopilotEngaged(unittest.TestCase,
                                   CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeAutopilotEngaged
        self.operational_combinations = [('Altitude AAL',
                                          'AP Engaged Selection',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAltitudeAutothrottleDisengaged(unittest.TestCase,
                                         CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeAutothrottleDisengaged
        self.operational_combinations = [('Altitude AAL',
                                          'AT Disengaged Selection',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAltitudeAutothrottleEngaged(unittest.TestCase,
                                      CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeAutothrottleEngaged
        self.operational_combinations = [('Altitude AAL',
                                          'AT Engaged Selection',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAltitudeFlapExtensionMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AltitudeFlapExtensionMax.get_operational_combinations(),
            [('Flap', 'Altitude AAL', 'Airborne',)])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeGoAroundFlapRetracted(unittest.TestCase,
                                        CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeGoAroundFlapRetracted
        self.operational_combinations = [('Altitude AAL',
                                          'Go Around Flap Retracted',)]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestAltitudeWithFlapsMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AltitudeWithFlapsMax.get_operational_combinations(),
            [('Flap', 'Altitude STD Smoothed', 'Airborne',)])  
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')

class TestDecelerateToStopOnRunwayDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')       
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestDecelerationLongitudinalPeakLanding(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestDecelerationFromTouchdownToStopOnRunway(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            DecelerationFromTouchdownToStopOnRunway.get_operational_combinations(),
            [('Groundspeed', 'Touchdown', 'Landing', 'Latitude At Touchdown', 
              'Longitude At Touchdown', 'FDR Landing Runway',
              'ILS Glideslope Established', 'ILS Localizer Established',
              'Precise Positioning')])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestDistanceFrom60KtToRunwayEnd(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestDistanceFromRunwayStartToTouchdown(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestDistanceFromTouchdownToRunwayEnd(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestDistancePastGlideslopeAntennaToTouchdown(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngBleedValvesAtLiftoff(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngEPRAboveFL100Max(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngEPRToFL100Max(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngGasTempGoAroundMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngGasTempMaximumContinuousPowerMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngGasTempStartMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN1500To20FtMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN1CyclesInFinalApproach(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN1GoAroundMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN1MaximumContinuousPowerMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN1TaxiMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN2CyclesInFinalApproach(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN2GoAroundMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN2MaximumContinuousPowerMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN2TakeoffMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN2TaxiMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN3GoAroundMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN3MaximumContinuousPowerMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN3TakeoffMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngN3TaxiMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngOilPressMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngOilPressMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngOilQtyMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngOilQtyMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngTorque500FtToTouchdownMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngTorque500FtToTouchdownMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngTorqueAbove10000FtMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngTorqueAbove10000FtMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngTorqueAboveFL100Max(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngTorqueGoAroundMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngTorqueMaximumContinuousPowerMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngTorqueTakeoffMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEngTorqueToFL100Max(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestEventMarkerPressed(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestFlapWithSpeedbrakesDeployedMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGenericDescent(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGroundspeedOnGroundMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGroundspeedThrustReversersDeployedMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeadingAtLowestPointOnApproach(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeadingExcursion500To20Ft(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeadingExcursionOnLandingAbove100Kts(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeadingExcursionOnTakeoffAbove100Kts(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeadingExcursionTouchdownPlus4SecTo60Kts(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeadingVacatingRunway(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeightLost1000To2000Ft(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeightLost35To1000Ft(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeightLostTakeoffTo35Ft(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestHeightOfBouncedLanding(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestIsolationValveOpenAtLiftoff(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestLatitudeAtLanding(unittest.TestCase, NodeTest):
    def setUp(self):
        self.node_class = LatitudeAtLanding
        self.operational_combinations = [
            ('Latitude', 'Touchdown'),
            ('Touchdown', 'AFR Landing Airport'),
            ('Touchdown', 'AFR Landing Runway'),
            ('Latitude', 'Touchdown', 'AFR Landing Airport'),
            ('Latitude', 'Touchdown', 'AFR Landing Runway'),
            ('Touchdown', 'AFR Landing Airport', 'AFR Landing Runway'),
            ('Latitude', 'Touchdown', 'AFR Landing Airport', 'AFR Landing Runway'),
        ]

    def test_derive_with_latitude(self):
        lat = P(name='Latitude')
        lat.array = Mock()
        tdwns = KTI(name='Touchdown')
        afr_land_rwy = None
        afr_land_apt = None
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lat, tdwns, afr_land_rwy, afr_land_apt)
        node.create_kpvs_at_ktis.assert_called_once_with(lat.array, tdwns)
        assert not node.create_kpv.called, 'method should not have been called'

    def test_derive_with_afr_land_rwy(self):
        lat = None
        tdwns = KTI(name='Touchdown', items=[KeyTimeInstance(index=0)])
        afr_land_rwy = A(name='AFR Landing Runway', value={
            'start': {'latitude': 0, 'longitude': 0},
            'end': {'latitude': 1, 'longitude': 1},
        })
        afr_land_apt = None
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lat, tdwns, afr_land_apt, afr_land_rwy)
        lat_m, lon_m = midpoint(0, 0, 1, 1)
        node.create_kpv.assert_called_once_with(tdwns[-1].index, lat_m)
        assert not node.create_kpvs_at_ktis.called, 'method should not have been called'

    def test_derive_with_afr_land_apt(self):
        lat = None
        tdwns = KTI(name='Touchdown', items=[KeyTimeInstance(index=0)])
        afr_land_rwy = None
        afr_land_apt = A(name='AFR Landing Airport', value={
            'latitude': 1,
            'longitude': 1,
        })
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lat, tdwns, afr_land_apt, afr_land_rwy)
        node.create_kpv.assert_called_once_with(tdwns[-1].index, 1)
        assert not node.create_kpvs_at_ktis.called, 'method should not have been called'

class TestLatitudeAtTakeoff(unittest.TestCase, NodeTest):
    def setUp(self):
        self.node_class = LatitudeAtTakeoff
        self.operational_combinations = [
            ('Latitude', 'Liftoff'),
            ('Liftoff', 'AFR Takeoff Airport'),
            ('Liftoff', 'AFR Takeoff Runway'),
            ('Latitude', 'Liftoff', 'AFR Takeoff Airport'),
            ('Latitude', 'Liftoff', 'AFR Takeoff Runway'),
            ('Liftoff', 'AFR Takeoff Airport', 'AFR Takeoff Runway'),
            ('Latitude', 'Liftoff', 'AFR Takeoff Airport', 'AFR Takeoff Runway'),
        ]

    def test_derive_with_latitude(self):
        lat = P(name='Latitude')
        lat.array = Mock()
        liftoffs = KTI(name='Liftoff')
        afr_toff_rwy = None
        afr_toff_apt = None
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lat, liftoffs, afr_toff_rwy, afr_toff_apt)
        node.create_kpvs_at_ktis.assert_called_once_with(lat.array, liftoffs)
        assert not node.create_kpv.called, 'method should not have been called'

    def test_derive_with_afr_toff_rwy(self):
        lat = None
        liftoffs = KTI(name='Liftoff', items=[KeyTimeInstance(index=0)])
        afr_toff_rwy = A(name='AFR Takeoff Runway', value={
            'start': {'latitude': 0, 'longitude': 0},
            'end': {'latitude': 1, 'longitude': 1},
        })
        afr_toff_apt = None
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lat, liftoffs, afr_toff_apt, afr_toff_rwy)
        lat_m, lon_m = midpoint(0, 0, 1, 1)
        node.create_kpv.assert_called_once_with(liftoffs[0].index, lat_m)
        assert not node.create_kpvs_at_ktis.called, 'method should not have been called'

    def test_derive_with_afr_toff_apt(self):
        lat = None
        liftoffs = KTI(name='Liftoff', items=[KeyTimeInstance(index=0)])
        afr_toff_rwy = None
        afr_toff_apt = A(name='AFR Takeoff Airport', value={
            'latitude': 1,
            'longitude': 1,
        })
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lat, liftoffs, afr_toff_apt, afr_toff_rwy)
        node.create_kpv.assert_called_once_with(liftoffs[0].index, 1)
        assert not node.create_kpvs_at_ktis.called, 'method should not have been called'


class TestLatitudeAtTouchdown(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = LatitudeAtTouchdown
        self.operational_combinations = [('Latitude Smoothed', 'Touchdown')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestLatitudeAtLiftoff(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = LatitudeAtLiftoff
        self.operational_combinations = [('Latitude Smoothed', 'Liftoff')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestLatitudeAtLowestPointOnApproach(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestLongitudeAtLanding(unittest.TestCase, NodeTest):
    def setUp(self):
        self.node_class = LongitudeAtLanding
        self.operational_combinations = [
            ('Longitude', 'Touchdown'),
            ('Touchdown', 'AFR Landing Airport'),
            ('Touchdown', 'AFR Landing Runway'),
            ('Longitude', 'Touchdown', 'AFR Landing Airport'),
            ('Longitude', 'Touchdown', 'AFR Landing Runway'),
            ('Touchdown', 'AFR Landing Airport', 'AFR Landing Runway'),
            ('Longitude', 'Touchdown', 'AFR Landing Airport', 'AFR Landing Runway'),
        ]

    def test_derive_with_longitude(self):
        lon = P(name='Latitude')
        lon.array = Mock()
        tdwns = KTI(name='Touchdown')
        afr_land_rwy = None
        afr_land_apt = None
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lon, tdwns, afr_land_rwy, afr_land_apt)
        node.create_kpvs_at_ktis.assert_called_once_with(lon.array, tdwns)
        assert not node.create_kpv.called, 'method should not have been called'

    def test_derive_with_afr_land_rwy(self):
        lon = None
        tdwns = KTI(name='Touchdown', items=[KeyTimeInstance(index=0)])
        afr_land_rwy = A(name='AFR Landing Runway', value={
            'start': {'latitude': 0, 'longitude': 0},
            'end': {'latitude': 1, 'longitude': 1},
        })
        afr_land_apt = None
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lon, tdwns, afr_land_apt, afr_land_rwy)
        lat_m, lon_m = midpoint(0, 0, 1, 1)
        node.create_kpv.assert_called_once_with(tdwns[-1].index, lon_m)
        assert not node.create_kpvs_at_ktis.called, 'method should not have been called'

    def test_derive_with_afr_land_apt(self):
        lon = None
        tdwns = KTI(name='Touchdown', items=[KeyTimeInstance(index=0)])
        afr_land_rwy = None
        afr_land_apt = A(name='AFR Landing Airport', value={
            'latitude': 1,
            'longitude': 1,
        })
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lon, tdwns, afr_land_apt, afr_land_rwy)
        node.create_kpv.assert_called_once_with(tdwns[-1].index, 1)
        assert not node.create_kpvs_at_ktis.called, 'method should not have been called'


class TestLongitudeAtTakeoff(unittest.TestCase, NodeTest):
    def setUp(self):
        self.node_class = LongitudeAtTakeoff
        self.operational_combinations = [
            ('Longitude', 'Liftoff'),
            ('Liftoff', 'AFR Takeoff Airport'),
            ('Liftoff', 'AFR Takeoff Runway'),
            ('Longitude', 'Liftoff', 'AFR Takeoff Airport'),
            ('Longitude', 'Liftoff', 'AFR Takeoff Runway'),
            ('Liftoff', 'AFR Takeoff Airport', 'AFR Takeoff Runway'),
            ('Longitude', 'Liftoff', 'AFR Takeoff Airport', 'AFR Takeoff Runway'),
        ]

    def test_derive_with_longitude(self):
        lon = P(name='Longitude')
        lon.array = Mock()
        liftoffs = KTI(name='Liftoff')
        afr_toff_rwy = None
        afr_toff_apt = None
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lon, liftoffs, afr_toff_rwy, afr_toff_apt)
        node.create_kpvs_at_ktis.assert_called_once_with(lon.array, liftoffs)
        assert not node.create_kpv.called, 'method should not have been called'

    def test_derive_with_afr_toff_rwy(self):
        lon = None
        liftoffs = KTI(name='Liftoff', items=[KeyTimeInstance(index=0)])
        afr_toff_rwy = A(name='AFR Takeoff Runway', value={
            'start': {'latitude': 0, 'longitude': 0},
            'end': {'latitude': 1, 'longitude': 1},
        })
        afr_toff_apt = None
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lon, liftoffs, afr_toff_apt, afr_toff_rwy)
        lat_m, lon_m = midpoint(0, 0, 1, 1)
        node.create_kpv.assert_called_once_with(liftoffs[0].index, lon_m)
        assert not node.create_kpvs_at_ktis.called, 'method should not have been called'

    def test_derive_with_afr_toff_apt(self):
        lon = None
        liftoffs = KTI(name='Liftoff', items=[KeyTimeInstance(index=0)])
        afr_toff_rwy = None
        afr_toff_apt = A(name='AFR Takeoff Airport', value={
            'latitude': 1,
            'longitude': 1,
        })
        node = self.node_class()
        node.create_kpv = Mock()
        node.create_kpvs_at_ktis = Mock()
        node.derive(lon, liftoffs, afr_toff_apt, afr_toff_rwy)
        node.create_kpv.assert_called_once_with(liftoffs[0].index, 1)
        assert not node.create_kpvs_at_ktis.called, 'method should not have been called'


class TestLongitudeAtTouchdown(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = LongitudeAtTouchdown
        self.operational_combinations = [('Longitude Smoothed', 'Touchdown')]
        
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestLongitudeAtLiftoff(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = LongitudeAtLiftoff
        self.operational_combinations = [('Longitude Smoothed', 'Liftoff')]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')     


class TestLongitudeAtLowestPointOnApproach(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestMachAsGearExtendingMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestMachAsGearRetractingMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestMachMax3Sec(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestMachWithGearDownMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestMagneticVariationAtLanding(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestMagneticVariationAtTakeoff(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPackValvesOpenAtLiftoff(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestSpeedbrakesDeployedInGoAroundDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestSpeedbrakesDeployedWithPowerOnInHeightBandsDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestStickPusherActivatedDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSAlertDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSDontSinkWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSGlideslopeWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSPullUpWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSSinkRateWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTerrainPullUpWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTerrainWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTooLowFlapWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTooLowGearWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTooLowTerrainWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSWindshearWarningBelow1500FtDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTCASRAInitialReaction(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTCASRAReactionDelay(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTCASRAToAPDisengageDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTCASRAWarningDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTouchdownTo60KtsDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTouchdownToElevatorDownDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestDescentToFlare(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGearExtending(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGoAround5MinRating(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestLevelFlight(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTakeoff5MinRating(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTakeoffRoll(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTakeoffRotation(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTwoDegPitchTo35Ft(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')







class TestAltitudeMinsToTouchdown(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AltitudeMinsToTouchdown.get_operational_combinations(),
            [('Altitude AAL', 'Mins To Touchdown',)])        
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestFlapAtGearDownSelection(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestFlapWithGearUpMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestFlapAtLiftoff(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = FlapAtLiftoff
        self.operational_combinations = [('Flap', 'Liftoff')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestFlapAtTouchdown(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = FlapAtTouchdown
        self.operational_combinations = [('Flap', 'Touchdown')]
        
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestFlareDuration20FtToTouchdown(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')
        

class TestFlareDistance20FtToTouchdown(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeOvershootAtSuspectedLevelBust(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test Not Implemented')      
    
    def test_derive_handling_no_data(self):
        alt=P('Altitude STD',np.ma.array([0,1000,1000,1000,1000]))
        kpv=AltitudeOvershootAtSuspectedLevelBust()
        kpv.derive(alt)
        expected=[]
        self.assertEqual(kpv,expected)
        
    def test_derive_up_down_and_up(self):
        testwave = np.ma.array(1.0+np.sin(np.arange(0,12.6,0.1)))*1000
        alt=P('Altitude STD',testwave)
        kpv=AltitudeOvershootAtSuspectedLevelBust()
        kpv.derive(alt)
        expected=[KeyPointValue(index=16, value=999.5736030415051, 
                                name='Altitude Overshoot At Suspected Level Bust'),
                  KeyPointValue(index=47, value=-1998.4666029387058, 
                                name='Altitude Overshoot At Suspected Level Bust'), 
                  KeyPointValue(index=79, value=1994.3775951461494, 
                                name='Altitude Overshoot At Suspected Level Bust'), 
                  KeyPointValue(index=110, value=-834.386031102394,  #-933.6683091995028, XXX: Ask Dave if the minimum value is correct.
                                name='Altitude Overshoot At Suspected Level Bust')]
        self.assertEqual(kpv,expected)
        
    def test_derive_too_slow(self):
        testwave = np.ma.array(1.0+np.sin(np.arange(0,12.6,0.1)))*1000
        alt=P('Altitude STD',testwave,0.02)
        kpv=AltitudeOvershootAtSuspectedLevelBust()
        kpv.derive(alt)
        expected=[]
        self.assertEqual(kpv,expected)

    def test_derive_straight_up_and_down(self):
        testwave = np.ma.array(range(0,10000,50)+range(10000,0,-50))
        alt=P('Altitude STD',testwave,1)
        kpv=AltitudeOvershootAtSuspectedLevelBust()
        kpv.derive(alt)
        expected=[]
        self.assertEqual(kpv,expected)
        
    def test_derive_up_and_down_with_overshoot(self):
        testwave = np.ma.array(range(0,10000,50)+range(10000,9000,-50)+[9000]*200+range(9000,0,-50))
        alt=P('Altitude STD',testwave,1)
        kpv=AltitudeOvershootAtSuspectedLevelBust()
        kpv.derive(alt)
        expected=[KeyPointValue(index=200, value=1000, 
                                name='Altitude Overshoot At Suspected Level Bust')] 
        self.assertEqual(kpv,expected)

    def test_derive_up_and_down_with_undershoot(self):
        testwave = np.ma.array(range(0,10000,50)+
                               [10000]*200+
                               range(10000,9000,-50)+
                               range(9000,20000,50)+
                               range(20000,0,-50))
        alt=P('Altitude STD',testwave,1)
        kpv=AltitudeOvershootAtSuspectedLevelBust()
        kpv.derive(alt)
        expected=[KeyPointValue(index=420, value=-1000, 
                                name='Altitude Overshoot At Suspected Level Bust')]
        self.assertEqual(kpv,expected)


class TestFuelQtyAtLiftoff(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = FuelQtyAtLiftoff
        self.operational_combinations = [('Fuel Qty', 'Liftoff')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 
        

class TestFuelQtyAtTouchdown(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = FuelQtyAtTouchdown
        self.operational_combinations = [('Fuel Qty', 'Touchdown')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestGrossWeightAtLiftoff(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = GrossWeightAtLiftoff
        self.operational_combinations = [('Gross Weight Smoothed', 'Liftoff')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestGrossWeightAtTouchdown(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = GrossWeightAtTouchdown
        self.operational_combinations = [('Gross Weight Smoothed', 'Touchdown')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestGroundspeedTaxiingStraightMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGroundspeedTaxiingTurnsMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGroundspeedRTOMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGroundspeedAtTouchdown(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestGroundspeedOnGroundMax(unittest.TestCase, CreateKPVFromSlicesTest):
    def setUp(self):
        self.node_class = GroundspeedOnGroundMax
        self.operational_combinations = [('Groundspeed', 'Grounded')]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')   


class TestGroundspeedVacatingRunway(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Pitch


class TestPitchMaxAfterFlapRetraction(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitchAtLiftoff(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = PitchAtLiftoff
        self.operational_combinations = [('Pitch', 'Liftoff')]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')     


class TestPitchAtTouchdown(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = PitchAtTouchdown
        self.operational_combinations = [('Pitch', 'Touchdown')]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestPitchAt35FtInClimb(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitchTakeoffTo35FtMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitch35To400FtMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Pitch35To400FtMax
        self.operational_combinations = [('Pitch',
                                          'Altitude AAL For Flight Phases')]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (35, 400,), {})]
        
    def test_derive_basic(self):
        pch = [0,2,4,7,9,8,6,3,-1]
        alt = [100,101,102,103,700,105,104,103,102]
        alt_ph = P('Altitude AAL For Flight Phases', np.ma.array(alt))
        pitch = P('Pitch', np.ma.array(pch))
        kpv = Pitch35To400FtMax()
        kpv.derive(pitch, alt_ph)
        self.assertEqual(len(kpv), 1)
        self.assertEqual(kpv[0].index, 3)
        self.assertEqual(kpv[0].value, 7)


class TestPitch35To400FtMin(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Pitch35To400FtMin
        self.operational_combinations = [('Pitch',
                                          'Altitude AAL For Flight Phases')]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (35, 400,), {})]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 
        

class TestPitch400To1000FtMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitch400To1000FtMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitch1000To500FtMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitch1000To500FtMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')
        

class TestPitch500To50FtMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitch500To20FtMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitch50FtToLandingMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitch20FtToLandingMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitch7FtToLandingMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        class TestPitchCyclesInFinalApproach(unittest.TestCase):
            @unittest.skip('Test Not Implemented')
            def test_can_operate(self):
                self.assertTrue(False, msg='Test not implemented.')
            
            @unittest.skip('Test Not Implemented')    
            def test_derive(self):
                self.assertTrue(False, msg='Test not implemented.')    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitchCyclesInFinalApproach(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Pitch Rate


class TestPitchRate35To1000FtMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitchRate20FtToTouchdownMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitchRate20FtToTouchdownMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitchRate2DegPitchTo35FtMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitchRate2DegPitchTo35FtMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitchRate2DegPitchTo35FtAverage(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTwoDegPitchTo35FtDuration(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Rate of Climb


class TestRateOfClimbMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRateOfClimb35To1000FtMin(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRateOfClimbBelow10000FtMax(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Rate of Descent


class TestRateOfDescentMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            RateOfDescentMax.get_operational_combinations(),
            [('Vertical Speed', 'Descending')])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRateOfDescentTopOfDescentTo10000FtMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            RateOfDescentTopOfDescentTo10000FtMax.get_operational_combinations(),
            [('Altitude AAL For Flight Phases', 'Vertical Speed', 'Descent')])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRateOfDescentBelow10000FtMax(unittest.TestCase,
                                        CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RateOfDescentBelow10000FtMax
        self.operational_combinations = [('Vertical Speed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (10000, 0), {})]
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRateOfDescent10000To5000FtMax(unittest.TestCase,
                                        CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RateOfDescent10000To5000FtMax
        self.operational_combinations = [('Vertical Speed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (10000, 5000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestRateOfDescent5000To3000FtMax(unittest.TestCase,
                                       CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RateOfDescent5000To3000FtMax
        self.operational_combinations = [('Vertical Speed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (5000, 3000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestRateOfDescent3000To2000FtMax(unittest.TestCase,
                                       CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RateOfDescent3000To2000FtMax
        self.operational_combinations = [('Vertical Speed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (3000, 2000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestRateOfDescent2000To1000FtMax(unittest.TestCase,
                                       CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RateOfDescent2000To1000FtMax
        self.operational_combinations = [('Vertical Speed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (2000, 1000), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 


class TestRateOfDescent1000To500FtMax(unittest.TestCase,
                                      CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RateOfDescent1000To500FtMax
        self.operational_combinations = [('Vertical Speed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (1000, 500), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 
        

class TestRateOfDescent500To20FtMax(unittest.TestCase,
                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RateOfDescent500To20FtMax
        self.operational_combinations = [('Vertical Speed',
                                          'Altitude AAL For Flight Phases',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_from_to', (500, 20), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented') 
        

# FIXME: Uses slices_to_kti(), not slices_from_to()!
class TestRateOfDescent500FtToTouchdownMax(unittest.TestCase,
                                           CreateKPVsWithinSlicesTest):
    # TODO: CreateKPVsWithinSlices with 3-Args
    def setUp(self):
        # XXX: This test does not explicitly test how the Touchdown dependency
        #      is used.
        self.node_class = RateOfDescent500FtToTouchdownMax
        self.operational_combinations = [('Vertical Speed',
                                          'Altitude AAL For Flight Phases',
                                          'Touchdown',)]
        self.function = min_value
        self.second_param_method_calls = [('slices_to_kti', (500, []), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestRateOfDescent20ToTouchdownMax(unittest.TestCase):
    # TODO: CreateKPVsWithinSlices with 3-Args
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRateOfDescentAtTouchdown(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            RateOfDescentAtTouchdown.get_operational_combinations(),
            [('Vertical Speed Inertial', 'Landing', 'Altitude AAL')])
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Roll


class TestRollTakeoffTo20FtMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RollTakeoffTo20FtMax
        self.operational_combinations = [
            ('Roll', 'Altitude AAL For Flight Phases',)]
        self.function = max_abs_value
        self.second_param_method_calls = [('slices_from_to', (1, 20), {})]
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRoll20To400FtMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Roll20To400FtMax
        self.operational_combinations = [
            ('Roll', 'Altitude AAL For Flight Phases',)]
        self.function = max_abs_value
        self.second_param_method_calls = [('slices_from_to', (20, 400), {})]
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRoll400To1000FtMax(unittest.TestCase,
                             CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Roll400To1000FtMax
        self.operational_combinations = [
            ('Roll', 'Altitude AAL For Flight Phases',)]
        self.function = max_abs_value
        self.second_param_method_calls = [('slices_from_to', (400, 1000), {})]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRollAbove1000FtMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RollAbove1000FtMax
        self.operational_combinations = [('Roll',
                                          'Altitude AAL For Flight Phases')]
        self.function = max_abs_value
        self.second_param_method_calls = [('slices_above', (1000,), {})]

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test Not Implemented')


class TestRoll1000To300FtMax(unittest.TestCase,
                             CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Roll1000To300FtMax
        self.operational_combinations = [
            ('Roll', 'Altitude AAL For Flight Phases',)]
        self.function = max_abs_value
        self.second_param_method_calls = [('slices_from_to', (1000, 300), {})]
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRoll300To20FtMax(unittest.TestCase,
                           CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Roll300To20FtMax
        self.operational_combinations = [
            ('Roll', 'Altitude AAL For Flight Phases',)]
        self.function = max_abs_value
        self.second_param_method_calls = [('slices_from_to', (300, 20), {})]
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRoll20FtToLandingMax(unittest.TestCase,
                               CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Roll20FtToLandingMax
        self.operational_combinations = [
            ('Roll', 'Altitude AAL For Flight Phases',)]
        self.function = max_abs_value
        self.second_param_method_calls = [('slices_from_to', (20, 1), {})]
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRollCyclesInFinalApproach(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            RollCyclesInFinalApproach.get_operational_combinations(),
            [('Roll', 'Final Approach')])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRollCyclesNotInFinalApproach(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            RollCyclesNotInFinalApproach.get_operational_combinations(),
            [('Roll', 'Airborne', 'Final Approach', 'Landing')])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Rudder


class TestRudderExcursionDuringTakeoff(unittest.TestCase,
                                   CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = RudderExcursionDuringTakeoff
        self.operational_combinations = [('Rudder', 'Takeoff Roll',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestRudderReversalAbove50Ft(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            RudderReversalAbove50Ft.get_operational_combinations(),
            [('Rudder', 'Altitude AAL For Flight Phases',)])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Speedbrake


class TestSpeedbrakesDeployed1000To20FtDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            SpeedbrakesDeployed1000To20FtDuration.get_operational_combinations(),
            [('Speedbrake Selected', 'Altitude AAL For Flight Phases',)])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestSpeedbrakesDeployedWithPowerOnDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            SpeedbrakesDeployedWithPowerOnDuration.get_operational_combinations(),
            [('Speedbrake Selected', 'Eng (*) N1 Avg', 'Airborne',
              'Manufacturer')])    
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestSpeedbrakesDeployedWithFlapDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            SpeedbrakesDeployedWithConfDuration.get_operational_combinations(),
            [('Speedbrake Selected', 'Configuration',)])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestSpeedbrakesDeployedWithConfDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            SpeedbrakesDeployedWithConfDuration.get_operational_combinations(),
            [('Speedbrake Selected', 'Configuration',)])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestSpeedbrakesDeployedWithPowerOnInHeightBandsDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            SpeedbrakesDeployedWithPowerOnInHeightBandsDuration.get_operational_combinations(),
            [('Speedbrake Selected', 'Eng (*) N1 Avg',
              'Altitude AAL For Flight Phases', 'Airborne')])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Warnings: Stick Pusher/Shaker


class TestStickPusherActivatedDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestStickShakerActivatedDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Tail Clearance


class TestTailClearanceOnTakeoffMin(unittest.TestCase,
                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = TailClearanceOnTakeoffMin
        self.operational_combinations = [('Altitude Tail', 'Takeoff',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTailClearanceOnLandingMin(unittest.TestCase,
                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = TailClearanceOnLandingMin
        self.operational_combinations = [('Altitude Tail', 'Landing',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTailClearanceOnApproach(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(TailClearanceOnApproach.get_operational_combinations(),
                         [('Altitude AAL', 'Altitude Tail',
                           'Distance To Landing')])
    
    def test_derive(self):
        # XXX: The BDUTerrain test files are missing from the repository?
        test_data_dir = os.path.join(test_data_path, 'BDUTerrain')
        alt_aal_array = np.ma.masked_array(np.load(os.path.join(test_data_dir,
                                                                'alt_aal.npy')))
        alt_radio_array = \
            np.ma.masked_array(np.load(os.path.join(test_data_dir,
                                                    'alt_radio.npy')))
        dtl_array = np.ma.masked_array(np.load(os.path.join(test_data_dir,
                                                            'dtl.npy')))
        alt_aal = P(array=alt_aal_array, frequency=8)
        alt_radio = P(array=alt_radio_array, frequency=0.5)
        dtl = P(array=dtl_array, frequency=0.25)
        alt_radio.array = align(alt_radio, alt_aal)
        dtl.array = align(dtl, alt_aal)        
        # Q: Should tests for the BDUTerrain node be in a separate TestCase?
        param = BDUTerrain()
        param.derive(alt_aal, alt_radio, dtl)
        self.assertEqual(param, [KeyPointValue(name='BDU Terrain', index=1008,
                                               value=0.037668517049960347)])


class TestTerrainClearanceAbove3000FtMin(unittest.TestCase,
                                         CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = TerrainClearanceAbove3000FtMin
        self.operational_combinations = [('Altitude Radio',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_above', (3000.0,), {})]
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Tailwind


class TestTailwindLiftoffTo100FtMax(unittest.TestCase,
                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = TailwindLiftoffTo100FtMax
        self.operational_combinations = [('Tailwind',
                                          'Altitude AAL For Flight Phases',)]
        self.second_param_method_calls = [('slices_from_to', (0, 100,), {})]
        self.function = max_value
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTailwind100FtToTouchdownMax(unittest.TestCase,
                                      CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = Tailwind100FtToTouchdownMax
        self.operational_combinations = [('Tailwind',
                                          'Altitude AAL For Flight Phases',)]
        self.function = max_value
        self.second_param_method_calls = [('slices_from_to', (100, 0,), {})]
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')
        

################################################################################
# Warnings: Takeoff Configuration Warning


class TestTakeoffConfigWarningDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')    


class TestMasterWarningInTakeoffDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')    


class TestMasterCautionInTakeoffDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Warnings: Terrain Awareness & Warning System (TAWS)


class TestTAWSGeneralDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSAlertDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSSinkRateWarningDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTooLowFlapWarningDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTerrainWarningDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTerrainPullUpWarningDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSGlideslopeWarningAbove1000FtDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSGlideslopeWarning1000To500FtDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSGlideslopeWarning500To150FtDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTooLowTerrainWarningDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSTooLowGearWarningDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSPullUpWarningDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSDontSinkWarningDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTAWSWindshearWarningBelow1500FtDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState Test Superclass
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Warnings: Traffic Collision Avoidance System (TCAS)


class TestTCASRAWarningDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            TCASRAWarningDuration.get_operational_combinations(),
            [('TCAS Combined Control', 'Airborne'),])
        
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTCASRAReactionDelay(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            TCASRAReactionDelay.get_operational_combinations(),
            [('Acceleration Normal Offset Removed', 'TCAS Combined Control',
              'Airborne'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTCASRAInitialReaction(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            TCASRAInitialReaction.get_operational_combinations(),
            [('Acceleration Normal Offset Removed', 'TCAS Combined Control',
              'Airborne'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTCASRAToAPDisengageDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            TCASRAToAPDisengageDuration.get_operational_combinations(),
            [('AP Disengaged Selection', 'TCAS Combined Control', 'Airborne'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################


class TestThrottleCyclesInFinalApproach(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            ThrottleCyclesInFinalApproach.get_operational_combinations(),
            [('Throttle Levers', 'Final Approach'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Thrust Asymmetry in different conditions


class TestThrustAsymmetryOnTakeoff(unittest.TestCase,
                                   CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = ThrustAsymmetryOnTakeoff
        self.operational_combinations = [('Thrust Asymmetry',
                                          'Takeoff Roll',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestThrustAsymmetryInFlight(unittest.TestCase,
                                  CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = ThrustAsymmetryInFlight
        self.operational_combinations = [('Thrust Asymmetry',
                                          'Airborne',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestThrustAsymmetryWithReverseThrustMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            ThrustAsymmetryWithReverseThrustMax.get_operational_combinations(),
            [('Thrust Asymmetry', 'Thrust Reversers'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestThrustAsymmetryWithReverseThrustDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            ThrustAsymmetryWithReverseThrustDuration.get_operational_combinations(),
            [('Thrust Asymmetry', 'Thrust Reversers', 'Mobile'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestThrustAsymmetryOnApproachMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            ThrustAsymmetryOnApproachMax.get_operational_combinations(),
            [('Thrust Asymmetry', 'Approach')])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestThrustAsymmetryOnApproachDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            ThrustAsymmetryOnApproachDuration.get_operational_combinations(),
            [('Thrust Asymmetry', 'Approach')])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTouchdownToElevatorDownDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            TouchdownToElevatorDownDuration.get_operational_combinations(),
            [('Airspeed', 'Elevator', 'Touchdown')])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTouchdownTo60KtsDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            TouchdownTo60KtsDuration.get_operational_combinations(),
            [('Airspeed', 'Touchdown',),
             ('Airspeed', 'Groundspeed', 'Touchdown'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Turbulence


class TestTurbulenceInApproachMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            TurbulenceInApproachMax.get_operational_combinations(),
            [('Turbulence RMS g', 'Approach'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTurbulenceInCruiseMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            TurbulenceInCruiseMax.get_operational_combinations(),
            [('Turbulence RMS g', 'Cruise'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestTurbulenceInFlightMax(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            TurbulenceInFlightMax.get_operational_combinations(),
            [('Turbulence RMS g', 'Airborne'),])
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')    


################################################################################


class TestWindSpeedInDescent(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            WindSpeedInDescent.get_operational_combinations(),
            [('Altitude AAL For Flight Phases', 'Wind Speed'),])
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestWindDirectionInDescent(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            WindDirectionInDescent.get_operational_combinations(),
            [('Altitude AAL For Flight Phases', 'Wind Direction Continuous'),])
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestWindAcrossLandingRunwayAt50Ft(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            WindAcrossLandingRunwayAt50Ft.get_operational_combinations(),
            [('Wind Across Landing Runway', 'Landing'),])
        
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestZeroFuelWeight(unittest.TestCase):
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertEqual(ZeroFuelWeight.get_operational_combinations(),
                         [('Fuel Qty', 'Gross Weight')])    
    
    def test_derive(self):
        fuel = P('Fuel Qty', np.ma.array([1,2,3,4]))
        weight = P('Gross Weight', np.ma.array([11,12,13,14]))
        zfw = ZeroFuelWeight()
        zfw.derive(fuel, weight)
        self.assertEqual(zfw[0].value, 10.0)


class TestHoldingDuration(unittest.TestCase):
    # TODO: CreateKPVsFromSliceDurations test superclass.
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


################################################################################
# Go Around Related KPVs 
        
#See also: EngGasTempGoAroundMax, EngN1GoAroundMax, EngN2GoAroundMax,
#EngN3GoAroundMax, EngTorqueGoAroundMax


class TestTOGASelectedInGoAroundDuration(unittest.TestCase):
    # TODO: CreateKPVsWhereState test superclass.
    @unittest.skip('Test Not Implemented')
    def test_can_operate(self):
        self.assertTrue(False, msg='Test not implemented.')
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeAtGoAroundMin(unittest.TestCase, CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeAtGoAroundMin
        self.operational_combinations = [('Altitude AAL', 'Go Around',)]
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeGoAroundFlapRetracted(unittest.TestCase,
                                        CreateKPVsAtKTIsTest):
    def setUp(self):
        self.node_class = AltitudeGoAroundFlapRetracted
        self.operational_combinations = [('Altitude AAL',
                                          'Go Around Flap Retracted',)]
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAltitudeAtGoAroundGearUpSelection(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            AltitudeAtGoAroundGearUpSelection.get_operational_combinations(),
            [('Altitude AAL', 'Go Around And Climbout',
              'Go Around Gear Selected Up'),])
    
    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestSpeedbrakesDeployedInGoAroundDuration(unittest.TestCase):
    def test_can_operate(self):
        self.assertEqual(
            SpeedbrakesDeployedInGoAroundDuration.get_operational_combinations(),
            [('Speedbrake Selected', 'Go Around And Climbout')],
        )
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestThrustAsymmetryInGoAround(unittest.TestCase,
                                    CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = ThrustAsymmetryInGoAround
        self.operational_combinations = [('Thrust Asymmetry',
                                          'Go Around And Climbout',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestPitchInGoAroundMax(unittest.TestCase,
                             CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = PitchInGoAroundMax
        self.operational_combinations = [('Pitch',
                                          'Go Around And Climbout',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')

   
class TestVerticalSpeedInGoAroundMax(unittest.TestCase,
                                     CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = VerticalSpeedInGoAroundMax
        self.operational_combinations = [('Vertical Speed',
                                          'Go Around And Climbout',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')


class TestAOAInGoAroundMax(unittest.TestCase, CreateKPVsWithinSlicesTest):
    def setUp(self):
        self.node_class = AOAInGoAroundMax
        self.operational_combinations = [('AOA', 'Go Around And Climbout',)]
        self.function = max_value
    
    @unittest.skip('Test Not Implemented')    
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented.')

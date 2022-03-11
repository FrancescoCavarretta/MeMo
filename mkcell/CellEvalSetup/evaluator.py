"""
Copyright (c) 2016-2020, EPFL/Blue Brain Project

 This file is part of BluePyOpt <https://github.com/BlueBrain/BluePyOpt>

 This library is free software; you can redistribute it and/or modify it under
 the terms of the GNU Lesser General Public License version 3.0 as published
 by the Free Software Foundation.

 This library is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 details.

 You should have received a copy of the GNU Lesser General Public License
 along with this library; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
# pylint: disable=R0914, R0912
import gc
gc.disable()

import json

import bluepyopt.ephys as ephys

from bluepyopt.ephys import evaluators 

from . import template  # pylint: disable=W0403
from . import protocols  # pylint: disable=W0403


import logging
logger = logging.getLogger(__name__)
import os
import bluepyopt as bpopt
import efel

soma_loc = ephys.locations.NrnSeclistCompLocation(
    name='soma',
    seclist_name='somatic',
    sec_index=0,
    comp_x=0.5)


import numpy as np

import logging
from datetime import datetime
logger = logging.getLogger()
    

from bluepyopt.ephys import simulators


##class CustomCellEvaluator( evaluators.CellEvaluator ):
##    def __init__(
##            self,
##            cell_model=None,
##            param_names=None,
##            fitness_protocols=None,
##            fitness_calculator=None,
##            isolate_protocols=None,
##            sim=None,
##            use_params_for_seed=False,
##            timeout=None):
##        
##        evaluators.CellEvaluator.__init__(self, 
##                                          cell_model=cell_model, 
##                                          param_names=param_names,
##                                          fitness_protocols=fitness_protocols,
##                                          fitness_calculator=fitness_calculator,
##                                          isolate_protocols=isolate_protocols,
##                                          sim=sim, 
##                                          use_params_for_seed=use_params_for_seed,
##                                          timeout=timeout)
##
##
##    def run_protocol(self, protocol, param_values, isolate=None, cell_model=None, sim=None, timeout=None):
##        response = super().run_protocol(protocol, param_values, isolate=isolate, cell_model=cell_model, sim=sim, timeout=timeout)
##        try:
##            
##            _response = list(response.values())[0]
##            _response.threshold = self.__get_threshold__(_response,
##                                                        protocol.step_stimulus.step_delay,
##                                                        protocol.step_stimulus.step_delay + protocol.step_stimulus.step_duration)
##        except:
##            pass
##        return response
##
##    
##    def _cut_efel_trace(self, trace, tshift_init=1000, tshift_end=2000.0):
##        t = trace['T']
##        v = trace['V']
##        idx = np.logical_and(t >= (trace['stim_start'][0]-tshift_init), t < (trace['stim_end'][0]+tshift_end))
##        trace['T'] = t[idx]
##        trace['V'] = v[idx]    
##
##
##    def __get_threshold__(self, response, stim_start, stim_end, inc_v=2.5):
##        import copy
##        import numpy as np
##        import efel
##        
##        trace = copy.deepcopy( { 'T':response['time'], 'V':response['voltage'], 'stim_start':[stim_start], 'stim_end':[stim_end]} )
##
##        self._cut_efel_trace(trace)
##        
##        min_v = round(np.min(trace['V']))
##        max_v = round(np.max(trace['V']))    
##        
##        best_thresh = None
##        best_nspk   = None
##        for thresh in np.arange(min_v, max_v+inc_v, inc_v):
##            efel.setThreshold(thresh)
##            try:
##                nspk = efel.getFeatureValues([trace], ['AP_begin_voltage'])[0]['AP_begin_voltage'].shape[0]
##            except:
##                nspk = 0
##
##            if best_nspk is None or best_nspk <= nspk:
##                best_nspk = nspk
##                best_thresh = thresh
##        return best_thresh
    
    


def read_step_protocol(protocol_name,
                    protocol_definition,
                    recordings,
                    prefix=""):
    """Read step protocol from definition"""

    step_definition = protocol_definition['stimuli']['step']
    

    step_stimulus_amp = step_definition['amp']
    
    step_stimulus = ephys.stimuli.NrnSquarePulse(
        step_amplitude=(0 if type(step_stimulus_amp)==str else step_stimulus_amp),
        step_delay=step_definition['delay'],
        step_duration=step_definition['duration'],
        location=soma_loc,
        total_duration=step_definition['totduration'])

    if 'holding' in protocol_definition['stimuli']:
        holding_definition = protocol_definition['stimuli']['holding']
        try:
            holding_voltage  = holding_definition['volt']
                
            holding_stimulus = ephys.stimuli.NrnSquarePulse(
                step_delay=holding_definition['delay'],
                step_duration=holding_definition['duration'],
                location=soma_loc,
                total_duration=holding_definition['totduration'])
        except KeyError:
            holding_amp  = holding_definition['amp']
                
            holding_stimulus = ephys.stimuli.NrnSquarePulse(
                step_amplitude=holding_amp,
                step_delay=holding_definition['delay'],
                step_duration=holding_definition['duration'],
                location=soma_loc,
                total_duration=holding_definition['totduration'])
            
            holding_voltage  = None
    else:
        holding_stimulus = None
        holding_voltage  = None

    return protocols.StepProtocolCustom(
        name=protocol_name,
        step_stimulus=step_stimulus,
        step_stimulus_amp=step_stimulus_amp,
        holding_stimulus=holding_stimulus,
        holding_voltage=holding_voltage,
        recordings=recordings)

def read_ramp_protocol(
        protocol_name,
        protocol_definition,
        recordings):
    """Read step protocol from definition"""

    ramp_definition = protocol_definition['stimuli']['ramp']
    ramp_stimulus = ephys.stimuli.NrnRampPulse(
        ramp_amplitude_start = ramp_definition['ramp_amp_start'],
        ramp_amplitude_end = ramp_definition['ramp_amp_end'],
        ramp_delay=ramp_definition['delay'],
        ramp_duration=ramp_definition['duration'],
        location=soma_loc,
        total_duration=ramp_definition['totduration'])

    if 'holding' in protocol_definition['stimuli']:
        holding_definition = protocol_definition[
            'stimuli']['holding']
        holding_stimulus = ephys.stimuli.NrnSquarePulse(
            step_amplitude=holding_definition['amp'],
            step_delay=holding_definition['delay'],
            step_duration=holding_definition['duration'],
            location=soma_loc,
            total_duration=holding_definition['totduration'])
    else:
        holding_stimulus = None


    return protocols.RampProtocol(
        name=protocol_name,
        ramp_stimulus=ramp_stimulus,
        holding_stimulus=holding_stimulus,
        recordings=recordings)


def define_protocols(protocols_filename, stochkv_det=None,
                runopt=False, prefix="", apical_sec=None):
    """Define protocols"""
    
    with open(os.path.join(os.path.dirname(__file__), '..', protocols_filename)) as protocol_file:
        protocol_definitions = json.load(protocol_file)

    if "__comment" in protocol_definitions:
        del protocol_definitions["__comment"]

    protocols_dict = {}

    for protocol_name, protocol_definition in protocol_definitions.items():
            # By default include somatic recording
            somav_recording = ephys.recordings.CompRecording(
                name='%s.%s.soma.v' % (prefix, protocol_name),
                location=soma_loc,
                variable='v')

            recordings = [somav_recording]
      
            if 'type' in protocol_definition and \
                    protocol_definition['type'] == 'StepProtocol':
                protocols_dict[protocol_name] = read_step_protocol(
                    protocol_name, protocol_definition, recordings, stochkv_det)
            elif 'type' in protocol_definition and \
                    protocol_definition['type'] == 'RampProtocol':
                protocols_dict[protocol_name] = read_ramp_protocol(
                    protocol_name, protocol_definition, recordings)                    
            else:
                stimuli = []
                for stimulus_definition in protocol_definition['stimuli']:
                    stimuli.append(ephys.stimuli.NrnSquarePulse(
                        step_amplitude=stimulus_definition['amp'],
                        step_delay=stimulus_definition['delay'], 
                        step_duration=stimulus_definition['duration'],
                        location=soma_loc,
                        total_duration=stimulus_definition['totduration']))

                protocols_dict[protocol_name] = ephys.protocols.SweepProtocol(
                    name=protocol_name,
                    stimuli=stimuli,
                    recordings=recordings)

    return protocols_dict


from bluepyopt.ephys.efeatures import eFELFeature


class ScoreValue:
  def __init__(self):
    pass





class ScoreMeanStd(ScoreValue):
  def __init__(self, mean, std, max_score=250.0):
    super(ScoreMeanStd, self).__init__()
    
    self.mean = mean
    self.std  = std
    self.max_score = max_score



        
  def score(self, value):
    try:
        if self.std > 0:
            return abs(value-self.mean)/self.std
        elif abs(value - self.mean) == 0.0:
            return 0.0
    except:
        pass
    return self.max_score



class ScoreMedian(ScoreValue):
  def __init__(self, median, quartile_left, quartile_right, max_score=250.0):
    super(ScoreMedian, self).__init__()
    
    self.median = median
    self.quartile_left  = quartile_left
    self.quartile_right = quartile_right
    self.max_score = max_score

        
  def score(self, value):
    try:
      if value <= self.median:
        if self.quartile_left > 0:
            return abs(value-self.median)/self.quartile_left
      else:
        if self.quartile_right > 0:
            return abs(value-self.median)/self.quartile_right
    except:
      pass
    return self.max_score




    



class eFELFeatureExtra(eFELFeature):

    """eFEL feature extra"""

    SERIALIZED_FIELDS = ('name', 'efel_feature_name', 'recording_names',
                         'stim_start', 'stim_end', 'exp_mean',
                         'exp_std', 'threshold', 'comment')

    def __init__(
            self,
            name,
            efel_feature_name=None,
            recording_names=None,
            stim_start=None,
            stim_end=None,
            score_function=None,
            threshold=None,
            stimulus_current=None,
            comment='',
            interp_step=None,
            double_settings=None,
            int_settings=None,
            string_settings=None,
            force_max_score=False,
            max_score = 250,
            prefix=''):

        """Constructor

        Args:
            name (str): name of the eFELFeature object
            efel_feature_name (str): name of the eFeature in the eFEL library
                (ex: 'AP1_peak')
            recording_names (dict): eFEL features can accept several recordings
                as input
            stim_start (float): stimulation start time (ms)
            stim_end (float): stimulation end time (ms)
            exp_mean (float): experimental mean of this eFeature
            exp_std(float): experimental standard deviation of this eFeature
            threshold(float): spike detection threshold (mV)
            comment (str): comment
        """

        super(eFELFeatureExtra, self).__init__(
            name,
            efel_feature_name=efel_feature_name,
            recording_names=recording_names,
            stim_start=stim_start,
            stim_end=stim_end,
            exp_mean=None,
            exp_std=None,
            threshold=threshold,
            stimulus_current=stimulus_current,
            comment=comment,
            interp_step=interp_step,
            double_settings=double_settings,
            int_settings=int_settings,
            force_max_score=force_max_score,
            max_score=max_score)

        extra_features = ['spikerate_tau_jj_skip', 'spikerate_drop_skip',
                        'spikerate_tau_log_skip', 'spikerate_tau_fit_skip']

        self.prefix = prefix


        self._custom_efeature = {
            'decay_time_constant_after_stim2':self._decay_time_constant_after_stim2,
            'input_resistance':self._input_resistance, 
            'clustering_index':self._clustering_index,
            'sag_deflection':self._sag_deflection,
            'sag_ratio3':self._sag_ratio3,
            'AP1_peak_after_stim':self._AP1_peak_after_stim,
            'AP2_peak_after_stim':self._AP2_peak_after_stim,
            'time_to_first_spike_after_stim':self._time_to_first_spike_after_stim,
            'inv_first_ISI_after_stim':self._inv_first_ISI_after_stim,
            'inv_second_ISI_after_stim':self._inv_second_ISI_after_stim,
            'inv_last_ISI_after_stim':self._inv_last_ISI_after_stim,
            'AP_count':self._AP_count,         
            'AP_count_after_stim':self._AP_count_after_stim,
            'AP_count_before_stim':self._AP_count_before_stim,
            'AP1_amp_after_stim':self._AP1_amp_after_stim,
            'AP2_amp_after_stim':self._AP2_amp_after_stim,
            'AHP_depth_after_stim':self._AHP_depth_after_stim,
            'AP_amplitude_min_max':self._AP_amplitude_min_max,
        }

        
        self._n_pt_interp = 100


        self.score_function = score_function

        

    def _cut_efel_trace(self, trace, tshift_init=1000, tshift_end=2000.0):
        t = trace['T']
        v = trace['V']
        idx = np.logical_and(t >= (trace['stim_start'][0]-tshift_init), t < (trace['stim_end'][0]+tshift_end))
        trace['T'] = t[idx]
        trace['V'] = v[idx]


    def getMeanFeatureValues(self, trace, name):
        import copy
        trace = copy.deepcopy(trace)
        
        """ eFEL efeatures """
        self._setup_efel()
        
        # set the threshold
        if 'threshold' in trace:
            efel.setThreshold(trace['threshold'])
            del trace['threshold']
            

        if name in self._custom_efeature:
          """ custom efeatures """
          value = self._custom_efeature[name](trace)    
        else:
        
          """Cut the trace to stim_start and stim_end as efel doesn't """
          self._cut_efel_trace(trace) 
          
          value = efel.getMeanFeatureValues(
            [trace],
            [name],
            raise_warnings=False)[0][self.efel_feature_name]
          
        efel.reset()
        return value
    
    
    def _after_stim(self, trace, efeature_name):     
      import copy
      trace = copy.deepcopy(trace)
      
      trace['stim_start'][0] = (trace['stim_start'][0] + trace['stim_end'][0])/2.0
      trace['stim_end'][0] = trace['T'][-1]
      
      self._cut_efel_trace(trace, tshift_init=0, tshift_end=0)
    
      return  efel.getFeatureValues([ trace ], [ efeature_name ])[0][efeature_name][0]

     
    def _AP1_peak_after_stim(self, trace): return self._after_stim(trace, 'AP1_peak')
    def _AP2_peak_after_stim(self, trace): return self._after_stim(trace, 'AP2_peak')

    def _AP1_amp_after_stim(self, trace): return self._after_stim(trace, 'AP1_amp')
    def _AP2_amp_after_stim(self, trace): return self._after_stim(trace, 'AP2_amp')
    def _AHP_depth_after_stim(self, trace): return self._after_stim(trace, 'AHP_depth')

    def _inv_first_ISI_after_stim(self, trace): return self._after_stim(trace, 'inv_first_ISI')
    def _inv_second_ISI_after_stim(self, trace): return self._after_stim(trace, 'inv_second_ISI')
    def _inv_last_ISI_after_stim(self, trace): return self._after_stim(trace, 'inv_last_ISI')
    def _time_to_first_spike_after_stim(self, trace): return self._after_stim(trace, 'time_to_first_spike')


    def _AP_amplitude_min_max(self, trace):
      import copy
      trace = copy.deepcopy(trace)
      self._cut_efel_trace(trace)
                                   
      ef = efel.getFeatureValues([trace], ['AP_amplitude'])[0]
      try:
        return ef['AP_amplitude'].max() - ef['AP_amplitude'].min()
      except:
        pass
      return 0

    
    
    def _AP_count(self, trace):
      import copy
      trace = copy.deepcopy(trace)
      self._cut_efel_trace(trace)  
      
      try:
        return efel.getFeatureValues([trace], ['AP_begin_voltage'])[0]['AP_begin_voltage'].shape[0]
      except:
        pass
      return 0
    
    
    def _AP_count_after_stim(self,  trace):
      import copy
      trace = copy.deepcopy(trace)
      
      trace['stim_start'][0] = (trace['stim_start'][0] + trace['stim_end'][0])/2.0
      trace['stim_end'][0] = trace['T'][-1]
      
      return self._AP_count(trace)   

  
    def _AP_count_before_stim(self, trace):
      pad = 500.0
      import copy
      trace = copy.deepcopy(trace)
      
      trace['stim_end'][0] = trace['stim_start'][0]
      trace['stim_start'][0] = pad
      
      return self._AP_count(trace)   
        
  
    """ membrane time constant as in Bichler's paper """
    def _decay_time_constant_after_stim2(self, trace):
        import copy
        import exp2_fit
        trace = copy.deepcopy(trace)
        trace['stim_end'] = [trace['T'][-1]]
        self._cut_efel_trace(trace, tshift_init=0, tshift_end=0)
        return exp2_fit.membrane_time_constant(trace['T'],  trace['V'])  


    """ AP clustering index """
    def _clustering_index(self, trace):
        import copy
        trace = copy.deepcopy(trace)

        # e-features
        ef_values = efel.getFeatureValues([trace], ['all_ISI_values', 'time_to_first_spike'])[0]

        # isis
        values = ef_values['all_ISI_values']

        # try to correct a Nan is occurring
        try:
            values[np.isnan(values)] = 0.
        except:
            return None
        
        # reconstructed spike time
        tspk = ef_values['time_to_first_spike'] + np.concatenate((
            np.array([0.]),
            np.cumsum(values)
        ))
            
        tlimit = (trace['stim_end'][0] - trace['stim_start'][0]) * 0.5

        return (tspk < tlimit).sum() / tspk.shape[0]
    


    """ Input Resistance as in Bichler's paper """
    def _input_resistance(self, trace):
        pad = 500
        
        import copy
        trace = copy.deepcopy(trace)
        
        # do not revert the next two lines!
        baseline = np.mean(trace['V'][ np.logical_and( trace['T'] < trace['stim_start'][0], trace['T'] >= trace['stim_start'][0] - pad ) ])
        self._cut_efel_trace(trace, tshift_init=0, tshift_end=0)
        
        Vpeak = trace['V'][-1] - baseline
        retval = (Vpeak * 1e-3) / (-10.0 * 1e-12) * 1e-6
        
        return retval   

    """ Sag deflection as in Bichler's paper """
    def _sag_deflection(self, trace):
        pad = 500
        
        import copy
        trace = copy.deepcopy(trace)
        
        # do not revert the next two lines!
        baseline = np.mean(trace['V'][ np.logical_and( trace['T'] < trace['stim_start'][0], trace['T'] >= trace['stim_start'][0] - pad ) ])
        self._cut_efel_trace(trace, tshift_init=0, tshift_end=0)
        
        Vpeak = np.min(trace['V'][trace['T'] < trace['stim_start'][0] + pad]) - baseline
        retval = -Vpeak
        
        return retval


    def _sag_ratio3(self, trace):
        pad = 500
        
        import copy
        trace = copy.deepcopy(trace)
        
        # do not revert the next two lines!
        baseline = np.mean(trace['V'][ np.logical_and( trace['T'] < trace['stim_start'][0], trace['T'] >= trace['stim_start'][0] - pad ) ])
        self._cut_efel_trace(trace, tshift_init=0, tshift_end=0)
        
        Vss   = np.mean(trace['V'][trace['T'] > trace['stim_start'][0] + pad]) - baseline
        Vpeak = np.min(trace['V'][trace['T'] < trace['stim_start'][0] + pad]) - baseline
        retval = 100.0 * (1 - Vss / Vpeak)
        
        return retval
    
            

        
    
    def get_bpo_score(self, responses):
        """Return internal score which is directly passed as a response"""

        feature_value = self.get_bpo_feature(responses)
        if feature_value == None:
            score = 250.
        else:
            score = self.score_function.score(feature_value)
        return score


    def _construct_efel_trace(self, responses):
        """Construct trace that can be passed to eFEL"""
        trace = super(eFELFeatureExtra, self)._construct_efel_trace(responses)
        trace['T'] = trace['T'].to_numpy()
        trace['V'] = trace['V'].to_numpy()
        try:
            trace['threshold'] = responses[self.recording_names['']].threshold
        except AttributeError:
            pass
        return trace
    
    

    def calculate_feature(self, responses, raise_warnings=False):
        """Calculate feature value"""

        if self.efel_feature_name.startswith('bpo_'): # check if internal feature
            feature_value = self.get_bpo_feature(responses)
        else:
            try:
                efel_trace = self._construct_efel_trace(responses)
            except:
                feature_value = None
                

            if efel_trace is None:
                feature_value = None
            else:
                try:
                    feature_value = self.getMeanFeatureValues(
                      efel_trace,
                      self.efel_feature_name
                    )
                except:
                    feature_value = None

        logger.debug(
            'Calculated value for %s: %s',
            self.name,
            str(feature_value))

        return feature_value

   
        

    def getDistance(self, efel_trace, efel_feature_name):
        try:
            feature_value = self.getMeanFeatureValues(
                efel_trace,
                self.efel_feature_name
            )

            print (efel_feature_name, feature_value)
        except:
            feature_value = None

        if feature_value == None: 
            score = 250.
        else:   
            try:
                score = self.score_function.score(feature_value)
            except ZeroDivisionError:
                score = 250.0
        return score


        
    def calculate_score(self, responses, trace_check=False):
        """Calculate the score"""
        try:
            if self.efel_feature_name.startswith('bpo_'): # check if internal feature
                score = self.get_bpo_score(responses)

            else:
                efel_trace = self._construct_efel_trace(responses)

                if efel_trace is None:
                    score = 250.0
                else:

                    
                    score = self.getDistance(
                      efel_trace,
                      self.efel_feature_name)

            logger.debug('Calculated score for %s: %f', self.name, score)

            return score
        except:
            return 250.0


from bluepyopt.ephys.objectives import SingletonObjective, EFeatureObjective, MaxObjective

class SingletonWeightObjective(EFeatureObjective):

    """Single EPhys feature"""

    def __init__(self, name, feature, weight):
        """Constructor

        Args:
            name (str): name of this object
            features (EFeature): single eFeature inside this objective
        """

        super(SingletonWeightObjective, self).__init__(name, [feature])
        self.weight = weight

    def calculate_score(self, responses):
        """Objective score"""

        return self.calculate_feature_scores(responses)[0] * self.weight
    
    def calculate_value(self, responses):
        """Objective score"""

        return self.calculate_feature_values(responses)[0] 
    
    def __str__(self):
        """String representation"""

        return '( %s ), weight:%f' % (self.features[0], self.weight)


def define_fitness_calculator(main_protocol, features_filename, etype, prefix=""):
    """Define fitness calculator"""

    with open(os.path.join(os.path.dirname(__file__), '..', features_filename)) as protocol_file:
        feature_definitions = json.load(protocol_file)

    if "__comment" in feature_definitions:
        del feature_definitions["__comment"]

    objectives = []
    efeatures = {}
    features = []

    for protocol_name, locations in feature_definitions.items():
        for recording_name, feature_configs in locations.items():
            for feature_config in feature_configs:
                efel_feature_name = feature_config["feature"]


                if 'val' in feature_config:
                    mean, std = feature_config['val']
                    scoreobj = ScoreMeanStd(mean, std)
                elif 'median' in feature_config:
                    median, lq, rq = feature_config['median']
                    scoreobj = ScoreMedian(median, lq, rq)
                    

                if hasattr(main_protocol, 'subprotocols'):
                    protocol = main_protocol.subprotocols()[protocol_name]
                else:
                    protocol = main_protocol[protocol_name]
                    
                feature_name = '%s.%s.%s.%s' % (
                    prefix, protocol_name, recording_name, efel_feature_name)
                recording_names = \
                    {'': '%s.%s.%s' % (prefix, protocol_name, recording_name)}

                if 'weight' in feature_config:
                    weight = feature_config['weight']
                else:
                    weight = 1

                if 'strict_stim' in feature_config:
                    strict_stim = feature_config['strict_stim']
                else:
                    strict_stim = True

                if hasattr(protocol, 'step_delay'):

                    stim_start = protocol.step_delay

                    if 'threshold' in feature_config:
                        threshold = feature_config['threshold']
                    else:
                        threshold = -20.0


                    

                    #if protocol_name.startswith("Rebound"):
                    #    stim_end = protocol.step_delay + protocol.step_duration + 500
                    #else:
                    stim_end = protocol.step_delay + protocol.step_duration
                        
                    try:
                        stimulus_current=protocol.step_stimulus.step_amplitude
                    except AttributeError:
                        print("Check stim_amp for RampProtocol")
                        stimulus_current = None
                else:
                    stim_start = None
                    stim_end = None
                    stimulus_current = None
                    threshold = -20.0

                feature = eFELFeatureExtra(
                    feature_name,
                    efel_feature_name=efel_feature_name,
                    recording_names=recording_names,
                    stim_start=stim_start,
                    stim_end=stim_end,
                    score_function=scoreobj,
                    stimulus_current=stimulus_current,
                    threshold=threshold,
                    prefix=prefix,
                    int_settings={'strict_stiminterval': strict_stim},
                    force_max_score = True,
                    max_score = 250)
                if feature_name not in efeatures:
                    efeatures[feature_name] = []
                efeatures[feature_name].append(feature)
                features.append(feature)
                objective = SingletonWeightObjective(
                    feature_name,
                    feature, weight)
                objectives.append(objective)

    #objectives.append(MaxObjective('global_maximum', features))
    fitcalc = ephys.objectivescalculators.ObjectivesCalculator(objectives)

    return fitcalc, efeatures

def create(etype, runopt=False, altmorph=None):
    """Setup"""

    with open(os.path.join(os.path.dirname(__file__), '..', 'config/recipes.json')) as f:
        recipe = json.load(f)

    prot_path = recipe[etype]['protocol']

    cell = template.create(recipe, etype, altmorph)

    protocols_dict = define_protocols(prot_path, runopt)

    fitness_calculator, efeatures = define_fitness_calculator(
        protocols_dict,
        recipe[etype]['features'],
        etype)

    fitness_protocols=protocols_dict

    param_names = [param.name
                   for param in cell.params.values()
                   if not param.frozen]

    nrn_sim = ephys.simulators.NrnSimulator(cvode_active = True)
    #cell_eval = CustomCellEvaluator(
    cell_eval = ephys.evaluators.CellEvaluator(
        cell_model=cell,
        param_names=param_names,
        fitness_protocols=fitness_protocols,
        fitness_calculator=fitness_calculator,
        sim=nrn_sim,
        use_params_for_seed=True)

    return cell_eval










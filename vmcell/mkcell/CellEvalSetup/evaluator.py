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

import json

import bluepyopt.ephys as ephys

from . import template  # pylint: disable=W0403
from . import protocols  # pylint: disable=W0403


import logging
logger = logging.getLogger(__name__)
import os
import bluepyopt as bpopt

soma_loc = ephys.locations.NrnSeclistCompLocation(
    name='soma',
    seclist_name='somatic',
    sec_index=0,
    comp_x=0.5)

import eFELExt
import numpy as np
import efel

from bluepyopt.ephys.efeatures import eFELFeature


def read_step_protocol(protocol_name,
                    protocol_definition,
                    recordings,
                    prefix=""):
    """Read step protocol from definition"""

    step_definition = protocol_definition['stimuli']['step']
    step_stimulus = ephys.stimuli.NrnSquarePulse(
        step_amplitude=step_definition['amp'],
        step_delay=step_definition['delay'],
        step_duration=step_definition['duration'],
        location=soma_loc,
        total_duration=step_definition['totduration'])

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

    return protocols.StepProtocolCustom(
        name=protocol_name,
        step_stimulus=step_stimulus,
        holding_stimulus=holding_stimulus,
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
    
    with open(os.path.join(os.path.dirname(__file__), protocols_filename)) as protocol_file:
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
            exp_mean=None,
            exp_std=None,
            threshold=None,
            stimulus_current=None,
            comment='',
            interp_step=None,
            double_settings=None,
            int_settings=None,
            force_max_score=False,
            max_score = 250,
            prefix='',
            t_trace_init=None,
            t_trace_end=None,
            dt=0.025):

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
            t_trace_init(float):padding left at the beginning of the simulation
        """

        super(eFELFeatureExtra, self).__init__(
            name,
            efel_feature_name=efel_feature_name,
            recording_names=recording_names,
            stim_start=stim_start,
            stim_end=stim_end,
            exp_mean=exp_mean,
            exp_std=exp_std,
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
        self.t_trace_init = t_trace_init
        self.t_trace_end = t_trace_end
        self.dt = dt

    def get_bpo_score(self, responses):
        """Return internal score which is directly passed as a response"""

        feature_value = self.get_bpo_feature(responses)
        if feature_value == None:
            score = 250.
        else:
            score = abs(feature_value - self.exp_mean) / self.exp_std
        return score


    def _preprocess_efel_trace(self, trace):
        """ remove the initial part of the trace """
        if hasattr(trace['T'], 'to_numpy'):
            trace['T'] = trace['T'].to_numpy()
    
        if hasattr(trace['V'], 'to_numpy'):
            trace['V'] = trace['V'].to_numpy()

        # cut the trace
        if self.t_trace_init:
            idx = trace['T'] >= self.t_trace_init
            trace['T'] = trace['T'][idx]
            trace['V'] = trace['V'][idx]
            
        if self.t_trace_end:
            idx = trace['T'] <= self.t_trace_end
            trace['T'] = trace['T'][idx]
            trace['V'] = trace['V'][idx]
            
        # interpolate the trace
        # new t-axis
        t = np.arange(trace['T'][0], trace['T'][-1] + self.dt, self.dt)
        
        # interpolation
        v = np.interp(t, trace['T'], trace['V'])

        # copy to the trace map
        trace['T'] = t
        trace['V'] = v
        
        
    def calculate_feature(self, responses, raise_warnings=False):
        """Calculate feature value"""

        if self.efel_feature_name.startswith('bpo_'): # check if internal feature
            feature_value = self.get_bpo_feature(responses)
        else:            
            efel_trace = self._construct_efel_trace(responses)
            
            if efel_trace is None:
                feature_value = None
            else:
                try:
                    self._preprocess_efel_trace(efel_trace)
                    
                    self._setup_efel()
                    
                    values = eFELExt.getFeatureValues(
                        efel_trace,
                        [self.efel_feature_name])
                    
                    feature_value = values[self.efel_feature_name]
                except:
                    feature_value = None
                finally:
                    efel.reset()

        logger.debug(
            'Calculated value for %s: %s',
            self.name,
            str(feature_value))

        return feature_value


    def calculate_score(self, responses, trace_check=False):
        """Calculate the score"""
        if self.efel_feature_name.startswith('bpo_'): # check if internal feature
            score = self.get_bpo_score(responses)
        elif self.exp_mean is None:
            score = 0
            
        else:
            efel_trace = self._construct_efel_trace(responses)

            if efel_trace is None:
                score = self.max_score
            else:
                try:
                    self._preprocess_efel_trace(efel_trace)
                    
                    self._setup_efel()

                    feature_value = eFELExt.getFeatureValues(efel_trace, [self.efel_feature_name])[self.efel_feature_name]
                    
                    score = abs(feature_value - self.exp_mean) / self.exp_std
                    
                    if self.force_max_score:
                        score = min(score, self.max_score)

                    if np.isnan(score):
                        score = self.max_score
                except:
                    score = self.max_score
                finally:
                    efel.reset()

        logger.debug('Calculated score for %s: %f', self.name, score)

        return score


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

    def __str__(self):
        """String representation"""

        return '( %s ), weight:%f' % (self.features[0], self.weight)


def define_fitness_calculator(main_protocol, features_filename, prefix=""):
    """Define fitness calculator"""

    with open(os.path.join(os.path.dirname(__file__), features_filename)) as protocol_file:
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
                meanstd = feature_config["val"]

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
                    strict_stim = False

                if hasattr(protocol, 'step_delay'):

                    stim_start = protocol.step_delay
                    
                    if 't_trace_init' in feature_config:
                        t_trace_init = feature_config['t_trace_init']
                    else:
                        t_trace_init = None
                        
                    if 't_trace_end' in feature_config:
                        t_trace_end = feature_config['t_trace_end']
                    else:
                        t_trace_end = None
                        
                    if 'threshold' in feature_config:
                        threshold = feature_config['threshold']
                    else:
                        threshold = -30
                        
                    if 'bAP' in protocol_name:
                        # bAP response can be after stimulus
                        stim_end = protocol.total_duration
                    else:
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
                    threshold = None

                feature = eFELFeatureExtra(
                    feature_name,
                    efel_feature_name=efel_feature_name,
                    recording_names=recording_names,
                    stim_start=stim_start,
                    stim_end=stim_end,
                    exp_mean=meanstd[0],
                    exp_std=meanstd[1],
                    stimulus_current=stimulus_current,
                    threshold=threshold,
                    prefix=prefix,
                    int_settings={'strict_stiminterval': strict_stim},
                    force_max_score = True,
                    max_score = 250,
                    t_trace_init=t_trace_init,
                    t_trace_end=t_trace_end)
                efeatures[feature_name] = feature
                features.append(feature)
                objective = SingletonWeightObjective(
                    feature_name,
                    feature, weight)
                objectives.append(objective)

    #objectives.append(MaxObjective('global_maximum', features))
    fitcalc = ephys.objectivescalculators.ObjectivesCalculator(objectives)

    return fitcalc, efeatures

def create(etype, coreneuron_active=False, use_process=False, runopt=False, altmorph=None):
    """Setup"""

    with open(os.path.join(os.path.dirname(__file__), 'config/recipes.json')) as f:
        recipe = json.load(f)

    prot_path = recipe[etype]['protocol']

    cell = template.create(recipe, etype, altmorph)

    protocols_dict = define_protocols(prot_path, runopt)

    fitness_calculator, efeatures = define_fitness_calculator(
        protocols_dict,
        recipe[etype]['features'],)

    fitness_protocols=protocols_dict

    param_names = [param.name
                   for param in cell.params.values()
                   if not param.frozen]


    try:
        nrn_sim = ephys.simulators.NrnSimulator(cvode_active=not coreneuron_active, coreneuron_active=coreneuron_active)

        cell_eval = ephys.evaluators.CellEvaluator(
            cell_model=cell,
            param_names=param_names,
            fitness_protocols=fitness_protocols,
            fitness_calculator=fitness_calculator,
            sim=nrn_sim,
            use_params_for_seed=True,
            use_process=use_process,
            py_protocol_filename='protocol_process.py')
    except:
        nrn_sim = ephys.simulators.NrnSimulator(cvode_active=True)

        cell_eval = ephys.evaluators.CellEvaluator(
            cell_model=cell,
            param_names=param_names,
            fitness_protocols=fitness_protocols,
            fitness_calculator=fitness_calculator,
            sim=nrn_sim,
            use_params_for_seed=True)
        
    return cell_eval


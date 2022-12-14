#!/bin/sh
#SBATCH --job-name=LabGCCRun #Job name
#SBATCH --partition=day-long # partition (queue)
#SBATCH --mem=30gb # set memory
#SBATCH -o slurm.%N.%j.out # STDOUT
#SBATCH -e slurm.%N.%j.err # STDERR

#python3 thalamicsim_launch.py --filenamein test.npy --filenameout test_0
#python3 thalamicsim_launch.py --filenamein test_firing_rate_0.npy --filenameout test_firing_rate_mod_only --dt 1
#python3 thalamicsim_launch.py --filenamein test_firing_rate_1.npy --filenameout test_firing_rate_drv_only --dt 1
#python3 thalamicsim_launch.py --filenamein test_firing_rate_2.npy --filenameout test_firing_rate --dt 1
#python3 thalamicsim_launch.py --filenamein test_firing_rate_3.npy --filenameout test_firing_rate_6ohda --dt 1
#python3 thalamicsim_launch.py --filenamein test_firing_rate_4.npy --filenameout test_firing_rate_6ohda_2 --dt 1
#python3 thalamicsim_launch.py --filenamein test_firing_rate_4.npy --filenameout test_firing_rate_4 --dt 1
#python3 thalamicsim_launch.py --filenamein test_firing_rate_5.npy --filenameout test_firing_rate_5 --dt 1
#python3 thalamicsim_launch.py --filenamein test_firing_rate_6.npy --filenameout test_firing_rate_6 --dt 1
#python3 thalamicsim_launch.py --filenamein test_firing_rate_7.npy --filenameout test_firing_rate_7 --dt 1
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_0.txt --no-run --index 0 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_1.txt --no-run --index 1 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_2.txt --no-run --index 2 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_3.txt --no-run --index 3 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_4.txt --no-run --index 4 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_5.txt --no-run --index 5 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_6.txt --no-run --index 6 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_7.txt --no-run --index 7 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_8.txt --no-run --index 8 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_9.txt --no-run --index 9 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_0.txt --no-run --index 10 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_1.txt --no-run --index 11 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_2.txt --no-run --index 12 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_3.txt --no-run --index 13 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_4.txt --no-run --index 14 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_5.txt --no-run --index 15 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_6.txt --no-run --index 16 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_7.txt --no-run --index 17 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_8.txt --no-run --index 18 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_9.txt --no-run --index 19 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_0.txt --no-run --index 20 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_1.txt --no-run --index 21 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_2.txt --no-run --index 22 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_3.txt --no-run --index 23 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_4.txt --no-run --index 24 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_5.txt --no-run --index 25 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_6.txt --no-run --index 26 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_7.txt --no-run --index 27 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_8.txt --no-run --index 28 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_async_on_9.txt --no-run --index 29 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_0.txt --no-run --index 30 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_1.txt --no-run --index 31 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_2.txt --no-run --index 32 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_3.txt --no-run --index 33 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_4.txt --no-run --index 34 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_5.txt --no-run --index 35 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_6.txt --no-run --index 36 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_7.txt --no-run --index 37 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_8.txt --no-run --index 38 &
#./x86_64/special thalamicsim.py --config_file test_bursting_v2_spiketrain.npy --save-spike-train spike_sync_on_9.txt --no-run --index 39 &

#python3 thalamicsim_launch.py --filenamein test_bursting_off.npy --filenameout test_bursting_off 
#python3 thalamicsim_launch.py --filenamein test_bursting_on.npy --filenameout test_bursting_on
#python3 thalamicsim_launch.py --filenamein test_bursting_off_2.npy --filenameout test_bursting_off_2 
#python3 thalamicsim_launch.py --filenamein test_bursting_on_2.npy --filenameout test_bursting_on_2
python3 thalamicsim_launch.py --filenamein test_bursting_off_3.npy --filenameout test_bursting_off_3 
python3 thalamicsim_launch.py --filenamein test_bursting_on_3.npy --filenameout test_bursting_on_3
python3 thalamicsim_launch.py --filenamein test_bursting_off_4.npy --filenameout test_bursting_off_4 
python3 thalamicsim_launch.py --filenamein test_bursting_on_4.npy --filenameout test_bursting_on_4
python3 thalamicsim_launch.py --filenamein test_bursting_off_5.npy --filenameout test_bursting_off_5 
python3 thalamicsim_launch.py --filenamein test_bursting_on_5.npy --filenameout test_bursting_on_5

#python3 thalamicsim_launch.py --filenamein test_firing_rate_9.npy --filenameout test_firing_rate_9 --dt 1
#python3 thalamicsim_launch.py --filenamein test_firing_rate_8.npy --filenameout test_firing_rate_8 --dt 1
#python3 thalamicsim_launch.py --filenamein test_bursting_v2_2_off.npy --filenameout test_bursting_v2_2_off
#python3 thalamicsim_launch.py --filenamein test_bursting_v2_2_on.npy --filenameout test_bursting_v2_2_on
#python3 thalamicsim_launch.py --filenamein test_modulation_0.npy --filenameout test_modulation_0
#python3 thalamicsim_launch.py --filenamein test_modulation_1.npy --filenameout test_modulation_1
#python3 thalamicsim_launch.py --filenamein test_bursting_v2_1_off.npy --filenameout test_bursting_v2_1_off
#python3 thalamicsim_launch.py --filenamein test_bursting_v2_1_on.npy --filenameout test_bursting_v2_1_on
#python3 thalamicsim_launch.py --filenamein test_bursting_v2_3_off.npy --filenameout test_bursting_v2_3_off
#python3 thalamicsim_launch.py --filenamein test_bursting_v2_3_on.npy --filenameout test_bursting_v2_3_on
#python3 thalamicsim_launch.py --filenamein test_bursting_v2_spiketrain_short_async.npy --filenameout test_bursting_short_async --all_section_recording

#python3 thalamicsim_launch.py --filenamein test_syn_properties.npy --filenameout test_sens_1
#python3 thalamicsim_launch.py --filenamein test_syn_properties_2.npy --filenameout test_sens_2
#python3 thalamicsim_launch.py --filenamein test_syn_properties_low_bg_2.npy --filenameout test_syn_2_lbg
#python3 thalamicsim_launch.py --filenamein test_firing_burst.npy --filenameout test_firing_burst
#python3 thalamicsim_launch.py --filenamein test_firing_2nd.npy --filenameout test_firing_2nd
#python3 thalamicsim_launch.py --filenamein test_firing_n2.npy --filenameout test_firing_n2
#python3 thalamicsim_launch.py --filenamein test_firing_2nd_part.npy --filenameout test_firing_2nd_part
#python3 thalamicsim_launch.py --filenamein test_firing_3.npy --filenameout test_firing_3
#python3 thalamicsim_launch.py --filenamein test_firing_burst.npy --filenameout test_firing_burst
#python3 thalamicsim_launch.py --filenamein test_firing_burst_2nd_part.npy --filenameout test_firing_burst_2nd_part
#python3 thalamicsim_launch.py --filenamein test_gsyn_1_2nd_part.npy --filenameout test_syn_init_1_2nd_part
#python3 thalamicsim_launch.py --filenamein test_gsyn_1_3nd_part.npy --filenameout test_syn_init_1_3nd_part
#python3 thalamicsim_launch.py --filenamein test_firing_burst_n2.npy --filenameout test_firing_burst_n2
#python3 thalamicsim_launch.py --filenamein test_firing_burst_n3.npy --filenameout test_firing_burst_n3
#python3 thalamicsim_launch.py --filenamein test_firing_burst_n5.npy --filenameout test_firing_burst_n5
#python3 thalamicsim_launch.py --filenamein test_firing_burst_n5_1.npy --filenameout test_firing_burst_n5_1
#python3 thalamicsim_launch.py --filenamein test_firing_burst_n5_2.npy --filenameout test_firing_burst_n5_2
#python3 thalamicsim_launch.py --filenamein test_firing_burst_n5_3.npy --filenameout test_firing_burst_n5_3
#python3 thalamicsim_launch.py --filenamein test_firing_burst_n5_4.npy --filenameout test_firing_burst_n5_4
#python3 thalamicsim_launch.py --filenamein test_firing_burst_hist_synchrony.npy --filenameout test_firing_burst_hist_synchrony
#python3 thalamicsim_launch.py --filenamein test_gsyn_1_4nd_part.npy --filenameout test_syn_init_1_4nd_part
#python3 thalamicsim_launch.py --filenamein test_firing_burst_hist_synchrony_2.npy --filenameout test_firing_burst_hist_synchrony_2
#python3 thalamicsim_launch.py --filenamein test_firing_burst_hist_synchrony_3.npy --filenameout test_firing_burst_hist_synchrony_3
#python3 thalamicsim_launch.py --filenamein test_firing_4th.npy --filenameout test_firing_4th
#python3 thalamicsim_launch.py --filenamein test_firing_burst_hist_synchrony_4.npy --filenameout test_firing_burst_hist_synchrony_4

#python3 thalamicsim_launch.py --filenamein test_syn.npy --filenameout test_syn
#python3 thalamicsim_launch.py --filenamein test_syn_spontaneous_1st.npy --filenameout test_syn_spontaneous_1st
#python3 thalamicsim_launch.py --filenamein test_syn_spontaneous_3rd.npy --filenameout test_syn_spontaneous_3rd
#python3 thalamicsim_launch.py --filenamein test_syn_spontaneous_4th.npy --filenameout test_syn_spontaneous_4th
#python3 thalamicsim_launch.py --filenamein test_syn_spontaneous_2nd.npy --filenameout test_syn_spontaneous_2nd --no-sim
#python3 thalamicsim_launch.py --filenamein test_sensitivity_syn_2.npy --filenameout test_sensitivity_syn_2
#python3 thalamicsim_launch.py --filenamein test_sensitivity_presyn_2.npy --filenameout test_sensitivity_presyn_2
#python3 thalamicsim_launch.py --filenamein test_sensitivity_syn_1.npy --filenameout test_sensitivity_syn_1
#python3 thalamicsim_launch.py --filenamein test_sensitivity_presyn_1.npy --filenameout test_sensitivity_presyn_1
#python3 thalamicsim_launch.py --filenamein test_sensitivity_syn_1_bak.npy --filenameout test_sensitivity_syn_1_bak

#python3 thalamicsim_launch.py --filenamein test_burst_on_1.npy --filenameout test_burst_on_1 --all_current_recording
#python3 thalamicsim_launch.py --filenamein test_burst_on_2.npy --filenameout test_burst_on_2 --all_current_recording
#python3 thalamicsim_launch.py --filenamein test_burst_off_1.npy --filenameout test_burst_off_1 --all_current_recording
#python3 thalamicsim_launch.py --filenamein test_burst_off_2.npy --filenameout test_burst_off_2 --all_current_recording
#python3 thalamicsim_launch.py --filenamein test_sensitivity_syn_5.npy --filenameout test_sensitivity_syn_5
#python3 thalamicsim_launch.py --filenamein test_sensitivity_presyn_5.npy --filenameout test_sensitivity_presyn_5
#python3 thalamicsim_launch.py --filenamein test_sensitivity_syn_6.npy --filenameout test_sensitivity_syn_6
#python3 thalamicsim_launch.py --filenamein test_sensitivity_presyn_6.npy --filenameout test_sensitivity_presyn_6
#python3 thalamicsim_launch.py --filenamein test_burst_on_1-short.npy --filenameout test_burst_on_1-short --all_current_recording --all_section_recording
#python3 thalamicsim_launch.py --filenamein test_burst_on_2-short.npy --filenameout test_burst_on_2-short --all_current_recording --all_section_recording


#python3 thalamicsim_launch.py --filenamein test_burst_on_1.npy --filenameout test_burst_on_1
#python3 thalamicsim_launch.py --filenamein test_burst_on_2.npy --filenameout test_burst_on_2
#python3 thalamicsim_launch.py --filenamein test_burst_off_1.npy --filenameout test_burst_off_1
#python3 thalamicsim_launch.py --filenamein test_burst_off_2.npy --filenameout test_burst_off_2
#python3 thalamicsim_launch.py --filenamein test_burst_on_5.npy --filenameout test_burst_on_5
#python3 thalamicsim_launch.py --filenamein test_burst_off_4.npy --filenameout test_burst_off_4
#python3 thalamicsim_launch.py --filenamein test_burst_on_4.npy --filenameout test_burst_on_4

#python3 thalamicsim_launch.py --filenamein test_burst_on_short_3.npy --filenameout test_burst_on_short_3 --all_current_recording --all_section_recording
#python3 thalamicsim_launch.py --filenamein test_burst_off_short_3.npy --filenameout test_burst_off_short_3 --all_current_recording --all_section_recording
#python3 thalamicsim_launch.py --filenamein test_burst_off_4-short.npy --filenameout test_burst_off_4-short --all_current_recording --all_section_recording


#python3 thalamicsim_launch.py --filenamein test_burst_on_7.npy --filenameout test_burst_on_7
#python3 thalamicsim_launch.py --filenamein test_burst_on_10.npy --filenameout test_burst_on_10
#python3 thalamicsim_launch.py --filenamein test_burst_off_7.npy --filenameout test_burst_off_7
#python3 thalamicsim_launch.py --filenamein test_burst_off_10.npy --filenameout test_burst_off_10
#python3 thalamicsim_launch.py --filenamein test_burst_off_v2_1.npy --filenameout test_burst_off_v2_1
#python3 thalamicsim_launch.py --filenamein test_burst_on_v2_1.npy --filenameout test_burst_on_v2_1
#python3 thalamicsim_launch.py --filenamein test_modulation_2.npy --filenameout test_modulation_2 --all_section_recording
#python3 thalamicsim_launch.py --filenamein test_burst_on_7.npy --filenameout test_burst_on_7
#python3 thalamicsim_launch.py --filenamein test_burst_off_7.npy --filenameout test_burst_off_7
#python3 thalamicsim_launch.py --filenamein test_burst_off_7.npy --filenameout test_burst_off_7 --no-sim
#python3 thalamicsim_launch.py --filenamein test_modulation_short.npy --filenameout test_modulation_short --all_synapse_recording



#python3 thalamicsim_launch.py --filenamein test_burst_off_v2_2.npy --filenameout test_burst_off_v2_2
#python3 thalamicsim_launch.py --filenamein test_burst_on_v2_2.npy --filenameout test_burst_on_v2_2
#python3 thalamicsim_launch.py --filenamein test_syn_spontaneous_3rd.npy --filenameout test_syn_spontaneous_3rd
#python3 thalamicsim_launch.py --filenamein test_sensitivity_syn_1st.npy --filenameout test_sensitivity_syn_1st
#python3 thalamicsim_launch.py --filenamein test_sensitivity_presyn_1st.npy --filenameout test_sensitivity_presyn_1st_2 --end_index 4480 --init_index 2520

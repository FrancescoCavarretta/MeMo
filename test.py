import sim.nwbio as nwbio

f = nwbio.FileReader('/home/francesco/Downloads/sub-HI207_ses-HI207-063019_ecephys+ogen.nwb')

print(f.nwbfile.analysis.keys())

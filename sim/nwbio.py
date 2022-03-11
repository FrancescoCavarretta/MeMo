class FileWriter:
    def __init__(self, filename, session_description, identifier, \
                 experimenter='', lab='Jaeger Lab', institution='Emory University', \
                     experiment_description='', session_id='happiness_in_silico', key_fmt=None):
        """
          Create a NWB handle for output
        """
        
        from datetime import datetime
        from dateutil.tz import tzlocal
        from pynwb import NWBFile      
    
        self.filename = filename
        self.session_description = session_description
        self.identifier = identifier
        self.experimenter = experimenter
        self.lab = lab
        self.institution = institution
        self.experiment_description = experiment_description
        self.session_id = session_id


        self._key_fmt = key_fmt # prefix
       
        # file handle
        self.nwbfile = NWBFile(
            self.session_description,
            self.identifier,
            datetime.now(tzlocal()),
            experimenter=self.experimenter,
            lab=self.lab,
            institution=self.institution,
            experiment_description=self.experiment_description,
            session_id=self.session_id
            )

    

    def close(self):
        from pynwb import NWBHDF5IO
        with NWBHDF5IO(self.filename, 'w') as io:
            io.write(self.nwbfile)
        self.nwbfile = None




    class DataWriter:
        def __init__(self, nwbfile, cell_name, key_fmt=None, description="section recordings", location="NEURON template"):
            self.nwbfile = nwbfile # nwb handle
            self._last_electrode_id = 0 # last electrode idx
        
            # electrode group
            self.electrode_group = self.nwbfile.create_electrode_group(cell_name + "_data", description=description, location=location, \
                                                                   device=self.nwbfile.create_device(name=cell_name))
    
            self._key_fmt = 'sim_ephys_data_%d' if key_fmt is None else key_fmt # prefix
    
    
        def add(self, xdata, ydata, location=''):
            from pynwb.ecephys import ElectricalSeries
    
            key = self._key_fmt %  self._last_electrode_id
        
            # create an electrode
            self.nwbfile.add_electrode(id=self._last_electrode_id, 
                                       x=.0, y=.0, z=.0, 
                                       imp=float(-self._last_electrode_id), location=location, filtering='none', 
                                       group=self.electrode_group)
    
    
    
            self.nwbfile.add_acquisition(
                ElectricalSeries(key, ydata, self.nwbfile.create_electrode_table_region([self._last_electrode_id], key), timestamps=xdata)
                )
        
            # increment the electrode id
            self._last_electrode_id += 1


    def get_cell_writer(self, cell_name, key_fmt=None, description="section recordings", location="NEURON template"):
        if key_fmt is None:
            key_fmt = self._key_fmt
        return FileWriter.DataWriter(self.nwbfile, cell_name, key_fmt=key_fmt, description=description, location=location)


class FileReader:
    def __init__(self, filename):
        from pynwb import NWBHDF5IO
        self.filename = filename
        self.nwbfile = NWBHDF5IO(self.filename, 'r').read()
    
    def read(self, key):
        import numpy as np
        data = self.nwbfile.acquisition[key]
        return np.array(data.timestamps), np.array(data.data)
    
    def close(self):
        self.nwbfile = None
    
    
        








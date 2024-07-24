import numpy as np
import os
import h5py
import datetime as dt

class sweep_processing:
    def __init__(self,times,num_pixels,filename,metadata):
        self.filename= filename.split('.')[0]
        self.hdf5_filename = self.filename+'.hdf5'
        i = 1
        while os.path.isfile(self.hdf5_filename) is True:
            self.hdf5_filename = self.filename+'_'+str(i)+'.hdf5'
            i += 1
        
        self.metadata = metadata
        
        self.sweep_index = 0
        self.times = np.array(times,ndmin=2)
        self.sweep_index_array = np.zeros(shape=(self.times.size,1))
        self.pixels = np.linspace(0,num_pixels-1,num_pixels)
        self.current_data = np.zeros(shape=(self.times.size,num_pixels))
        self.current_pumpOn = np.zeros(shape=(self.times.size,num_pixels)) ###################
        self.current_pumpOff = np.zeros(shape=(self.times.size,num_pixels)) ###################
        self.avg_data = np.zeros(shape=(self.times.size,num_pixels))
        self.avg_pumpOn = np.zeros(shape=(self.times.size,num_pixels)) ##########################
        self.avg_pumpOff = np.zeros(shape=(self.times.size,num_pixels)) ##########################
# =============================================================================
#         if self.delay_type == 2:
#             self.total_weight = np.zeros(self.disco_times.size)
# =============================================================================
        
    def add_current_data(self,dtt,probe_on,probe_off,time_point):
        self.current_data[time_point,:] = dtt
        self.current_pumpOn[time_point,:] = probe_on
        self.current_pumpOff[time_point,:] = probe_off
        if self.sweep_index == 0:
            self.avg_data[time_point,:] = dtt
            self.avg_pumpOn[time_point,:] = probe_on
            self.avg_pumpOff[time_point,:] = probe_off
        else:
            self.avg_data[time_point,:] = np.array(((self.avg_data[time_point,:]*self.sweep_index_array[time_point])+dtt)/(self.sweep_index_array[time_point]+1))
            self.avg_pumpOn[time_point,:] = np.array(((self.avg_pumpOn[time_point,:]*self.sweep_index_array[time_point])+probe_on)/(self.sweep_index_array[time_point]+1))
            self.avg_pumpOff[time_point,:] = np.array(((self.avg_pumpOff[time_point,:]*self.sweep_index_array[time_point])+probe_off)/(self.sweep_index_array[time_point]+1))
        self.sweep_index_array[time_point] = self.sweep_index_array[time_point]+1 
        return
    
# =============================================================================
#     def add_current_data_disco(self,staged_dtt,staged_weight):
#         '''takes the binned data (staged data) and adds it to the data for this sweep'''
#         for kdx, st_dtt in enumerate(self.staged_dtt):
#             if self.sweep_weight[kdx] + self.staged_weight[kdx] != 0:
#                 self.sweep_dtt[kdx,:] = ((self.sweep_dtt[kdx,:]*self.sweep_weight[kdx]) + (self.staged_dtt[kdx,:]*self.staged_weight[kdx]))/(self.sweep_weight[kdx]+self.staged_weight[kdx])
#                 self.sweep_weight[kdx] = self.sweep_weight[kdx] + self.staged_weight[kdx]
#         return
# =============================================================================
        
            
    def next_sweep(self):
        self.sweep_index = self.sweep_index+1
        self.current_data = np.zeros(shape=(self.times.size,self.pixels.size))
        #self.total_weight = self.total_weight + self.sweep_weight
        return
        
#    def save_current_data_old(self,waves):
#        basename = os.path.basename(self.filename)
#        pathname= os.path.dirname(self.filename)
#        new_path = pathname+'/'+basename+'_Sweeps/'
#        new_filename = new_path+basename+'_Sweep_'+str(self.sweep_index+1)+'.dtc'
#        if not os.path.exists(new_path):
#            os.makedirs(new_path)
#        save_data = np.vstack((np.hstack((0,waves)),
#                                np.hstack((self.times.T,
#                                           self.current_data))))
#        np.savetxt(new_filename,save_data,newline='\r\n',delimiter='\t',fmt='%1.4e')
        
    def save_current_data(self,waves):
        save_data = np.vstack((np.hstack((0,waves)),
                               np.hstack((self.times.T,
                                          self.current_data))))
        save_pumpOn = np.vstack((np.hstack((0,waves)), np.hstack((self.times.T,self.current_pumpOn)))) ###################
        save_pumpOff = np.vstack((np.hstack((0,waves)), np.hstack((self.times.T,self.current_pumpOff)))) ###################

        with h5py.File(self.hdf5_filename,'a') as hdf5_file:
            dset = hdf5_file.create_dataset('Sweeps/Sweep_'+str(self.sweep_index),data=save_data)
            dset.attrs['date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
            dset.attrs['time'] = str(dt.datetime.now().time()).encode('ascii','ignore')

            dset1 = hdf5_file.create_dataset('Sweeps/Sweep_'+str(self.sweep_index)+'_pump_on',data=save_pumpOn) #####################
            dset1.attrs['date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
            dset1.attrs['time'] = str(dt.datetime.now().time()).encode('ascii','ignore')

            dset2 = hdf5_file.create_dataset('Sweeps/Sweep_'+str(self.sweep_index)+'_pump_off',data=save_pumpOff) #####################
            dset2.attrs['date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
            dset2.attrs['time'] = str(dt.datetime.now().time()).encode('ascii','ignore')
        return
    
    def save_current_data_disco(self,waves):
        save_data = np.vstack((np.hstack((0,waves)),
                               np.hstack((self.disco_times.T,
                                          self.sweep_dtt))))
        
        with h5py.File(self.hdf5_filename,'a') as hdf5_file:
            dset = hdf5_file.create_dataset('Sweeps/Sweep_'+str(self.sweep_index),data=save_data)
            dset.attrs['date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
            dset.attrs['time'] = str(dt.datetime.now().time()).encode('ascii','ignore')
            
        save_weight = np.dstack((self.disco_times.T,
                                            self.sweep_weight))
        
        with h5py.File(self.hdf5_filename,'a') as hdf5_file:
            dset = hdf5_file.create_dataset('Sweeps/Weights_'+str(self.sweep_index),data=save_weight)
            dset.attrs['date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
            dset.attrs['time'] = str(dt.datetime.now().time()).encode('ascii','ignore')
                 
        return
        
#    def save_avg_data_old(self,waves):
#        save_data = np.vstack((np.hstack((0,waves)),
#                               np.hstack((self.times.T,
#                                          self.avg_data))))
#        
#        np.savetxt(self.filename,save_data,newline='\r\n',delimiter='\t',fmt='%1.4e')
        
    def save_avg_data(self,waves):
        save_data = np.vstack((np.hstack((0,waves)),
                               np.hstack((self.times.T,
                                          self.avg_data))))
        
        save_pumpOn = np.vstack((np.hstack((0,waves)),
                               np.hstack((self.times.T,
                                          self.avg_pumpOn)))) ####################################

        save_pumpOff = np.vstack((np.hstack((0,waves)),
                               np.hstack((self.times.T,
                                          self.avg_pumpOff)))) ####################################

        with h5py.File(self.hdf5_filename,'a') as hdf5_file:
            try:
                dset = hdf5_file['Average']
                dset[:,:] = save_data
                dset.attrs.modify('end_date',str(dt.datetime.now().date()).encode('ascii','ignore'))
                dset.attrs.modify('end_time',str(dt.datetime.now().time()).encode('ascii','ignore'))
                dset.attrs.modify('num_sweeps',str(self.sweep_index).encode('ascii','ignore'))
                
                dset1 = hdf5_file['Average_Pump_On']  ###################################
                dset1[:,:] = save_pumpOn
                dset1.attrs.modify('end_date',str(dt.datetime.now().date()).encode('ascii','ignore'))
                dset1.attrs.modify('end_time',str(dt.datetime.now().time()).encode('ascii','ignore'))
                dset1.attrs.modify('num_sweeps',str(self.sweep_index).encode('ascii','ignore'))

                dset2 = hdf5_file['Average_Pump_Off']  ###################################
                dset2[:,:] = save_pumpOff
                dset2.attrs.modify('end_date',str(dt.datetime.now().date()).encode('ascii','ignore'))
                dset2.attrs.modify('end_time',str(dt.datetime.now().time()).encode('ascii','ignore'))
                dset2.attrs.modify('num_sweeps',str(self.sweep_index).encode('ascii','ignore'))
            except:
                self.save_metadata_initial()
                dset = hdf5_file.create_dataset('Average',data=save_data)
                dset.attrs['start date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
                dset.attrs['start time'] = str(dt.datetime.now().time()).encode('ascii','ignore')
                for key,item in self.metadata.items():
                    dset.attrs[key] = str(item).encode('ascii','ignore')
                dset.attrs['num_sweeps'] = str(self.sweep_index).encode('ascii','ignore')

                dset1 = hdf5_file.create_dataset('Average_Pump_On',data=save_pumpOn)  ###################################
                dset1.attrs['start date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
                dset1.attrs['start time'] = str(dt.datetime.now().time()).encode('ascii','ignore')

                dset2 = hdf5_file.create_dataset('Average_Pump_Off',data=save_pumpOff)  ###################################
                dset2.attrs['start date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
                dset2.attrs['start time'] = str(dt.datetime.now().time()).encode('ascii','ignore')

                for key,item in self.metadata.items():
                    dset1.attrs[key] = str(item).encode('ascii','ignore')
                dset1.attrs['num_sweeps'] = str(self.sweep_index).encode('ascii','ignore')
        return
    
# =============================================================================
#     def save_avg_data_disco(self,waves):
#         save_data = np.vstack((np.hstack((0,waves)),
#                                np.hstack((self.disco_times.T,
#                                           self.avg_data))))
#         
#         save_weight = np.dstack((self.disco_times.T,
#                                             self.total_weight))
#         
#         with h5py.File(self.hdf5_filename) as hdf5_file:
#             try:
#                 dset = hdf5_file['Average']
#                 dset[:,:] = save_data
#                 dset.attrs.modify('end_date',str(dt.datetime.now().date()).encode('ascii','ignore'))
#                 dset.attrs.modify('end_time',str(dt.datetime.now().time()).encode('ascii','ignore'))
#                 dset.attrs.modify('num_sweeps',str(self.sweep_index).encode('ascii','ignore'))
#                 
#                 dset2 = hdf5_file['Total_weights']
#                 dset2[:,:] = save_weight
#                 dset2.attrs.modify('end_date',str(dt.datetime.now().date()).encode('ascii','ignore'))
#                 dset2.attrs.modify('end_time',str(dt.datetime.now().time()).encode('ascii','ignore'))
#                 dset2.attrs.modify('num_sweeps',str(self.sweep_index).encode('ascii','ignore'))
#             except:
#                 self.save_metadata_initial()
#                 dset = hdf5_file.create_dataset('Average',data=save_data)
#                 dset.attrs['start date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
#                 dset.attrs['start time'] = str(dt.datetime.now().time()).encode('ascii','ignore')
#                 
#                 dset2 = hdf5_file.create_dataset('Total_weights',data=save_weight)
#                 dset2.attrs['start date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
#                 dset2.attrs['start time'] = str(dt.datetime.now().time()).encode('ascii','ignore')
#                 for key,item in self.metadata.items():
#                     dset.attrs[key] = str(item).encode('ascii','ignore')
#                 dset.attrs['num_sweeps'] = str(self.sweep_index).encode('ascii','ignore')
#         return
# =============================================================================
        
    def save_metadata_initial(self):
        with h5py.File(self.hdf5_filename,'a') as hdf5_file:
            data = np.zeros((1,1))
            dset = hdf5_file.create_dataset('Metadata',data=data)
            for key, item in self.metadata.items():
                dset.attrs[key] = str(item).encode('ascii','ignore')
                    
    #def save_metadata_each_sweep(self,probe,reference,error):
    def save_metadata_each_sweep(self,probe,error):
        with h5py.File(self.hdf5_filename,'a') as hdf5_file:
            dset = hdf5_file.create_dataset('Spectra/Sweep_'+str(self.sweep_index)+'_Probe_Spectrum',data=probe)
            dset.attrs['date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
            dset.attrs['time'] = str(dt.datetime.now().time()).encode('ascii','ignore')
                
            #dset2 = hdf5_file.create_dataset('Spectra/Sweep_'+str(self.sweep_index)+'_Reference_Spectrum',data=reference)
            #dset2.attrs['date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
            #dset2.attrs['time'] = str(dt.datetime.now().time()).encode('ascii','ignore')
                
            dset3 = hdf5_file.create_dataset('Spectra/Sweep_'+str(self.sweep_index)+'_Error_Spectrum',data=error)
            dset3.attrs['date'] = str(dt.datetime.now().date()).encode('ascii','ignore')
            dset3.attrs['time'] = str(dt.datetime.now().time()).encode('ascii','ignore')
            
                    
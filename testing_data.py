from ta_data_processing_class import *
from TA2_camera import *
import timeit
import numpy as np
import json


def get_camera_data():
    lines_per_frame = 1000
    camera= octoplus()
    camera.Initialize( lines_per_frame=lines_per_frame)
    camera.Acquire()
    probe = camera.probe
    reference= camera.reference
    first_pixel=camera.first_pixel
    num_pixels = camera.num_pixels
    camera.Exit()
    return [probe, reference, first_pixel, num_pixels]

def get_dummy_data(n):
    probe = np.ones([n,2048])
    reference= np.ones([n,2048])
    first_pixel=1
    num_pixels = 2000
    return [probe, reference, first_pixel, num_pixels]

def run_diagnostics_complicated(ta, dict_of_funcs, n):
    times=[]
    for func, diagnostics in dict_of_funcs.items():
        for i in range(n+1):
            start=time.time()
            func() #would this work? or do i have to name them ta.func in the list...
            end=time.time()
            times.append(start-end)
        diagnostics.append(np.mean(times))
    return

def check_improvement(dict_of_funcs, a,b):
    for func, diagnostics in dict_of_funcs.items():
        percent_improve= (diagnostics[a]-diagnostics[b])/diagnostics[a]
        print(func, percent_improve)
    return

#needlessly complicated, entails saving data to files n stuff
def main_complicated():
    first= True
    if first:
        data= get_dummy_data() #runs camera to grab arrays
        ta = ta_data_processing(*data)
        dict_of_funcs= {ta.average_shots : []}
        run_diagnostics(ta, dict_of_funcs, 4)
        print(dict_of_funcs)
        #doesn't exist
        save_data(data)
        save_dict(dict_of_funcs)
    else:
        data=open_data()
        dict_of_funcs=open_dict()
        run_diagnostics(ta, dict_of_funcs, 4) #times functions n times, gets avg
        check_improvement(dict_of_funcs, 0,1) #prints percent improvement
    return

def run_diagnostics_simple(ta, func, params, n):
    times=[]
    if params:
        for i in range(n+1):
            start=time.time()
            func(params)
            end=time.time()
            times.append(end-start)
    else:
        for i in range(n+1):
            start=time.time()
            func()
            end=time.time()
            times.append(end-start)
    return np.mean(times)

#simple
def main_simple():
    runs=100
    shots=1000
    data= get_dummy_data(shots) #runs camera to grab arrays
    ta = ta_data_processing(*data)
    func=ta.linear_pixel_correlation
    params=[2,2] #if no params, set to None
    time=run_diagnostics_simple(ta, func, params, runs)
    print(func.__name__, " took ", time, " seconds to process ", shots, " shots")
    #check_improvement(dict_of_funcs, 0,1) #prints percent improvement

def run_diagnostics_timeit(setup, stmt, n, avg):
    times=[]
    if not avg: #gets shortest time it takes #except this doesn't work??
        time= timeit.timeit(stmt=stmt, setup=setup, number=n) #setup?
        return time
    else: #gets average time it takes
        times=timeit.repeat(repeat=n,stmt=stmt, setup=setup, number=1)
        return np.mean(times)

#timeit
def main_timeit():
    runs=10000
    avg = True #(non-avg doesnt work....)

    setup="from ta_data_processing_class import ta_data_processing; import numpy as np; shots=1000; ta = ta_data_processing(np.ones([shots,2048]),np.ones([shots,2048]),1,2000)"

    #stmt= "ta.linear_pixel_correlation([2,2])"
    stmt= "ta.linear_pixel_correlation_new([2,2])"
    time= run_diagnostics_timeit(setup, stmt, runs, avg)
    #print("linear_pixel_correlation (old) took ", time, " seconds to process 1000 shots")
    print("linear_pixel_correlation_new took ", time, " seconds to process 1000 shots")

def main_timeit_new():
    runs=10000
    avg = True #(non-avg doesnt work....)

    #shots=1000
    #probe_array= np.random.rand(shots,2000)
    #probe_array = np.divide(probe_array,2)

    setup="import numpy as np; shots=1000; probe_array= np.random.rand(shots,2000)"

    stmt= "probe_array = probe_array/2"
    #stmt= "probe_array = np.divide(probe_array,2)"
    time= run_diagnostics_timeit(setup, stmt, runs, avg)
    print("linear_pixel_correlation (old) took ", time, " seconds to process 1000 shots")
    #print("linear_pixel_correlation_new took ", time, " seconds to process 1000 shots")

def main():
    #main_simple()
    #main_timeit()
    main_timeit_new()


if __name__ == '__main__':
    main()

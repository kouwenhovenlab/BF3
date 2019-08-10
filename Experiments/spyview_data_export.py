import numpy as np
import os, sys
import qcodes

def export_to_spyview(dat, directory):
    """
    Unpacks all data columns in the qcodes dataset 'dat'.
    Writes .dat and .meta.txt files in the directory specified.
    Returns the filename (without postfixes)
    """
    filename, independent_variable_list, dependent_variable_list, number_of_results = extract_from_dat(dat)

    with open(os.path.join(directory, filename) + '.dat', 'w') as dat_file:
        set_points = [independent_variable_list[k]['data'][0] for k in range(3)]
        
        for i in range(number_of_results):
            set_points_prev = set_points
            set_points = [independent_variable_list[k]['data'][i] for k in range(3)]
            
            if sum(np.array(set_points) != np.array(set_points_prev)) > 1:
                dat_file.write('\n')
            
            for k in range(3):
                dat_file.write('{}\t'.format(set_points[k]))
            for k in range(len(dependent_variable_list)):
                dat_file.write('{}\t'.format(dependent_variable_list[k]['data'][i]))
            dat_file.write('\n')
    
    with open(os.path.join(directory, filename) + '.meta.txt', 'w') as meta_file:
        for i in range(3):
            current_array = independent_variable_list[i]['data']
            meta_file.write('{}\n'.format(len(np.unique(current_array))))
            meta_file.write('{}\n{}\n'.format(min(current_array), max(current_array))) 
            meta_file.write('{} ({})\n'.format(independent_variable_list[i]['name'], independent_variable_list[i]['unit']))
        for i in range(len(dependent_variable_list)):
            meta_file.write('{}\n'.format(i+4))
            meta_file.write('{} ({})\n'.format(dependent_variable_list[i]['name'], dependent_variable_list[i]['unit']))

    return filename

def extract_from_dat(dat):
    """
    Takes a dat object that is returned by load_by_id() and extracts relevant data that will be used to write the spyview .dat files.
    returns: filename ([DB filename]_runID_[runID].dat),
        independent_variable_list (always of length 3),
        dependent_variable_list,
        number of results
    
    Data format:

    independent_variable_list = [
        {'name': str,
        'unit': str,
        'data': list},
        ...
    ]
    
    dependent_variable_list = [
        {'name': str,
        'unit': str,
        'data': list},
        ...
    ]
    
    """
    if type(dat) != qcodes.dataset.data_set.DataSet:
        print('Input must be a qcodes dataset!')
        raise ValueError

    filename = dat.path_to_db.split('/')[-1][:-3] + '_runID_{}'.format(dat.run_id)
    
    independent_variable_list = []
    dependent_variable_list = []

    for ps in dat.get_parameters():
        column_item = {
            'name': ps.name,
            'unit': ps.unit,
            'data': np.array(dat.get_data(ps.name))[:,0].tolist()
        }

        if ps.depends_on == '':
            independent_variable_list.insert(0, column_item) # this instead of appending because the faster axis needs to be in front in the meta.txt file
        else:
            dependent_variable_list.append(column_item)

    empty_column_item = {
        'name': 'None',
        'unit': 'None',
        'data': [0] * dat.number_of_results
    }

    while len(independent_variable_list) < 3:
        independent_variable_list.append(empty_column_item)
        
    return filename, independent_variable_list, dependent_variable_list, dat.number_of_results

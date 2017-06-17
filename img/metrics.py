import math

class Area:
    Small, Medium, Big = range(3)

    areas = {Small: 'small', Medium: 'medium', Big: 'big'}


generations = {Area.Small: (100, 500, 1000), \
               Area.Medium: (100, 500, 1000, 2000), \
               Area.Big: (100, 1000, 2000, 5000)}


paths = {Area.Small: '../results_small/', \
         Area.Medium: '../results_medium/', \
         Area.Big: '../results_big/'}


algorithms = ('nsga', 'spea')


results = 'results'


pop_size = 200


def _get_results_file_name(algorithm, generations, size):
    return '%s_results_%d_%d_%s.csv' % (algorithm, pop_size, generations, size)


def _get_pareto_file_name(size):
    return 'pareto_front_%s.csv' % size


def _get_small_results():
    nsga_results = {generation: [] for generation in generations[Area.Small]}
    spea_results = {generation: [] for generation in generations[Area.Small]}
        
    for generation in nsga_results:
        path = paths[Area.Small] + _get_results_file_name('nsga', generation, 'small')
        with open(path, 'r') as f:
            for line in f:
                nsga_results[generation].append(list(map(float, line.rstrip('\n').split(','))))
                
    for generation in spea_results:
        path = paths[Area.Small] + _get_results_file_name('spea', generation, 'small')
        with open(path, 'r') as f:
            for line in f:
                spea_results[generation].append(list(map(float, line.rstrip('\n').split(','))))

    return nsga_results, spea_results


def _get_medium_results():
    nsga_results = {generation: [] for generation in generations[Area.Medium]}
    spea_results = {generation: [] for generation in generations[Area.Medium]}
        
    for generation in nsga_results:
        path = paths[Area.Medium] + _get_results_file_name('nsga', generation, 'medium')
        with open(path, 'r') as f:
            for line in f:
                nsga_results[generation].append(list(map(float, line.rstrip('\n').split(','))))
                
    for generation in spea_results:
        path = paths[Area.Medium] + _get_results_file_name('spea', generation, 'medium')
        with open(path, 'r') as f:
            for line in f:
                spea_results[generation].append(list(map(float, line.rstrip('\n').split(','))))

    return nsga_results, spea_results


def _get_big_results():
    nsga_results = {generation: [] for generation in generations[Area.Big]}
    spea_results = {generation: [] for generation in generations[Area.Big]}
        
    for generation in nsga_results:
        path = paths[Area.Big] + _get_results_file_name('nsga', generation, 'big')
        with open(path, 'r') as f:
            for line in f:
                nsga_results[generation].append(list(map(float, line.rstrip('\n').split(','))))
                
    for generation in spea_results:
        path = paths[Area.Big] + _get_results_file_name('spea', generation, 'big')
        with open(path, 'r') as f:
            for line in f:
                spea_results[generation].append(list(map(float, line.rstrip('\n').split(','))))

    return nsga_results, spea_results


def _get_small_pareto():
    result = []
    with open(paths[Area.Small] + _get_pareto_file_name(Area.areas[Area.Small])) as f:
        for line in f:
            result.append(list(map(float,line.rstrip('\n').split(','))))
    return result


def _get_medium_pareto():
    result = []
    with open(paths[Area.Medium] + _get_pareto_file_name(Area.areas[Area.Medium])) as f:
        for line in f:
            result.append(list(map(float,line.rstrip('\n').split(','))))
    return result


def _get_big_pareto():
    result = []
    with open(paths[Area.Big] + _get_pareto_file_name(Area.areas[Area.Big])) as f:
        for line in f:
            result.append(list(map(float,line.rstrip('\n').split(','))))
    return result


#####################################################################################
def _calculate_ER(nsga, spea, front, size):
    results_nsga = {generation: 0 for generation in nsga}
    results_spea = {generation: 0 for generation in spea}
    
    for generation in results_nsga:
        results_nsga[generation] = sum(int(el not in front) for el in nsga[generation])/len(nsga[generation])

    for generation in results_spea:
        results_spea[generation] = sum(int(el not in front) for el in spea[generation])/len(spea[generation])

    print('NSGA:\n',results_nsga)

    print('SPEA:\n',results_spea)


def _calculate_SP(nsga, spea, size):
    results_nsga = {generation: 0 for generation in nsga}
    results_spea = {generation: 0 for generation in spea}

    for generation in results_nsga:
        total_dist = 0
        distances = []
        for el in nsga[generation]:
            dist = _get_nearest_neighbor_dist(el, nsga[generation])
            total_dist += dist
            distances.append(dist)
        n = len(nsga[generation])
        avg_dist = total_dist/n
        variance = sum((avg_dist - distance)**2 for distance in distances)
        results_nsga[generation] = math.sqrt(variance/(n-1))
    
    for generation in results_spea:
        total_dist = 0
        distances = []
        for el in spea[generation]:
            dist = _get_nearest_neighbor_dist(el, spea[generation])
            total_dist += dist
            distances.append(dist)
        n = len(spea[generation])
        avg_dist = total_dist/n
        variance = sum((avg_dist - distance)**2 for distance in distances)
        results_spea[generation] = math.sqrt(variance/(n-1))

    print('NSGA:\n',results_nsga)

    print('SPEA:\n',results_spea)

def _get_nearest_neighbor_dist(el, solutions):
    solutions = solutions[:]
    solutions.remove(el)
    distances = (abs(el[0] - x[0]) + abs(el[1] - x[1]) for x in solutions)
    return sorted(distances)[0]


def _calculate_GD(nsga, spea, front, size):
    results_nsga = {generation: 0 for generation in nsga}
    results_spea = {generation: 0 for generation in spea}

    for generation in results_nsga:
        total_dist = 0
        for el in nsga[generation]:
            total_dist += _get_dist_to_pareto(el, front)**2
        n = len(nsga[generation])
        results_nsga[generation] = math.sqrt(total_dist)/n

    for generation in results_spea:
        total_dist = 0
        for el in spea[generation]:
            total_dist += (_get_dist_to_pareto(el, front)**2)
        n = len(spea[generation])
        results_spea[generation] = math.sqrt(total_dist)/n

    print('NSGA:\n',results_nsga)

    print('SPEA:\n',results_spea)

def _get_dist_to_pareto(el, front):
    distances = (math.sqrt((x[0] - el[0])**2 + (x[1] - el[1])**2) for x in front)
    return sorted(distances)[0]


def _calculate_FE(nsga, spea, size):
    results_nsga = {generation: 0 for generation in nsga}
    results_spea = {generation: 0 for generation in spea}

    for generation in results_nsga:
        max_dist_fst_obj, max_dist_snd_obj = 0, 0
        for el in nsga[generation]:
            dist_fst = _get_max_fst_obj(el, nsga[generation])
            dist_snd = _get_max_snd_obj(el, nsga[generation])   

            max_dist_fst_obj = max(max_dist_fst_obj, dist_fst)
            max_dist_snd_obj = max(max_dist_snd_obj, dist_snd)
        results_nsga[generation] = math.sqrt(max_dist_fst_obj + max_dist_snd_obj)

    for generation in results_spea:
        max_dist_fst_obj, max_dist_snd_obj = 0, 0
        for el in spea[generation]:
            dist_fst = _get_max_fst_obj(el, spea[generation])
            dist_snd = _get_max_snd_obj(el, spea[generation])   

            max_dist_fst_obj = max(max_dist_fst_obj, dist_fst)
            max_dist_snd_obj = max(max_dist_snd_obj, dist_snd)
        results_spea[generation] = math.sqrt(max_dist_fst_obj + max_dist_snd_obj)

    print('NSGA:\n',results_nsga)

    print('SPEA:\n',results_spea)


def _get_max_fst_obj(el, solutions):
    solutions = solutions[:]
    solutions.remove(el)

    distances = (abs(el[0] - x[0]) for x in solutions)
    return sorted(distances, reverse=True)[0]

def _get_max_snd_obj(el, solutions):
    solutions = solutions[:]
    solutions.remove(el)

    distances = (abs(el[1] - x[1]) for x in solutions)
    return sorted(distances, reverse=True)[0]


if __name__ == '__main__':
    nsga_small_results, spea_small_results = _get_small_results()
    nsga_medium_results, spea_medium_results = _get_medium_results()
    nsga_big_results, spea_big_results = _get_big_results()


    small_pareto = _get_small_pareto()
    medium_pareto = _get_medium_pareto()
    big_pareto = _get_big_pareto()
    
    '''
    print("Small:\n")
    for size in nsga_small_results:
        print('%d: %d %d' % (size, len(nsga_small_results[size]), len(spea_small_results[size])))   
    print('Pareto: ', len(small_pareto))

    print("\nMedium:\n")
    for size in nsga_medium_results:
        print('%d: %d %d' % (size, len(nsga_medium_results[size]), len(spea_medium_results[size])))   
    print('Pareto: ', len(medium_pareto))

    print("\Big:\n")
    for size in nsga_big_results:
        print('%d: %d %d' % (size, len(nsga_big_results[size]), len(spea_big_results[size])))   
    print('Pareto: ', len(big_pareto))
    '''

    #results = _calculate_ER(nsga_big_results, spea_big_results, big_pareto, Area.Big)
    #_calculate_SP(nsga_big_results, spea_big_results, Area.Big)
    #_calculate_GD(nsga_big_results, spea_big_results, big_pareto, Area.Big)
    _calculate_FE(nsga_big_results, nsga_big_results, Area.Big)


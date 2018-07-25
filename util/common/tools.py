# -*- coding: utf-8 -*-

def finder(result, find):
    '''finder
    params:
        result: Json struct data waiting to be found.
        find:   List of find path.
    result:
        result after find by path.
    '''
    # print("********\n{}\n{}\n".format(result, find))
    if len(find) == 1:
        return result[find[0]]

    if isinstance(result, dict):
        result = result[find[0]]
        result = finder(result, find[1:])
    return result
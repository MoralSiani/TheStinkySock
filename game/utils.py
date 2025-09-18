def rotate_list(lst, n):
    '''
    :param lst: List to rotate to the left
    :param n: Steps to move
    :return: A new list with the values of the original list, but rotated n steps to the left
    '''
    return lst[n:] + lst[:n]

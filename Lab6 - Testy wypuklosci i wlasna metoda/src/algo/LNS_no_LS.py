from algo.LNS import LNS

def LNS_no_LS(starting_paths, distances, time_limiter):
    return LNS(starting_paths, distances, time_limiter, if_LS=False)
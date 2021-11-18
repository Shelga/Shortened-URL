import shortuuid


def get_hash(urlToSort): 

    shotrUrl = shortuuid.uuid(urlToSort)[:8]

    return shotrUrl




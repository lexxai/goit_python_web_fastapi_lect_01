import hashlib
import uuid
from time import perf_counter


TOTAL_DATA = 14_000

def prepare_data() -> list[str]:
    return [str(uuid.uuid4())*6 for _ in range(TOTAL_DATA)]

def hasing_data(data, method):
    sum_hash = ""
    start = perf_counter()
    for r in data:
        sum_hash = method(bytes(sum_hash+r, "utf-8")).hexdigest()
        # hash:hashlib._Hash = method(bytes(sum_hash, "utf-8"))
        # hash.update(bytes(r, "utf-8"))
        # sum_hash = hash.hexdigest()
        #sum_hash = method(bytes(sum_hash, "utf-8")).hexdigest()
        #print(sum_hash)
    duration = perf_counter() - start
    return (duration, sum_hash)

def hasing_data_update(data, method):
    sum_hash = ""
    start = perf_counter()
    for r in data:
        #sum_hash = method(bytes(sum_hash+r, "utf-8")).hexdigest()
        hash:hashlib._Hash = method(bytes(sum_hash, "utf-8"))
        hash.update(bytes(r, "utf-8"))
        sum_hash = hash.hexdigest()
        #sum_hash = method(bytes(sum_hash, "utf-8")).hexdigest()
        #print(sum_hash)
    duration = perf_counter() - start
    return (duration, sum_hash)

def measure():
    iter = 20
    data = prepare_data()
    print(hashlib.algorithms_guaranteed)
    methods = [hashlib.sha256, hashlib.sha224, hashlib.sha1, hashlib.blake2b ]
    for method in methods:
        start = perf_counter()
        for _ in range(iter):
            result = hasing_data(data,method)
        duration = perf_counter() - start
        print(f"total {duration} {method.__name__}. avr: {duration/iter}")
    # print("UDDATE:")
    # for method in methods:
    #     start = perf_counter()
    #     for _ in range(iter):
    #         result = hasing_data_update(data,method)
    #     duration = perf_counter() - start
    #     print(f"total {duration} {method.__name__}. avr: {duration/iter}")

if __name__ == "__main__":
    measure()
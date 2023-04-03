import json

class Util:

    def dump(path: str, item):
        json_dump = json.dumps(item, indent=2)
        with open(path, "w") as out_f:
            out_f.write(json_dump)
    
    def insert_sorted(arr, x, sort_by = None):
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if (sort_by is not None and arr[mid][sort_by] == x[sort_by]) or (sort_by is None and arr[mid][sort_by] == x[sort_by]):
                while mid < len(arr) and (sort_by is not None and arr[mid][sort_by] == x[sort_by]) or (sort_by is None and arr[mid][sort_by] == x[sort_by]):
                    mid += 1
                arr.insert(mid, x)
                return
            elif (sort_by is not None and arr[mid][sort_by] < x[sort_by]) or (sort_by is None and arr[mid][sort_by] < x[sort_by]):
                left = mid + 1
            else:
                right = mid - 1
        arr.insert(left, x)

    def binary_search_between(arr, low, high, search_by):
        left = 0
        right = len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid][search_by] < low:
                left = mid + 1
            else:
                right = mid - 1
        
        start_index = left
        
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid][search_by] > high:
                right = mid - 1
            else:
                left = mid + 1
        
        end_index = right
        
        return arr[start_index:end_index+1]

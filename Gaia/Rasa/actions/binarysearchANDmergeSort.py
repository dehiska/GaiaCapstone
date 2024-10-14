numbered_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
not_numbered_list = [4,3,2,6,7,8,9,1,5,10]


def binary_search(numbered_list, target):
    low = 0
    high = len(numbered_list) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if numbered_list[mid] == target:
            return mid
        elif numbered_list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def merge_sort(not_numbered_list):
    if len(not_numbered_list) > 1:    
        mid = len(not_numbered_list) // 2
        left_half = not_numbered_list[:mid]
        right_half = not_numbered_list[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                not_numbered_list[k] = left_half[i]
                i += 1
            else:
                not_numbered_list[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            not_numbered_list[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            not_numbered_list[k] = right_half[j]
            j += 1
            k += 1
        return not_numbered_list


def main():
    (binary_search(not_numbered_list, 3))
    print(merge_sort(not_numbered_list))


if __name__ =="__main__":
    main() 
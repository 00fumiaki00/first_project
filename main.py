def find_max(numbers):
    max = numbers[0]
    for num in numbers:
        if num > max:
            max = num
    return max
print(find_max([5,4,5,8,4,1]))
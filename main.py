def get_even_numbers(numbers):
    even_list = []
    for num in numbers:
        if num % 2 == 0:
            even_list.append(num)
    return even_list
print(get_even_numbers([6,5,4,8,5,5,4]))
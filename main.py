def get_even_numbers(numbers):              # 偶数だけを取り出す関数
    even_list = []                          # 偶数を入れる空のリスト
    for num in numbers:                     # numbersから１つずつ取り出す
        if num % 2 == 0:                    # ２で割り切れる（偶数）なら
            even_list.append(num)           # even_listに追加
    return even_list                        # 完成したリストに返す
print(get_even_numbers([6,5,4,8,5,5,4]))    # 偶数だけ取り出す




def goukei_list(numbers):           # リストの合計を返す関数
    total = 0                       # 合計を入れる変数を0で初期化
    for num in numbers:             # numbersから１つずつ取り出す
        total = total + num         # totalにnumを足す
    return total                    # 合計を返す        
print(goukei_list([1,2,3,4,5]))     # 合計を出す




def find_max(numbers):                  # リストの最大値を返す関数
    max = numbers[0]                    # 最初の数字を暫定の最大値にする
    for num in numbers:                 # numbersから１つずつ取り出す
        if num > max:                   # numが今の最大値より大きければ
            max = num                   # 最大値を更新する
    return max                          # 最大値を返す
print(find_max([3,6,5,5,5,8,5,5]))      # 最大値を出す
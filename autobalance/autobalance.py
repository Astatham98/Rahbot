from autobalance import getRanks
from autobalance import sumsplit

def autobalance(members, message):
    rank_nums = getRanks.get_ranks(members, message)
    split = sumsplit.sumSplit(list(rank_nums.values()))
    print(split)
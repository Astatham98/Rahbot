def sumSplit(left,right=[],difference=0):
    sumLeft, sumRight = sum(left),sum(right)

    # stop recursion if left is smaller than right
    if sumLeft<sumRight or len(left)<len(right): return

    # return a solution if sums match the tolerance target
    if sumLeft-sumRight == difference:
        return left, right, difference

    # recurse, brutally attempting to move each item to the right
    for i,value in enumerate(left):
        solution = sumSplit(left[:i]+left[i+1:],right+[value], difference)
        if solution: return solution

    if right or difference > 0: return
    # allow for imperfect split (i.e. larger difference) ...
    for targetDiff in range(1, sumLeft-min(left)+1):
        solution = sumSplit(left, right, targetDiff)
        if solution: return solution
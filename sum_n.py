# coding=utf-8


def soda(sum, n):
    if sum > 45 or n < 1 or n > 9:
        return None
    ans = []

    for i in range(1,10):
    	if n==1 and sum in range(1,10) and sum not in ans:
    		ans.append(sum)
    		return ans
    	if i in ans:
    		pass
    	else:
    		ans.append(i)
    		soda(sum-i, n-1)

    return []

print soda(8,2)
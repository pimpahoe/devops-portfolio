nums = [2,7,11,15]
target = 9
answer = []
for i in range(len(nums)):
    for k in range(len(nums)):
        if i!=k and nums[i] + nums[k] == target:
            answer.append(i)
            answer.append(k)
    if answer != []:
        break
print(answer)
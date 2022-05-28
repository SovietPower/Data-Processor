'''
10w

select card_id, count(*) from `like` group by card_id limit 100;
select user_id, count(*) from `like` group by user_id limit 100;
'''

import os
from random import randint, shuffle

PATH = os.path.dirname(os.path.abspath(__file__))


cnt = [1000, 700, 500, 500, 300]
total = 100000 # 10w
total_card = 25000
total_user = 100000

A = [i for i in range(1, total_user+1)]

def GetLikes(i, rest):
	if 1 and i <= len(cnt):
		return cnt[i-1]
	if i == total:
		return rest

	#
	delta = [1, 3, 8, 15, 20]
	x = randint(1, sum(delta))
	for i in range(0, 5):
		x -= delta[i]
		if x <= 0:
			if i == 0: return randint(100, 500)
			if i == 1: return randint(20, 99)
			if i == 2: return randint(5, 20)
			if i == 3: return randint(1, 5)
			return 0

def GetX():
	# 提高前面一部分用户的点赞量
	x = randint(1, 10)
	if x <= 1:
		return randint(1, 15)
	if x <= 2:
		return randint(1, 30)
	if x <= 3:
		return randint(1, 50)
	return 0

def Generate(tot):
	if tot > 100:
		shuffle(A)
		return A[:tot]
	st = set()
	st.add(0)
	B = [0]*tot
	for i in range(0, tot):
		x = GetX()
		while x in st:
			x = randint(1, total_user)
		st.add(x)
		B[i] = x
	return B

def Solve():
	f = open(PATH + '\\like_insert'+'.sql', 'w', encoding='utf-8')
	f.write('delete from `like`;\n')
	f.write('alter table `like` AUTO_INCREMENT 1;\n\n')
	f.write('insert into `like` values\n')

	rest = total
	for i in range(1, total_card+1):
		likes = min(rest, GetLikes(i, rest))
		if likes == 0:
			continue
		# print('Working on card:', i, 'rest:', rest, 'likes:', likes)
		rest -= likes

		# Test
		# if likes < 100:
		# 	print('likes:', Generate(likes+1))
		# continue

		for j in Generate(likes+1):
			if j == i:
				continue
			if not(j != i and j > 0 and j <= total_user):
				print('Error:', i, j)
				assert(0)

			f.write('''(%d, %d)%s\n''' % (j, i, ";" if rest==0 and likes==1 else ","))
			likes -= 1
			if likes == 0:
				break
		assert(likes == 0)

		if rest == 0:
			break
	f.close()

def main():
	Solve()

main()


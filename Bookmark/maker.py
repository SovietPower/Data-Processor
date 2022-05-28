'''
30w

select card_id, count(*) from `bookmark` group by card_id limit 100;
select user_id, count(*) from `bookmark` group by user_id limit 100;
'''

import os
from random import randint, shuffle

PATH = os.path.dirname(os.path.abspath(__file__))

cnt = [1200, 800, 400, 555, 400]
total = 300000 # 30w
total_card = 25000
total_user = 100000

A = [i for i in range(1, total_user+1)]

def GetBookmarks(i, rest):
	if 1 and i <= len(cnt):
		return cnt[i-1]
	if i == total:
		return rest

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
	# 提高前面一部分用户的收藏量
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
	f = open(PATH + '\\bookmark_insert'+'.sql', 'w', encoding='utf-8')
	f.write('delete from `bookmark`;\n')
	f.write('alter table `bookmark` AUTO_INCREMENT 1;\n\n')
	f.write('insert into `bookmark` values\n')

	rest = total
	for i in range(1, total_card+1):
		bookmarks = min(rest, GetBookmarks(i, rest))
		if bookmarks == 0:
			continue
		# print('Working on card:', i, 'rest:', rest, 'bookmarks:', bookmarks)
		rest -= bookmarks

		# Test
		# if bookmarks < 100:
		# 	print('bookmarks:', Generate(bookmarks+1))
		# continue

		for j in Generate(bookmarks+1):
			if j == i:
				continue
			if not(j != i and j > 0 and j <= total_user):
				print('Error:', i, j)
				assert(0)

			f.write('''(%d, %d)%s\n''' % (j, i, ";" if rest==0 and bookmarks==1 else ","))
			bookmarks -= 1
			if bookmarks == 0:
				break
		assert(bookmarks == 0)

		if rest == 0:
			break
	f.close()

def main():
	Solve()

main()


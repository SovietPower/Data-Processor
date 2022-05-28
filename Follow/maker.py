'''
20w

只控制了粉丝量的分布，用户关注量的分布是均匀的（前几个较多）
但两个接口是基本一样的，所以就这样吧

select follower_id, count(*) from follow group by follower_id limit 100;
select followee_id, count(*) from follow group by followee_id limit 100;
'''

import os
from random import randint, uniform, shuffle

PATH = os.path.dirname(os.path.abspath(__file__))


cnt = [10000, 8000, 7000, 5000]
total = 200000 # 20w/sql
total_user = 100000

A = [i for i in range(1, total_user+1)]

def RandYear():
	x = randint(1, 3)
	if x <= 2:
		return '2022'
	return '2021'
Days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def Rand(lim, start = 1):
	x = randint(start, lim)
	if x<10:
		return '0'+str(x)
	return str(x)

def RandTime():
	y = RandYear()
	m = Rand(12 if y!="2022" else 4)
	d = Rand(Days[int(m)])
	return y + m + d + Rand(23, 0) + Rand(59, 0) + Rand(59, 0)

def GetFollows(i, rest):
	if 1 and i <= len(cnt):
		return cnt[i-1]
	if i == total:
		return rest

	#	千粉 百粉 几十粉 个粉 0
	delta = [1, 7, 7, 40, 40]
	x = randint(1, sum(delta))
	for i in range(0, 5):
		x -= delta[i]
		if x <= 0:
			if i == 0: return randint(1000, 5000)
			if i == 1: return randint(100, 900)
			if i == 2: return randint(10, 90)
			if i == 3: return randint(1, 9)
			return 0

def GetX():
	# 提高前面一部分用户的关注量
	x = randint(1, 10)
	if x <= 1:
		return randint(1, 10)
	if x <= 2:
		return randint(1, 30)
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
	f = open(PATH + '\\follow_insert'+'.sql', 'w', encoding='utf-8')
	f.write('delete from follow;\n')
	f.write('alter table follow AUTO_INCREMENT 1;\n\n')
	f.write('insert into follow values\n')

	rest = total
	for i in range(1, total_user+1):
		follows = min(rest, GetFollows(i, rest))
		if follows == 0:
			continue
		# print('Working on user:', i, 'rest:', rest, 'follows:', follows)
		rest -= follows

		# Test
		# if follows < 100:
		# 	print('follows:', Generate(follows+1))
		# continue

		for j in Generate(follows+1):
			if j == i:
				continue
			if not(j != i and j > 0 and j <= total_user):
				print('Error:', i, j)
				assert(0)

			f.write('''(%d, %d, %s)%s\n''' % (j, i, RandTime(), ";" if rest==0 and follows==1 else ","))
			follows -= 1
			if follows == 0:
				break
		assert(follows == 0)

		if rest == 0:
			break
	f.close()

def main():
	Solve()

main()


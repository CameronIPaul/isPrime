import time

import redis
from flask import Flask, jsonify, json

import math

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
	retries = 5
	while True:
		try:
			return cache.incr('hits')
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)

def add_prime_to_redis(prime):
	retries = 5
	while True:
		try:
			cache.set(prime, prime)
			break
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)
	return prime

def list_primes_in_redis():
	ListK = []
	retries = 5
	while True:
		try:
			ListK = cache.keys()
			break
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)
	j = 0
	List = []
	for i in range(0, ListK.__len__()):
		empDict = str(j) + ":" + str(ListK[i]) + ", "
		List.append(empDict)
		j += 1
	return ''.join(List)

@app.route('/')
def hello():
	count = get_hit_count()
	return 'Hello from Docker! I have been seen {} times.\n'.format(count)
	
@app.route('/isPrime/<int:number>')
def isPrime(number):
	if (number == 2):
		add_prime_to_redis(number)
		return "{} is prime".format(number)
	if (number == 1):
		return "{} is not prime".format(number)
	if (number % 2 == 0):
		return "{} is not prime".format(number)
	for i in range(2, math.ceil(math.sqrt(number)) + 1):
		if number % i == 0:
			return "{} is not prime".format(number)
	add_prime_to_redis(number)
	return "{} is prime".format(number)
	
@app.route('/primesStored')
def primesStored():
	r = ''
	r = list_primes_in_redis()
	return jsonify(Primes=r)

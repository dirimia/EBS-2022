import sys
import os
import argparse
import random
import math
import yaml


configuration = None


class Rule:
	def __init__(self, field, operator, value):
		self.field = field
		self.operator = operator
		self.value = value

	def __str__(self):
		if isinstance(self.value, str):
			strValue = f"\"{self.value}\""
		else:
			strValue = f"{self.value:.2f}"
		return f"({self.field},{self.operator},{strValue})"

	def __repr__(self):
		return self.__str__()


class Subscription:
	__fieldPrecedence__ = {
		"company": 0,
		"value": 1,
		"drop": 2,
		"variation": 3,
		"date": 4
	}

	def __init__(self, rules = []):
		self.rules = [rule for rule in rules if rule is not None]

	def __str__(self):
		self.rules.sort(key = lambda rule: Subscription.__fieldPrecedence__[rule.field])
		strRules = ";".join([str(rule) for rule in self.rules])
		return f"{{{strRules}}}"

	def __repr__(self):
		return self.__str__()


class Publication:
	def __init__(self, company, value, drop, variation, date):
		self.company = company
		self.value = value
		self.drop = drop
		self.variation = variation
		self.date = date

	def __str__(self):
		strCompany = f"(company,\"{self.company}\")"
		strValue = f"(value,{self.value:.2f})"
		strDrop = f"(drop,{self.drop:.2f})"
		strVariation = f"(variation,{self.variation:.2f})"
		strDate = f"(date,{self.date})"
		return f"{{{strCompany};{strValue};{strDrop};{strVariation};{strDate}}}"

	def __repr__(self):
		return self.__str__()


def GenerateOperators(choices, equalFrequency, count):
	if equalFrequency > 0.0:
		equalFrequency = random.uniform(equalFrequency, 1.0)
	equalCount = math.ceil(equalFrequency * count)
	randomCount = count - equalCount
	operators = ["="] * equalCount
	operators.extend(random.choices(choices, k = randomCount))
	random.shuffle(operators)
	return operators


def GenerateFieldValues(field, amount):
	global configuration
	fieldConf = configuration["fields"][field]
	if fieldConf["type"] == "str":
		return random.choices(fieldConf["choices"], k = amount)
	else:
		return [random.uniform(fieldConf["min"], fieldConf["max"]) for _ in range(amount)]


def GenerateFieldRules(field):
	global configuration
	fieldConf = configuration["fields"][field]
	subscriptions = configuration["subscriptions"]
	equals = 0.0 if "equals" not in fieldConf else fieldConf["equals"]
	frequency = fieldConf["frequency"]
	operators = fieldConf["operators"]
	fieldType = fieldConf["type"]
	ruleCount = math.ceil(frequency * subscriptions)
	generatedValues = GenerateFieldValues(field, ruleCount)
	generatedOperators = GenerateOperators(operators, equals, ruleCount)
	rules = [Rule(field, operator, value) for operator, value in zip(generatedOperators,generatedValues)]
	return rules


def GenerateSubscriptions():
	global configuration
	subscriptions = configuration["subscriptions"]
	ruleLists = []
	for field in configuration["fields"]:
		fieldRules = GenerateFieldRules(field)
		padding = subscriptions - len(fieldRules)
		fieldRules.extend([None] * padding)
		random.shuffle(fieldRules)
		ruleLists.append(fieldRules)
	subscriptions = [Subscription(ruleSet) for ruleSet in zip(*ruleLists)]
	return subscriptions


def GeneratePublications():
	global configuration
	amount = configuration["publications"]
	companies = GenerateFieldValues("company", amount)
	values = GenerateFieldValues("value", amount)
	drops = GenerateFieldValues("drop", amount)
	variations = GenerateFieldValues("variation", amount)
	dates = GenerateFieldValues("date", amount)
	zipped = zip(companies, values, drops, variations, dates)
	publications = [Publication(company, value, drop, variation, date) for company, value, drop, variation, date in zipped]
	return publications


def CreateRulePool():
	global configuration
	pool = {}
	for field in configuration["fields"]:
		pool[field] = GenerateFieldRules(field)
	return pool


def CreateSubscriptionPool():
	global configuration
	amount = configuration["subscriptions"]
	fields = configuration["fields"].keys()
	pool = {Subscription() : random.sample(fields, k = len(fields)) for _ in range(amount)}
	return pool


def GenerateSubscriptions2():
	global configuration
	rulePool = CreateRulePool()
	subscriptionPool = CreateSubscriptionPool()
	while sum([len(rules) for field, rules in rulePool.items()]) > 0:
		for subscription, fieldsLeft in subscriptionPool.items():
			while len(fieldsLeft) > 0:
				field = fieldsLeft.pop()
				try:
					subscription.rules.append(rulePool[field].pop())
					break
				except Exception as e:
					continue
	return subscriptionPool.keys()


def LoadConfiguration(configPath):
	global configuration
	with open(configPath, "r") as hin:
		configuration = yaml.safe_load(hin)
	if configuration is None:
		raise Exception(f"There was a problem loading the configuration from \"{configPath}\"")


def Args():
	parser = argparse.ArgumentParser(description="Tool for generating publications and subscriptions")
	parser.add_argument("-c", "--config", required = True, help = "Path to yaml configuration file")
	parser.add_argument("-p", "--publications", type = str, default = "Publications.txt", help = "File path where publications will be stored. Defaults to 'Publications.txt'")
	parser.add_argument("-s", "--subscriptions", type = str, default = "Subscriptions.txt", help = "File path where subscriptions will be stored. Defaults to 'Publications.txt'")
	args = parser.parse_args()
	if not os.path.isfile(args.config):
		raise Exception(f"\"{args.config}\" is not a valid file path")
	args.config = os.path.abspath(args.config)
	return args


def Main():
	args = Args()
	LoadConfiguration(args.config)
	subscriptions = GenerateSubscriptions2()
	publications = GeneratePublications()
	with open(args.publications, "w") as hout:
		hout.write("\n".join([str(s) for s in publications]))
	with open(args.subscriptions, "w") as hout:
		hout.write("\n".join([str(s) for s in subscriptions]))


if __name__ == "__main__":
	Main()
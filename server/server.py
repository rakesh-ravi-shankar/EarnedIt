from flask import Blueprint, Flask, request
from .fitbit_wrapper import fitbitwrap
from . import db

blueprint = Blueprint('server', __name__)

@blueprint.route("/")
def index():
    return "Welcome to Earned It!"

@blueprint.route("/fitbittest")
def fitbittest():
	fitbitwrap.authorize()
	return

@blueprint.route('/getplans')
def getPlans():
	userId = request.args.get('userId', '')
	productId = request.args.get('productId', '')
	userId.strip()

	fitbitUserId = db.sql_select("SELECT fitbit_user_id FROM users WHERE id = '" + userId + "'")[0]
	totalPrice =  db.sql_select("SELECT price FROM products WHERE id = '" + productId + "'")[0]


	averageSteps = fitbitwrap.getAverageSteps(userId)

	# use to test
	# totalPrice = 50.00
	# averageSteps = 15000

	#set average goal days to 30
	defaultDeadline = 15
	priceRate = round(totalPrice/ (averageSteps * defaultDeadline), 4)

	totalSteps = totalPrice/priceRate

	steps = [averageSteps + 3000, averageSteps + 5000, averageSteps + 8000]
	deadlines = [round(totalSteps/i) + 4 for i in steps]

	resList = list(zip(steps, deadlines))
	resList.append(("priceRate", priceRate))
	return str(resList)


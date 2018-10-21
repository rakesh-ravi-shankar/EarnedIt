from flask import Blueprint, Flask, request
from .fitbit_wrapper import fitbitwrap
from . import db

blueprint = Blueprint('server', __name__)

@blueprint.route("/")
def index():
	from . import db
	db.init_db()
	return "Welcome to Earned It!"

@blueprint.route("/reset")
def reset():
	from . import db
	db.init_db()
	return "Reset complete!"

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
	totalPrice, =  tuple(db.sql_select("SELECT price FROM products WHERE id = '" + productId + "'")[0])

	averageSteps = fitbitwrap.getAverageSteps(fitbitUserId)

	# use to test
	# totalPrice = 50.00
	# averageSteps = 15000

	#set average goal days to 15
	defaultDeadline = 15
	priceRate = round(totalPrice/ (averageSteps * defaultDeadline), 4)

	totalSteps = totalPrice/priceRate

	steps = [averageSteps + 3000, averageSteps + 5000, averageSteps + 8000]
	deadlines = [round(totalSteps/i) + 4 for i in steps]

	resList = list(zip(steps, deadlines))
	resList.append(("priceRate", priceRate))
	return str(resList)

@blueprint.route("/selectPlan", methods=['POST'])
def selectPlan():
	payload = request.get_json()
	print(payload)

	db.sql_update("INSERT INTO %s VALUES (%s, %s, %s, %s, %s)" % ("plans", "NULL", payload.get("user_id"), payload.get("product_id"), payload.get("deadline"), payload.get("price_rate")))

	plan_id, =  tuple(db.sql_select("SELECT id FROM plans WHERE user_id='" + payload.get("user_id") + "' AND product_id='" + payload.get("product_id") + "'")[0])
	# TODO: Need to pull current step count
	db.sql_update("INSERT INTO reserved VALUES (NULL, " + str(plan_id) + ", 0.00, 0, 'PAYING')")

	return "Success"

@blueprint.route("/getUserPlans")
def getUserPlans():
	user_id = request.args.get('user_id', '')
	plans =  [for list(row) in db.sql_select("SELECT id, product_id, deadline FROM plans WHERE user_id = '" + user_id + "'")]
	for res in plans:
		amount_paid =  tuple(db.sql_select("SELECT amount_paid FROM reserved WHERE plan_id = '" + res[0] + "'"))
		res.append(amount_paid)

	# [[plan_id, product_id, deadline, amount_paid], ...]
	return str(plans)



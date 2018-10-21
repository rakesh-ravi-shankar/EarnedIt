import time, datetime
import atexit
from .fitbit_wrapper import fitbitwrap
from apscheduler.schedulers.background import BackgroundScheduler

from . import db

def update_steps_amt(reservedId, steps, amount):
	db.sql_update("UPDATE reserved SET amount_paid = " + 
		amount + ", last_step_count = " + steps +
		" WHERE id=" + reservedId)


def update_status(reservedId, status):
	db.sql_update("UPDATE reserved SET status = '" + status + "'' WHERE id = " + reservedId)


def collect_money(reservedId, alreadyPaid, amountDiff, productId, currentSteps):
	# productPrice = db.sql_select("SELECT price FROM products WHERE id = '" + productId + "'")[0]
	productPrice = 0.007
	totalAmount = alreadyPaid + amountDiff
	
	if totalAmount > productPrice:
		amountDiff = round(productPrice - alreadyPaid, 2)
		# update_status(reservedId, 'PAID')

	#collect from nmoney-d amountdiff Value
	print("Time:" datetime.datetime.now())
	print("Steps Updated: " + str(currentSteps))
	print("Amount Earned: $" + str(amountDiff))	
	print("\n")
	# update_steps_amt(reservedId, currentSteps, totalAmount)


def update_payments():
	reserved = [(1, 1, 20.00, 30000, "PAYING")]
	for reservedInfo in reserved:
		planId = reservedInfo[1]
		planId, userId, productId, deadline, priceRate = (1, 1, '0015', '2018-10-30', 0.0007)
		
		fitbitUserId = 1
		
		currentSteps = fitbitwrap.getCurrentSteps(fitbitUserId)
		
		previousSteps = reservedInfo[3]
		difference = currentSteps - previousSteps
		amountDiff = round(difference * priceRate, 2)

		collect_money(reservedInfo[0], reservedInfo[2], amountDiff, productI, currentSteps)


# def verify_deadline():
# 	for plans in db.sql_select("SELECT * FROM plans WHERE deadline = '" + datetime.date.today() + "'"):
# 		reservedInfo = db.sql_select("SELECT * FROM reserved WHERE plan_id = '" + plans[0] + "'")[0]
# 		refundAmt = 0.8 * reservedInfo[3]

# 		#refund that with money-d
# 		update_status(reservedInfo[0], 'REFUNDED')

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_payments, trigger="interval", seconds=3)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
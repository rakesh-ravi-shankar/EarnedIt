import time
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


def collect_money(reservedId, alreadyPaid, amountDiff, productId):
	productPrice = db.sql_select("SELECT price FROM products WHERE id = '" + productId + "'")[0]
	totalAmount = alreadyPaid + amountDiff
	
	if totalAmount > productPrice:
		amountDiff = productPrice - alreadyPaid
		update_status(reservedId, 'PAID')

	#collect from nmoney-d amountdiff Value
	update_steps_amt(reservedId, currentSteps, totalAmount)


def update_payments():
	for reservedInfo in db.sql_select("SELECT * FROM reserved WHERE status='PAYING'"):
		planId = reservedInfo[1]
		planId, userId, productId, deadline, priceRate = db.sql_select("SELECT * FROM plans WHERE id = '" + reservedInfo[1] + "'")[0]
		
		fitbitUserId = db.sql_select("SELECT fitbit_user_id FROM users WHERE id = '" + userId + "'")[0]
		currentSteps = fitbitwrap.getCurrentSteps(fitbitUserId)
		
		previousSteps = reservedInfo[3]
		difference = currentSteps - previousSteps
		amountDiff = difference * priceRate

		collect_money(reservedInfo[0], reservedInfo[2], amountDiff, productI, currentSteps)


def verify_deadline():
	for plans in db.sql_select("SELECT * FROM plans WHERE deadline = '" + datetime.date.today() + "'"):
		reservedInfo = db.sql_select("SELECT * FROM reserved WHERE plan_id = '" + planId + "'")[0]
		refundAmt = 0.8 * reservedInfo[3]
		
		#refund that with money-d
		update_status(reservedInfo[0], 'REFUNDED')




#uncomment while testing
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=update_payments, trigger="interval", minutes=5)
# scheduler.start()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())
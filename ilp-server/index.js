'use strict'

const ilp = require('ilp')
const debug = require('debug')('ilp-spsp')
const app = require('express')()
const bodyParser = require('body-parser')

// recipient is the payment pointer
// amount is 1 XRP = 10^9 units

async function pay(recipient, amount) {
    try {
        const plugin = ilp.createPlugin()
        debug('connection plugin')
        await plugin.connect()

        debug('sending payment')
        await ilp.SPSP.pay(plugin, {
            receiver: recipient,
            sourceAmount: amount
        })
    } catch(e) {
        console.error(e)
        process.exit(1)
    }
}

/*
// sending 0.0000001 XRP
function run() {
    pay('$bharat.localtunnel.me', 10)
}

run()
*/

;(async () => {
    //const spsp = await ilp.express.createMiddleware({receiver_info:{name: 'Bob Smith'}})

    function receivePayment(req, res) {
        var body = req.body
        var amount = body.amount
        if (Number.isInteger(amount)) {
            pay('$earnedit.localtunnel.me', amount)
            var success = {
                'message':'Payment successfully sent!'
            }
            res.json(success)
        } else {
            console.log('Please enter valid amount for transfer')
            var error = {
                'message':'Please enter valid amount for transfer'
            }
            res.json(error)
        }
    }
    const port = process.env.PORT || 8443

    //app.get('.well-known/pay', spsp)
    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({ extended: true }));
    app.get('/', (req, res) => res.send('Hello World'))
    app.post('/payment', receivePayment)
    console.log('Starting server now')
    app.listen(port, () => console.log(`App listening on port ${port}!`))
})()

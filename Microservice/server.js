// This is your test secret API key.
const stripe = require('stripe')('sk_test_51KXBsHEDG1XCk3ImvLY9ICBxOoBkKfss0sZ6hORGpACiFTEZdUinXi3LvCVhKFeqJEA3HcuJ7PA1cyrhZlUIQMmi00uWlIZbE0');
const express = require('express');
const res = require('express/lib/response');
const path = require('path');
const app = express();
var flash = require('connect-flash');

app.use(express.static('public'));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '/public'));

require('dotenv').config();

const PORT = process.env.PORT || 3000;



const YOUR_DOMAIN = 'https://bidonitpayments.azurewebsites.net';

app.post('/create-checkout-session/:product/:price/:id', async (req, res) => {
  
  
  const session = await stripe.checkout.sessions.create({
    line_items: [
      {
        // Provide the exact Price ID (for example, pr_1234) of the product you want to sell
        price_data: {
          unit_amount: req.params['price'],
          currency: 'usd',
          product_data: {
            name: req.params['product'],
            //'images': req.params['img']
          },
        },
        quantity: 1,
      }
    ],
    mode: 'payment',
    success_url: `https://bidonit.herokuapp.com/listings?id=${req.params['id']}&status=success`,
    cancel_url: `${YOUR_DOMAIN}/cancel.html`,
  });

  res.redirect(303, session.url);
});

app.get('/', function(req, res){
  console.log(req.query)

  res.render('checkout', {
    product: req.query['product'],
    id: req.query['id'],
    price: req.query['price'],
    image_url: req.query['img']
  })
})

app.listen(PORT, () => console.log(`Server is listening on port ${PORT}`));
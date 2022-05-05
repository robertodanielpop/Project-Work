var express = require('express');
var router = express.Router();

/* GET home page. */

router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/login', function(req, res, next) {
  res.render('login');
});

router.get('/loading', function(req, res, next) {
  res.render('loading');
});


router.get('/navigation', function(req, res, next) {
  res.render('navigation');
});

router.get('/orders', function(req, res, next) {
  res.render('orders');
});

router.get('/profile', function(req, res, next) {
  res.render('profile');
});

router.get('/checkout', function(req, res, next) {
  res.render('checkout');
});

router.get('/address', function(req, res, next) {
  res.render('address');
});

router.get('/basket', function(req, res, next) {
  res.render('basket');
});

router.get('/payment', function(req, res, next) {
  res.render('payment');
});

router.get('/footer', function(req, res, next) {
  res.render('footer');
});

router.get('/contact', function(req, res, next) {
  res.render('contact');
});

router.get('/register', function(req, res, next) {
  res.render('register');
});

router.get('/products', function(req, res, next) {
  res.render('products');
});

router.get('/wishlist', function(req, res, next) {
  res.render('wishlist');
});

router.get('/productstest', function(req, res, next) {
  res.render('productstest');
});

router.get('/product', function(req, res, next) {
  res.render('product');
});

router.get('/searchproducts', function(req, res, next) {
  res.render('searchproducts');
});

router.get('/privacy', function(req, res, next) {
  res.render('privacy');
});

router.get('/terms', function(req, res, next) {
  res.render('terms');
});

module.exports = router;


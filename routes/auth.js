const express = require('express');
const router = express.Router();
const passport = require('passport')



router.get('/signup', (req, res) => {

    res.render('auth/newuser')
})

router.post('/signup', passport.authenticate('local.signup', {
  successRedirect: '/auth/login',
  failureRedirect: '/auth/signup',
  failureFlash: true
}))

router.get('/login', (req, res) => {
    res.render('auth/login')
})

router.post('/login', (req, res, next) => {

    passport.authenticate('local.login', {
        successRedirect: '/users',
        failureRedirect: '/auth/login',
        failureFlash: true
    }) (req, res, next)
})


router.get('/logout', function(req, res, next) {
    req.logout(function(err) {
      if (err) { return next(err); }
      res.redirect('/');
    });
  });

router.post('/sigin', (req, res) => {
  console.log(req.body)
  res.redirect('/users')
})




module.exports = router;

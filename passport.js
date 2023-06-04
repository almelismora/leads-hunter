const passport = require('passport')
const LocalStrategy = require('passport-local').Strategy
const pool = require('./db.js')
const helpers = require('./helpers')


passport.use('local.login', new LocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    passReqToCallback: true
}, async (req, email, password, done) => {

    console.log(req.body)
    const [rows] = await pool.query('SELECT * FROM users WHERE email = ?', [email])
    if (rows.length > 0 ){
        const user = rows[0]
        const validPass = await helpers.comparePass(password, user.password)

        if (validPass) {
            done(null, user, req.flash('info', 'Welcome' + user.email))
        } else {
            done(null, false, req.flash('message' ,'Incorrect password'))
        }
    } else {
        return done(null, false, req.flash('message','The email does not exist'))
    }
}))

passport.use('local.signup', new LocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    passReqToCallback: true
}, async (req, email, password, done) => {

    const newuser = {
        email,
        password
    }

    newuser.password = await helpers.encryptPass(password)

    const [result] = await pool.query('INSERT INTO users SET ?', [newuser])
    newuser.id = result.insertId
    return done(null, newuser)
}))

passport.serializeUser((user, done) => {
    done(null, user.id)
})

passport.deserializeUser(async (id, done) => {
    const rows = await pool.query('SELECT * FROM users WHERE id = ?', [id])
    done(null, rows[0])
})


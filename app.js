const createError = require('http-errors');
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const bodyParser = require('body-parser')
const flash = require('connect-flash')
const session = require('express-session')
const MySQLStore = require('express-mysql-session')(session);
const connection = require('./db')
const passport = require('passport')

const sessionStore = new MySQLStore({
  createDatabaseTable: true,
  schema: {
    tableName: 'sessions',
    columnNames: {
      session_id: 'session_id',
      expires: 'expires',
      data: 'data'
    }
  }
}, connection);


const indexRouter = require('./routes/index');
const usersRouter = require('./routes/users');
const favRouter = require('./routes/favoritos');
const authRouter = require('./routes/auth')


const app = express();
require('./passport')

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');


app.use(session({
  secret: 'tfgsession', 
  resave: true, 
  saveUninitialized: true,
  store: sessionStore
}))

app.use(flash())
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(passport.initialize())
app.use(passport.session())


app.use((req, res, next) => {
  res.locals.info = req.flash('info')
  res.locals.message = req.flash('message')
  app.locals.user = req.user
  next()
})


app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/favoritos', favRouter)
app.use('/auth', authRouter)


app.use(express.static(path.join(__dirname, 'public')));


// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;

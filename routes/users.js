const express = require('express');
const router = express.Router();
const { spawnSync } = require('child_process')
const pool = require('../db');



/* GET users listing. */
router.get('/', async (req, res, next) => {

  const [ users ] = await pool.query("SELECT * FROM clients")
  // console.log(users)

  res.render('users', {users})

});

// extract.py
router.post('/run-script', async(req, res) => {

  const selectedTag = req.body.select_tag
  
  const py = spawnSync('py', ['../extract_insta/extract.py', selectedTag]);
  console.log(py.output.toString());
  
  res.redirect('/users')
})


// add to favorites
router.post('/addtofav/:userid', async (req, res, next) => {
  
  const selectedRow = parseInt(req.body.selectedRow)
  console.log(selectedRow)

  const [fav_list_id] = await pool.query("SELECT user_id FROM c_favorites")

  let list_fav = []

  for (let i = 0; i < fav_list_id.length; i++){
    console.log(fav_list_id[i].user_id)
    list_fav.push(fav_list_id[i].user_id)
  }

  if (!list_fav.includes(selectedRow)) {
    await pool.query('INSERT INTO c_favorites (name, account, description, website_link, website_name, email, phone, user_id) SELECT name, account, description, website_link, website_name, email, phone, id FROM clients WHERE id = ?', [selectedRow])
    req.flash('info', 'Client has been added successfully')
  } else {
    console.log('Client is in fav already')
    req.flash('info', 'Client has been added successfully')
  }


  res.redirect('/favoritos')
})




// aplicadores
router.get('/aplicadores', async (req, res, next) => {

  const [ aplicadores ] = await pool.query("SELECT * FROM clients WHERE description LIKE '%aplica%' OR description LIKE '%appli%' OR description LIKE '%aplika%'")

  res.render('categorias/aplicadores', {aplicadores})

})


// distribuidores
router.get('/distribuidores', async (req, res, next) => {

  const [ distribuidores ] = await pool.query("SELECT * FROM clients WHERE description LIKE '%distri%' OR description LIKE '%proveed%' OR description LIKE '%suppl%' OR description LIKE '%provid%' OR description LIKE '%dystry%' ")

  res.render('categorias/distribuidores', {distribuidores})

})


// fabricantes
router.get('/fabricantes', async (req, res, next) => {

  const [ fabricantes ] = await pool.query("SELECT * FROM clients WHERE description LIKE '%fabric%' OR description LIKE '%production%' OR description LIKE '%manufact%'")

  res.render('categorias/fabricantes', {fabricantes})

})


// otros 
router.get('/otros', async(req, res, next) =>{

  const [ otros ] = await pool.query("SELECT * FROM clients WHERE description NOT LIKE '%aplica%' AND description NOT LIKE '%appli%' AND description NOT LIKE '%distri%' AND description NOT LIKE '%proveed%' AND description NOT LIKE '%suppl%' AND description NOT LIKE '%provid%' AND description NOT LIKE '%fabric%' AND description NOT LIKE '%production%' AND description NOT LIKE '%manufact%' ")

  res.render('categorias/otros', {otros})

})





module.exports = router;

const express = require('express');
const router = express.Router();
const pool = require('../db');

router.get('/', async (req, res, next) => {

    const [ favoritos ] = await pool.query("SELECT * FROM c_favorites")

    res.render('favoritos/favoritos', {favoritos})
})

  

// delete from favoritos
router.post('/delete/:userid', async (req, res, next) => {
    // const favid = req.params.favid
    const selectedRow = parseInt(req.body.selectedRow)
    console.log(selectedRow)
    await pool.query("DELETE FROM c_favorites WHERE id = ?", [selectedRow])
    req.flash('info', 'The client has been removed from your favorites')
    res.redirect('/favoritos')
})

// edit favoritos 
router.post('/addnote/:userid', async (req, res, next) => {

    const selectedRow = parseInt(req.body.selectedRow)
    console.log(selectedRow)

    const [ fav ] = await pool.query("SELECT * FROM c_favorites WHERE id = ?", [selectedRow])

    res.render('favoritos/addnote', {fav:fav[0]})
})

router.post('/updatenote/:userid', async (req, res, next) => {

    const selectedRow = parseInt(req.body.selectedRow)
    console.log(selectedRow)

    const note = req.body.note
    console.log(note)
  
    
    await pool.query("UPDATE c_favorites SET note = ? WHERE id = ?", [note, selectedRow]);
    
    // const [ fav_update ] = await pool.query("SELECT * FROM c_favorites")
  
    // res.render('favoritos/favoritos', {favoritos:fav_update});
    req.flash('info', 'The note has been saved successfully')

    res.redirect('/favoritos')
  
  });



module.exports = router
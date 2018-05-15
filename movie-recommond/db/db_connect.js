const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/movie_recommend');
const db = mongoose.connection;

const userlinks = db.collection('userlinks');

db.on('open',(date)=>{
	// console.log(date);
	console.log("db connect success");
});

db.on('error',(err)=>{
	console.error(err);
	console.error("db connection error");
});

module.exports = {mongoose,userlinks};
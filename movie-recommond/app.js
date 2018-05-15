var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var fs = require('fs');

const m =  require('./db/db_connect');
const ID = 672;
const model = require('./db/schema');
const user = model.user;
const movie = model.movie;
const rate = model.rate;
const date = model.date;
const userlinks = m.userlinks;

const session = require('express-session');
var exec = require('child_process').exec;

var isUpdate  = false;

var app = express();

app.use(session({
  secret:'what the fuck',
  resave: false,
  saveUninitialized: false,
}));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.engine('html', require('ejs').__express);
app.set('view engine', 'html');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

function getToday(){
	var a = new Date();
	return a.getFullYear()+'/'+a.getMonth()+'/'+a.getDate();
}

function saveLog(log,ip){
	date.findOne({date:getToday()},(err,data)=>{
		if(err)
		{
			console.error(err);
			return
		}
		if(data)
		{
			data.logs.unshift({
				time:(new Date()).toString(),
				log:String(log),
				ip:ip
			});
			data.save();
		}
	});
}
//获取页面
app.get('/', function(req,res,next){
	date.findOne({date:getToday()},(err,data)=>{
		if(err)
			console.error(err);
		if(!data)
		{
			var newDate = new date({
				date:getToday(),
				visit_num:0,
				register:0,
				watch_movie:{0:0},
				review_movie:{0:0},
				rate_movie:{0:0},
				review_movie_detail:[],
				logs:[]
			});
			newDate.save((err)=>{
				if(err)
					console.log(err)
			})
		}else{
			data.visit_num ++;
			data.save((err)=>{
				if(err)
					console.log(err)
			});
		}
	});

	res.render('index');
});

//检查用户名是否重复
app.get('/checkUsername', function(req, res, next) {
	console.log('-------checkUsername---------');
	user.findOne({name:req.query.name},(err,user)=>{
		if(err)
		{
			console.error(err);
			res.send({status:false});
			return
		}
		if(!user)
		{
			res.send({status:true});
		}else{
			res.send({status:false});
		}
	});
});

//注册
app.post('/signin', function(req, res, next) {
	console.log('-------signin---------');
	user.count({},(err,num)=>{
		if(err) 
		{
			console.error(err);
			res.send({status:false});
			return
		}

		var newUser = new user({
			name:req.body.name,
			password:req.body.password,
			id:ID+num,
			sign_in_time:(new Date()).toString(),
			watch:[],
			rates:[],
			reviews:[],
			logMes:[],
			total_rate:0
		});
		newUser.save((err,newUser)=>{
			if(err)
			{
				console.error(err);
				res.send({status:false});
				return
			}
			console.log('-------save new user------');
			console.log(newUser);
			res.send({status:true});

			date.findOne({date:getToday()},(err,data)=>{
				if(err)
					saveLog(err,req.ip);
				if(data)
				{
					data.register ++;
					data.logs.unshift({
						ip:req.ip,
						time:(new Date()).toString(),
						log:'signin '+ req.body.name
					})
					data.save((err)=>{
						if(err)
							console.log(err)
					});
				}
			});
		});
	});
});

//登陆
app.post('/login',function(req,res,next){
	console.log('-------login---------');
	user.findOne({name:req.body.name},(err,user)=>{
		if(err)
		{
			console.error(err);
			res.send({status:false});
			return
		}

		if(!user)
		{
			console.error(err);
			res.send({status:false});
			return
		}else{
			if(req.body.password !=  user.password)
				res.send({status:false});
			else{
				req.session.living  = true;
				req.session.name = user.name;

				user.logMes.push({
					logtime:(new Date()).toString(),
					ip:req.ip
				});
				if(user.logMes.length > 50)
					user.logMes.shift();

				user.save((err)=>{
					if(err)console.log('logMes save err!'+ err)
				})
				res.send({status:true});

				var msg = user.name+'login';
				saveLog(msg,req.ip);
			}
		}
	})
});

//检查登陆状态
app.get('/checkLogin',function(req,res,next){
	if(req.session.living)
		res.send({
			status:true,
			name:req.session.name
		});
	else
		res.send({status:false});
});

//获取用户信息
app.get('/userData',function(req,res,next){
	if(req.session.living && req.session.name)
	{
		user.findOne({name:req.session.name},(err,user)=>{
			if(err){
				console.log('------------get user fail--------');
				console.error(err);
				res.send({status:false});
				return
			}

			if(!user)
				res.send({status:false});
			else
			{
				var newuserData = {
					name:user.name,
					sign_in_time:user.sign_in_time,
					watch:user.watch,
					total_rate:user.total_rate,
					rates:user.rates,
					reviews:user.reviews,
				}
				res.send({
					status:true,
					user:newuserData
				})
			}
		});
	}else{
		res.send({status:false})
	}
});

//获取电影评论（本地）
app.get('/getMovieReviews',function(req,res,next){
	movie.findOne({movieId:req.query.movieId},(err,movie)=>{
		if(err){
			console.log('------------get movie fail--------');
			console.error(err);
			res.send({status:false});
			return
		}

		if(!movie)
			res.send({status:false});
		else
			res.send({
				status:true,
				reviews:movie.reviews
			})
	});
});

//检查是否有此电影信息
app.get('/checkMovieId',function(req,res,next){
	movie.findOne({movieId:req.query.movieId},(err,movie)=>{
		if(err)
		{
			console.log('-----------checkMovieId error----------');
			console.error(err);
			res.send({status:false});
			return
		}
		if(!movie)
		{
			res.send({status:true});
		}else{
			res.send({status:false});
		}
	});

	date.findOne({date:getToday()},(err,data)=>{
		if(err)
			saveLog(err,req.ip);
		if(data)
		{
			// var a = Object.assign(data.watch_movie);
			if(data.watch_movie[req.query.movieId])
				data.watch_movie[req.query.movieId]++;
			else
				data.watch_movie[req.query.movieId]=1;
			data.markModified('watch_movie');
			data.save((err,data1)=>{
				if(err)
					console.log(err);
			});	
			
		}
	});
});

//输入电影信息到本地
app.post('/saveMovie',function(req,res,next){

	var newMovie = new movie({
		movieId:req.body.movieId,
		title:req.body.title,
		cast:req.body.cast,
		genres:req.body.genres,
		production_companies:req.body.production_companies,
		vote_average:req.body.vote_average,
		crew:req.body.crew,
		rate:[],
		reviews:[]
	});

	newMovie.save((err,newMovie)=>{
		if(err)
		{
			console.error(err);
			res.send({status:false});
			return
		}
		console.log('-------save new movie------');
		console.log(newMovie);
		res.send({status:true});
	});

	var msg = 'save new movie '+req.body.title;
	saveLog(msg,req.ip);
});

//保存电影评论
app.post('/saveReview',function(req,res,next){
	if(req.session.living && req.session.name)
	{
		movie.findOne({movieId:req.body.movieId},(err,movieData)=>{
			if(err){
				console.log('-----------saveReview error------------');
				console.error(err);
				res.send({status:false});
				return
			}
			if(!movieData)
				res.send({status:false});
			else{
				movieData.reviews.push({
					username:req.session.name,
					time:(new Date()).toString(),
					content:req.body.content
				});
				movieData.save((err)=>{
					if(err)
					{
						console.log(err);
						res.send({status:false});
					}else
						res.send({status:true})
				});

				user.findOne({name:req.session.name},(err,user2)=>{
					if(err){
						console.log('-----------saveReview error------------');
						console.error(err);
					}
					if(user2)
					{
						user2.reviews.unshift({
							movieName:movieData.title,
							movieId:req.body.movieId,
							content:req.body.content,
							time:(new Date()).toString()
						});
						user2.save((err)=>{
							if(err)
								console.log(err);
						});
					}
				})
			}
		});

		date.findOne({date:getToday()},(err,data)=>{
			if(err)
				saveLog(err,req.ip);
			if(data)
			{
				if(data.review_movie[req.body.movieId])
					data.review_movie[req.body.movieId]++;
				else
					data.review_movie[req.body.movieId]=1;
				data.markModified('review_movie');

				data.review_movie_detail.unshift({
					user:req.session.name,
					movieId:parseInt(req.body.movieId),
					time:(new Date()).toString(),
					content:req.body.content
				});

				data.logs.unshift({
					time:(new Date()).toString(),
					log:'user '+req.session.name+' review movie id:'+req.body.movieId,
					ip:req.ip
				});

				data.save((err)=>{
					if(err)
						console.log(err)
				});
			}
		});
	}else{
		res.send({status:false})
	}
});

//用户评分
app.post('/userRate',function(req,res,next){
	if(req.session.living && req.session.name){
		user.findOne({name:req.session.name},(err,user2)=>{
			if(err)
			{
				console.log('--------userRate error ---------');
				console.log(err);
				res.send({status:false,msg:'查询用户出错'});  
			}
			if(!user2)
				res.send({status:false,msg:'未发现此用户'}); 
			else{
				var uflag = true;
				for(var i = 0 ;i<user2.rates.length;i++)
				{
					if(user2.rates[i].movieId == req.body.movieId)
					{
						uflag = false;
						user2.rates[i].rate = req.body.rate;
						break;
					}
				}
				if(uflag)
				{
					user2.rates.push({
						movieId:req.body.movieId,
						rate:req.body.rate
					});
					user2.total_rate++;
				}
					
				user2.save((err)=>{
					if(err)
					{
						console.log(err);
						res.send({status:false,msg:'保存用户出错'});
					}

					rate.findOne({username:req.session.name,movieId:req.body.movieId},(err,rateData)=>{
						if(err) console.log(err);

						if(rateData)
						{
							rateData.rate = req.body.rate;
							rateData.time = (new Date()).getTime();

							rateData.save((err)=>{
								if(err)
								{
									console.log(err);
									res.send({status:false,msg:'新电影评分数据保存出错'});
								}
								res.send({status:true});
							});
						}else{
							if(uflag){
								var newMovieRate = new rate({
									username:req.session.name,
									userId:user2.id,
									movieId:req.body.movieId,
									time:(new Date()).getTime(),
									rate:req.body.rate
								});
								newMovieRate.save((err)=>{
									if(err)
									{
										console.log(err);
										res.send({status:false,msg:'新电影评分数据保存出错'});
									}
									res.send({status:true});
								})	
							}
							else{
								res.send({status:true,msg:'暂不更新推荐表！'});
							}
						}
					});
				});
			}
		})
		date.findOne({date:getToday()},(err,data)=>{
			if(err)
				saveLog(err,req.ip);
			if(data)
			{
				if(data.rate_movie[req.body.movieId])
					data.rate_movie[req.body.movieId]++;
				else
					data.rate_movie[req.body.movieId]=1;
				data.markModified('rate_movie');

				data.logs.unshift({
					ip:req.ip,
					time:(new Date()).toString(),
					log:req.session.name+' rate movie,movieId:'+req.body.movieId
				})
				data.save((err)=>{
					if(err)
						console.log(err)
				});
			}
		});

	}else{
		res.send({status:false})
	}
})

//用户浏览电影信息输入
app.get('/userVisit',function(req,res,next){
	if(req.session.living && req.session.name)
	{
		user.findOne({name:req.session.name},(err,user2)=>{
			if(err)
			{
				console.log(err);
				res.send({status:false});
			}
			if(!user2)
				res.send({status:false});
			else{
				movie.findOne({movieId:req.query.movieId},(err,movieData)=>{
					if(err)
					{
						console.log(err);
						res.send({status:false});
					}
					if(!movieData)
						res.send({status:false});
					else{
						user2.watch.unshift({
							movieName:movieData.title,
							movieId:req.query.movieId,
						});

						user2.save((err)=>{
							if(err)
							{
								console.log(err);
								res.send({status:false});
							}
							res.send({status:true});
						});
					}
				});
				
			}
		});
	}else{
		res.send({
			status:false
		});
	}
});

app.get('/update',function(req,res,next){
	if(req.session.living)
	{
		if(isUpdate)
			res.send({status:false,mes:'正在更新中！'});
		else
		{
			isUpdate = true;
			rate.count({},(err,num)=>{
				if(err)
				{
					console.error(err);
					res.send({status:false,mes:err});
					isUpdate = false;
				}

				if(num && num >0)
				{
					exec('python ../svd/update.py',(err,stdout,stderr)=>{
						if(err)
						{
							console.error(err);
							res.send({status:false})
						}
						console.log(stdout);
						isUpdate = false;	
						res.send({status:true,mes:'更新完毕！'});
					});	
				}else{
					res.send({status:false,mes:'无数据更新！'});
					isUpdate = false;
				}
			});

			var msg = req.session.name+' try update';
			saveLog(msg,req.ip);
		}
			
		
	}else{
		res.send({status:false})
	}

})

app.get('/getRecommend',function(req,res,next){
	if(req.session.living && req.session.name)
	{
		user.findOne({name:req.session.name},(err,user2)=>{
			if(err)
			{
				console.log(err);
				res.send({status:false,msg:'查询用户出错!'});
				return;
			}
			if(!user2)
			{
				res.send({status:false,msg:'查询用户出错!'});
				return;
			}else{
				userlinks.findOne({userId:String(user2.id)},(err,user3)=>{
					if(user3)
						exec('python ../svd/get-recommend.py '+ user2.id,(err,stdout,stderr)=>{
							if(err)
							{
								console.error(err);
								res.send({status:false})
							}
							console.log(stdout);
							res.send({status:true,mes:stdout});
						});
					else
					{
						res.send({status:false,msg:'未更新用户表!'});
						return;
					}
				})
					
			}
		});
		var msg = req.session.name+' get recommend';
		saveLog(msg,req.ip);
	}else{
		res.send({status:false,msg:'未登录!'});
	}
})

app.get('/getItemRecommend',function(req,res,next){
	if(req.session.living && req.session.name)
	{
		user.findOne({name:req.session.name},(err,user2)=>{
			if(err)
			{
				console.log(err);
				res.send({status:false,msg:'查询用户出错!'});
				return;
			}
			if(!user2)
			{
				res.send({status:false,msg:'查询用户出错!'});
				return;
			}else{
				if(user2.rates.length <= 0)
				{
					res.send({status:false,msg:'暂无评分数据'});
					return;
				}else {
					exec('python ../svd/item-basic.py '+ user2.id,(err,stdout,stderr)=>{
						if(err)
						{
							console.error(err);
							res.send({status:false})
						}
						console.log(stdout);
						res.send({status:true,mes:stdout});
					});
				}	
			}
		});
	}else{
		res.send({status:false,msg:'未登录!'});
	}
})

app.get('/getLogs',function(req,res,next){
	//res.set("Access-Control-Allow-Origin", "*");
	if(req.session.living && req.session.name == 'guan')
	{
		date.findOne({date:getToday()},(err,data)=>{
			if(err)
				saveLog(err)
			if(data)
				res.send({status:true,data:data});
			else
				res.send({status:false,msg:'no data'});
		});

		var msg = 'guan get logs';
		saveLog(msg,req.ip);
	}else{
		res.send({status:false,msg:'you are not guan shao'});
	}
})
app.get('/getUserNunm',function(req,res,next){
	//res.set("Access-Control-Allow-Origin", "*");
	if(req.session.living && req.session.name == 'guan')
	{
		user.count((err,data)=>{
			if(err)
				console.log(err)
			if(data)
				res.send({status:true,data:data});
			else
				res.send({status:false,msg:'no data'});
		})
		
	}else{
		res.send({status:false,msg:'you are not guan shao'});
	}
})
app.get('/getUser',function(req,res,next){
	r//es.set("Access-Control-Allow-Origin", "*");
	if(req.session.living && req.session.name == 'guan')
	{
		var skip = 5 *(parseInt(req.query.index) - 1)
		user.find({},null,{skip:skip,limit:5},(err,data)=>{
			if(err)
				console.log(err)
			if(data)
				res.send({status:true,data:data});
		})
		
	}else{
		res.send({status:false,msg:'you are not guan shao'});
	}
})
// app.use('/*', usersRouter);

// catch 404 and forward to error handler
// app.use(function(req, res, next) {
//   next(createError(404));
// });

// app.use('*',function(req,res,next){
// 	res.redirect('/');
// });
// error handler
// app.use(function(err, req, res, next) {
//   // set locals, only providing error in development
//   res.locals.message = err.message;
//   res.locals.error = req.app.get('env') === 'development' ? err : {};

//   // render the error page
//   res.status(err.status || 500);
//   res.render('error');
// });

module.exports = app;

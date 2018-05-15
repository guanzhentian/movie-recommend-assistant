<template>
	<div class="management">
		<div class="content" v-if="mes">
			<div class="box">
				<h1>今日统计数据</h1>
				<div class="main">
					<p>时间：{{mes.date}}</p>
					<p>注册人数：{{mes.register}}</p>
					<p>访问次数：{{mes.visit_num}}</p>
					<p>电影查看次数：{{watch_movie_times}}</p>
					<p>最多查看电影(id)：{{watch_movie_most}}</p>
					<p>电影评分次数：{{rate_movie_times}}</p>
					<p>最多评分电影(id)：{{rate_movie_most}}</p>
					<p>电影评论次数：{{review_times}}</p>
					<p>最多评论电影(id)：{{review_most}}</p>
				</div>
			</div>
			<div class="box">
				<h1>今日最新评论</h1>
				<div class="main">
					<div v-for="item in mes.review_movie_detail.slice(0,5)" class="review">
						<div>
							<span>User Name : {{item.user}}</span>
							<span>Movie Id : {{item.movieId}}</span>
							<span>Time : {{computed_time(item.time)}}</span>	
						</div>
						
						<p>{{item.content.slice(0,100)}}</p>
					</div>
				</div>
			</div>
			<div class="box">
				<h1>今日最新日记</h1>
				<div class="main">
					<div v-for="item in mes.logs.slice(0,10)" class="logs">
						<div>
							<span>IP address : {{item.ip}}</span>
							<span>Time : {{computed_time(item.time)}}</span>
						</div>
						<p>
							<span>{{item.log}}</span>
						</p>
					</div>
				</div>
			</div>
			<div class="box">
				<h1>用户管理</h1>
				<div class="main">
					<p class="userTop">
						<span>all User:{{allUser}}</span>
						<span> all page:{{allIndex}}</span>
						<span> cur page:{{index}}</span></p>
					<div v-for="(item,index) in showUser" v-if="showUser" class="user" @click="choose(index)">
						<p><strong>Name:</strong> {{item.name}}</p>
						<p><strong>Id:</strong> {{item.id}}</p>
						<p><strong>Total rate:</strong> {{item.total_rate}}</p>
						<p><strong>Total reviews:</strong> {{item.reviews.length}}</p>
						<p><strong>Sign in time:</strong> {{computed_time(item.sign_in_time)}}</p>
						<div class="detail" v-if="showIndex == index">
							<p><strong>Password :</strong> {{item.password}}</p>
							<div class="rates">
								<p><strong>Rates</strong></p>
								<div v-for="r in item.rates">
									<p><span>movieId : {{r.movieId}}</span> <span>rate : {{r.rate}}</span></p>
								</div>
							</div>
							<div class="reviews">
								<p><strong>Reviews</strong></p>
								<div v-for="r in item.reviews">
									<p><span>movieName : {{r.movieName}}</span><span>Time : {{computed_time(r.time)}}</span> <span>content : {{r.content}}</span></p>
								</div>
							</div>
							<div class="watch">
								<p><strong>Watch</strong></p>
								<div v-for="w in item.watch">
									<p><span>movieId : {{w.movieId}}</span> <span>movieName : {{w.movieName}}</span></p>
								</div>
							</div>
						</div>
					</div>
					<p v-if="index > 1" @click="getuser('up')" class="userUp"><img src="../assets/leftcircle.png" ></p>
					<p v-if="index < allIndex" @click="getuser('down')" class="userDown"><img src="../assets/rightcircle.png" ></p>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/javascript">
	export default{
		data(){
			return{
				mes:null,
				rate_movie_times:0,
				rate_movie_most:0,
				watch_movie_most:0,	
				watch_movie_times:0,
				review_times:0,
				review_most:0,
				showUser:null,
				index:1,
				allIndex:0,
				allUser:0,
				showIndex:null
			}
			
		},
		methods:{
			choose(index){
				if(this.showIndex == index)
					this.showIndex = null;
				else
					this.showIndex = index;
			},
			calc(){
				var wm = this.mes.watch_movie;
				var wmost = 0;
				var wmost_name = 0;
				var wmall = 0;
				for (var item in wm)
				{
					if(wm[item] > wmost)
					{
						wmost = wm[item];
						wmost_name = item;
					}
					wmall += wm[item];
				}
				this.watch_movie_most = wmost_name;	
				this.watch_movie_times = wmall;

				var rm = this.mes.rate_movie;
				var rmost = 0;
				var rmost_name = 0;
				var rmall = 0;
				for (var item in rm)
				{
					if(rm[item] > rmost)
					{
						rmost = rm[item];
						rmost_name = item;
					}
					rmall += rm[item];
				}
				this.rate_movie_most = rmost_name;	
				this.rate_movie_times = rmall;

				var rem = this.mes.review_movie;
				var remost = 0;
				var remost_name = 0;
				var remall = 0;
				for (var item in rem)
				{
					if(rem[item] > remost)
					{
						remost = rem[item];
						remost_name = item;
					}
					remall += rem[item];
				}
				this.review_most = remost_name;	
				this.review_times = remall;
			},
			getuser(val){
				if(val == 'up')
					this.index --;
				else if(val == 'down')
					this.index ++;
				this.showIndex = null;
				this.axios.get('/getUser?index='+this.index)
				.then((res)=>{
					if(res.status)
						this.showUser = res.data.data;
					else
						console.log(res.msg);
				}).catch((err)=>{
					console.log(err);
				})
			},
			computed_time(time){
				var ary = time.split(' ');
				ary.pop();
				ary.pop();
				return ary.toString().replace(/\,/g,' ')
			}
		},
		mounted(){
			this.axios.get('/getLogs')
			.then((res)=>{
				if(res.status)
				{
					this.mes = res.data.data;
					this.calc();
				}else {
					console.log(res.msg);
				}
			})
			.catch((err)=>{
				console.log(err);
			});

			this.axios.get('/getUserNunm')
			.then((res)=>{
				if(res.status)
				{
					this.allUser = res.data.data;
					this.allIndex = Math.ceil(this.allUser/5);
					this.getuser();
				}
				else
					console.log(res.msg);
			})
			.catch((err)=>{
				console.log(err);
			})

		}
	}
</script>
<style type="text/css" lang="less" scoped>
	.management{
		width:100%;
		display: flex;
		justify-content: center;
		padding-top: 60px;
		padding-bottom: 60px;
		.content{
			width:1000px;
			.box{
				padding:30px 20px;
				box-sizing: border-box;
				h1{
					display:flex;
					align-items: center;
				}
				h1::before{
					display: inline-block;
					width:10px;
					height:40px;
					background-color: black;
					content:'';
					margin-right: 10px;
				}
				.main{
					box-sizing: border-box;
					padding:0 20px;
					.review{
						border:1px solid #d7d7d7d7;
						padding:20px;
						box-sizing: border-box;
						>div{
							display: flex;
							justify-content: space-between;
							color:#666666;
						}
						>p{
							text-indent: 2em;
							color:#333333;
							margin-bottom: 0px;
						}
					}
					.review + .review{
						margin-top: 20px;
					}
					.logs{
						border:1px solid #d7d7d7d7;
						padding:20px;
						box-sizing: border-box;
						div:first-child{
							display:flex;
							justify-content: space-between;
							color:#666666;
						}
						>p{
							text-indent: 2em;
							color:#333333;
							margin-bottom: 0px;
						}
					}
					.logs + .logs{
						margin-top: 20px;
					}
					.userTop{
						span + span{
							margin-left: 20px;
							color:#333333;
						}
					}
					.user{
						box-sizing: border-box;
						padding:0 20px;
						border:1px solid #d7d7d7;
						color:#666666;
						cursor: pointer;
						.detail{
							.rates,.reviews,.watch{
								max-height:300px;
								overflow: auto;
								border-top: 1px solid #d7d7d7;
								padding:20px 0px;
								p{
									span + span{
										margin-left:30px;
									}
								}
							}
						}
					}
					.user + .user{
						margin-top:20px;
					}
					.userDown{
						float: right;
					}
					.userUp,.userDown{
						cursor: pointer;
					}
				}
			}
			.box + .box{
				border-top:1px solid #d7d7d7;
			}
		}
	}
</style>
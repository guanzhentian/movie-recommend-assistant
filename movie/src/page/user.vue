<template>
	<div class="muser" v-if="user">
		<div class="top" :style="{backgroundImage:'url('+bg+')'}">
			<div class="mengban">
				<div class="content" >
					<div class="name">
						{{user.name.slice(0,1).toUpperCase()}}
					</div>
					<div class="info">
						<div class="small">
							<h1 >{{user.name}}</h1><p>{{sign_time}} Join as a member of this website.</p>
						</div>
						<div class="rate">
							<p>Average Movie Rating</p>	
							<rate :name="'avg'" :value="rate_average"></rate>
						</div>
					</div>
				</div>	
			</div>
		</div>
		<div class="link">
			<div class="content">
				<span class="active">OVERVIEW</span>
			</div>
		</div>
		<div class="detail">
			<div class="content">
				<div class="box box1">
					<h2>STATUS</h2>
					<div class="status">
						<div>
							<p>Number of rates:</p>
							<div v-if="user.total_rate">
								{{user.total_rate}}
							</div>
							<div v-else>
								no rate yet
							</div>
						</div>
						<div>
							<p>Rating Overview:</p>
							<div>
								<span><strong>1 point and below：</strong>{{rateNum[0]}}</span>
								<span><strong>2 points to 1 point：</strong>{{rateNum[1]}}</span>
								<span><strong>3 points to 2 points：</strong>{{rateNum[2]}}</span>
								<span><strong>4 points to 3 points：</strong>{{rateNum[3]}}</span>
								<span><strong>5 points to 4 points：</strong>{{rateNum[4]}}</span>
							</div>
						</div>
					</div>
				</div>
				<div class="box box2">
					<h2>Recent comments</h2>
					<div class="content">
						<div v-if="user.reviews == null || user.reviews.length == 0">
							You have not commented recently
						</div>
						<div v-else v-for="item in user.reviews.slice(0,5)" class="comment">
							<p>{{item.movieName}} <span>{{calcTime(item.time)}}</span></p>
							<p>{{item.content}}</p>
						</div>	
					</div>
					
				</div>
				<div class="box box2">
					<h2>Recently browsed movies</h2>
					<div class="content">
						<div v-if="watch == null || watch.length == 0">
							You have not browsed recently
						</div>
						<router-link tag="div" v-else v-for="item in watch" class="watch" :to="'/movie/'+item.movieId" :key="item.movieId">
							<p><span>Movie Name : </span>{{item.movieName}}</p>
							<p><span>Movie Id : </span>{{item.movieId}}</p>
						</router-link>	
					</div>
				</div>
			</div>
		</div>
		<div class="spcial">
			<div class="content">
				<input type="text" v-model="spcial">
				<button @click="submitSpical">submit</button>
				<router-link to="/test" tag="button">test</router-link>
			</div>
		</div>
		<foot></foot>
	</div>
</template>
<script type="text/javascript">
	import foot from '@/components/foot'
	import rate from '@/components/rate'
	export default{
		components:{
			foot,rate
		},
		computed:{
			sign_time(){
				var a = this.user.sign_in_time.split(' ');
				return a[1]+' '+a[3]
			},
			watch(){
				if(this.user.watch.length > 0)
				{
					var num = 1,w =[];				
					w.push(this.user.watch[0]);
					for(var i =1;i<this.user.watch.length;i++)
					{
						var flag = true;
						for(var j =0;j<w.length;j++)
						{
							if(w[j].movieId == this.user.watch[i].movieId)
							{
								flag = false;
								break;
							}
						}
						if(flag)
						{
							w.push(this.user.watch[i]);
							num++;
							if(num >= 10)
								return w;
						}
					}
					return w;
				}else{
					return null
				}
			}
		},
		data(){
			return{
				bg:require('../assets/3.jpg'),
				user:null,
				rateNum:[0,0,0,0,0],
				rate_average:null,
				spcial:'',
			}
		},
		methods:{
			// b.toString().replace(/\,/g,' ')
			calc(){
				if(this.user.rates.length <= 0)
					return
				var avg = 0;
				for(var i = 0 ;i<this.user.rates.length; i++)
				{
					avg += parseFloat(this.user.rates[i].rate);
					
					if(parseFloat(this.user.rates[i].rate)<= 1)
						this.rateNum[0]++;
					else if(parseFloat(this.user.rates[i].rate)<= 2)
						this.rateNum[1]++;
					else if(parseFloat(this.user.rates[i].rate)<= 3)
						this.rateNum[2]++;
					else if(parseFloat(this.user.rates[i].rate)<= 4)
						this.rateNum[3]++;
					else if(parseFloat(this.user.rates[i].rate)<= 5)
						this.rateNum[4]++;
				}
				if(this.user.total_rate)
					this.rate_average = avg /this.user.total_rate;
			},
			calcTime(val){
				var a = val.split(' ');
				a.pop();
				a.pop();
				return a.toString().replace(/\,/g,' ');
			},
			submitSpical(){
				if(this.spcial == 'update')
				{
					this.axios.get('/update').then((res)=>{
						if(res.data.status)
						{
							alert('success!');
						}else{
							alert('fail!' + res.data.mes)
						}
					}).catch((err)=>{
						console.log(err);
						alert('fail!');
					})
				}
			}
		},
		mounted(){
			this.axios.get('/userData')
			.then((res)=>{
				if(res.data.status)
				{
					this.user = res.data.user;
					this.calc();
				}else
				{
					this.$router.push({path:'/'});
				}	
			}).catch((err)=>{
				console.log(err);
				this.$router.push({path:'/'});
			});

			//test
			// this.user = this.testData.user;
			// this.calc();
		}
	}
</script>
<style type="text/css" lang="less" scoped>
	.muser{
		padding-top: 60px;
		width: 100%;
		.top{	
			width:100%;
			background-position: center 10%;
			background-size: cover;
			background-repeat: no-repeat;
			.mengban{
				width:100%;
				display: flex;
				justify-content: center;
				background-color: rgba(0,0,0,0.5);
				.content{
					width:1000px;
					padding:40px 20px;
					display: flex;
					align-items: center;
					color:rgba(255,255,255,0.95);
					.name{
						width:150px;
						height:150px;
						border-radius: 50%;
						background-color:#d29001;
						color:white;
						font-size:64px;
						text-align: center;
						line-height: 145px;
						margin-right: 40px;
					}
					.info{
						.small{
							display: flex;
							align-items: flex-end;
							h1{
								margin:0;
								margin-right: 10px;
								font-size: 35.2px;
								font-weight: bold;
							}
							p{
								margin:0;
								font-size: 17.6px;
								color:#f4f4f4;
							}
						}
						.rate{
							display: flex;
							align-items: center;
							padding-top: 20px;
							>p{
								margin-right: 20px;
							}
						}
					}

				}	
			}
			
		}
		.link{
			width:100%;
			height:66px;
			background-color: white;
			border-bottom: 1px solid rgba(0, 0, 0, 0.1);
			display: flex;
			justify-content: center;
			.content{
				height:100%;
				width: 1000px;
				padding:0 20px;
				font-size: 20px;
				font-weight: bold;
				display: flex;
				span{
					display: flex;
					align-items: center;
				}
				.active{
					border-bottom: 5px solid #d29001;
				}
			}
		}
		.detail{
			width:100%;
			background-color: #f4f4f4;
			padding:30px 0px;
			display: flex;
			justify-content: center;
			border-bottom: 1px solid rgba(0, 0, 0, 0.1);
			.content{
				width:1000px;
				padding:0 20px;
				.box1{
					.status{
						box-sizing: border-box;
						padding:0 20px 40px;
						>div:first-child{
							display: flex;
							align-items: center;
							>p{
								margin-right: 20px;
								font-weight: bold;
							}
							>div{
								
								font-size:18px;
							}
						}
						>div:last-child{
							>p{
								font-weight: bold;
							}
							>div{
								text-indent: 2em;
								span{
									display: block;
									strong{
										width:250px;
										display: inline-block;
									}
									
								}
								span + span{
									margin-top: 10px;
								}
							}
						}
					}
				}
				.box2{
					padding:0 0 30px;
					.content{
						box-sizing: border-box;
						padding:0 20px;
						.comment{
							border:1px solid #d7d7d7;
							box-sizing: border-box;
							padding:20px 20px;
							background-color: white;
							>p:first-child{
								font-weight: bold;
								font-size: 18px;
								span{
									font-weight: normal;
									font-size:12px;
									padding-left: 10px;
								}
							}
							>p:last-child{
								text-indent: 2em;
								font-size: 16px;
							}
						}
						.comment + .comment{
							margin-top: 30px;
						}
						.watch{
							box-sizing: border-box;
							padding:0 20px;
							border:1px solid #d7d7d7;
							background-color: white;
							cursor: pointer;
							&:hover{
								background-color: rgba(255,255,255,0.1);
							}
							>p{
								span{
									font-weight: bold;
								}
							}
						}
						.watch + .watch{
							margin-top: 20px;
						}
					}
					
				}
			}
		}
		.spcial{
			width:100%;
			background-color: white;
			padding:30px 0px;
			display: flex;
			justify-content: center;
			border-bottom: 1px solid rgba(0, 0, 0, 0.1);
			.content{
				width:1000px;
				padding:0 20px;
				input{
					margin-right: 30px;
				}
				button + button{
					margin-left:30px;
				}
			}
		}
	}
	@media screen and (max-width: 1024px) {
		.muser{
			padding-top: 40px;
			.top{
				.mengban{
					.content{
						width:100%;
						padding:30px 10px;
						box-sizing: border-box;
						.name{
							flex:0 0 100px;
							height:100px;
							font-size:64px;
							line-height: 100px;
							margin-right:20px;
						}
						.info{
							.small{
								h1{
									font-size: 24px;
								}
								p{
									font-size:14px;
								}
							}
						}

					}	
				}
			}
			.link{
				.content{
					width: 100%;
					padding:0 10px;
					box-sizing: border-box;
					font-size: 16px;
				}
			}
			.detail{
				.content{
					width:100%;
					box-sizing: border-box;
					padding:0 10px;
					.box1{
						h2{
							font-size: 16px;
						}
						.status{
							box-sizing: border-box;
							padding:0 20px 40px;
							font-size: 14px;
							>div:first-child{
								>div{
									font-size:14px;
								}
							}
							>div:last-child{
								>div{
									text-indent: 1em;
									span{
										display: block;
										strong{
											width:200px;
										}
									}
								}
							}
						}
					}
					.box2{
						padding:0 0 30px;
						h2{
							font-size: 16px;
						}
						.content{							
							padding:0 10px;
							.comment{
								max-height: 400px;
								overflow-y: hidden;
								>p:first-child{
									font-size: 14px;
									margin:0;
									span{
										font-size:12px;
									}
								}
								>p:last-child{
									text-indent: 1em;
									font-size: 14px;
								}
							}
							.watch{
								font-size: 14px;
							}
						}
						
					}
				}
			}
			.spcial{
				width:100%;
				background-color: white;
				padding:30px 0px;
				display: flex;
				justify-content: center;
				border-bottom: 1px solid rgba(0, 0, 0, 0.1);
				.content{
					width:1000px;
					padding:0 20px;
					input{
						margin-right: 30px;
					}
					button + button{
						margin-left:30px;
					}
				}
			}
		}
	}
</style>
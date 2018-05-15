<template>
	<div class="mregister ">
		<div class="content">
			<h1 v-if="flag">Sign In</h1>
			<h1 v-else>Login</h1>
			<div class="input">
				<span>Name</span>
				<input type="text" v-model="name" placeholder="input your name" @blur="checkName">
				<span :class="{active:nameCheck,error:!nameCheck}">{{nameMessage}}</span>
			</div>
			<div class="input">
				<span>Password</span>
				<input type="password" v-model="password" placeholder="input your password" @blur="checkPassword">
				<span :class="{active:passwordCheck,error:!passwordCheck}">{{passwordMessage}}</span>
			</div>
			<div class="input" v-if="flag">
				<span>Check Pasword</span>
				<input type="password" v-model="checkWord" placeholder="input your password agin" @blur="checkSpass">
				<span :class="{active:checkWordCheck,error:!checkWordCheck}">{{checkWordMessage}}</span>
			</div>
			<div class="input">
				<span>Verification code</span>
				<input type="text" v-model="yanzhengma" placeholder="input verification code" @keyup.enter="submit">
				<canvas width="100" height="30" id="can" @click="buildYanzhenma"></canvas>
			</div>
			<div class="btn"  @click="submit">
				<span v-if="flag">Sign In</span>
				<span v-else>Login</span>
			</div>
		</div>
	</div>
</template>
<script type="text/javascript">
	export default{
		data(){
			return{
				flag:true,
				name:'',
				password:'',
				checkWord:'',
				yanzhengma:'',
				check:'',
				nameMessage:'',
				nameCheck:false,
				passwordCheck:false,
				passwordMessage:'',
				checkWordCheck:false,
				checkWordMessage:''
			}
		},
		watch:{
			$route(){
				if(this.$route.path.indexOf('login') != -1)
				{
					this.flag = false;
					this.clear();
				}
				else
				{
					this.flag = true;
					this.clear();
				}
			}
		},
		methods:{
			buildYanzhenma(){
				var canvas = document.getElementById('can');
				var c = canvas.getContext('2d');
				var check = '';
				c.clearRect(0,0,100,30);
				for(var i =0;i<4;i++)
				{
					var ran = Math.random()*3;
					if(ran < 1){
						check += Math.floor(Math.random()*10)
					}
					else if(ran <2)
					{
						var ranNum = Math.floor(Math.random()*26)
						check += String.fromCharCode(65+ranNum);
					}
					else{
						var ranNum = Math.floor(Math.random()*26)
						check += String.fromCharCode(97+ranNum);
					}
				}
				c.fillStyle="white";
				c.fillRect(0,0,100,30);
				c.fillStyle="black";
				c.font = '20px Arial';
				c.fillText(check,25,20);
				this.check = check;
				//48-5-2123
			},
			checkName(){
				var reg = /^[A-z]{3,}$/;
				if(reg.test(this.name))
				{
					if(this.flag)
					{
						this.axios.get('/checkUsername',{
							params:{
								name:this.name
							}
						}).
						then((res)=>{
							console.log(res);
							if(res.data.status)
							{
								this.nameMessage='OK';
								this.nameCheck  = true;
							}else{
								this.nameMessage='User name has been used';
								this.nameCheck  = false;
							}
						}).catch((err)=>{
							console.log(err);
							this.nameMessage='User name has been used';
							this.nameCheck  = false;
						});
					}else{
						this.nameMessage='OK';
						this.nameCheck  = true;
					}
					
				}else{
					this.nameMessage='Please enter more than three letters(only letter)';
					this.nameCheck  = false;
				}
			},
			checkPassword(){
				if(this.password.length<8)
				{
					this.passwordCheck = false;
					this.passwordMessage = 'Please enter more than eight letters';
				}else{
					this.passwordMessage='OK';
					this.passwordCheck  = true;
				}
			},
			checkSpass(){
				if(this.checkWord != this.password)
				{
					this.checkWordCheck = false;
					this.checkWordMessage = 'Please enter the same string as the password';
				}else{
					this.checkWordCheck = true;
					this.checkWordMessage = 'OK';
				}
			},
			submit(){
				if(this.flag)
				{
					if(this.yanzhengma != this.check)
					{
						this.buildYanzhenma();
						this.yanzhengma = '';
						return alert('Verification code Error!');
					}
					if(!this.nameCheck)
					{
						this.buildYanzhenma();
						this.yanzhengma = '';
						this.name = '';
						return alert('name error!');
					}
					if(!this.passwordCheck)
					{
						this.buildYanzhenma();
						this.yanzhengma = '';
						this. checkWord = '';
						return alert('password error!');
					}
					if(!this.checkWordCheck)
					{
						this.buildYanzhenma();
						this.yanzhengma = '';
						this.checkPassword = '';
						return alert('password not same');
					}

					this.axios.post('/signin',{
						name:this.name,
						password:this.password
					}).then((res)=>{
						console.log(res);
						if(res.data.status)
						{
							alert('success!');
							this.$router.push({path:'/login'});
						}else{
							alert('fail!');
							this.clear()
						}
					}).catch((err)=>{
						console.log(err);
						alert('fail!');
						this.clear();
					});	
				}
				else{
					if(this.yanzhengma != this.check)
					{
						this.buildYanzhenma();
						this.yanzhengma = '';
						return alert('Verification code Error!');
					}
					if(!this.nameCheck)
					{
						this.buildYanzhenma();
						this.yanzhengma = '';
						this.name = '';
						return alert('name error!');
					}
					if(!this.passwordCheck)
					{
						this.buildYanzhenma();
						this.yanzhengma = '';
						this.password = '';
						return alert('password error!');
					}

					this.axios.post('/login',{
						name:this.name,
						password:this.password
					}).then((res)=>{
						if(res.data.status)
						{
							alert('login success!');
							this.$router.push({path:'/'});
						}else{
							alert('login fail!');
							this.clear();
						}
					}).catch((err)=>{
						alert('login fail!');
						this.clear();
					})
				}
			},
			clear(){
				
				this.name='';
				this.password='';
				this.checkWord='';
				this.yanzhengma='';
				this.nameMessage='';
				this.nameCheck=false;
				this.passwordCheck=false;
				this.passwordMessage='';
				this.checkWordCheck=false;
				this.checkWordMessage='';
				
				this.buildYanzhenma();
			}
		},
		mounted(){
			if(this.$route.path.indexOf('login') != -1)
				this.flag = false;
			else
				this.flag = true;
			this.$nextTick(()=>{
				this.buildYanzhenma();
			})
		}
	}
</script>
<style type="text/css" lang="less" scoped>
	.mregister{
		background-color: #f4f4f4;
		width:100%;
		display: flex;
		justify-content: center;
		padding-top:80px;
		.content{
			color:#081c24;
			min-width: 600px;
			padding:0 20px;
			padding-bottom: 50px;
			display: flex;
			flex-direction: column;
			align-items: center;
			h1{
				margin-bottom: 50px;
			}
			.input{
				padding-bottom: 20px;
				position: relative;
				span{
					display: inline-block;
					width:150px;
				}
				input{
					border: 1px solid #d6d6d6;
					height:20px;
					padding-left: 10px;
					&:focus{
						outline: 0;
					}
				}
				canvas{
					position: absolute;
					border:1px solid #d6d6d6;
					right:-130px;
					cursor: pointer;
					top:-5px;
				}
				span:nth-child(3){
					position: absolute;
					font-size: 10px;
					right:-160px;
					top:0;
				}
				span.active{
					color:#00CC66;
				}
				span.error{
					color:#CC3300;
				}
			}
			.btn{
				font-size: 14px;
				margin-top: 50px;
				width:100px;
				height:30px;
				line-height: 30px;
				color:rgba(255,255,255,0.8);
				background-color: #081c24;
				text-align: center;
				cursor: pointer;
				border-radius: 5px;
			}
		}
	}
	@media screen and (max-width: 1024px) {
		.mregister{
			padding-top:80px;
			.content{
				min-width:100%;
				padding:0px;
				padding-bottom: 50px;
				align-items: flex-start;
				h1{
					margin-bottom: 50px;
					font-size: 20px;
					text-align: center;
					width:100%;
				}
				.input{
					align-self: stretch;
					margin-left: 20px;
					padding-bottom: 20px;
					position: relative;
					display: flex;
					flex-direction: column;
					span{
						width:auto;
						margin-bottom: 10px;
					}
					input{
						width:90%;
						margin-bottom: 10px;
					}
					canvas{
						align-self: flex-start;
						position:static;
					}
					span:nth-child(3){
						position: static;
					}
				}
				.btn{
					align-self: center;
				}
			}
		}
	}
</style>